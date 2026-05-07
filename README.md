# Health Diary NLP Module

사용자의 건강 일기를 분석하여 수치화된 데이터를 추출하는 NLP 모듈입니다.
전략 패턴(Strategy Pattern)을 사용하여 다양한 LLM 공급자(Gemini, OpenAI 등)를 지원하며, 메타데이터 기반으로 추출 필드를 동적으로 구성합니다.

## 🛠️ 개발 환경 설정

이 프로젝트는 파이썬 가상환경 사용을 권장합니다. 프로젝트 루트 디렉토리에서 아래 단계를 진행하세요.

### 1. 가상환경 생성 및 활성화

**Windows:**

````bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
.\venv\Scripts\activate



**macOS/Linux:**

```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate
````

### 2. 의존성 설치

가상환경이 활성화된 상태(`(venv)` 표시 확인)에서 아래 명령어를 실행하여 필요한 라이브러리를 일괄 설치합니다.

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정 (.env)

애플리케이션 구동에 필요한 API Key 및 설정값 관리를 위해 프로젝트 루트에 `.env` 파일을 생성해야 합니다.

1. 프로젝트 루트의 `.env.template` 파일을 복사하여 `.env` 파일을 생성합니다.
2. 생성한 `.env` 파일에 본인의 환경에 맞는 값을 입력합니다.

**설정 항목:**

- `LLM_PROVIDER`: 사용할 LLM 공급자 선택 (`GEMINI` 또는 `OPENAI` 등등 (추가됨에 따라 기재할 예정))
- `GOOGLE_API_KEY`: Google AI Studio에서 발급받은 API 키
- `OPENAI_API_KEY`: OpenAI에서 발급받은 API 키

````

---

### 📄 .env.template

```text
# LLM 공급자 설정 (GEMINI / OPENAI)
LLM_PROVIDER=GEMINI

# Google API Key (Gemini 사용 시 필요)
GOOGLE_API_KEY=your_google_api_key_here

# OpenAI API Key (OpenAI 사용 시 필요)
OPENAI_API_KEY=your_openai_api_key_here
```
````
