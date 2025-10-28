from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Sequence


def add_column_to_csv(
    column_name: str,
    values: Sequence[Any],
    *,
    csv_path: str,
    encoding: str = "utf-8",
    delimiter: str = ",",
) -> Path:
    """
    为指定 CSV 文件新增一列。

    参数:
        column_name: 新列名。
        values: 新列的数据，长度需与 CSV 中现有数据行数一致。
    关键字参数:
        csv_path: 目标 CSV 文件路径。
        encoding: 文件编码，默认 utf-8。
        delimiter: 列分隔符，默认逗号。

    返回:
        写入完成后的 CSV 文件路径。

    异常:
        FileNotFoundError: 指定的 CSV 文件不存在。
        ValueError: 列名为空、列已存在或数据长度不匹配时抛出。
    """
    if not column_name:
        raise ValueError("列名不能为空。")

    target_path = Path(csv_path)
    if not target_path.exists():
        raise FileNotFoundError(f"未找到 CSV 文件: {target_path}")

    with target_path.open("r", newline="", encoding=encoding) as src_file:
        reader = csv.reader(src_file, delimiter=delimiter)
        rows = list(reader)

    if not rows:
        raise ValueError(f"CSV 文件为空: {target_path}")

    header, *data_rows = rows
    if column_name in header:
        raise ValueError(f"列 '{column_name}' 已存在于 CSV 文件中。")

    if len(values) != len(data_rows):
        raise ValueError(
            f"提供的值数量({len(values)})与数据行数({len(data_rows)})不一致。"
        )

    updated_rows = [header + [column_name]]
    for row, value in zip(data_rows, values):
        updated_rows.append(list(row) + [value])

    with target_path.open("w", newline="", encoding=encoding) as dst_file:
        writer = csv.writer(dst_file, delimiter=delimiter)
        writer.writerows(updated_rows)

    return target_path


def count_csv_rows(
    csv_path: str | Path,
    *,
    encoding: str = "utf-8",
    delimiter: str = ",",
) -> int:
    """
    统计 CSV 文件的行数（包含表头行）。

    参数:
        csv_path: 待统计的 CSV 文件路径。
    关键字参数:
        encoding: 文件编码，默认 utf-8。
        delimiter: 列分隔符，默认逗号。

    返回:
        读取到的总行数。

    异常:
        FileNotFoundError: 指定的 CSV 文件不存在。
    """
    target_path = Path(csv_path)
    if not target_path.exists():
        raise FileNotFoundError(f"未找到 CSV 文件: {target_path}")

    with target_path.open("r", newline="", encoding=encoding) as src_file:
        reader = csv.reader(src_file, delimiter=delimiter)
        row_count = sum(1 for _ in reader)

    return row_count


def _coerce_csv_bool(value: Any) -> bool:
    """
    将 CSV 单元格内容转换为布尔值；允许常见的 True/False 表示。
    """
    if isinstance(value, bool):
        return value
    if value is None:
        return False

    normalized = str(value).strip().lower()
    if not normalized:
        return False
    if normalized in {"true", "1", "yes", "y"}:
        return True
    if normalized in {"false", "0", "no", "n"}:
        return False

    raise ValueError(f"无法将值 '{value}' 解释为布尔类型。")


def clear_column_when_flag_requires_empty(
    csv_path: str | Path,
    *,
    flag_column: str,
    target_column: str,
    empty_when_flag_true: bool = False,
    encoding: str = "utf-8",
    delimiter: str = ",",
) -> Path:
    """
    根据布尔标记列控制另一列是否应为空，如果应为空且存在数据则清空该单元格。

    参数:
        csv_path: 目标 CSV 文件路径。
    关键字参数:
        flag_column: 标记是否应为空的列名，值需能解析为布尔。
        target_column: 需要被清空的列名。
        empty_when_flag_true: 为 True 时，flag_column 为真代表 target_column 应为空；
            否则为 False 时代表 flag_column 为假时 target_column 应为空。默认 False。
        encoding: 文件编码，默认 utf-8。
        delimiter: 列分隔符，默认逗号。

    返回:
        写入完成后的 CSV 文件路径。

    异常:
        FileNotFoundError: 指定的 CSV 文件不存在。
        ValueError: 缺失列、文件无表头或布尔值不可解析时抛出。
    """
    target_path = Path(csv_path)
    if not target_path.exists():
        raise FileNotFoundError(f"未找到 CSV 文件: {target_path}")

    with target_path.open("r", newline="", encoding=encoding) as src_file:
        reader = csv.DictReader(src_file, delimiter=delimiter)
        fieldnames = reader.fieldnames
        if not fieldnames:
            raise ValueError(f"CSV 文件缺少表头: {target_path}")
        if flag_column not in fieldnames:
            raise ValueError(f"未在 CSV 中找到布尔列: {flag_column}")
        if target_column not in fieldnames:
            raise ValueError(f"未在 CSV 中找到目标列: {target_column}")

        rows = list(reader)

    updated_rows: list[dict[str, Any]] = []
    for row in rows:
        flag_value = _coerce_csv_bool(row.get(flag_column, ""))
        should_empty = flag_value if empty_when_flag_true else not flag_value

        if should_empty:
            cell_value = row.get(target_column, "")
            if cell_value and cell_value.strip():
                row[target_column] = ""

        updated_rows.append(row)

    with target_path.open("w", newline="", encoding=encoding) as dst_file:
        writer = csv.DictWriter(dst_file, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(updated_rows)

    return target_path


def remove_csv_column(
    csv_path: str | Path,
    column_name: str,
    *,
    encoding: str = "utf-8",
    delimiter: str = ",",
) -> Path:
    """
    删除 CSV 文件中的指定列并写回文件。

    参数:
        csv_path: 目标 CSV 文件路径。
        column_name: 待删除的列名。
    关键字参数:
        encoding: 文件编码，默认 utf-8。
        delimiter: 列分隔符，默认逗号。

    返回:
        写入完成后的 CSV 文件路径。

    异常:
        FileNotFoundError: 指定的 CSV 文件不存在。
        ValueError: CSV 缺少表头或指定列不存在时抛出。
    """
    target_path = Path(csv_path)
    if not target_path.exists():
        raise FileNotFoundError(f"未找到 CSV 文件: {target_path}")

    with target_path.open("r", newline="", encoding=encoding) as src_file:
        reader = csv.DictReader(src_file, delimiter=delimiter)
        fieldnames = reader.fieldnames
        if not fieldnames:
            raise ValueError(f"CSV 文件缺少表头: {target_path}")
        if column_name not in fieldnames:
            raise ValueError(f"未在 CSV 中找到列: {column_name}")

        remaining_fieldnames = [name for name in fieldnames if name != column_name]
        rows = [
            {key: value for key, value in row.items() if key != column_name}
            for row in reader
        ]

    with target_path.open("w", newline="", encoding=encoding) as dst_file:
        writer = csv.DictWriter(dst_file, fieldnames=remaining_fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(rows)

    return target_path


def extract_csv_columns(
    source_csv_path: str | Path,
    selected_columns: Sequence[str],
    *,
    output_csv_path: str | Path,
    encoding: str = "utf-8",
    delimiter: str = ",",
) -> Path:
    """
    从源 CSV 中提取指定列并写入新的 CSV 文件。

    参数:
        source_csv_path: 原始 CSV 文件路径。
        selected_columns: 需要提取的列名列表。
    关键字参数:
        output_csv_path: 输出 CSV 文件路径。
        encoding: 文件编码，默认 utf-8。
        delimiter: 列分隔符，默认逗号。

    返回:
        新 CSV 文件的路径。

    异常:
        FileNotFoundError: 源 CSV 文件不存在时抛出。
        ValueError: CSV 缺少表头或任一目标列不存在时抛出。
    """
    if not selected_columns:
        raise ValueError("selected_columns 不能为空")

    source_path = Path(source_csv_path)
    if not source_path.exists():
        raise FileNotFoundError(f"未找到 CSV 文件: {source_path}")

    with source_path.open("r", newline="", encoding=encoding) as src_file:
        reader = csv.DictReader(src_file, delimiter=delimiter)
        fieldnames = reader.fieldnames
        if not fieldnames:
            raise ValueError(f"CSV 文件缺少表头: {source_path}")

        normalized_map = {
            name.lstrip("\ufeff"): name for name in fieldnames
        }

        missing_columns = [
            col for col in selected_columns if col not in normalized_map
        ]
        if missing_columns:
            missing_str = ", ".join(missing_columns)
            raise ValueError(f"未找到列: {missing_str}")

        rows = [
            {col: row[normalized_map[col]] for col in selected_columns}
            for row in reader
        ]

    output_path = Path(output_csv_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding=encoding) as dst_file:
        writer = csv.DictWriter(dst_file, fieldnames=list(selected_columns), delimiter=delimiter)
        writer.writeheader()
        writer.writerows(rows)

    return output_path
