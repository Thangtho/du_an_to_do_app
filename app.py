# ============================================================
# app.py – Đoàn Đức Thắng
# Thiết lập Flask app, kết nối DB, cấu hình JWT & Bcrypt
# ============================================================

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__)   # template_folder mặc định là 'templates/' — đúng rồi

app.config['SECRET_KEY']                 = 'ltnc-python-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI']    = 'sqlite:///taskmanager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY']             = 'ltnc-jwt-secret-2026'
app.config['JWT_ACCESS_TOKEN_EXPIRES']   = timedelta(hours=24)

db     = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt    = JWTManager(app)
CORS(app)


# ── Serve HTML pages ──────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')       # → templates/index.html

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')   # → templates/dashboard.html
