import paramiko

def convert_ssh_to_pem(ssh_rsa_key: str) -> str:
    """
    Перетворює SSH pkey (формат ssh-rsa) в формат PEM.

    :param ssh_rsa_key: Публічний ключ у форматі ssh-rsa.
    :return: Публічний ключ у форматі PEM.
    """
    try:
        # Завантажуємо SSH ключ у форматі ssh-rsa
        key = paramiko.RSAKey(filename=ssh_rsa_key)

        # Експортуємо його у формат PEM
        pem_key = key.get_base64()

        # Повертаємо ключ у форматі PEM
        return f"-----BEGIN PUBLIC KEY-----\n{pem_key}\n-----END PUBLIC KEY-----"
    except Exception as e:
        print(f"Помилка при перетворенні ключа: {e}")
        return None


# Тестовий SSH ключ у форматі ssh-rsa
ssh_rsa_key = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDtgIZ0B3+Rt2nUiWai4T8D0MJ1dQ96sIO38CgB7MBUp1aNTEGzjeW3yRT6Awk1kqhWdryp112qbjrHzKpJIkuE4hD9d5t51cYBIFfNggdqVqsftAEFqpTbwDU/DL8H928pBnLzku94cKnGoS9fUVteOlYaBPH5MbCK0o3QvPXMWPY0tKWUUmsraXQAq0T/3R8WViGmKAIZ0ef8WQ9u0cXZRs74CUsXJq5RcuUKaOp2p9IVbT3Mthjj0U4N+hngRk6BjddfTVh5i+V/TbjaO0QDiiOb5eyAZQjf4YzdO36KZC7xi2Y73k1+11DliEhAP7yJ9GpRru8K2Gx4c/7Z/Y8U9jSV0BqVOWJwTypYxnjPMD4qdulBFHDKxDfkf6Y9Uq3QrJLcYG8Ni8CdTl9COzH3mQk3KvVsacntwkrt1qFaOMKzmWQu+/chs1C0WQp7WpCQGE5gLcJLcT7sEb+en9GTr1HGOEgE+m+4Fq2yAttVZZ9ePYifdHbUpnb3RIObzC8"""

# Конвертація в формат PEM
pem_key = convert_ssh_to_pem(ssh_rsa_key)

if pem_key:
    print("Перетворений ключ у форматі PEM:")
    print(pem_key)
else:
    print("Не вдалося перетворити ключ.")
