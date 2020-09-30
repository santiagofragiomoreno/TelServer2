import jwt


class JWTEncoder:

    def __init__(self):
        self.secret = "zrre79gzmazeq2uudhjtxkbkq147o8vn01ic8ksgeic4hrflknhx6e8fri6bewasd"

    def get_jwt(self, payload):
        jwt_code = jwt.encode(payload, self.secret, algorithm='HS256')
        return jwt_code
