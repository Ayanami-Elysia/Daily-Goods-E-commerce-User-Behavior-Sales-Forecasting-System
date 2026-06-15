from flask import Blueprint, request, jsonify
from Dao.orderDao import OrderDao
from Dao.promotionDao import PromotionDao
from Dao.BadyDao import BadyDao
from datetime import datetime, timedelta
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import os
from Predictive.Predictive import SalesPredictive
import joblib

analysis_api = Blueprint('analysis_api', __name__)
order_dao = OrderDao()
promotion_dao = PromotionDao()
bady_dao = BadyDao()

# 创建预测实例
sales_predictive = SalesPredictive()

@analysis_api.route('/analysis/overview', methods=['GET'])
def get_overview():
    """获取总览数据"""
    try:
        # 获取时间范围
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        if request.args.get('start_date'):
            start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
        if request.args.get('end_date'):
            end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')
            end_date = end_date.replace(hour=23, minute=59, second=59)

        # 获取当前时间段的统计数据
        order_stats = order_dao.get_order_statistics(start_date, end_date)
        promotion_stats = promotion_dao.get_promotion_statistics(start_date, end_date)
        product_stats = bady_dao.get_product_statistics(start_date, end_date)

        # 获取上一个时间段的统计数据（用于计算环比）
        time_diff = end_date - start_date
        last_end_date = start_date
        last_start_date = last_end_date - time_diff
        
        last_order_stats = order_dao.get_order_statistics(last_start_date, last_end_date)
        last_promotion_stats = promotion_dao.get_promotion_statistics(last_start_date, last_end_date)
        last_product_stats = bady_dao.get_product_statistics(last_start_date, last_end_date)

        return jsonify({
            'code': 200,
            'message': '获取总览数据成功',
            'data': {
                'order': {
                    'current': order_stats,
                    'last': last_order_stats
                },
                'promotion': {
                    'current': promotion_stats,
                    'last': last_promotion_stats
                },
                'product': {
                    'current': product_stats,
                    'last': last_product_stats
                }
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取总览数据失败: {str(e)}'
        })

@analysis_api.route('/analysis/sales_trend', methods=['GET'])
def get_sales_trend():
    """获取销售趋势数据"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            end_date = end_date.replace(hour=23, minute=59, second=59)

        trend_data = order_dao.get_sales_trend(start_date, end_date)
        return jsonify({
            'code': 200,
            'message': '获取销售趋势成功',
            'data': trend_data
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取销售趋势失败: {str(e)}'
        })

@analysis_api.route('/analysis/hot_products', methods=['GET'])
def get_hot_products():
    """获取热销商品排行"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        limit = int(request.args.get('limit', 10))
        
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            end_date = end_date.replace(hour=23, minute=59, second=59)

        hot_products = order_dao.get_hot_products(start_date, end_date, limit)
        return jsonify({
            'code': 200,
            'message': '获取热销商品成功',
            'data': hot_products
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取热销商品失败: {str(e)}'
        })

@analysis_api.route('/analysis/promotion_rank', methods=['GET'])
def get_promotion_rank():
    """获取推广效果排行"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        limit = int(request.args.get('limit', 10))
        
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

        promotion_rank = promotion_dao.get_promotion_rank(start_date, end_date, limit)
        return jsonify({
            'code': 200,
            'message': '获取推广排行成功',
            'data': promotion_rank
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取推广排行失败: {str(e)}'
        })

@analysis_api.route('/analysis/order_stats', methods=['GET'])
def get_order_stats():
    """获取订单统计数据"""
    try:
        # 获取时间范围
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            end_date = end_date.replace(hour=23, minute=59, second=59)

        # 获取当前时间段的统计数据
        current_stats = order_dao.get_order_statistics(start_date, end_date)
        
        # 获取上一个时间段的统计数据（用于计算环比）
        time_diff = end_date - start_date
        last_end_date = start_date
        last_start_date = last_end_date - time_diff
        last_stats = order_dao.get_order_statistics(last_start_date, last_end_date)

        return jsonify({
            'code': 200,
            'message': '获取订单统计成功',
            'data': {
                'current': current_stats,
                'last': last_stats
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取订单统计失败: {str(e)}'
        })

@analysis_api.route('/analysis/daily_sales', methods=['GET'])
def get_daily_sales():
    """获取每日销售数据"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            end_date = end_date.replace(hour=23, minute=59, second=59)

        daily_data = order_dao.get_daily_sales(start_date, end_date)
        return jsonify({
            'code': 200,
            'message': '获取每日销售数据成功',
            'data': daily_data
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取每日销售数据失败: {str(e)}'
        })

@analysis_api.route('/analysis/promotion_stats', methods=['GET'])
def get_promotion_stats():
    """获取推广统计数据"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # 获取当前时间段的统计数据
        current_stats = promotion_dao.get_promotion_statistics(start_date, end_date)
        
        # 获取上一个时间段的统计数据
        time_diff = end_date - start_date
        last_end_date = start_date
        last_start_date = last_end_date - time_diff
        last_stats = promotion_dao.get_promotion_statistics(last_start_date, last_end_date)

        return jsonify({
            'code': 200,
            'message': '获取推广统计成功',
            'data': {
                'current': current_stats,
                'last': last_stats
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取推广统计失败: {str(e)}'
        })

@analysis_api.route('/analysis/top_products', methods=['GET'])
def get_top_products():
    """获取热销商品排行"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        limit = int(request.args.get('limit', 10))
        
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            end_date = end_date.replace(hour=23, minute=59, second=59)

        products = order_dao.get_top_products(start_date, end_date, limit)
        return jsonify({
            'code': 200,
            'message': '获取热销商品成功',
            'data': products
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取热销商品失败: {str(e)}'
        })

@analysis_api.route('/analysis/train_model', methods=['POST'])
def train_model():
    """训练模型的API端点"""
    try:
        # 获取训练数据
        start_date = datetime(2024, 9, 1)
        end_date = datetime(2024, 9, 30)
        historical_data = order_dao.get_daily_sales(start_date, end_date)
        
        if not historical_data:
            print("没有真实历史数据，生成测试数据进行训练...")
            historical_data = []
            base_amount = 10000
            for i in range(30):
                current_date = start_date + timedelta(days=i)
                day_factor = 1 + 0.2 * np.sin(2 * np.pi * i / 7)
                trend_factor = 1 + 0.01 * i
                random_factor = np.random.normal(1, 0.1)
                
                amount = base_amount * day_factor * trend_factor * random_factor
                historical_data.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'total_amount': max(0, amount),
                    'order_count': int(amount / 100)
                })

        success = sales_predictive.train_and_save_model(historical_data)
        if success:
            return jsonify({
                'code': 200,
                'message': 'LSTM模型训练成功'
            })
        else:
            return jsonify({
                'code': 500,
                'message': '模型训练失败'
            })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'模型训练失败: {str(e)}'
        })

@analysis_api.route('/analysis/sales_forecast', methods=['GET'])
def get_sales_forecast():
    """使用保存的LSTM模型获取销售预测数据"""
    try:
        # 检查模型和scaler文件是否存在
        if not (os.path.exists(sales_predictive.MODEL_PATH) and os.path.exists(sales_predictive.SCALER_PATH)):
            print("模型文件不存在，开始训练新模型...")
            # 获取训练数据
            start_date = datetime(2024, 9, 1)
            end_date = datetime(2024, 9, 30)
            historical_data = order_dao.get_daily_sales(start_date, end_date)
            
            if not historical_data:
                print("没有真实历史数据，生成测试数据进行训练...")
                historical_data = []
                base_amount = 10000
                for i in range(30):
                    current_date = start_date + timedelta(days=i)
                    day_factor = 1 + 0.2 * np.sin(2 * np.pi * i / 7)
                    trend_factor = 1 + 0.01 * i
                    random_factor = np.random.normal(1, 0.1)
                    amount = base_amount * day_factor * trend_factor * random_factor
                    historical_data.append({
                        'date': current_date.strftime('%Y-%m-%d'),
                        'total_amount': max(0, amount),
                        'order_count': int(amount / 100)
                    })
            
            if not sales_predictive.train_and_save_model(historical_data):
                return jsonify({
                    'code': 500,
                    'message': '模型训练失败，无法进行预测'
                })

        # 获取最近7天的历史数据用于预测
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        recent_data = order_dao.get_daily_sales(start_date, end_date)
        
        if not recent_data or len(recent_data) < 7:
            print("生成测试数据用于预测...")
            recent_data = []
            base_amount = 10000
            for i in range(7):
                current_date = start_date + timedelta(days=i)
                amount = base_amount + np.random.normal(0, 1000)
                recent_data.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'total_amount': max(0, amount),
                    'order_count': int(amount / 100)
                })

        # 准备预测数据
        scaler = joblib.load(sales_predictive.SCALER_PATH)
        recent_amounts = [float(day['total_amount']) for day in recent_data]
        scaled_sequence = scaler.transform(np.array(recent_amounts).reshape(-1, 1))

        # 使用保存的模型进行预测
        forecast_data = sales_predictive.load_model_and_predict(scaled_sequence)
        
        if forecast_data is None:
            return jsonify({
                'code': 500,
                'message': '预测失败'
            })
        
        print(f"预测结果: {forecast_data}")
        
        return jsonify({
            'code': 200,
            'message': '使用LSTM模型获取销售预测成功',
            'data': forecast_data
        })
        
    except Exception as e:
        print(f"LSTM预测失败: {str(e)}")
        return jsonify({
            'code': 500,
            'message': f'LSTM预测失败: {str(e)}'
        }) 