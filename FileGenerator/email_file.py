from email import policy
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from pathlib import Path
from typing import Mapping, Optional, Sequence, Tuple


def create_email_file(
    output_path: str,
    *,
    subject: str,
    sender: str,
    to: Sequence[str],
    body: str,
    cc: Optional[Sequence[str]] = None,
    bcc: Optional[Sequence[str]] = None,
    additional_headers: Optional[Mapping[str, str]] = None,
    attachments: Optional[Sequence[Tuple[str, bytes, str]]] = None,
    encoding: str = "utf-8",
) -> Path:
    """
    根据传入参数构造一封邮件并写入 .eml 文件。

    参数:
      output_path: 邮件保存路径。
      subject: 邮件主题。
      sender: 发件人地址。
      to: 收件人列表。
      body: 邮件正文（纯文本）。
      cc / bcc: 抄送、密送列表（可选）。
      additional_headers: 额外自定义头部，例如 {"X-Env": "staging"}。
      attachments: 附件列表，每项为 (filename, content_bytes, mime_type)。
      encoding: 正文编码。

    返回:
      实际写入的 Path 对象。
    """
    message = EmailMessage(policy=policy.default)
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = ", ".join(to)
    if cc:
        message["Cc"] = ", ".join(cc)
    if bcc:
        message["Bcc"] = ", ".join(bcc)
    message["Date"] = formatdate(localtime=True)
    message["Message-ID"] = make_msgid()

    if additional_headers:
        for key, value in additional_headers.items():
            message[key] = value

    message.set_content(body, charset=encoding)

    if attachments:
        for filename, content, mime_type in attachments:
            maintype, _, subtype = mime_type.partition("/")
            if not subtype:
                maintype, subtype = "application", "octet-stream"
            message.add_attachment(
                content,
                maintype=maintype,
                subtype=subtype,
                filename=filename,
            )

    output_path_obj = Path(output_path)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)
    output_path_obj.write_bytes(message.as_bytes())
    return output_path_obj


if __name__ == "__main__":
    demo_body = (
        "各位同事，\n\n"
        "附件为本周项目进展，请查收。若有疑问可直接回复本邮件或在会议上讨论。\n\n"
        "此致\n敬礼"
    )

    csv_attachment_path = Path("demo_report.csv")
    csv_attachment_path.write_text("id,value\n1,42\n2,84\n", encoding="utf-8")

    create_email_file(
        output_path="demo_email.eml",
        subject="【示例】项目周报",
        sender="project.owner@example.com",
        to=["dev.team@example.com", "qa.team@example.com"],
        body=demo_body,
        cc=["stakeholder@example.com"],
        bcc=["manager@example.com"],
        additional_headers={"X-Demo": "true"},
        attachments=[
            ("report.txt", b"Week summary: all milestones on track.", "text/plain"),
            ("chart.png", b"\x89PNG\r\n\x1a\n...", "image/png"),
            (csv_attachment_path.name, csv_attachment_path.read_bytes(), "text/csv"),
        ],
        encoding="utf-8",
    )
    print("Demo email written to demo_email.eml")
