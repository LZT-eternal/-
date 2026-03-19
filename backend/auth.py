from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from models import db, User, Role

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# 硬编码测试账号（用于快速测试）
TEST_USERS = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'user': {'password': '123456', 'role': 'user'}
}


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 先检查硬编码测试账号（方便测试）
    if username in TEST_USERS and TEST_USERS[username]['password'] == password:
        # 创建JWT，额外包含角色信息
        additional_claims = {'role': TEST_USERS[username]['role']}
        access_token = create_access_token(identity=username, additional_claims=additional_claims)
        return jsonify({
            'access_token': access_token,
            'user': {
                'username': username,
                'role': TEST_USERS[username]['role']
            }
        }), 200

    # 否则查询数据库
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        # 获取用户角色
        roles = [role.name for role in user.roles]
        role = 'admin' if 'admin' in roles else 'user'
        additional_claims = {'role': role}
        access_token = create_access_token(identity=user.username, additional_claims=additional_claims)
        return jsonify({
            'access_token': access_token,
            'user': {
                'username': user.username,
                'role': role
            }
        }), 200

    return jsonify({'msg': '用户名或密码错误'}), 401


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if User.query.filter_by(username=username).first():
        return jsonify({'msg': '用户名已存在'}), 400

    user = User(
        username=username,
        password_hash=generate_password_hash(password),
        email=email
    )
    # 默认分配普通用户角色
    user_role = Role.query.filter_by(name='user').first()
    if user_role:
        user.roles.append(user_role)

    db.session.add(user)
    db.session.commit()

    return jsonify({'msg': '注册成功'}), 201


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_identity()  # 实际上这里返回的是identity，不是claims
        # 从请求中获取JWT的claims
        from flask_jwt_extended import get_jwt
        jwt_data = get_jwt()
        role = jwt_data.get('role', 'user')
        if role != 'admin':
            return jsonify({'msg': '需要管理员权限'}), 403
        return fn(*args, **kwargs)

    return wrapper