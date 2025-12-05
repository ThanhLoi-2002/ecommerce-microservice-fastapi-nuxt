# Sử dụng image Python
FROM python:3.10

# Đặt thư mục làm việc
WORKDIR /app

# Sao chép file requirements.txt vào image
COPY requirements.txt .

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn vào image
COPY . .

EXPOSE 8001
# Chạy FastAPI với lệnh dev
CMD ["fastapi", "dev", "main.py", "--port", "8001"]