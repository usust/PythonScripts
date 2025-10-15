from FileGenerator.pcap.save_pcap import save_packets_to_pcap
from ssh_package import *
from random_package import *

# 占位私钥内容（严格禁止放真实密钥）
placeholder_key = (
'''
-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----
'''
)

if __name__ == "__main__":
    pcap_out = "ssh_transfer_example.pcap"

    start_packages, start_time = generate_random_tcp_packets(count=10000, start_time=0.0)

    packets, actual_start_time = simulate_ssh_file_transfer(
        pcap_path=pcap_out,
        ether_src="02:00:00:00:00:01",    # 客户端 MAC（示例）
        ether_dst="02:00:00:00:00:02",    # 服务器 MAC（示例）
        client_ip="10.0.9.88",            # 发起下载的主机
        server_ip="10.0.1.50",            # Git/SSH 服务器
        client_port=34567,                # 随机高位源端口
        server_port=22,                   # SSH 目标端口
        file_name="deploy_rsa.key",       # 文件名
        file_content=placeholder_key,     # 传入占位私钥（str 或 bytes 均可）
        chunk_size=512,                   # 每包数据大小（可调）
        start_time=start_time,           # 起始时间（UNIX 秒）
        time_between_packets=0.001,       # 包间隔（秒）
        initial_ip_id=100,                # IP id 起始值
        initial_seq_client=1000,          # 客户端初始 seq
        initial_seq_server=2000,          # 服务器初始 seq
        # pre_noise_packets=10000,          # 传输前噪声包数量
        # post_noise_packets=10000,         # 传输后噪声包数量
        noise_packet_kwargs={"seed": 42}  # 固定随机种子便于复现
    )

    end_packages, _ = generate_random_tcp_packets(count=10000, start_time=actual_start_time)

    combined_packets = start_packages + packets + end_packages

    save_packets_to_pcap(combined_packets, pcap_out)
    print(f"Wrote {len(packets)} packets to {pcap_out}, start_time={actual_start_time}")
    print("在 Wireshark 中打开 pcap，搜索字符串 'BEGIN PRIVATE KEY' 可快速定位私钥传输包。")
