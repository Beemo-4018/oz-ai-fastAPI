FROM python:3.13
WORKDIR /app

# 여기는 compose에서 build: ./worker 로 잡았으므로 현재 폴더가 기준입니다.
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# [수정] 점(.)을 콜론(:) 대신 써야 합니다.
CMD ["python", "-u", "main.py"]