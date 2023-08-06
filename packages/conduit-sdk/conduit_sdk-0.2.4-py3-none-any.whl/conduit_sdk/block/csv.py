import datetime
from csv import QUOTE_MINIMAL, DictWriter
from decimal import Decimal, InvalidOperation
from typing import Any, Iterable, Protocol

from conduit_sdk.common.schema import ColumnType, DataColumnSchema
from conduit_sdk.errors import ValidationError


class SupportsWrite(Protocol):
    def write(self, row: str) -> None:
        ...


def write_csv(target: SupportsWrite, columns: list[DataColumnSchema], rows: Iterable[dict[str, Any]]) -> None:
    column_names = [col.name for col in columns]
    writer = DictWriter(target, fieldnames=column_names, quoting=QUOTE_MINIMAL)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)


def convert_data_for_csv(row: dict[str, Any], columns: list[DataColumnSchema]) -> dict[str, str]:
    prepared_row = {col.name: _convert_value(col.type, row.get(col.name)) for col in columns}
    return prepared_row


def convert_rows_and_write_csv(
    target: SupportsWrite,
    columns: list[DataColumnSchema],
    rows: Iterable[dict[str, Any]],
) -> None:
    converted_rows = (convert_data_for_csv(row, columns) for row in rows)
    write_csv(target, columns=columns, rows=converted_rows)


def _convert_value(column_type: ColumnType, value: Any) -> str:
    return {
        ColumnType.DATE: _convert_date,
        ColumnType.DATETIME: _convert_datetime,
        ColumnType.STRING: _convert_str,
        ColumnType.BOOL: _convert_bool,
        ColumnType.INTEGER: _convert_int,
        ColumnType.MONEY: _convert_decimal,
        ColumnType.DECIMAL: _convert_decimal,
        ColumnType.PERCENT: _convert_decimal,
    }[column_type](value)


def _convert_date(value: Any) -> str:
    if value is None:
        return ''

    if isinstance(value, datetime.datetime):
        return value.date().isoformat()

    if isinstance(value, datetime.date):
        return value.isoformat()

    try:
        return datetime.date.fromisoformat(value).isoformat()
    except (ValueError, TypeError) as ex:
        raise ValidationError(f'Invalid date format: {value}') from ex


def _convert_datetime(value: Any) -> str:
    if value is None:
        return ''

    result = _parse_datetime(value)

    if result.tzinfo is None:
        raise ValidationError(f'Datetime must contain timezone info: {value}')

    return result.isoformat()


def _parse_datetime(value: Any) -> datetime.datetime:
    if isinstance(value, datetime.datetime):
        return value

    try:
        return datetime.datetime.fromisoformat(value)
    except (ValueError, TypeError) as ex:
        raise ValidationError(f'Invalid datetime format: {value}') from ex


def _convert_str(value: Any) -> str:
    if value is None:
        return ''

    return str(value)


def _convert_bool(value: Any) -> str:
    bool_map = {
        '+': True,
        '-': False,
        'true': True,
        'false': False,
        '1': True,
        '0': False,
        '': False,
    }
    if isinstance(value, str):
        v = value.strip().lower()
        if v not in bool_map:
            raise ValidationError(f'Invalid bool value: {value}')
        return str(bool_map[v])

    return str(bool(value))


def _convert_int(value: Any) -> str:
    if value is None:
        value = 0

    try:
        return str(int(value))
    except (ValueError, TypeError) as ex:
        raise ValidationError(f'Invalid int format: {value}') from ex


def _convert_decimal(value: Any) -> str:
    if value is None:
        value = 0

    try:
        value = Decimal(value)
        value = round(value, 4)
        return str(value)
    except (InvalidOperation, TypeError, ValueError) as ex:
        raise ValidationError(f'Invalid decimal format: {value}') from ex
