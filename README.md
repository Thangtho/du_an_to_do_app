# du_an_to_do_app
# 📋 TaskFlow – Hệ thống Quản lý Công việc

> **Môn học:** Lập Trình Nâng Cao Python  
> **Đề tài:** Hệ thống quản lý công việc (Task Management System)

---

## 👥 Thành viên nhóm

| STT | Họ và Tên | MSSV | Vai trò | Đóng góp |
|-----|-----------|------|---------|----------|
| 1 | **Đoàn Đức Thắng** | 745105091 | Trưởng nhóm / Fullstack | `app.py` `main.py` `models.py` `auth.py` – Cấu hình Flask, CSDL, API xác thực JWT/Bcrypt |
| 2 | **Nguyễn Đức Lương** | 745105063 | Backend & DB | `tasks.py` `static/js/dashboard.js` (phần gọi API) – Thiết kế schema, CRUD API, gọi API từ FE |
| 3 | **Nguyễn Đức Minh** | 745105068 | Frontend & Logic | `templates/` `static/css/` `static/js/` (phần UI) – Giao diện, thuật toán lọc, check quá hạn |

---

## 🚀 Cài đặt & Chạy

### Yêu cầu
- Python >= 3.8
- pip

### Các bước

```bash
# 1. Clone repo về máy
git clone https://github.com/Thangtho/du_an_to_do_app.git
cd du_an_to_do_app

# 2. Tạo môi trường ảo
python -m venv venv
source venv/bin/activate      # Linux/macOS
# venv\Scripts\activate       # Windows

# 3. Cài thư viện
pip install -r requirements.txt

# 4. Chạy server
python main.py
```

### Truy cập

| URL | Trang |
|-----|-------|
| http://localhost:5000 | Trang đăng nhập |
| http://localhost:5000/dashboard | Dashboard quản lý task |

---

## ✨ Chức năng

| # | Chức năng | Mô tả |
|---|-----------|-------|
| 1 | ➕ Thêm công việc | Nhập tiêu đề, mô tả, deadline, mức ưu tiên |
| 2 | ✏️ Sửa công việc | Cập nhật nội dung, trạng thái, deadline |
| 3 | 🗑️ Xóa công việc | Xác nhận trước khi xóa |
| 4 | 📅 Đặt deadline | Gắn thời hạn cho từng công việc |
| 5 | ⚠️ Nhắc việc quá hạn | BE + FE tự động phát hiện và đánh dấu |
| 6 | 🔍 Lọc theo trạng thái | Todo / Đang làm / Hoàn thành / Quá hạn |

---

## 🏗️ Cấu trúc thư mục

```
du_an_to_do_app/
│
├── main.py              # Entry point – khởi động server
├── app.py               # Cấu hình Flask, SQLite, JWT, Bcrypt, CORS
├── models.py            # ORM: class User, class Task
├── auth.py              # API: /api/register  /api/login  /api/me
├── tasks.py             # API: CRUD /api/tasks  /api/tasks/stats
├── requirements.txt     # Danh sách thư viện
│
├── templates/
│   ├── index.html       # Trang đăng nhập / đăng ký (HTML only)
│   └── dashboard.html   # Dashboard quản lý task (HTML only)
│
├── static/
│   ├── css/
│   │   ├── index.css    # Styles trang login
│   │   └── dashboard.css# Styles dashboard
│   └── js/
│       ├── index.js     # Logic đăng nhập / đăng ký (Minh)
│       └── dashboard.js # Logic dashboard: render, filter, API calls (Minh + Lương)
│
├── docs/
│   ├── uml_class.png    # Class Diagram
│   ├── uml_usecase.png  # Use Case Diagram
│   └── uml_sequence.png # Sequence Diagram
│
└── taskmanager.db       # SQLite – tự tạo khi chạy lần đầu
```

---

## 🗄️ Database Schema

### Bảng `users`

| Column | Type | Constraint |
|--------|------|-----------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `username` | VARCHAR(80) | UNIQUE, NOT NULL |
| `email` | VARCHAR(120) | UNIQUE, NOT NULL |
| `password_hash` | VARCHAR(256) | NOT NULL |
| `created_at` | DATETIME | DEFAULT utcnow |

### Bảng `tasks`

| Column | Type | Constraint |
|--------|------|-----------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `title` | VARCHAR(200) | NOT NULL |
| `description` | TEXT | DEFAULT '' |
| `status` | VARCHAR(20) | DEFAULT 'todo' |
| `priority` | VARCHAR(10) | DEFAULT 'medium' |
| `deadline` | DATETIME | NULLABLE |
| `created_at` | DATETIME | DEFAULT utcnow |
| `updated_at` | DATETIME | DEFAULT utcnow |
| `user_id` | INTEGER | FK → users.id |

**Quan hệ:** `users.id (1) ──────── tasks.user_id (N)`

**Status values:** `todo` · `in_progress` · `done`  
**Priority values:** `low` · `medium` · `high`

---

## 📡 API Endpoints

| Method | Endpoint | Auth | Mô tả |
|--------|----------|------|-------|
| `POST` | `/api/register` | ❌ | Đăng ký tài khoản |
| `POST` | `/api/login` | ❌ | Đăng nhập, trả JWT token |
| `GET` | `/api/me` | ✅ JWT | Lấy thông tin user |
| `GET` | `/api/tasks` | ✅ JWT | Danh sách task (có filter) |
| `POST` | `/api/tasks` | ✅ JWT | Tạo task mới |
| `GET` | `/api/tasks/<id>` | ✅ JWT | Chi tiết 1 task |
| `PUT` | `/api/tasks/<id>` | ✅ JWT | Cập nhật task |
| `DELETE` | `/api/tasks/<id>` | ✅ JWT | Xóa task |
| `GET` | `/api/tasks/stats` | ✅ JWT | Thống kê theo trạng thái |

### Filter params
```
GET /api/tasks?status=todo
GET /api/tasks?status=in_progress
GET /api/tasks?status=done
GET /api/tasks?status=overdue
GET /api/tasks?priority=high
```

---

## 🛠️ Công nghệ

| Tầng | Công nghệ |
|------|-----------|
| **Backend** | Flask 3.0 (Python) |
| **Database** | SQLite + SQLAlchemy ORM |
| **Auth** | Flask-JWT-Extended + Flask-Bcrypt |
| **Frontend** | HTML5 + CSS3 + Vanilla JS |
| **API** | RESTful JSON API |

---

## 🖼️ Sơ đồ UML

### Class Diagram
<img width="1350" height="960" alt="uml_class" src="https://github.com/user-attachments/assets/7e2bbc5f-4787-4c0e-9e7d-d39fd151b6a2" />


### Use Case Diagram
<img width="1350" height="930" alt="uml_usecase" src="https://github.com/user-attachments/assets/3a58729d-9978-4fbc-ad16-4e1bcd05ba43" />


### Sequence Diagram
<img width="1470" height="1080" alt="uml_sequence" src="https://github.com/user-attachments/assets/3efaa5fc-d8fb-4e1b-b780-81dff36b9aa8" />


---

## 💡 Thuật toán phát hiện quá hạn

```python
# Backend (models.py) – Đoàn Đức Thắng
def is_overdue(self) -> bool:
    if self.deadline and self.status != 'done':
        return datetime.utcnow() > self.deadline
    return False
```

```javascript
// Frontend (dashboard.js) – Nguyễn Đức Minh
function checkOverdue(task) {
    if (!task.deadline || task.status === 'done') return false;
    return new Date() > new Date(task.deadline);
}
```

---

*TaskFlow – Nhóm LTNC Python 2026*
