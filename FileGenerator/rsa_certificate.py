from DataGenerator.Certificate.rsa_private import generate_rsa_private_key

def generate_rsa_private_file(out_file:str, key_size:int=4096):
    """
    生成一个RSA私钥文件
    :param out_file:生成的私钥文件
    :param key_size:私钥的长度
    :return:
    """
    private_key = generate_rsa_private_key(key_size=key_size)
    with open(out_file, "w") as f:
        f.write(private_key.decode())


if __name__ == '__main__':
    generate_rsa_private_file("rsa_private.key", 4096)