from __future__ import annotations

import random
from typing import List, Sequence


class _ProvinceEntry(dict):
    """Typed helper for static province data."""


PROVINCE_DATA: Sequence[_ProvinceEntry] = (
    {
        "province": "北京市",
        "cities": ("北京市",),
        "districts": ("东城区", "西城区", "朝阳区", "海淀区", "丰台区", "石景山区"),
    },
    {
        "province": "天津市",
        "cities": ("天津市",),
        "districts": ("和平区", "河西区", "河北区", "南开区", "滨海新区"),
    },
    {
        "province": "上海市",
        "cities": ("上海市",),
        "districts": ("黄浦区", "徐汇区", "长宁区", "静安区", "浦东新区"),
    },
    {
        "province": "重庆市",
        "cities": ("重庆市",),
        "districts": ("渝中区", "江北区", "沙坪坝区", "九龙坡区", "南岸区"),
    },
    {
        "province": "广东省",
        "cities": ("广州市", "深圳市", "佛山市", "东莞市", "珠海市"),
        "districts": ("天河区", "福田区", "南海区", "莞城区", "香洲区"),
    },
    {
        "province": "浙江省",
        "cities": ("杭州市", "宁波市", "温州市", "绍兴市"),
        "districts": ("西湖区", "余杭区", "鄞州区", "鹿城区", "越城区"),
    },
    {
        "province": "江苏省",
        "cities": ("南京市", "苏州市", "无锡市", "常州市"),
        "districts": ("玄武区", "鼓楼区", "吴中区", "滨湖区", "天宁区"),
    },
    {
        "province": "四川省",
        "cities": ("成都市", "绵阳市", "德阳市", "乐山市"),
        "districts": ("锦江区", "青羊区", "涪城区", "广汉市", "市中区"),
    },
    {
        "province": "湖北省",
        "cities": ("武汉市", "宜昌市", "襄阳市"),
        "districts": ("江汉区", "洪山区", "宜都市", "樊城区", "东津新区"),
    },
    {
        "province": "陕西省",
        "cities": ("西安市", "咸阳市", "宝鸡市"),
        "districts": ("雁塔区", "碑林区", "秦都区", "金台区"),
    },
    {
        "province": "山东省",
        "cities": ("济南市", "青岛市", "烟台市"),
        "districts": ("历下区", "市南区", "芝罘区", "崂山区"),
    },
    {
        "province": "湖南省",
        "cities": ("长沙市", "株洲市", "岳阳市"),
        "districts": ("岳麓区", "雨花区", "天元区", "岳阳楼区"),
    },
    {
        "province": "河北省",
        "cities": ("石家庄市", "唐山市", "保定市"),
        "districts": ("长安区", "路北区", "竞秀区", "桥西区"),
    },
    {
        "province": "福建省",
        "cities": ("福州市", "厦门市", "泉州市"),
        "districts": ("鼓楼区", "仓山区", "思明区", "丰泽区"),
    },
    {
        "province": "海南省",
        "cities": ("海口市", "三亚市"),
        "districts": ("龙华区", "美兰区", "吉阳区", "天涯区"),
    },
    {
        "province": "广西壮族自治区",
        "cities": ("南宁市", "桂林市", "柳州市"),
        "districts": ("青秀区", "西乡塘区", "象山区", "柳北区"),
    },
    {
        "province": "内蒙古自治区",
        "cities": ("呼和浩特市", "包头市", "鄂尔多斯市"),
        "districts": ("新城区", "玉泉区", "昆都仑区", "东胜区"),
    },
    {
        "province": "宁夏回族自治区",
        "cities": ("银川市", "石嘴山市"),
        "districts": ("兴庆区", "金凤区", "大武口区"),
    },
    {
        "province": "新疆维吾尔自治区",
        "cities": ("乌鲁木齐市", "喀什地区", "昌吉市"),
        "districts": ("天山区", "沙依巴克区", "乌鲁木齐县", "喀什市"),
    },
    {
        "province": "西藏自治区",
        "cities": ("拉萨市", "日喀则市"),
        "districts": ("城关区", "堆龙德庆区", "桑珠孜区"),
    },
    {
        "province": "香港特别行政区",
        "cities": ("香港特别行政区",),
        "districts": ("中西区", "湾仔区", "深水埗区", "油尖旺区"),
    },
    {
        "province": "澳门特别行政区",
        "cities": ("澳门特别行政区",),
        "districts": ("花地玛堂区", "花王堂区", "望德堂区", "圣方济各堂区"),
    },
    {
        "province": "甘肃省",
        "cities": ("兰州市", "天水市"),
        "districts": ("城关区", "七里河区", "秦州区"),
    },
    {
        "province": "青海省",
        "cities": ("西宁市", "海东市"),
        "districts": ("城东区", "城中区", "乐都区"),
    },
)


def generate_location(*, seed: int | None = None) -> str:
    """
    生成一个概略地址（省/直辖市/自治区 + 地级市/地区 + 区县）。

    参数:
        seed: 可选随机种子，便于复现。

    返回:
        形如“广东省 广州市 天河区”的字符串。
    """
    if not PROVINCE_DATA:
        raise ValueError("未配置可用的省份数据")

    rng = random.Random(seed)
    entry = rng.choice(PROVINCE_DATA)

    province = entry["province"]
    city = rng.choice(entry["cities"])
    district = rng.choice(entry["districts"])

    return f"{province} {city} {district}"


def generate_locations(
    count: int,
    *,
    seed: int | None = None,
) -> List[str]:
    """
    批量生成概略地址。

    参数:
        count: 所需地址数量，必须为正整数。
    关键字参数:
        seed: 可选随机种子，便于复现。

    返回:
        地址字符串列表。
    """
    if count <= 0:
        raise ValueError("count 必须为正整数")

    rng = random.Random(seed)
    return [
        generate_location(seed=rng.randint(0, 1_000_000_000))
        for _ in range(count)
    ]
