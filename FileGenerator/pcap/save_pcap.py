from typing import Iterable

from scapy.all import wrpcap, Packet


def save_packets_to_pcap(packets: Iterable[Packet], output_path: str) -> None:
    """
    将 Iterable[Packet] 写入指定路径的 pcap 文件。

    参数:
      packets: 任意可迭代的 Scapy Packet 对象。
      output_path: 输出 pcap 文件路径。
    """
    wrpcap(output_path, list(packets))
