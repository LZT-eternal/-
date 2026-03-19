from flask import Blueprint, request, jsonify
from sqlalchemy import func, extract
from models import db, BoxOffice, Movie
from datetime import datetime, timedelta

boxoffice_bp = Blueprint('boxoffice', __name__, url_prefix='/api/boxoffice')


# 票房趋势（近30天）
@boxoffice_bp.route('/trend', methods=['GET'])
def trend():
    days = request.args.get('days', 30, type=int)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days - 1)

    # 按日期分组汇总票房
    results = db.session.query(
        BoxOffice.date,
        func.sum(BoxOffice.amount).label('total')
    ).filter(
        BoxOffice.date >= start_date,
        BoxOffice.date <= end_date
    ).group_by(BoxOffice.date).order_by(BoxOffice.date).all()

    # 生成完整日期列表
    date_list = [start_date + timedelta(days=i) for i in range(days)]
    data = []
    for d in date_list:
        amount = next((r.total for r in results if r.date == d), 0)
        data.append({
            'date': d.strftime('%Y-%m-%d'),
            'amount': float(amount) if amount else 0
        })

    return jsonify(data)


# 地区票房分布（最近7天或指定日期范围）
@boxoffice_bp.route('/region', methods=['GET'])
def region_distribution():
    start = request.args.get('start')
    end = request.args.get('end')
    if not start or not end:
        # 默认最近30天
        end = datetime.now().date()
        start = end - timedelta(days=30)
    else:
        start = datetime.strptime(start, '%Y-%m-%d').date()
        end = datetime.strptime(end, '%Y-%m-%d').date()

    results = db.session.query(
        BoxOffice.region,
        func.sum(BoxOffice.amount).label('total')
    ).filter(
        BoxOffice.date >= start,
        BoxOffice.date <= end
    ).group_by(BoxOffice.region).all()

    data = [{'region': r.region, 'amount': float(r.total)} for r in results]
    return jsonify(data)


# 多片对比（指定多个电影ID的票房趋势）
@boxoffice_bp.route('/compare', methods=['GET'])
def compare():
    movie_ids = request.args.getlist('movie_ids', type=int)
    days = request.args.get('days', 30, type=int)
    if not movie_ids:
        return jsonify([])

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days - 1)

    movies = Movie.query.filter(Movie.id.in_(movie_ids)).all()
    result = []
    for movie in movies:
        # 获取该电影在日期范围内的每日票房
        daily = db.session.query(
            BoxOffice.date,
            BoxOffice.amount
        ).filter(
            BoxOffice.movie_id == movie.id,
            BoxOffice.date >= start_date,
            BoxOffice.date <= end_date
        ).order_by(BoxOffice.date).all()

        # 填充日期
        date_amount = {d.date.strftime('%Y-%m-%d'): float(d.amount) for d in daily}
        series = []
        for i in range(days):
            date_str = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
            series.append({
                'date': date_str,
                'amount': date_amount.get(date_str, 0)
            })

        result.append({
            'movie_id': movie.id,
            'movie_title': movie.title,
            'data': series
        })

    return jsonify(result)