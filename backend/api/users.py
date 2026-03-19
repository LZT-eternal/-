from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Role
from auth import admin_required

users_bp = Blueprint('users', __name__, url_prefix='/api/users')


# 管理员接口：获取用户列表
@users_bp.route('/', methods=['GET'])
@admin_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    username = request.args.get('username', '')
    email = request.args.get('email', '')
    phone = request.args.get('phone', '')

    query = User.query
    if username:
        query = query.filter(User.username.contains(username))
    if email:
        query = query.filter(User.email.contains(email))
    if phone:
        query = query.filter(User.phone.contains(phone))

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    users = []
    for u in paginated.items:
        users.append({
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'phone': u.phone,
            'gender': u.gender,
            'age': u.age,
            'region': u.region,
            'is_active': u.is_active,
            'created_at': u.created_at.strftime('%Y-%m-%d %H:%M:%S') if u.created_at else None,
            'roles': [{'id': r.id, 'name': r.name} for r in u.roles]
        })

    return jsonify({
        'total': paginated.total,
        'page': page,
        'per_page': per_page,
        'data': users
    })


# 管理员接口：更新用户信息
@users_bp.route('/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    user.email = data.get('email', user.email)
    user.phone = data.get('phone', user.phone)
    user.gender = data.get('gender', user.gender)
    user.age = data.get('age', user.age)
    user.region = data.get('region', user.region)

    db.session.commit()
    return jsonify({'msg': '更新成功'})


# 管理员接口：启用/禁用用户
@users_bp.route('/<int:user_id>/toggle-active', methods=['PUT'])
@admin_required
def toggle_active(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    return jsonify({'is_active': user.is_active})


# 管理员接口：分配角色
@users_bp.route('/<int:user_id>/roles', methods=['POST'])
@admin_required
def assign_roles(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    role_ids = data.get('role_ids', [])

    # 清空原有角色
    user.roles = []
    for rid in role_ids:
        role = Role.query.get(rid)
        if role:
            user.roles.append(role)

    db.session.commit()
    return jsonify({'msg': '角色分配成功'})


# 获取所有角色（用于分配）
@users_bp.route('/roles', methods=['GET'])
@admin_required
def get_roles():
    roles = Role.query.all()
    return jsonify([{'id': r.id, 'name': r.name, 'description': r.description} for r in roles])


# 获取当前用户信息（个人中心用）
@users_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'msg': '用户不存在'}), 404

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'phone': user.phone,
        'gender': user.gender,
        'age': user.age,
        'region': user.region,
        'is_active': user.is_active,
        'roles': [{'id': r.id, 'name': r.name} for r in user.roles]
    })