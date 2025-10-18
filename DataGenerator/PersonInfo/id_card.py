from faker import Faker


def generate_unique_id_numbers(n: int)->list:
    """
    批量生成不重复的身份证号
    Args:
        n (int): 批量生成的数量
    Returns:
        身份证号码集合
    """
    fake = Faker("zh_CN")
    id_set = set()

    while len(id_set) < n:
        id_num = fake.ssn()
        id_set.add(id_num)

    return list(id_set)



def parse_birth_ymd_from_id(id_number: str, auto_century: bool = True, century_for_15: int = 1900)->tuple[int, int, int]:
    """
    根据中国身份证号解析出生 年、月、日。

    规则:
    - 18位身份证: 第7-14位为出生日期 YYYYMMDD。
    - 15位身份证: 第7-12位为出生日期 YYMMDD；
      当 auto_century=True 时，若 YY 小于等于当前年份的后两位，推断为 2000 年代，否则 1900 年代；
      当 auto_century=False 时，使用 century_for_15 作为世纪（默认为 1900）。

    参数:
        id_number (str): 身份证号，支持 18/15 位，末位可为 X/x（18位）。
        auto_century (bool): 是否对 15 位证号自动推断世纪。
        century_for_15 (int): 当 auto_century=False 时用于 15 位证号的世纪基数（1900 或 2000）。

    返回:
        tuple[int, int, int]: (year, month, day)，均为零填充字符串，例如 ("1990","01","05")。

    异常:
        ValueError: 当格式非法或日期无效时抛出。
    """
    if not id_number:
        raise ValueError("身份证号不能为空")

    s = id_number.strip().upper()

    if len(s) == 18:
        # 18位: YYYYMMDD 在 [6:14]
        if not (s[:17].isdigit() and (s[-1].isdigit() or s[-1] == 'X')):
            raise ValueError("18位身份证格式非法")
        birth = s[6:14]
        year, month, day = birth[:4], birth[4:6], birth[6:8]
    elif len(s) == 15:
        # 15位: YYMMDD 在 [6:12]
        if not s.isdigit():
            raise ValueError("15位身份证应全为数字")
        birth = s[6:12]
        yy = int(birth[:2])
        if auto_century:
            from datetime import datetime
            cur_yy = datetime.now().year % 100
            century = 2000 if yy <= cur_yy else 1900
        else:
            if century_for_15 not in (1900, 2000):
                raise ValueError("century_for_15 只能是 1900 或 2000")
            century = century_for_15
        year = str(century + yy)
        month, day = birth[2:4], birth[4:6]
    else:
        raise ValueError("身份证号长度应为15或18位")

    # 校验日期有效性
    from datetime import date
    try:
        date(int(year), int(month), int(day))
    except Exception as e:
        raise ValueError("身份证中的出生日期无效") from e

    return int(year), int(month), int(day)
