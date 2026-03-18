from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Celebrity
from auth import admin_required

celebrities_bp = Blueprint('celebrities', __name__, url_prefix='/api/celebrities')


# 公开接口：获取影人列表
@celebrities_bp.route('/', methods=['GET'])
def get_celebrities():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    name = request.args.get('name', '')
    nationality = request.args.get('nationality', '')

    query = Celebrity.query.filter_by(is_blocked=False)
    if name:
        query = query.filter(Celebrity.name.contains(name))
    if nationality:
        query = query.filter(Celebrity.nationality.contains(nationality))

    query = query.order_by(Celebrity.is_sticky.desc(), Celebrity.id.desc())
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    celebrities = []
    for c in paginated.items:
        celebrities.append({
            'id': c.id,
            'name': c.name,
            'gender': c.gender,
            'birth_date': c.birth_date.strftime('%Y-%m-%d') if c.birth_date else None,
            'nationality': c.nationality,
            'photo_url': c.photo_url,
            'biography': c.biography[:100] + '...' if c.biography and len(c.biography) > 100 else c.biography
        })

    return jsonify({
        'total': paginated.total,
        'page': page,
        'per_page': per_page,
        'data': celebrities
    })


# 公开接口：获取单个影人详情
@celebrities_bp.route('/<int:celebrity_id>', methods=['GET'])
def get_celebrity(celebrity_id):
    c = Celebrity.query.get_or_404(celebrity_id)
    if c.is_blocked:
        return jsonify({'msg': '影人已屏蔽'}), 404

    data = {
        'id': c.id,
        'name': c.name,
        'gender': c.gender,
        'birth_date': c.birth_date.strftime('%Y-%m-%d') if c.birth_date else None,
        'nationality': c.nationality,
        'biography': c.biography,
        'photo_url': c.photo_url,
        'is_sticky': c.is_sticky
    }
    return jsonify(data)


# 管理员接口：新增影人
@celebrities_bp.route('/', methods=['POST'])
@admin_required
def create_celebrity():
    data = request.get_json()
    c = Celebrity(
        name=data['name'],
        gender=data.get('gender'),
        birth_date=datetime.strptime(data['birth_date'], '%Y-%m-%d') if data.get('birth_date') else None,
        nationality=data.get('nationality'),
        biography=data.get('biography'),
        photo_url=data.get('photo_url'),
        is_blocked=data.get('is_blocked', False),
        is_sticky=data.get('is_sticky', False)
    )
    db.session.add(c)
    db.session.commit()
    return jsonify({'id': c.id, 'msg': '创建成功'}), 201


# 管理员接口：更新影人
@celebrities_bp.route('/<int:celebrity_id>', methods=['PUT'])
@admin_required
def update_celebrity(celebrity_id):
    c = Celebrity.query.get_or_404(celebrity_id)
    data = request.get_json()

    c.name = data.get('name', c.name)
    c.gender = data.get('gender', c.gender)
    if data.get('birth_date'):
        c.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d')
    c.nationality = data.get('nationality', c.nationality)
    c.biography = data.get('biography', c.biography)
    c.photo_url = data.get('photo_url', c.photo_url)
    c.is_blocked = data.get('is_blocked', c.is_blocked)
    c.is_sticky = data.get('is_sticky', c.is_sticky)

    db.session.commit()
    return jsonify({'msg': '更新成功'})


# 管理员接口：删除影人
@celebrities_bp.route('/<int:celebrity_id>', methods=['DELETE'])
@admin_required
def delete_celebrity(celebrity_id):
    c = Celebrity.query.get_or_404(celebrity_id)
    db.session.delete(c)
    db.session.commit()
    return jsonify({'msg': '删除成功'})