FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 전체 소스 코드 복사
COPY . .

# 포트 명시
EXPOSE 8000

# 실행 명령어 (uvicorn 실행)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]