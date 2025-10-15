# 运行前请先安装 scapy：
# pip install scapy
import time
from typing import List, Optional, Tuple

from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP
from scapy.packet import Raw
from scapy.utils import wrpcap

from .random_package import generate_random_tcp_packets


def simulate_ssh_file_transfer(
    pcap_path: str,
    ether_src: str,
    ether_dst: str,
    client_ip: str,
    server_ip: str,
    client_port: int,
    server_port: int,
    file_name: str,
    file_content,
    chunk_size: int = 512,
    start_time: float = None,
    time_between_packets: float = 0.001,
    initial_ip_id: int = 1,
    initial_seq_client: int = 1000,
    initial_seq_server: int = 2000,
    pre_noise_packets: int = 0,
    post_noise_packets: int = 0,
    noise_packet_kwargs: Optional[dict] = None,
) -> Tuple[List[Ether], float]:
    """
    构造并写入一个模拟的 SSH/SCP 文件传输的 pcap（离线构造，无网络 I/O）。
    所有配置均通过参数传入（无全局变量），并返回生成的包列表，方便与其它流量组合。

    参数说明（全部必须由调用者传入）:
      pcap_path: 输出 pcap 文件路径（例如 "incident_traffic.pcap"）
      ether_src / ether_dst: 以太网层的源/目的 MAC 字符串（例如 "02:00:00:00:00:01"）
      client_ip / server_ip: 客户端(发起方)与服务器 IP（字符串）
      client_port / server_port: 客户端源端口与服务器目标端口（整数，server_port 常为 22）
      file_name: 要模拟传输的文件名（例如 "deploy_rsa.key"）
      file_content: 文件内容；可以是 bytes 或 str（若为 str 会被 utf-8 编码）
      chunk_size: 每个 TCP 数据包内放置的最大字节数（默认 512）
      start_time: 第一个包的时间戳（float，UNIX 秒）。若为 None 则使用当前时间 time.time()
      time_between_packets: 包之间的时间间隔（秒）
      initial_ip_id: 第一个 IP 包的 ID 起始值（默认 1）
      initial_seq_client / initial_seq_server: TCP 初始序列号（分别用于 client/server 方向）
      pre_noise_packets / post_noise_packets: 在 SSH 传输前/后插入的随机背景包数量
      noise_packet_kwargs: 传递给 generate_random_tcp_packets 的可选参数（除 start_time 外）

    行为说明（模拟流程）:
      - 创建三次握手（SYN, SYN-ACK, ACK）
      - 模拟服务器端向客户端发送 SCP-like 控制行："C0644 <size> <filename>\\n"
      - 将文件内容分片成多个 TCP 包（server -> client），每个包标记 TCP flags 'PA'
      - 每发送一个数据包，插入一条来自客户端的纯 ACK（无 payload）
      - 发送文件结束后一个小的 NUL 控制字节（若符合 SCP 行为）
      - 发送 FIN/ACK 进行连接关闭
      - 所有包按时间戳递增写入 pcap
      - 不会进行真实网络连接；仅离线构造并写文件

    依赖:
      scapy (pip install scapy)

    返回值:
      (packets, actual_start_time):
        packets: 包含完整传输过程的 Packet 列表，可用于与其他流量拼接。
        actual_start_time: 本次生成流量的起始时间戳（float），便于外部继续排布时间线。

    注意:
      - 请确保传入的 file_content 不包含真实私钥或真实敏感信息。若为字符串，函数会自动 utf-8 编码。
      - 函数不会做任何 I/O 除了写出 pcap_path 文件。
    """


    # prepare timing and bytes
    if start_time is None:
        start_time = time.time()
    t = float(start_time)
    actual_start_time = t

    # normalize file content to bytes (caller responsible for using placeholder data)
    if isinstance(file_content, str):
        file_bytes = file_content.encode("utf-8")
    else:
        file_bytes = bytes(file_content)

    file_size = len(file_bytes)

    pkts = []
    ip_id = int(initial_ip_id)
    seq_c = int(initial_seq_client)
    seq_s = int(initial_seq_server)
    ack_c = seq_s
    ack_s = seq_c + 1  # after client's SYN

    noise_kwargs = dict(noise_packet_kwargs or {})
    noise_kwargs.pop("start_time", None)

    if pre_noise_packets > 0:
        pre_pkts, t = generate_random_tcp_packets(pre_noise_packets, t, **noise_kwargs)
        pkts.extend(pre_pkts)

    # 1) SYN (client -> server)
    syn = Ether(src=ether_src, dst=ether_dst) / IP(src=client_ip, dst=server_ip, id=ip_id) / TCP(sport=client_port, dport=server_port, flags="S", seq=seq_c)
    syn.time = t
    pkts.append(syn)
    t += time_between_packets
    ip_id += 1
    seq_c += 1  # SYN consumes 1 seq

    # 2) SYN-ACK (server -> client)
    synack = Ether(src=ether_dst, dst=ether_src) / IP(src=server_ip, dst=client_ip, id=ip_id) / TCP(sport=server_port, dport=client_port, flags="SA", seq=seq_s, ack=seq_c)
    synack.time = t
    pkts.append(synack)
    t += time_between_packets
    ip_id += 1
    seq_s += 1

    # 3) ACK (client -> server) - completes handshake
    ack = Ether(src=ether_src, dst=ether_dst) / IP(src=client_ip, dst=server_ip, id=ip_id) / TCP(sport=client_port, dport=server_port, flags="A", seq=seq_c, ack=seq_s)
    ack.time = t
    pkts.append(ack)
    t += time_between_packets
    ip_id += 1

    # 4) SCP-like control line from server indicating file send
    #    Example control line: C0644 <size> <filename>\n
    ctrl_line = f"C0644 {file_size} {file_name}\n".encode("utf-8")
    pkt_ctrl = Ether(src=ether_dst, dst=ether_src) / IP(src=server_ip, dst=client_ip, id=ip_id) / TCP(sport=server_port, dport=client_port, flags="PA", seq=seq_s, ack=seq_c) / Raw(load=ctrl_line)
    pkt_ctrl.time = t
    pkts.append(pkt_ctrl)
    t += time_between_packets
    ip_id += 1
    seq_s += len(ctrl_line)

    # client ACK for control line
    ack1 = Ether(src=ether_src, dst=ether_dst) / IP(src=client_ip, dst=server_ip, id=ip_id) / TCP(sport=client_port, dport=server_port, flags="A", seq=seq_c, ack=seq_s)
    ack1.time = t
    pkts.append(ack1)
    t += time_between_packets
    ip_id += 1

    # 5) Server sends file bytes in chunks (server -> client), with interleaved client ACKs
    offset = 0
    chunk_index = 0
    while offset < file_size:
        chunk = file_bytes[offset: offset + chunk_size]
        raw_pkt = Ether(src=ether_dst, dst=ether_src) / IP(src=server_ip, dst=client_ip, id=ip_id) / TCP(sport=server_port, dport=client_port, flags="PA", seq=seq_s, ack=seq_c) / Raw(load=chunk)
        raw_pkt.time = t
        pkts.append(raw_pkt)
        t += time_between_packets
        ip_id += 1

        seq_s += len(chunk)
        offset += len(chunk)
        chunk_index += 1

        # client immediate ACK for this chunk
        ack_chunk = Ether(src=ether_src, dst=ether_dst) / IP(src=client_ip, dst=server_ip, id=ip_id) / TCP(sport=client_port, dport=server_port, flags="A", seq=seq_c, ack=seq_s)
        ack_chunk.time = t
        pkts.append(ack_chunk)
        t += time_between_packets
        ip_id += 1

    # 6) SCP end-of-file NUL byte (some SCP implementations expect a NUL)
    nul = b"\x00"
    pkt_nul = Ether(src=ether_dst, dst=ether_src) / IP(src=server_ip, dst=client_ip, id=ip_id) / TCP(sport=server_port, dport=client_port, flags="PA", seq=seq_s, ack=seq_c) / Raw(load=nul)
    pkt_nul.time = t
    pkts.append(pkt_nul)
    t += time_between_packets
    ip_id += 1
    seq_s += 1

    # client ACK for NUL
    ack_nul = Ether(src=ether_src, dst=ether_dst) / IP(src=client_ip, dst=server_ip, id=ip_id) / TCP(sport=client_port, dport=server_port, flags="A", seq=seq_c, ack=seq_s)
    ack_nul.time = t
    pkts.append(ack_nul)
    t += time_between_packets
    ip_id += 1

    # 7) FIN from server
    fin = Ether(src=ether_dst, dst=ether_src) / IP(src=server_ip, dst=client_ip, id=ip_id) / TCP(sport=server_port, dport=client_port, flags="FA", seq=seq_s, ack=seq_c) / Raw(load=b"")
    fin.time = t
    pkts.append(fin)
    t += time_between_packets
    ip_id += 1
    seq_s += 1

    # ACK of FIN by client
    finack = Ether(src=ether_src, dst=ether_dst) / IP(src=client_ip, dst=server_ip, id=ip_id) / TCP(sport=client_port, dport=server_port, flags="A", seq=seq_c, ack=seq_s)
    finack.time = t
    pkts.append(finack)
    t += time_between_packets
    ip_id += 1

    # 8) Client FIN -> server (close both sides)
    fin2 = Ether(src=ether_src, dst=ether_dst) / IP(src=client_ip, dst=server_ip, id=ip_id) / TCP(sport=client_port, dport=server_port, flags="FA", seq=seq_c, ack=seq_s) / Raw(load=b"")
    fin2.time = t
    pkts.append(fin2)
    t += time_between_packets
    ip_id += 1
    seq_c += 1

    # Server ACK of client's FIN
    fin2ack = Ether(src=ether_dst, dst=ether_src) / IP(src=server_ip, dst=client_ip, id=ip_id) / TCP(sport=server_port, dport=client_port, flags="A", seq=seq_s, ack=seq_c)
    fin2ack.time = t
    pkts.append(fin2ack)

    t = fin2ack.time + time_between_packets
    if post_noise_packets > 0:
        post_pkts, _ = generate_random_tcp_packets(post_noise_packets, t, **noise_kwargs)
        pkts.extend(post_pkts)

    # write pcap
    wrpcap(pcap_path, pkts)

    return pkts, actual_start_time
