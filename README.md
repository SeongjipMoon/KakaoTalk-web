# 카카오톡 웹

```
* 피시방에서 카톡 깔기 귀찮고 인증하기 싫을 때
* 우분투 사용 중 wine 깔기 싫고 pc의 부담을 줄이기 위해
* 사지방(군대 사이버 지식 정보방)에서 카톡하고 싶을 때
* 폰을 잃어버려 핸드폰으로 카톡을 못할 때
```

## 카카오 REST API 개발가이드
https://developers.kakao.com/docs/restapi

### 카카오톡 제공 API
```
1. 프로필 요청
2. 친구 목록
3. 메시지 전송
4. 나에게 보내기
5. 좀 더 해주지
```

### 실행 전
```buildoutcfg
app.constants.py의 정보를 바꿔줘야한다.
```

### 맨 처음 목표
```buildoutcfg
웹서버 로그인 -> (카톡 로그인) -> 사용자의 친구목록 다 뜸 -> 친구1에게 (메세지 + 서버 채팅방 초대장) 보냄 
-> 친구1과 사용자가 채팅 -> 사용자가 채팅을 끝냄 -> 채팅방 내용을 친구1에게 모두 전송 
-> 다시 친구1에게 (메세지 + 서버 채팅방 초대장) 보냄 -> 이전에 대화 나눴던 내용 존재
```

(문제점) 카카오가 친구목록을 제공하긴 하는데 / (origin 카톡 친구) + 웹서버에 회원가입 된 사용자 = 친구 목록 뜸

### 바뀐 목표 (사용자와 친구1이 웹서버를 사용한다 가정)
```buildoutcfg
웹서버 로그인 -> (카톡 로그인) -> (origin 카톡 친구 + 웹서버에 회원가입 된 사용자) 목록을 보여줌 
-> 사용자가 친구1에게 메세지 + socket.io를 보냄 -> 친구1이 사용자에게 메세지 + socket.io를 보냄 = db에 다 쌓임
```
