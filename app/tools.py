from app.constants import TOKEN_ROUTE


def save_token(access_token):
    f = open(TOKEN_ROUTE, 'w')
    f.write(access_token)
    f.close()


def call_token():
    f = open(TOKEN_ROUTE, 'r')
    access_token = f.read()
    f.close()

    return access_token
