from flask import Blueprint, request, jsonify
from Dao.promotionDao import PromotionDao
from datetime import datetime

# 创建蓝图
promotion_api = Blueprint('promotion_api', __name__)
promotion_dao = PromotionDao()

@promotion_api.route('/promotions', methods=['POST'])
def add_promotion():
    """添加推广数据"""
    try:
        promotion_data = request.get_json()
        # 处理日期字段
        if 'date' in promotion_data:
            promotion_data['date'] = datetime.strptime(promotion_data['date'], '%Y-%m-%d').date()
        
        promotion_id = promotion_dao.add_promotion(promotion_data)
        if promotion_id:
            return jsonify({
                'code': 200,
                'message': '添加推广数据成功',
                'data': {'id': promotion_id}
            })
        else:
            return jsonify({
                'code': 500,
                'message': '添加推广数据失败'
            })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'添加推广数据失败: {str(e)}'
        })

@promotion_api.route('/promotions/<int:promotion_id>', methods=['DELETE'])
def delete_promotion(promotion_id):
    """删除推广数据"""
    try:
        success = promotion_dao.delete_promotion(promotion_id)
        if success:
            return jsonify({
                'code': 200,
                'message': '删除推广数据成功'
            })
        else:
            return jsonify({
                'code': 500,
                'message': '删除推广数据失败'
            })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'删除推广数据失败: {str(e)}'
        })

@promotion_api.route('/promotions/<int:promotion_id>', methods=['PUT'])
def update_promotion(promotion_id):
    """更新推广数据"""
    try:
        promotion_data = request.get_json()
        # 处理日期字段
        if 'date' in promotion_data:
            promotion_data['date'] = datetime.strptime(promotion_data['date'], '%Y-%m-%d').date()
        
        success = promotion_dao.update_promotion(promotion_id, promotion_data)
        if success:
            return jsonify({
                'code': 200,
                'message': '更新推广数据成功'
            })
        else:
            return jsonify({
                'code': 500,
                'message': '更新推广数据失败'
            })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'更新推广数据失败: {str(e)}'
        })

@promotion_api.route('/promotions/<int:promotion_id>', methods=['GET'])
def get_promotion(promotion_id):
    """获取推广数据详情"""
    try:
        promotion = promotion_dao.get_promotion_by_id(promotion_id)
        if promotion:
            # 处理日期的JSON序列化
            if 'date' in promotion:
                promotion['date'] = promotion['date'].strftime('%Y-%m-%d')
            
            return jsonify({
                'code': 200,
                'message': '获取推广数据成功',
                'data': promotion
            })
        else:
            return jsonify({
                'code': 404,
                'message': '推广数据不存在'
            })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取推广数据失败: {str(e)}'
        })

@promotion_api.route('/promotions', methods=['GET'])
def get_promotions():
    """获取推广数据列表"""
    try:
        # 获取查询参数
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        
        # 构建查询条件
        conditions = {}
        if request.args.get('date_start'):
            conditions['date_start'] = datetime.strptime(request.args.get('date_start'), '%Y-%m-%d').date()
        if request.args.get('date_end'):
            conditions['date_end'] = datetime.strptime(request.args.get('date_end'), '%Y-%m-%d').date()
        if request.args.get('scene_name'):
            conditions['scene_name'] = request.args.get('scene_name')
        if request.args.get('plan_name'):
            conditions['plan_name'] = request.args.get('plan_name')
        if request.args.get('item_name'):
            conditions['item_name'] = request.args.get('item_name')
        
        promotions, total = promotion_dao.get_promotions_by_condition(conditions, page, page_size)
        
        # 处理日期的JSON序列化
        for promotion in promotions:
            if 'date' in promotion:
                promotion['date'] = promotion['date'].strftime('%Y-%m-%d')
        
        return jsonify({
            'code': 200,
            'message': '获取推广数据列表成功',
            'data': {
                'total': total,
                'page': page,
                'page_size': page_size,
                'promotions': promotions
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取推广数据列表失败: {str(e)}'
        })

@promotion_api.route('/promotions/statistics', methods=['GET'])
def get_statistics():
    """获取推广统计信息"""
    try:
        # 获取日期范围参数
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        stats = promotion_dao.get_promotion_statistics(start_date, end_date)
        if stats:
            return jsonify({
                'code': 200,
                'message': '获取统计信息成功',
                'data': stats
            })
        else:
            return jsonify({
                'code': 500,
                'message': '获取统计信息失败'
            })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取统计信息失败: {str(e)}'
        })
