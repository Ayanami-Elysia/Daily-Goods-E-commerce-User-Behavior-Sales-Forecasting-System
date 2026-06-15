from flask import Blueprint, jsonify, render_template
from Dao.orderDao import OrderDao
from utils.cache_manager import cache
from datetime import datetime, timedelta

dashboard_api = Blueprint('dashboard_api', __name__)
order_dao = OrderDao()

def format_money(amount):
    """格式化金额"""
    return round(float(amount or 0), 2)

def format_int(value):
    """格式化整数"""
    return int(value or 0)

@dashboard_api.route('/dashboard')
def dashboard_page():
    """渲染数据大屏页面"""
    return render_template('dashboard.html')

@dashboard_api.route('/dashboard/overview')
def get_overview():
    """获取概览数据"""
    try:
        data = order_dao.get_overview_stats()
        return jsonify({
            'code': 200,
            'data': {
                'sales': format_money(data['total_amount']),
                'orders': format_int(data['order_count']),
                'products': format_int(data['product_count']),
                'avg_order': format_money(data['avg_order_amount']),
                'conversion': data['conversion_rate'],
                'roi': data['roi']
            }
        })
    except Exception as e:
        print(f"获取概览数据失败: {str(e)}")
        return jsonify({'code': 500, 'message': str(e)})

@dashboard_api.route('/dashboard/sales_trend')
def get_sales_trend():
    """获取销售趋势"""
    try:
        data = order_dao.get_daily_trend()
        return jsonify({
            'code': 200,
            'data': [{
                'date': item['date'].strftime('%m-%d'),
                'sales': format_money(item['total_amount']),
                'orders': format_int(item['order_count'])
            } for item in data]
        })
    except Exception as e:
        print(f"获取销售趋势失败: {str(e)}")
        return jsonify({'code': 500, 'message': str(e)})

@dashboard_api.route('/dashboard/category_stats')
def get_category_stats():
    """获取商品类别统计"""
    try:
        data = order_dao.get_category_stats()
        return jsonify({
            'code': 200,
            'data': [{
                'name': item['name'],
                'value': float(item['value'])
            } for item in data]
        })
    except Exception as e:
        print(f"获取类别统计失败: {str(e)}")
        return jsonify({'code': 500, 'message': str(e)})

@dashboard_api.route('/dashboard/product_rank')
def get_product_rank():
    """获取商品销售排行"""
    try:
        data = order_dao.get_product_rank()
        return jsonify({
            'code': 200,
            'data': [{
                'title': item['title'],
                'sales': float(item['sales']),
                'quantity': int(item['quantity'])
            } for item in data]
        })
    except Exception as e:
        print(f"获取商品排行失败: {str(e)}")
        return jsonify({'code': 500, 'message': str(e)})

@dashboard_api.route('/dashboard/promotion_stats')
def get_promotion_stats():
    """获取推广数据统计"""
    try:
        data = order_dao.get_promotion_stats()
        return jsonify({
            'code': 200,
            'data': [{
                'date': item['date'],
                'cost': float(item['cost']),
                'roi': float(item['roi']),
                'conversion': float(item['conversion'])
            } for item in data]
        })
    except Exception as e:
        print(f"获取推广统计失败: {str(e)}")
        return jsonify({'code': 500, 'message': str(e)})