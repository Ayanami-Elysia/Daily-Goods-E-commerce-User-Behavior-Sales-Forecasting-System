from flask import Blueprint, request, jsonify
from Dao.orderDao import OrderDao
from datetime import datetime

# 创建蓝图
order_api = Blueprint('order_api', __name__)
order_dao = OrderDao()

@order_api.route('/orders', methods=['POST'])
def add_order():
    """添加订单"""
    try:
        order_data = request.get_json()
        # 处理日期时间字段
        datetime_fields = ['order_create_time', 'order_payment_time', 'receive_time']
        for field in datetime_fields:
            if field in order_data and order_data[field]:
                order_data[field] = datetime.strptime(order_data[field], '%Y-%m-%d %H:%M:%S')
        
        order_id = order_dao.add_order(order_data)
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

@order_api.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """删除订单"""
    try:
        success = order_dao.delete_order(order_id)
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

@order_api.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """更新订单"""
    try:
        order_data = request.get_json()
        # 处理日期时间字段
        datetime_fields = ['order_create_time', 'order_payment_time', 'receive_time']
        for field in datetime_fields:
            if field in order_data and order_data[field]:
                order_data[field] = datetime.strptime(order_data[field], '%Y-%m-%d %H:%M:%S')
        
        success = order_dao.update_order(order_id, order_data)
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

@order_api.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """获取订单详情"""
    try:
        order = order_dao.get_order_by_id(order_id)
        if order:
            # 处理日期时间的JSON序列化
            datetime_fields = ['order_create_time', 'order_payment_time', 'receive_time', 'create_time']
            for field in datetime_fields:
                if field in order and order[field]:
                    order[field] = order[field].strftime('%Y-%m-%d %H:%M:%S')
            
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

@order_api.route('/orders', methods=['GET'])
def get_orders():
    """获取订单列表"""
    try:
        # 获取查询参数
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        
        # 构建查询条件
        conditions = {}
        if request.args.get('order_no'):
            conditions['order_no'] = request.args.get('order_no')
        if request.args.get('order_status'):
            conditions['order_status'] = request.args.get('order_status')
        if request.args.get('product_title'):
            conditions['product_title'] = request.args.get('product_title')
        if request.args.get('store_name'):
            conditions['store_name'] = request.args.get('store_name')
        if request.args.get('start_time'):
            conditions['start_time'] = datetime.strptime(request.args.get('start_time'), '%Y-%m-%d %H:%M:%S')
        if request.args.get('end_time'):
            conditions['end_time'] = datetime.strptime(request.args.get('end_time'), '%Y-%m-%d %H:%M:%S')
        print(1)
        orders, total = order_dao.get_orders_by_condition(conditions, page, page_size)
        
        # 处理日期时间的JSON序列化
        datetime_fields = ['order_create_time', 'order_payment_time', 'receive_time', 'create_time']
        for order in orders:
            for field in datetime_fields:
                if field in order and order[field]:
                    order[field] = order[field].strftime('%Y-%m-%d %H:%M:%S')
        
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

@order_api.route('/orders/statistics', methods=['GET'])
def get_statistics():
    """获取订单统计信息"""
    try:
        # 获取日期范围参数
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        
        if start_time:
            start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        if end_time:
            end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        
        stats = order_dao.get_order_statistics(start_time, end_time)
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
