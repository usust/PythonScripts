import random
from typing import List, Optional, Sequence, Tuple
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP
from scapy.packet import Raw


def generate_random_tcp_packets(
    count: int,
    start_time: float = 0.0,
    mac_pool: Optional[Sequence[str]] = None,
    ip_pool: Optional[Sequence[str]] = None,
    port_range: Tuple[int, int] = (1024, 65535),
    time_gap_range: Tuple[float, float] = (0.0001, 0.003),
    payload_size_range: Tuple[int, int] = (20, 600),
    server_port_pool: Optional[Sequence[int]] = None,
    seed: Optional[int] = None,
) -> Tuple[List[Ether], float]:
    """
    随机生成指定数量的 TCP 背景流量包，用更真实的会话流程（握手/数据/关闭），
    避免在 Wireshark 中因异常 TCP 标记而出现黑色告警。

    参数:
      count: 目标生成包数量。
      start_time: 第一个包的时间戳。
      mac_pool: MAC 地址候选列表，若不提供将使用默认随机地址。
      ip_pool: IP 地址候选列表，若不提供将使用默认随机地址。
      port_range: TCP 源端口随机范围 (闭区间)。
      time_gap_range: 每个包之间的时间随机间隔范围 (秒)。
      payload_size_range: TCP payload 的随机大小范围 (字节)。
      server_port_pool: 服务器端口候选列表；为 None 时使用常见服务端口。
      seed: 为 None 时使用系统随机源；否则使用固定随机种子，便于复现。

    返回:
      (packets, next_time):
        packets: List[Packet]，带 .time 字段。
        next_time: 生成的最后一个包时间再加一个随机间隔，可用于续接其它流量。
    """
    if count <= 0:
        return [], start_time

    rng = random.Random(seed)

    if not mac_pool:
        mac_pool = [
            "02:00:00:00:AA:01",
            "02:00:00:00:AA:02",
            "02:00:00:00:AA:03",
            "02:00:00:00:AA:04",
        ]
    if not ip_pool:
        ip_pool = [
            "10.0.0.10",
            "10.0.0.20",
            "10.0.1.30",
            "10.0.1.40",
            "192.168.1.5",
            "192.168.1.25",
        ]
    if not server_port_pool:
        server_port_pool = [22, 53, 80, 123, 389, 443, 445, 8000, 8080, 3389]

    sport_min, sport_max = port_range
    payload_min, payload_max = payload_size_range
    gap_min, gap_max = time_gap_range

    def rand_payload(n: int) -> bytes:
        return bytes(rng.randrange(0, 256) for _ in range(n))

    t = float(start_time)
    packets: List[Ether] = []

    while len(packets) < count:
        client_mac = rng.choice(mac_pool)
        server_mac_candidates = [m for m in mac_pool if m != client_mac]
        server_mac = rng.choice(server_mac_candidates) if server_mac_candidates else client_mac

        client_ip = rng.choice(ip_pool)
        server_ip_candidates = [ip for ip in ip_pool if ip != client_ip]
        server_ip = rng.choice(server_ip_candidates) if server_ip_candidates else client_ip

        client_port = rng.randint(sport_min, sport_max)
        server_port = rng.choice(server_port_pool)

        seq_client = rng.randrange(0, 2**32)
        seq_server = rng.randrange(0, 2**32)

        client_seq_curr = seq_client
        server_seq_curr = seq_server

        def add_packet(pkt) -> bool:
            nonlocal t
            if len(packets) >= count:
                return False
            pkt.time = t
            packets.append(pkt)
            t += rng.uniform(gap_min, gap_max)
            return len(packets) < count

        # SYN (client -> server)
        syn = (
            Ether(src=client_mac, dst=server_mac)
            / IP(src=client_ip, dst=server_ip, id=rng.randrange(1, 65535))
            / TCP(sport=client_port, dport=server_port, flags="S", seq=client_seq_curr)
        )
        client_seq_curr += 1
        if not add_packet(syn):
            break

        # SYN-ACK (server -> client)
        synack = (
            Ether(src=server_mac, dst=client_mac)
            / IP(src=server_ip, dst=client_ip, id=rng.randrange(1, 65535))
            / TCP(sport=server_port, dport=client_port, flags="SA", seq=server_seq_curr, ack=client_seq_curr)
        )
        server_seq_curr += 1
        if not add_packet(synack):
            continue

        # ACK (client -> server)
        ack = (
            Ether(src=client_mac, dst=server_mac)
            / IP(src=client_ip, dst=server_ip, id=rng.randrange(1, 65535))
            / TCP(sport=client_port, dport=server_port, flags="A", seq=client_seq_curr, ack=server_seq_curr)
        )
        if not add_packet(ack):
            continue

        # Random data exchange (1-3 bursts per flow)
        bursts = rng.randint(1, 3)
        for _ in range(bursts):
            if len(packets) >= count:
                break

            direction = rng.choice(["server", "client"])
            payload_len = rng.randint(payload_min, payload_max)

            if direction == "server":
                data_pkt = (
                    Ether(src=server_mac, dst=client_mac)
                    / IP(src=server_ip, dst=client_ip, id=rng.randrange(1, 65535))
                    / TCP(sport=server_port, dport=client_port, flags="PA", seq=server_seq_curr, ack=client_seq_curr)
                    / Raw(load=rand_payload(payload_len))
                )
                server_seq_curr += payload_len
                if not add_packet(data_pkt):
                    break

                ack_pkt = (
                    Ether(src=client_mac, dst=server_mac)
                    / IP(src=client_ip, dst=server_ip, id=rng.randrange(1, 65535))
                    / TCP(sport=client_port, dport=server_port, flags="A", seq=client_seq_curr, ack=server_seq_curr)
                )
                if not add_packet(ack_pkt):
                    break
            else:
                data_pkt = (
                    Ether(src=client_mac, dst=server_mac)
                    / IP(src=client_ip, dst=server_ip, id=rng.randrange(1, 65535))
                    / TCP(sport=client_port, dport=server_port, flags="PA", seq=client_seq_curr, ack=server_seq_curr)
                    / Raw(load=rand_payload(payload_len))
                )
                client_seq_curr += payload_len
                if not add_packet(data_pkt):
                    break

                ack_pkt = (
                    Ether(src=server_mac, dst=client_mac)
                    / IP(src=server_ip, dst=client_ip, id=rng.randrange(1, 65535))
                    / TCP(sport=server_port, dport=client_port, flags="A", seq=server_seq_curr, ack=client_seq_curr)
                )
                if not add_packet(ack_pkt):
                    break

        # Connection teardown (server initiated)
        if len(packets) >= count:
            continue

        fin_server = (
            Ether(src=server_mac, dst=client_mac)
            / IP(src=server_ip, dst=client_ip, id=rng.randrange(1, 65535))
            / TCP(sport=server_port, dport=client_port, flags="FA", seq=server_seq_curr, ack=client_seq_curr)
        )
        server_seq_curr += 1
        if not add_packet(fin_server):
            continue

        fin_server_ack = (
            Ether(src=client_mac, dst=server_mac)
            / IP(src=client_ip, dst=server_ip, id=rng.randrange(1, 65535))
            / TCP(sport=client_port, dport=server_port, flags="A", seq=client_seq_curr, ack=server_seq_curr)
        )
        if not add_packet(fin_server_ack):
            continue

        fin_client = (
            Ether(src=client_mac, dst=server_mac)
            / IP(src=client_ip, dst=server_ip, id=rng.randrange(1, 65535))
            / TCP(sport=client_port, dport=server_port, flags="FA", seq=client_seq_curr, ack=server_seq_curr)
        )
        client_seq_curr += 1
        if not add_packet(fin_client):
            continue

        fin_client_ack = (
            Ether(src=server_mac, dst=client_mac)
            / IP(src=server_ip, dst=client_ip, id=rng.randrange(1, 65535))
            / TCP(sport=server_port, dport=client_port, flags="A", seq=server_seq_curr, ack=client_seq_curr)
        )
        add_packet(fin_client_ack)

    return packets, t


def demo_generate_random_tcp_packets() -> None:
    """示例：调用 generate_random_tcp_packets 并打印基本信息。"""
    start_time = 0.0
    packets, next_time = generate_random_tcp_packets(
        count=20,
        start_time=start_time,
        seed=42,
    )
    print(f"Generated {len(packets)} packets; next_time={next_time}")


if __name__ == "__main__":
    demo_generate_random_tcp_packets()
