from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable, List, Sequence, Tuple


DEFAULT_FILE_TYPES = (
    "合同协议", "通告", "告示", "会议记录", "通知", "报告", "申请书",
    "工作总结", "方案说明", "计划书", "合作备忘录", "会议纪要", "考核表",
    "调研报告", "培训资料", "制度规范", "公告", "通知函", "声明", "公告栏",
    "日常通知", "工作安排", "临时通告", "材料清单", "技术说明", "调度记录",
)

DEFAULT_LONG_SENTENCES = (
    "鉴于当前形势复杂多变，且各项任务紧迫，为确保工作顺利推进，特制定以下规定，望各相关部门认真贯彻落实，确保责任明确到人，措施具体有效。",
    "根据上级文件精神，同时结合我单位实际情况，经多次调研与充分讨论，形成本方案，旨在规范管理流程，提高工作效率，推动整体发展迈上新台阶。",
    "会议期间，参会人员围绕核心议题展开充分讨论，不仅针对存在的问题进行了深入剖析，而且提出了切实可行的改进措施，为后续工作指明了方向。",
    "为确保项目按计划实施，各责任部门须密切配合，合理调配资源，并严格按照时间节点完成各项任务，从而保证质量和进度双达标，避免延误带来的不利影响。",
    "本协议自双方签字盖章之日起生效，合同有效期为一年，期满后双方可根据实际情况协商续签或终止，所有条款均具有同等法律效力，不得随意变更。",
    "各单位应高度重视文件精神，加强组织领导，落实具体措施，确保各项任务按时高质量完成，同时积极防范各类风险隐患，保障工作安全稳定开展。",
    "在工作开展过程中，应建立健全监督机制，及时发现并整改存在的问题，推动工作规范化、制度化，进一步保障各项目标的顺利实现。",
    "鉴于近年来行业形势变化，结合我司战略规划，特制定本发展计划，明确目标任务和实施步骤，以推动企业持续健康发展，增强市场竞争力。",
    "本次调研重点围绕市场需求变化、客户满意度及竞争态势展开，结合调研结果提出切实有效的改进建议，为后续决策提供科学依据。",
    "双方同意加强合作，共享资源信息，充分发挥各自优势，推动项目高效落地，实现合作共赢的目标，促进共同发展与繁荣。",
)

DEFAULT_CONNECTORS = (
    "此外，", "同时，", "因此，", "然而，", "不过，", "总的来说，", "鉴于上述情况，",
    "需要特别指出的是，", "值得注意的是，", "总体来看，", "综上所述，", "显然，",
    "据此，", "基于以上分析，", "为此，",
)

DEFAULT_FORMAL_CLAUSES = (
    "第一条 适用范围：本文件适用于相关部门及人员，明确职责和义务，保障各项工作顺利实施。",
    "第二条 工作要求：须严格按照流程执行，确保工作质量与效率达到预期标准，杜绝任何违规操作。",
    "第三条 时间安排：各阶段任务须按时完成，逾期将影响整体进度，并承担相应责任。",
    "第四条 责任分工：明确责任人，落实岗位职责，确保各项任务有人负责，有序推进。",
    "第五条 监督检查：建立定期检查制度，确保各项工作按计划开展，发现问题及时整改。",
    "第六条 违约处理：违反规定者将依据相关条例进行处理，包括但不限于罚款、警告及解除合同。",
    "第七条 保密要求：涉及信息须严格保密，未经授权不得对外泄露，违者承担法律责任。",
    "第八条 变更管理：文件内容变更须经双方同意并签署书面协议，确保变更合法有效。",
    "第九条 期限及终止：合同有效期限为一年，期满后双方可协商续签或终止合作。",
    "第十条 附则：本文件未尽事项由双方另行协商确定，具有同等法律效力。",
)

DEFAULT_SIGN_OFFS = (
    "甲方代表签字：______________",
    "乙方代表签字：______________",
    "签署日期：{}",
    "以上内容请知悉并遵照执行。",
    "此通知自发布之日起生效，请相关部门认真落实。",
    "文件由办公室负责解释。",
    "感谢配合。",
)


@dataclass
class DocumentGeneratorConfig:
    """配置文档生成策略。
    """


    target_length: int = 500
    """目标输出的文本长度（字符数），用于控制生成内容规模。"""

    intro_paragraphs: Tuple[int, int] = (2, 4)
    """开头部分段落数量范围（含标题后的引言）。"""

    body_paragraphs: Tuple[int, int] = (15, 20)
    """正文部分段落数量范围（主内容）。"""

    sentences_per_paragraph: Tuple[int, int] = (1, 4)
    """每个段落包含句子的数量范围。"""

    allow_empty_lines: bool = False
    """是否允许段落之间插入额外空行。"""

    empty_line_probability: float = 0.2
    """当允许空行时，插入空行的概率。"""

    max_extra_empty_lines: int = 2
    """单次插入空行时的最大额外空行数量。"""

    clause_probability: float = 0.7
    """是否插入条款段落的概率。"""

    clauses_per_document: Tuple[int, int] = (3, 6)
    """当插入条款时，选择条款数量的范围。"""

    sign_off_probability: float = 0.6
    """在结尾添加落款信息的概率。"""

    file_types: Sequence[str] = field(default_factory=lambda: DEFAULT_FILE_TYPES)
    """标题类型候选池。"""

    sentences_pool: Sequence[str] = field(default_factory=lambda: DEFAULT_LONG_SENTENCES)
    """正文句子素材池。"""

    connectors: Sequence[str] = field(default_factory=lambda: DEFAULT_CONNECTORS)
    """可选句首连接词集合。"""

    clauses: Sequence[str] = field(default_factory=lambda: DEFAULT_FORMAL_CLAUSES)
    """条款段落素材集合。"""

    sign_offs: Sequence[str] = field(default_factory=lambda: DEFAULT_SIGN_OFFS)
    """落款及附言素材集合。"""

    def validate(self) -> None:
        if self.target_length <= 0:
            raise ValueError("target_length 必须大于 0")
        if self.intro_paragraphs[0] <= 0 or self.body_paragraphs[0] <= 0:
            raise ValueError("段落数量需要为正整数")
        if self.sentences_per_paragraph[0] <= 0:
            raise ValueError("每段最少句子数量必须大于 0")
        if not 0 <= self.empty_line_probability <= 1:
            raise ValueError("empty_line_probability 必须在 0 与 1 之间")
        if not 0 <= self.clause_probability <= 1:
            raise ValueError("clause_probability 必须在 0 与 1 之间")
        if not 0 <= self.sign_off_probability <= 1:
            raise ValueError("sign_off_probability 必须在 0 与 1 之间")
        if not self.file_types or not self.sentences_pool:
            raise ValueError("file_types 与 sentences_pool 不能为空")


def generate_document(config: DocumentGeneratorConfig, *, seed: int | None = None) -> str:
    """
    根据配置生成单个文档内容。

    :param config: 文档生成配置
    :param seed: 可选随机种子，便于复现
    :return: 文档内容字符串
    """
    config.validate()
    rng = random.Random(seed)

    title = f"{rng.choice(config.file_types)} 编号：{rng.randint(10000, 99999)}"
    content: List[str] = [title, ""]

    intro_count = rng.randint(*config.intro_paragraphs)
    content.extend(_generate_paragraphs(intro_count, config, rng))

    if rng.random() < config.clause_probability and config.clauses:
        clause_count = min(len(config.clauses), rng.randint(*config.clauses_per_document))
        content.append("")
        for clause in rng.sample(config.clauses, clause_count):
            content.append(clause)

    body_count = rng.randint(*config.body_paragraphs)
    content.extend(_generate_paragraphs(body_count, config, rng))

    if rng.random() < config.sign_off_probability:
        content.append("")
        date_str = datetime.now().strftime("%Y年%m月%d日")
        for line in config.sign_offs:
            content.append(line.format(date_str) if "{}" in line else line)
    else:
        content.append("")
        content.append("本文档内容为参考资料，未经授权不得擅自修改或外传。")

    full_text = "\n".join(content).strip()

    while len(full_text) < config.target_length:
        full_text = (full_text + "\n" + _generate_paragraph(config, rng)).strip()

    full_text = _truncate_text(full_text, config.target_length)
    return full_text + "\n"


def generate_documents(config: DocumentGeneratorConfig, count: int, *, seed: int | None = None) -> List[str]:
    """
    批量生成文档。

    :param config: 文档生成配置
    :param count: 生成数量
    :param seed: 可选随机种子
    :return: 文本列表
    """
    if count <= 0:
        raise ValueError("count 必须为正整数")
    rng = random.Random(seed)
    return [generate_document(config, seed=rng.randint(0, 1_000_000_000)) for _ in range(count)]


def _generate_paragraphs(count: int, config: DocumentGeneratorConfig, rng: random.Random) -> List[str]:
    return [_generate_paragraph(config, rng) for _ in range(count)]


def _generate_paragraph(config: DocumentGeneratorConfig, rng: random.Random) -> str:
    min_sentences, max_sentences = config.sentences_per_paragraph
    sentence_total = rng.randint(min_sentences, max_sentences)

    sentences = []
    for _ in range(sentence_total):
        sentence = rng.choice(config.sentences_pool)
        if rng.random() < 0.5 and config.connectors:
            connector = rng.choice(config.connectors)
            sentence = connector + sentence[0].lower() + sentence[1:]
        sentences.append(sentence)

    paragraph = " ".join(sentences)

    if config.allow_empty_lines and rng.random() < config.empty_line_probability:
        extra_lines = rng.randint(1, config.max_extra_empty_lines)
        paragraph = paragraph + ("\n" * extra_lines)

    return paragraph


def _truncate_text(text: str, target_length: int) -> str:
    if target_length <= 0:
        return ""
    if len(text) <= target_length:
        return text
    return text[:target_length].rstrip()


if __name__ == "__main__":
    demo_config = DocumentGeneratorConfig(target_length=500, allow_empty_lines=True, clause_probability=0)
    docs = generate_documents(demo_config, count=1, seed=42)
    for idx, doc in enumerate(docs, 1):
        print(f"=== 文档 {idx} ===")
        print(doc)
