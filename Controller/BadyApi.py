from flask import Blueprint, request, jsonify
from Dao.BadyDao import BadyDao
from datetime import datetime

# 创建蓝图
bady_api = Blueprint('bady_api', __name__)
bady_dao = BadyDao()

@bady_api.route('/orders', methods=['POST'])
def add_order():
    """添加订单"""
    try:
        order_data = request.get_json()
        # 处理日期时间字段
        if 'order_create_time' in order_data:
            order_data['order_create_time'] = datetime.strptime(order_data['order_create_time'], '%Y-%m-%d %H:%M:%S')
        if 'order_payment_time' in order_data:
            order_data['order_payment_time'] = datetime.strptime(order_data['order_payment_time'], '%Y-%m-%d %H:%M:%S')
        if 'receive_time' in order_data:
            order_data['receive_time'] = datetime.strptime(order_data['receive_time'], '%Y-%m-%d %H:%M:%S')
        
        order_id = bady_dao.add_order(order_data)
        if order_id:
            return jsonify({
                'code': 200,
                'message': '添加订单成功',
                'data': {'id': order_id}
            })
        else:
            return jsonify({
                'code': 500,
                'message': '添加订单失败'
            })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'添加订单失败: {str(e)}'
        })

@bady_api.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """删除订单"""
    try:
        success = bady_dao.delete_order(order_id)
        if success:
            return jsonify({
                'code': 200,
                'message': '删除订单成功'
            })
        else:
            return jsonify({
                'code': 500,
                'message': '删除订单失败'
            })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'删除订单失败: {str(e)}'
        })

@bady_api.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """更新订单"""
    try:
        order_data = request.get_json()
        # 处理日期时间字段
        if 'order_create_time' in order_data:
            order_data['order_create_time'] = datetime.strptime(order_data['order_create_time'], '%Y-%m-%d %H:%M:%S')
        if 'order_payment_time' in order_data:
            order_data['order_payment_time'] = datetime.strptime(order_data['order_payment_time'], '%Y-%m-%d %H:%M:%S')
        if 'receive_time' in order_data:
            order_data['receive_time'] = datetime.strptime(order_data['receive_time'], '%Y-%m-%d %H:%M:%S')
        
        success = bady_dao.update_order(order_id, order_data)
        if success:
            return jsonify({
                'code': 200,
                'message': '更新订单成功'
            })
        else:
            return jsonify({
                'code': 500,
                'message': '更新订单失败'
            })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'更新订单失败: {str(e)}'
        })

@bady_api.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """获取订单详情"""
    try:
        order = bady_dao.get_order_by_id(order_id)
        if order:
            # 处理datetime对象的JSON序列化
            for key, value in order.items():
                if isinstance(value, datetime):
                    order[key] = value.strftime('%Y-%m-%d %H:%M:%S')
            
            return jsonify({
                'code': 200,
                'message': '获取订单成功',
                'data': order
            })
        else:
            return jsonify({
                'code': 404,
                'message': '订单不存在'
            })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取订单失败: {str(e)}'
        })

@bady_api.route('/orders', methods=['GET'])
def get_orders():
    """获取订单列表"""
    try:
        # 获取查询参数
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        
        # 构建查询条件
        conditions = {}
        if request.args.get('product_title'):
            conditions['product_title'] = request.args.get('product_title')
        if request.args.get('order_status'):
            conditions['order_status'] = request.args.get('order_status')
        
        orders, total = bady_dao.get_orders_by_condition(conditions, page, page_size)
        
        # 处理datetime对象的JSON序列化
        for order in orders:
            for key, value in order.items():
                if isinstance(value, datetime):
                    order[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify({
            'code': 200,
            'message': '获取订单列表成功',
            'data': {
                'total': total,
                'page': page,
                'page_size': page_size,
                'orders': orders
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取订单列表失败: {str(e)}'
        })

@bady_api.route('/orders/statistics', methods=['GET'])
def get_statistics():
    """获取订单统计信息"""
    try:
        # 获取日期范围参数
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        stats = bady_dao.get_order_statistics(start_date, end_date)
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
