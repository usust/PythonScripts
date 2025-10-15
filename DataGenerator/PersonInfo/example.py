import argparse
import csv
import os
from pathlib import Path

# from 中文姓名 import *
# from 性别 import *
# from 民族 import *
# from 出生日期 import *
# from 中国地址 import *
# from 手机号 import *
# from 身份证号 import *

from DataGenerator.DateTime.date import generate_date_range
from mobile_phone import *
from name import *

save_dir = Path("/Users/lyu/Code/GitHub/PythonScripts/DataGenerator/PersonInfo/out")
save_file_name = "phone.csv"
save_file = save_dir / save_file_name


if __name__ == "__main__":
    size = 200
    os.makedirs(save_dir, exist_ok=True)
    phones = generate_mobile_phone(n=size)
    names = generate_unique_names(n=size)
    with open(save_dir / save_file_name, "w", newline='', encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["phone", "name"])

        for phone, name in zip(phones, names):
            writer.writerow([phone, name])
