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
        #
        #
        # # 性别
        # gender = generate_gender_by_ratio(n=size,ratios={"男": 50, "女": 50})
        # # 民族
        # ethnic = generate_ethnic_sample(n=size)
        # # 出生日期
        # birthdate = generate_birthdates(n=size, start_year=1950)
        # # 地址
        # home_addresses = generate_home_addresses(n=size)
        # # 手机号
        # phones = generate_phone_numbers(n=size)
        # # 身份证号
        # ids = generate_unique_id_numbers(n=size)
        # # 组装成 DataFrame
        # df = pd.DataFrame({
        #     "姓名": names,
        #     "性别": gender,
        #     "民族": ethnic,
        #     "出生日期": birthdate,
        #     "家庭住址": home_addresses,
        #     "手机号": phones,
        #     "身份证号": ids
        # })
        #
        # # 保存为 CSV 文件（默认 UTF-8 编码）
        # df.to_csv("/Users/lyu/TMP/4/persons_sender.csv", index=False, encoding='utf-8')  # utf-8-sig 为加上 BOM 防止 Excel 乱码
        #
        # print("✅ 模拟数据已保存为 '模拟用户数据.csv'")
