from passlib.hash import pbkdf2_sha256


class Hash:
    @classmethod
    def hash(cls, password: str):
        return pbkdf2_sha256.hash(password)

    @classmethod
    def verify(cls, plain_password: str, hashed_password: str):
        return pbkdf2_sha256.verify(plain_password, hashed_password)
