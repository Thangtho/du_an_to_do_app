# ============================================================
# main.py – File chạy chính
# Chạy lệnh: python main.py
# ============================================================

from app import app, db

# Import để đăng ký routes vào app
import models    # tạo bảng User, Task
import auth      # routes đăng ký / đăng nhập
import tasks     # routes CRUD task

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✓ Database đã khởi tạo!")
        print("✓ Truy cập:  http://localhost:5000")
        print("✓ API docs:  http://localhost:5000/api/tasks")
    app.run(debug=True, port=5000)
