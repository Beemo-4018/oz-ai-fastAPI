# 1. 파이썬 최신 안정화 버전 사용
FROM python:3.13-slim

# 2. 컨테이너 내부 작업 디렉토리 설정
WORKDIR /app

# 3. 필요한 라이브러리 설치를 위해 requirements.txt 먼저 복사
# 빌드 컨텍스트(상위 폴더) 기준으로 경로 설정
COPY api/requirements.txt .

# 4. 설치
RUN pip install --no-cache-dir -r requirements.txt

# 5. 1day 폴더 내의 모든 소스 코드를 컨테이너의 /app으로 복사
COPY api/ .

# 6. FastAPI 서버 실행 (main.py 내에 app 객체가 있다고 가정)
# --host 0.0.0.0은 외부 접속을 허용하기 위해 필수입니다.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]