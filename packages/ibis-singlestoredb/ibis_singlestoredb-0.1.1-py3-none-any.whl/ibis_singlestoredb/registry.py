#!/usr/bin/env python
"""SingleStoreDB function registry."""
from __future__ import annotations

import operator
from typing import Callable

import ibis
import ibis.backends.base.sql.compiler.translator as tr
import ibis.common.exceptions as com
import ibis.expr.datatypes as dt
import ibis.expr.operations as ops
import ibis.expr.types as ir
import pandas as pd
import sqlalchemy as sa
from ibis.backends.base.sql.alchemy import fixed_arity
from ibis.backends.base.sql.alchemy import sqlalchemy_operation_registry
from ibis.backends.base.sql.alchemy import sqlalchemy_window_functions_registry
from ibis.backends.base.sql.alchemy import unary

operation_registry = sqlalchemy_operation_registry.copy()
operation_registry.update(sqlalchemy_window_functions_registry)


def _substr(t: tr.ExprTranslator, expr: ir.Expr) -> ir.Expr:
    f = sa.func.substr

    arg, start, length = expr.op().args

    sa_arg = t.translate(arg)
    sa_start = t.translate(start)

    if length is None:
        return f(sa_arg, sa_start + 1)
    else:
        sa_length = t.translate(length)
        return f(sa_arg, sa_start + 1, sa_length)


def _capitalize(t: tr.ExprTranslator, expr: ir.Expr) -> ir.Expr:
    (arg,) = expr.op().args
    sa_arg = t.translate(arg)
    return sa.func.concat(
        sa.func.ucase(sa.func.left(sa_arg, 1)), sa.func.substring(sa_arg, 2),
    )


def _extract(fmt: str) -> Callable[[tr.ExprTranslator, ir.Expr], ir.Expr]:
    def translator(t: tr.ExprTranslator, expr: ir.Expr) -> ir.Expr:
        (arg,) = expr.op().args
        sa_arg = t.translate(arg)
        if fmt == 'millisecond':
            return sa.extract('microsecond', sa_arg) % 1000
        return sa.extract(fmt, sa_arg)

    return translator


_truncate_formats = {
    's': '%Y-%m-%d %H:%i:%s',
    'm': '%Y-%m-%d %H:%i:00',
    'h': '%Y-%m-%d %H:00:00',
    'D': '%Y-%m-%d',
    # 'W': 'week',
    'M': '%Y-%m-01',
    'Y': '%Y-01-01',
}


def _truncate(t: tr.ExprTranslator, expr: ir.Expr) -> ir.Expr:
    arg, unit = expr.op().args
    sa_arg = t.translate(arg)
    try:
        fmt = _truncate_formats[unit]
    except KeyError:
        raise com.UnsupportedOperationError(
            f'Unsupported truncate unit {unit}',
        )
    return sa.func.date_format(sa_arg, fmt)


def _cast(t: tr.ExprTranslator, expr: ir.Expr) -> ir.Expr:
    arg, typ = expr.op().args

    sa_arg = t.translate(arg)
    sa_type = t.get_sqla_type(typ)

    # specialize going from an integer type to a timestamp
    if isinstance(arg.type(), dt.Integer) and isinstance(sa_type, sa.DateTime):
        return sa.func.convert_tz(sa.func.from_unixtime(sa_arg), 'SYSTEM', 'UTC')

    if arg.type().equals(dt.binary) and typ.equals(dt.string):
        return sa.func.hex(sa_arg)

    if typ.equals(dt.binary):
        #  decode yields a column of memoryview which is annoying to deal with
        # in pandas. CAST(expr AS BYTEA) is correct and returns byte strings.
        return sa.cast(sa_arg, sa.LargeBinary())

    return sa.cast(sa_arg, sa_type)


def _log(t: tr.ExprTranslator, expr: ir.Expr) -> ir.Expr:
    arg, base = expr.op().args
    sa_arg = t.translate(arg)
    sa_base = t.translate(base)
    return sa.func.log(sa_base, sa_arg)


def _identical_to(t: tr.ExprTranslator, expr: ir.Expr) -> ir.Expr:
    left, right = args = expr.op().args
    if left.equals(right):
        return True
    else:
        left, right = map(t.translate, args)
        return left.op('<=>')(right)


def _round(t: tr.ExprTranslator, expr: ir.Expr) -> ir.Expr:
    arg, digits = expr.op().args
    sa_arg = t.translate(arg)

    if digits is None:
        sa_digits = 0
    else:
        sa_digits = t.translate(digits)

    return sa.func.round(sa_arg, sa_digits)


def _floor_divide(t: tr.ExprTranslator, expr: ir.Expr) -> ir.Expr:
    left, right = map(t.translate, expr.op().args)
    return sa.func.floor(left / right)


def _string_join(t: tr.ExprTranslator, expr: ir.Expr) -> ir.Expr:
    sep, elements = expr.op().args
    return sa.func.concat_ws(t.translate(sep), *map(t.translate, elements))


def _interval_from_integer(t: tr.ExprTranslator, expr: ir.Expr) -> ir.Expr:
    arg, unit = expr.op().args
    if unit in {'ms', 'ns'}:
        raise com.UnsupportedOperationError(
            'SingleStoreDB does not allow operation '
            'with INTERVAL offset {}'.format(unit),
        )

    sa_arg = t.translate(arg)
    text_unit = expr.type().resolution.upper()

    # XXX: Is there a better way to handle this? I.e. can we somehow use
    # the existing bind parameter produced by translate and reuse its name in
    # the string passed to sa.text?
    if isinstance(sa_arg, sa.sql.elements.BindParameter):
        return sa.text(f'INTERVAL :arg {text_unit}').bindparams(
            arg=sa_arg.value,
        )
    return sa.text(f'INTERVAL {sa_arg} {text_unit}')


def _timestamp_diff(t: tr.ExprTranslator, expr: ir.Expr) -> ir.Expr:
    left, right = expr.op().args
    sa_left = t.translate(left)
    sa_right = t.translate(right)
    return sa.func.timestampdiff(sa.text('SECOND'), sa_right, sa_left)


def _literal(t: tr.ExprTranslator, expr: ir.Expr) -> ir.Expr:
    if isinstance(expr, ir.IntervalScalar):
        if expr.type().unit in {'ms', 'ns'}:
            raise com.UnsupportedOperationError(
                'SingleStoreDB does not allow operation '
                'with INTERVAL offset {}'.format(expr.type().unit),
            )
        text_unit = expr.type().resolution.upper()
        value = expr.op().value
        return sa.text(f'INTERVAL :value {text_unit}').bindparams(value=value)
    elif isinstance(expr, ir.SetScalar):
        return list(map(sa.literal, expr.op().value))
    else:
        value = expr.op().value
        if isinstance(value, pd.Timestamp):
            value = value.to_pydatetime()
        return sa.literal(value)


def _random(t: tr.ExprTranslator, expr: ir.Expr) -> ir.Expr:
    return sa.func.random()


def _group_concat(t: tr.ExprTranslator, expr: ir.Expr) -> ir.Expr:
    op = expr.op()
    arg, sep, where = op.args
    if where is not None:
        case = where.ifelse(arg, ibis.NA)
        arg = t.translate(case)
    else:
        arg = t.translate(arg)
    return sa.func.group_concat(arg.op('SEPARATOR')(t.translate(sep)))


def _day_of_week_index(t: tr.ExprTranslator, expr: ir.Expr) -> ir.Expr:
    (arg,) = expr.op().args
    left = sa.func.dayofweek(t.translate(arg)) - 2
    right = 7
    return ((left % right) + right) % right


def _day_of_week_name(t: tr.ExprTranslator, expr: ir.Expr) -> ir.Expr:
    (arg,) = expr.op().args
    return sa.func.dayname(t.translate(arg))


def _string_find(t: tr.ExprTranslator, expr: ir.Expr) -> ir.Expr:
    op = expr.op()

    if op.end is not None:
        raise NotImplementedError('`end` not yet implemented')

    if op.start is not None:
        return sa.func.locate(
            t.translate(op.substr),
            t.translate(op.arg),
            t.translate(op.start),
        ) - 1

    return sa.func.locate(t.translate(op.substr), t.translate(op.arg)) - 1


def _string_contains(t: tr.ExprTranslator, expr: ir.Expr) -> ir.Expr:
    return _string_find(t, expr) >= 0


operation_registry.update(
    {
        ops.Literal: _literal,
        # strings
        ops.Substring: _substr,
        ops.StringFind: _string_find,
        ops.StringContains: _string_contains,
        ops.Capitalize: _capitalize,
        ops.RegexSearch: fixed_arity(lambda x, y: x.op('REGEXP')(y), 2),
        ops.Cast: _cast,
        # math
        ops.Log: _log,
        ops.Log2: unary(sa.func.log2),
        ops.Log10: unary(sa.func.log10),
        ops.Round: _round,
        ops.RandomScalar: _random,
        # dates and times
        ops.Date: unary(sa.func.date),
        ops.DateAdd: fixed_arity(operator.add, 2),
        ops.DateSub: fixed_arity(operator.sub, 2),
        ops.DateDiff: fixed_arity(sa.func.datediff, 2),
        ops.TimestampAdd: fixed_arity(operator.add, 2),
        ops.TimestampSub: fixed_arity(operator.sub, 2),
        ops.TimestampDiff: _timestamp_diff,
        ops.DateTruncate: _truncate,
        ops.TimestampTruncate: _truncate,
        ops.IntervalFromInteger: _interval_from_integer,
        ops.Strftime: fixed_arity(sa.func.date_format, 2),
        ops.ExtractYear: _extract('year'),
        ops.ExtractMonth: _extract('month'),
        ops.ExtractDay: _extract('day'),
        ops.ExtractDayOfYear: unary('dayofyear'),
        ops.ExtractQuarter: _extract('quarter'),
        ops.ExtractEpochSeconds: unary('UNIX_TIMESTAMP'),
        ops.ExtractWeekOfYear: fixed_arity('weekofyear', 1),
        ops.ExtractHour: _extract('hour'),
        ops.ExtractMinute: _extract('minute'),
        ops.ExtractSecond: _extract('second'),
        ops.ExtractMillisecond: _extract('millisecond'),
        # reductions
        #       ops.BitAnd: reduction(sa.func.bit_and),
        #       ops.BitOr: reduction(sa.func.bit_or),
        #       ops.BitXor: reduction(sa.func.bit_xor),
        #       ops.Variance: variance_reduction('var'),
        #       ops.StandardDev: variance_reduction('stddev'),
        #       ops.IdenticalTo: _identical_to,
        #       ops.TimestampNow: fixed_arity(sa.func.now, 0),
        # others
        ops.GroupConcat: _group_concat,
        ops.DayOfWeekIndex: _day_of_week_index,
        ops.DayOfWeekName: _day_of_week_name,
        #       ops.HLLCardinality: reduction(
        #           lambda arg: sa.func.count(arg.distinct()),
        #       ),
    },
)
