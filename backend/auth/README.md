# Auth Service Backend

Đây là dịch vụ backend auth cho hệ thống microservice e-commerce, cung cấp các tính năng xác thực người dùng, quản lý cuộc trò chuyện, tin nhắn, và tích hợp Socket.IO cho thời gian thực.

## Công nghệ sử dụng

- **FastAPI**: Framework web API nhanh và hiện đại cho Python.
- **SQLAlchemy**: ORM để tương tác với cơ sở dữ liệu PostgreSQL.
- **Socket.IO**: Thư viện để giao tiếp thời gian thực qua WebSocket.
- **Redis**: Bộ nhớ cache và lưu trữ phiên.
- **Cloudinary**: Dịch vụ lưu trữ và xử lý media.
- **Pydantic**: Validation dữ liệu và quản lý cấu hình.
- **Alembic**: Migration cơ sở dữ liệu.
- **JWT**: Xác thực token.
- **SMTP**: Gửi email.

## Cấu trúc thư mục

```
backend/auth/
├── app/
│   ├── api/v1/
│   │   ├── api.py              # Router chính
│   │   └── routes/             # Các endpoint API
│   │       ├── auth.py         # Xác thực (signin, signup, refresh-token)
│   │       ├── user.py         # Quản lý người dùng
│   │       ├── conversation.py # Quản lý cuộc trò chuyện
│   │       ├── message.py      # Quản lý tin nhắn
│   │       ├── media.py        # Upload và quản lý media
│   │       ├── category.py     # Danh mục sản phẩm
│   │       ├── size.py         # Kích thước sản phẩm
│   │       └── color.py        # Màu sắc sản phẩm
│   ├── core/
│   │   ├── config.py           # Cấu hình ứng dụng
│   │   ├── security.py         # Bảo mật JWT
│   │   └── redis.py            # Cấu hình Redis
│   ├── crud/                   # CRUD operations
│   ├── db/
│   │   ├── models/             # SQLAlchemy models
│   │   ├── session.py          # Database session
│   │   └── base.py             # Base model
│   ├── schemas/                # Pydantic schemas
│   ├── socketio/               # Socket.IO handlers
│   └── utils/                  # Utility functions
├── alembic/                    # Database migrations
├── email-templates/            # Email templates
├── requirements.txt            # Dependencies
├── Dockerfile                  # Docker configuration
├── alembic.ini                 # Alembic config
└── .env                        # Environment variables
```

## Cài đặt

### 1. Tạo và kích hoạt virtual environment

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt (Windows)
venv\Scripts\activate

# Kích hoạt (Linux/Mac)
source venv/bin/activate
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Cấu hình môi trường

Sao chép file `.env.example` thành `.env` và điền các giá trị cần thiết:

```env
PROJECT_NAME=Auth Service
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database

REDIS_URL=redis://localhost:6379

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAILS_FROM_EMAIL=your_email@gmail.com
EMAILS_FROM_NAME=Your App

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

SECRET_KEY=your_secret_key
FRONTEND_HOST=http://localhost:5173
```

### 4. Khởi tạo cơ sở dữ liệu

```bash
# Tạo migration
alembic revision --autogenerate -m "init"

# Chạy migration
alembic upgrade head
```

## Chạy ứng dụng

### Chạy local

```bash
uvicorn app.main:app --reload
```

Ứng dụng sẽ chạy tại `http://localhost:8000`

### API Documentation

Khi ứng dụng đang chạy, truy cập:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /api/v1/auth/signin` - Đăng nhập
- `POST /api/v1/auth/signup` - Đăng ký
- `POST /api/v1/auth/refresh-token` - Làm mới token
- `GET /api/v1/auth/preview?url=<url>` - Preview URL

### Users
- `GET /api/v1/users/me` - Thông tin người dùng hiện tại
- `PUT /api/v1/users/me` - Cập nhật thông tin
- `DELETE /api/v1/users/me` - Xóa tài khoản

### Conversations
- `GET /api/v1/conversations` - Danh sách cuộc trò chuyện
- `POST /api/v1/conversations` - Tạo cuộc trò chuyện mới
- `GET /api/v1/conversations/{id}` - Chi tiết cuộc trò chuyện
- `DELETE /api/v1/conversations/{id}` - Xóa cuộc trò chuyện

### Messages
- `GET /api/v1/messages/{conversation_id}` - Danh sách tin nhắn
- `POST /api/v1/messages` - Gửi tin nhắn
- `PUT /api/v1/messages/{id}` - Chỉnh sửa tin nhắn
- `DELETE /api/v1/messages/{id}` - Xóa tin nhắn

### Media
- `POST /api/v1/media/upload` - Upload file
- `GET /api/v1/media/{id}` - Lấy thông tin media

### Categories, Sizes, Colors
- CRUD operations cho categories, sizes, colors (dành cho sản phẩm e-commerce)

## Socket.IO Events

Ứng dụng tích hợp Socket.IO để giao tiếp thời gian thực:

### Events
- `connect` - Kết nối client
- `disconnect` - Ngắt kết nối
- `join_conversation` - Tham gia cuộc trò chuyện
- `leave_conversation` - Rời cuộc trò chuyện
- `send_message` - Gửi tin nhắn
- `message_received` - Nhận tin nhắn
- `typing_start` - Bắt đầu gõ
- `typing_stop` - Dừng gõ

### Presence System
- Theo dõi trạng thái online/offline của người dùng
- Hiển thị danh sách bạn bè đang online

## Docker

### Build image

```bash
docker build -t auth-service .
```

### Chạy container

```bash
docker run -p 8000:8000 --env-file .env auth-service
```

## Testing

```bash
# Chạy tests (nếu có)
pytest

# Với coverage
pytest --cov=app
```

## Deployment

### Production

Đối với production, sử dụng:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Environment Variables

Đảm bảo thiết lập các biến môi trường cho production:
- `ENVIRONMENT=production`
- Cấu hình database, Redis, SMTP, Cloudinary phù hợp

## Đóng góp

1. Fork project
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.