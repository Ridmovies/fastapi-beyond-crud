from passlib.context import CryptContext

passwd_context = CryptContext(schemes=["bcrypt"])


def generate_passwd_hash(password: str) -> str:
    hash_password = passwd_context.hash(password)
    return hash_password

def verify_password(password: str, hash_password: str) -> bool:
    return passwd_context.verify(password, hash_password)
