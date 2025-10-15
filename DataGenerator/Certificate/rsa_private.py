from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_rsa_private_key(key_size=2048)->bytes:
    """
    生成私钥信息
    :param key_size: 私钥长度
    :return:
    """

    # public_exponent: 公钥指数（e）
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    return private_bytes


if __name__ == "__main__":
    print(f"{generate_rsa_private_key()}")
