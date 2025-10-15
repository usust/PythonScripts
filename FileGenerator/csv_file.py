from typing import Dict, Iterable, List
import csv

from DataGenerator.PersonInfo.email import generate_unique_emails
from DataGenerator.PersonInfo.name import generate_unique_names
from DataGenerator.Numerical.integer import generate_random_integers

def write_column_lists_to_csv(columns: Dict[str, Iterable], output_path: str) -> None:
    """
    将每一列的数据（以列名为键，对应可迭代对象为值）写入 CSV 文件。
    如果不同列长度不一致，缺失项会填充为空字符串。

    参数:
      columns: {列名: 数据序列}。
      output_path: 输出 CSV 路径。
    """
    headers: List[str] = list(columns.keys())
    column_data = [list(columns[name]) for name in headers]
    max_len = max((len(col) for col in column_data), default=0)

    with open(output_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for row_idx in range(max_len):
            row = [
                column_data[col_idx][row_idx] if row_idx < len(column_data[col_idx]) else ""
                for col_idx in range(len(headers))
            ]
            writer.writerow(row)

if __name__ == "__main__":
    count = 111
    ids = generate_random_integers(count, 11111111,99999999)
    emails = generate_unique_emails(count)
    names = generate_unique_names(count)
    write_column_lists_to_csv(
        {
        "id": ids,
        "email": emails,
        "name": names,},
        f"emails_{count}.csv")
