
# tasks.py – Nguyễn Đức Lương

from datetime import datetime
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import app, db
from models import Task

# Hàm tiện ích để phân tích deadline từ chuỗi ISO
def _parse_deadline(value):
    """Parse chuỗi ISO thành datetime"""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        raise ValueError('Định dạng deadline không hợp lệ')


# API thống kê số lượng task theo trạng thái
@app.route('/api/tasks/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Thống kê số lượng task theo trạng thái"""
    user_id = get_jwt_identity()
    tasks   = Task.query.filter_by(user_id=user_id).all()

    total       = len(tasks)
    done        = sum(1 for t in tasks if t.status == 'done')
    in_progress = sum(1 for t in tasks if t.status == 'in_progress')
    todo        = sum(1 for t in tasks if t.status == 'todo')
    overdue     = sum(1 for t in tasks if t.is_overdue())

    return jsonify({
        'total':       total,
        'done':        done,
        'in_progress': in_progress,
        'todo':        todo,
        'overdue':     overdue
    }), 200

# API lấy danh sách task, có thể lọc theo trạng thái hoặc độ ưu tiên
@app.route('/api/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    """Lấy danh sách task, lọc theo status hoặc priority"""
    user_id         = get_jwt_identity()
    status_filter   = request.args.get('status',   'all')
    priority_filter = request.args.get('priority', 'all')

    query = Task.query.filter_by(user_id=user_id)

    if status_filter == 'overdue':
        query = query.filter(
            Task.deadline < datetime.utcnow(),
            Task.status   != 'done'
        )
    elif status_filter != 'all':
        query = query.filter_by(status=status_filter)

    if priority_filter != 'all':
        query = query.filter_by(priority=priority_filter)

    tasks = query.order_by(Task.created_at.desc()).all()
    return jsonify({'tasks': [t.to_dict() for t in tasks]}), 200

# API tạo task mới
@app.route('/api/tasks', methods=['POST'])
@jwt_required()
def create_task():
    """Tạo task mới"""
    user_id = get_jwt_identity()
    data    = request.get_json()

    if not data or not data.get('title', '').strip():
        return jsonify({'error': 'Tiêu đề công việc là bắt buộc'}), 400

    try:
        deadline = _parse_deadline(data.get('deadline'))
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    task = Task(
        title       = data['title'].strip(),
        description = data.get('description', '').strip(),
        status      = data.get('status',   'todo'),
        priority    = data.get('priority', 'medium'),
        deadline    = deadline,
        user_id     = user_id
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Tạo công việc thành công!', 'task': task.to_dict()}), 201

# API lấy chi tiết 1 task
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    """Lấy chi tiết 1 task"""
    user_id = get_jwt_identity()
    task    = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'error': 'Không tìm thấy công việc'}), 404
    return jsonify({'task': task.to_dict()}), 200

# API cập nhật task
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """Cập nhật task"""
    user_id = get_jwt_identity()
    task    = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'error': 'Không tìm thấy công việc'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dữ liệu không hợp lệ'}), 400

    if 'title'       in data: task.title       = data['title'].strip()
    if 'description' in data: task.description = data['description'].strip()
    if 'status'      in data: task.status      = data['status']
    if 'priority'    in data: task.priority    = data['priority']
    if 'deadline'    in data:
        try:
            task.deadline = _parse_deadline(data['deadline'])
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    task.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Cập nhật thành công!', 'task': task.to_dict()}), 200

# API xóa task
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """Xóa task"""
    user_id = get_jwt_identity()
    task    = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'error': 'Không tìm thấy công việc'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Xóa công việc thành công!'}), 200
