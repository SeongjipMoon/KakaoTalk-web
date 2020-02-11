CLIENT_ID='1714c2d9871d0b439f21d27c38051dc4'
REDIRECT_URL='http://localhost:8080'

TOKEN_ROUTE = "app/data/access_token.txt"

HEADERS = {
    'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
    'Cache-Control' : "no-cache"
}
# 메세지
REQ_PROFILE_URL = 'https://kapi.kakao.com/v1/api/talk/profile'
SEND_MESSAGE_ME_TO_URL = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'

# 사용자 URL
OAUTH_TOKEN_URL = 'https://kauth.kakao.com/oauth/token'
SIGNUP_URL = 'https://kauth.kakao.com/vi/user/signup'

LOGOUT_URL = 'https://kapi.kakao.com/v1/user/logout'
UNLINK_URL = 'https://kapi.kakao.com/v1/user/unlink'
USER_ME_URL = 'https://kapi.kakao.com/v2/user/me'
USER_LIST_URL = 'https://kapi.kakao.com/v1/user/ids'