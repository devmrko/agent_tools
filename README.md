# OCI Functions + Email Delivery(SMTP) 함수 가이드 (Korean)

## 1. 프로젝트 구조

- `send-email/`
  - `func.py`: 이메일 전송 함수 코드
  - `func.yaml`: OCI Functions 설정
  - `requirements.txt`: Python 의존성
- `env.sh`: Fn App(애플리케이션) Config에 SMTP 환경변수 설정
- `config.sh`: App/Function 상태 확인
- `.env`: 로컬에서만 사용하는 환경변수 파일(보통 gitignore)

## 2. 사전 준비 (OCI)

### 2.1 Email Delivery 설정

- **Email Delivery**에서 발신자(Approved Sender) 또는 도메인을 승인해야 합니다.
- **SMTP Credential**을 생성합니다.
  - `SMTP_USERNAME`, `SMTP_PASSWORD`로 사용합니다.

### 2.2 Fn 애플리케이션(App)

이미 App이 있다면 그대로 사용합니다.

```bash
fn list apps
```

## 3. 로컬 `.env` 파일 준비

프로젝트 루트(`agent_tool/`)에 `.env`를 생성하고 아래 값을 채웁니다.

```bash
APP_NAME=agent_tool

SMTP_HOST=smtp.email.us-chicago-1.oci.oraclecloud.com
SMTP_PORT=587
SMTP_USERNAME=YOUR_SMTP_CREDENTIAL_USERNAME
SMTP_PASSWORD=YOUR_SMTP_CREDENTIAL_PASSWORD
SMTP_FROM=approved-sender@yourdomain.com
SMTP_STARTTLS=true
```

주의:
- `KEY=VALUE` 형태로 작성합니다.
- 공백이 들어가는 값은 따옴표로 감싸세요.
  - 예: `SMTP_FROM="홍길동 <no-reply@domain.com>"`

## 4. App Config 설정하기

`env.sh`는 `.env`를 읽어서 `fn config app`에 반영합니다.

```bash
chmod u+x env.sh
./env.sh
```

확인:

```bash
chmod u+x config.sh
./config.sh
```

## 5. 함수 배포(Deploy)

`send-email/` 폴더에서 App으로 배포합니다.

```bash
cd send-email
fn -v deploy --app "$APP_NAME"
```

배포 후 함수 목록 확인:

```bash
fn list functions "$APP_NAME"
```

## 6. 함수 호출(Invoke)

아래 예시로 테스트 이메일을 보냅니다.

```bash
echo '{"to":["receiver@example.com"],"subject":"Test","text":"Hello from OCI Functions"}' \
| fn invoke "$APP_NAME" send-email
```

정상 결과 예:

```json
{"ok": true, "to": ["receiver@example.com"], "subject": "Test"}
```

## 7. 자주 발생하는 문제(트러블슈팅)

### 7.1 `tls: failed to verify certificate` (Docker Hub Pull 실패)

- 회사/기관 네트워크 방화벽/프록시/SSL 검사 때문에 발생할 수 있습니다.
- 해결 방법:
  - **핫스팟/다른 네트워크로 전환**

### 7.2 `Missing required env var(s)`

- App Config 또는 Function Config에 필요한 환경변수가 없을 때 발생합니다.
- `.env`를 채우고 `./env.sh`를 다시 실행하세요.

### 7.3 Email Delivery에서 발신자 미승인

- `SMTP_FROM` 주소가 Approved Sender가 아니면 발송 실패할 수 있습니다.
- Email Delivery에서 발신자 승인 여부 확인.

### 7.4 보안 주의

- `fn inspect app` 출력에는 `SMTP_PASSWORD`가 노출될 수 있습니다.
- 터미널 로그/스크린샷 공유 시 반드시 마스킹하세요.
