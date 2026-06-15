import pymysql
from datetime import datetime, timedelta
from utils.db_manager import db
from utils.cache_manager import cache

class OrderDao:
    CACHE_PREFIX = 'order_'
    CACHE_EXPIRE = 300  # 缓存5分钟
    
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306
        self.user = 'root'
        self.password = '123456'
        self.db = 'py_ryp'
        self.charset = 'utf8'

    def get_connection(self):
        """获取数据库连接"""
        return pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.password,
            db=self.db,
            charset=self.charset
        )

    def add_order(self, order_data):
        """添加订单"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
            INSERT INTO py_order (
                order_no, payment_no, payment_detail, buyer_payment, shipping_fee,
                total_amount, points_earned, actual_payment, points_paid, order_status,
                buyer_message, order_create_time, order_payment_time, product_title,
                product_count, tracking_no, shipping_company, note_tags, merchant_note,
                total_quantity, store_id, store_name, product_sku, receive_time,
                receive_amount, points_payment, old_total_amount
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """
            cursor.execute(sql, (
                order_data.get('order_no'),
                order_data.get('payment_no'),
                order_data.get('payment_detail'),
                order_data.get('buyer_payment'),
                order_data.get('shipping_fee'),
                order_data.get('total_amount'),
                order_data.get('points_earned'),
                order_data.get('actual_payment'),
                order_data.get('points_paid'),
                order_data.get('order_status'),
                order_data.get('buyer_message'),
                order_data.get('order_create_time'),
                order_data.get('order_payment_time'),
                order_data.get('product_title'),
                order_data.get('product_count'),
                order_data.get('tracking_no'),
                order_data.get('shipping_company'),
                order_data.get('note_tags'),
                order_data.get('merchant_note'),
                order_data.get('total_quantity'),
                order_data.get('store_id'),
                order_data.get('store_name'),
                order_data.get('product_sku'),
                order_data.get('receive_time'),
                order_data.get('receive_amount'),
                order_data.get('points_payment'),
                order_data.get('old_total_amount')
            ))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            print(f"添加订单失败: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()

    def delete_order(self, order_id):
        """删除订单"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            sql = "DELETE FROM py_order WHERE id = %s"
            cursor.execute(sql, (order_id,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"删除订单失败: {str(e)}")
            return False
        finally:
            cursor.close()
            conn.close()

    def update_order(self, order_id, order_data):
        """更新订单"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
            UPDATE py_order SET
                order_no = %s, payment_no = %s, payment_detail = %s,
                buyer_payment = %s, shipping_fee = %s, total_amount = %s,
                points_earned = %s, actual_payment = %s, points_paid = %s,
                order_status = %s, buyer_message = %s, order_create_time = %s,
                order_payment_time = %s, product_title = %s, product_count = %s,
                tracking_no = %s, shipping_company = %s, note_tags = %s,
                merchant_note = %s, total_quantity = %s, store_id = %s,
                store_name = %s, product_sku = %s, receive_time = %s,
                receive_amount = %s, points_payment = %s, old_total_amount = %s
            WHERE id = %s
            """
            cursor.execute(sql, (
                order_data.get('order_no'),
                order_data.get('payment_no'),
                order_data.get('payment_detail'),
                order_data.get('buyer_payment'),
                order_data.get('shipping_fee'),
                order_data.get('total_amount'),
                order_data.get('points_earned'),
                order_data.get('actual_payment'),
                order_data.get('points_paid'),
                order_data.get('order_status'),
                order_data.get('buyer_message'),
                order_data.get('order_create_time'),
                order_data.get('order_payment_time'),
                order_data.get('product_title'),
                order_data.get('product_count'),
                order_data.get('tracking_no'),
                order_data.get('shipping_company'),
                order_data.get('note_tags'),
                order_data.get('merchant_note'),
                order_data.get('total_quantity'),
                order_data.get('store_id'),
                order_data.get('store_name'),
                order_data.get('product_sku'),
                order_data.get('receive_time'),
                order_data.get('receive_amount'),
                order_data.get('points_payment'),
                order_data.get('old_total_amount'),
                order_id
            ))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"更新订单失败: {str(e)}")
            return False
        finally:
            cursor.close()
            conn.close()

    def get_order_by_id(self, order_id):
        """根据ID获取订单"""
        conn = self.get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            sql = "SELECT * FROM py_order WHERE id = %s"
            cursor.execute(sql, (order_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"获取订单失败: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_orders_by_condition(self, conditions, page=1, page_size=10):
        """条件查询订单"""
        conn = self.get_connection()
        print(1)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            # 构建WHERE子句
            where_clause = "WHERE 1=1"
            values = []
            if conditions.get('order_no'):
                where_clause += " AND order_no LIKE %s"
                values.append(f"%{conditions['order_no']}%")
            if conditions.get('order_status'):
                where_clause += " AND order_status = %s"
                values.append(conditions['order_status'])
            if conditions.get('product_title'):
                where_clause += " AND product_title LIKE %s"
                values.append(f"%{conditions['product_title']}%")
            if conditions.get('store_name'):
                where_clause += " AND store_name LIKE %s"
                values.append(f"%{conditions['store_name']}%")
            if conditions.get('start_time'):
                where_clause += " AND order_create_time >= %s"
                values.append(conditions['start_time'])
            if conditions.get('end_time'):
                where_clause += " AND order_create_time <= %s"
                values.append(conditions['end_time'])

            # 获取总记录数
            count_sql = f"SELECT COUNT(*) as total FROM py_order {where_clause}"
            print(count_sql)

            cursor.execute(count_sql, tuple(values))
            total = cursor.fetchone()['total']

            # 获取分页数据
            sql = f"""
            SELECT * FROM py_order 
            {where_clause}
            ORDER BY order_create_time DESC, id DESC
            LIMIT %s OFFSET %s
            """
            values.extend([page_size, (page - 1) * page_size])

            cursor.execute(sql, tuple(values))
            orders = cursor.fetchall()

            return orders, total
        except Exception as e:
            print(f"查询订单失败: {str(e)}")
            return [], 0
        finally:
            cursor.close()
            conn.close()

    def get_order_statistics(self, start_time=None, end_time=None):
        """获取订单统计信息"""
        conn = self.get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            where_clause = "WHERE 1=1"
            values = []
            if start_time:
                where_clause += " AND order_create_time >= %s"
                values.append(start_time)
            if end_time:
                where_clause += " AND order_create_time <= %s"
                values.append(end_time)

            sql = f"""
            SELECT 
                COUNT(*) as total_orders,
                COALESCE(SUM(total_amount), 0) as total_amount,
                COALESCE(SUM(actual_payment), 0) as total_actual_payment,
                COUNT(DISTINCT store_id) as store_count,
                COALESCE(SUM(total_quantity), 0) as total_quantity
            FROM py_order
            {where_clause}
            """
            cursor.execute(sql, tuple(values))
            result = cursor.fetchone()
            
            # 确保返回值不为None
            return {
                'total_orders': result['total_orders'] or 0,
                'total_amount': float(result['total_amount'] or 0),
                'total_actual_payment': float(result['total_actual_payment'] or 0),
                'store_count': result['store_count'] or 0,
                'total_quantity': result['total_quantity'] or 0
            }
        except Exception as e:
            print(f"获取订单统计信息失败: {str(e)}")
            return {
                'total_orders': 0,
                'total_amount': 0,
                'total_actual_payment': 0,
                'store_count': 0,
                'total_quantity': 0
            }
        finally:
            cursor.close()
            conn.close()

    def get_sales_trend(self, start_date, end_date):
        """获取销售趋势"""
        conn = self.get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            sql = """
            SELECT 
                DATE(order_create_time) as date,
                COUNT(*) as order_count,
                SUM(total_amount) as total_amount
            FROM py_order
            WHERE order_create_time BETWEEN %s AND %s
            GROUP BY DATE(order_create_time)
            ORDER BY date
            """
            cursor.execute(sql, (start_date, end_date))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_hot_products(self, start_date, end_date, limit=10):
        """获取热销商品排行"""
        conn = self.get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            sql = """
            SELECT 
                product_title,
                COUNT(*) as order_count,
                SUM(total_amount) as total_amount
            FROM py_order
            WHERE order_create_time BETWEEN %s AND %s
            GROUP BY product_title
            ORDER BY order_count DESC
            LIMIT %s
            """
            cursor.execute(sql, (start_date, end_date, limit))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_daily_sales(self, start_date, end_date):
        """获取每日销售数据"""
        conn = self.get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            # 首先生成日期序列
            dates = []
            current_date = start_date
            while current_date <= end_date:
                dates.append(current_date.strftime('%Y-%m-%d'))
                current_date += timedelta(days=1)

            # 获取每日销售数据
            sql = """
            SELECT 
                DATE(order_create_time) as date,
                COUNT(*) as order_count,
                COALESCE(SUM(total_amount), 0) as total_amount,
                COALESCE(SUM(actual_payment), 0) as actual_payment
            FROM py_order
            WHERE order_create_time BETWEEN %s AND %s
            GROUP BY DATE(order_create_time)
            """
            cursor.execute(sql, (start_date, end_date))
            sales_data = cursor.fetchall()
            print(sales_data)
            # 将销售数据转换为字典，方便查找
            sales_dict = {row['date'].strftime('%Y-%m-%d'): row for row in sales_data}
            
            # 合并日期序列和销售数据
            result = []
            for date in dates:
                if date in sales_dict:
                    data = sales_dict[date]
                    result.append({
                        'date': date,
                        'order_count': int(data['order_count']),
                        'total_amount': float(data['total_amount']),
                        'actual_payment': float(data['actual_payment'])
                    })
                else:
                    result.append({
                        'date': date,
                        'order_count': 0,
                        'total_amount': 0.0,
                        'actual_payment': 0.0
                    })
            
            return sales_data
        except Exception as e:
            print(f"获取每日销售数据失败: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()

    def get_daily_sales1(self, start_date, end_date):
        """获取每日销售数据"""
        conn = self.get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            # 首先生成日期序列
            dates = []
            current_date = start_date
            while current_date <= end_date:
                dates.append(current_date.strftime('%Y-%m-%d'))
                current_date += timedelta(days=1)

            # 获取每日销售数据
            sql = """
            SELECT 
                DATE(order_create_time) as date,
                COUNT(*) as order_count,
                COALESCE(SUM(total_amount), 0) as total_amount,
                COALESCE(SUM(actual_payment), 0) as actual_payment
            FROM py_order
            WHERE order_create_time BETWEEN %s AND %s
            GROUP BY DATE(order_create_time)
            """
            cursor.execute(sql, (start_date, end_date))
            sales_data = cursor.fetchall()
            print(sales_data)
            # 将销售数据转换为字典，方便查找
            sales_dict = {row['date'].strftime('%Y-%m-%d'): row for row in sales_data}

            # 合并日期序列和销售数据
            result = []
            for date in dates:
                if date in sales_dict:
                    data = sales_dict[date]
                    result.append({
                        'date': date,
                        'order_count': int(data['order_count']),
                        'total_amount': float(data['total_amount']),
                        'actual_payment': float(data['actual_payment'])
                    })
                else:
                    result.append({
                        'date': date,
                        'order_count': 0,
                        'total_amount': 0.0,
                        'actual_payment': 0.0
                    })

            return sales_data
        except Exception as e:
            print(f"获取每日销售数据失败: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()
    def get_top_products(self, start_date, end_date, limit=10):
        """获取热销商品排行"""
        conn = self.get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            sql = """
            SELECT 
                product_title,
                COUNT(*) as order_count,
                COALESCE(SUM(total_amount), 0) as total_amount,
                COALESCE(SUM(actual_payment), 0) as actual_payment
            FROM py_order
            WHERE order_create_time BETWEEN %s AND %s
                AND product_title IS NOT NULL
            GROUP BY product_title
            ORDER BY order_count DESC
            LIMIT %s
            """
            cursor.execute(sql, (start_date, end_date, limit))
            results = cursor.fetchall()
            
            # 处理金额格式
            for row in results:
                row['total_amount'] = float(row['total_amount'])
                row['actual_payment'] = float(row['actual_payment'])
            
            return results
        finally:
            cursor.close()
            conn.close()

    def get_payment_methods_stats(self):
        """获取支付方式统计"""
        conn = self.get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            sql = """
            SELECT 
                payment_detail,
                COUNT(*) as count,
                SUM(total_amount) as amount
            FROM py_order
            GROUP BY payment_detail
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_hourly_order_stats(self):
        """获取每小时订单统计"""
        conn = self.get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            sql = """
            SELECT 
                HOUR(order_create_time) as hour,
                COUNT(*) as count,
                SUM(total_amount) as amount
            FROM py_order
            GROUP BY HOUR(order_create_time)
            ORDER BY hour
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_overview_stats(self, start_date=None, end_date=None):
        """获取总体统计数据"""
        with db.get_connection() as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                where_clause = "WHERE order_status NOT IN ('交易关闭', '已退款')"
                if start_date:
                    where_clause += f" AND order_create_time >= '{start_date}'"
                if end_date:
                    where_clause += f" AND order_create_time <= '{end_date}'"
                
                # 订单数据统计
                cursor.execute(f"""
                    SELECT 
                        COUNT(*) as order_count,
                        COUNT(DISTINCT title) as product_count,
                        SUM(quantity) as total_quantity,
                        ROUND(SUM(buyer_payment), 2) as total_amount,
                        ROUND(AVG(buyer_payment), 2) as avg_order_amount
                    FROM py_baby
                    {where_clause}
                """)
                order_stats = cursor.fetchone()
                
                # 推广数据统计
                promo_where = "WHERE 1=1"
                if start_date:
                    promo_where += f" AND date >= '{start_date}'"
                if end_date:
                    promo_where += f" AND date <= '{end_date}'"
                
                cursor.execute(f"""
                    SELECT 
                        SUM(clicks) as total_clicks,
                        SUM(total_transaction_count) as transaction_count,
                        ROUND(SUM(cost), 2) as total_cost,
                        ROUND(SUM(total_transaction_amount), 2) as transaction_amount
                    FROM py_promotion
                    {promo_where}
                """)
                promo_stats = cursor.fetchone()
                
                return {
                    **order_stats,
                    'conversion_rate': round(promo_stats['transaction_count'] / promo_stats['total_clicks'] * 100, 2) if promo_stats['total_clicks'] > 0 else 0,
                    'roi': round(promo_stats['transaction_amount'] / promo_stats['total_cost'] * 100, 2) if promo_stats['total_cost'] > 0 else 0
                }

    def get_daily_trend(self):
        """获取销售趋势"""
        with db.get_connection() as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        DATE(order_create_time) as date,
                        COUNT(*) as order_count,
                        SUM(quantity) as total_quantity,
                        ROUND(SUM(buyer_payment), 2) as total_amount
                    FROM py_baby
                    WHERE 
                        order_status NOT IN ('交易关闭', '已退款')
                    GROUP BY DATE(order_create_time)
                    ORDER BY date ASC
                """)
                data = cursor.fetchall()
                print(data)
                # 补充缺失的日期
                date_dict = {item['date']: item for item in data}
                result = []
                
                for i in range(30, -1, -1):
                    date = (datetime.now() - timedelta(days=i)).date()
                    if date in date_dict:
                        result.append(date_dict[date])
                    else:
                        result.append({
                            'date': date,
                            'order_count': 0,
                            'total_quantity': 0,
                            'total_amount': 0
                        })
                
                return data

    def get_payment_stats(self):
        """获取支付方式统计"""
        with db.get_connection() as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        CASE
                            WHEN payment_detail LIKE '%支付宝%' THEN '支付宝'
                            WHEN payment_detail LIKE '%微信%' THEN '微信'
                            WHEN payment_detail LIKE '%银行卡%' THEN '银行卡'
                            ELSE '其他'
                        END as payment_method,
                        COUNT(*) as order_count,
                        ROUND(SUM(total_amount), 2) as total_amount,
                        ROUND(SUM(actual_payment), 2) as actual_payment,
                        ROUND(SUM(points_payment), 2) as points_payment,
                        ROUND(AVG(points_earned), 2) as avg_points_earned
                    FROM py_order
                    WHERE order_status NOT IN ('已取消', '已退款')
                    GROUP BY payment_method
                    ORDER BY total_amount DESC
                """)
                return cursor.fetchall()

    def get_top_products(self):
        """获取热销商品TOP10"""
        conn = self.get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            sql = """
            SELECT 
                product_title as name,
                COUNT(*) as orders,
                ROUND(SUM(total_amount), 2) as sales
            FROM py_order
            WHERE 
                order_create_time >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                AND product_title IS NOT NULL
            GROUP BY product_title
            ORDER BY orders DESC
            LIMIT 10
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_hourly_stats(self):
        """获取时段分布统计"""
        with db.get_connection() as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        HOUR(order_create_time) as hour,
                        COUNT(*) as order_count,
                        COUNT(DISTINCT product_title) as product_count,
                        SUM(product_count) as total_quantity,
                        ROUND(SUM(total_amount), 2) as total_amount,
                        ROUND(SUM(actual_payment), 2) as actual_payment,
                        ROUND(SUM(points_payment), 2) as points_payment,
                        ROUND(AVG(points_earned), 2) as avg_points_earned
                    FROM py_order
                    WHERE order_status NOT IN ('已取消', '已退款')
                    GROUP BY HOUR(order_create_time)
                    ORDER BY hour
                """)
                return cursor.fetchall()

    def get_category_stats(self):
        """获取商品类别统计"""
        with db.get_connection() as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        CASE 
                            WHEN title LIKE '%保温杯%' OR title LIKE '%水杯%' THEN '保温杯/水杯'
                            WHEN title LIKE '%饭盒%' OR title LIKE '%餐盒%' THEN '饭盒/餐盒'
                            WHEN title LIKE '%手套%' THEN '手套'
                            ELSE '其他'
                        END as name,
                        COUNT(*) as order_count,
                        SUM(quantity) as total_quantity,
                        ROUND(SUM(buyer_payment), 2) as total_amount
                    FROM py_baby
                    WHERE order_status NOT IN ('交易关闭', '已退款')
                    GROUP BY 
                        CASE 
                            WHEN title LIKE '%保温杯%' OR title LIKE '%水杯%' THEN '保温杯/水杯'
                            WHEN title LIKE '%饭盒%' OR title LIKE '%餐盒%' THEN '饭盒/餐盒'
                            WHEN title LIKE '%手套%' THEN '手套'
                            ELSE '其他'
                        END
                    ORDER BY total_amount DESC
                """)
                data = cursor.fetchall()
                
                # 计算总金额用于计算占比
                total = sum(float(item['total_amount']) for item in data)
                
                # 格式化数据
                formatted_data = []
                for item in data:
                    formatted_data.append({
                        'name': item['name'],
                        'value': float(item['total_amount']),
                        'percentage': round(float(item['total_amount']) / total * 100, 2) if total > 0 else 0
                    })
                
                return formatted_data

    def get_product_rank(self):
        """获取商品销售排行"""
        with db.get_connection() as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        SUBSTRING_INDEX(title, '【活动价】', -1) as title,
                        COUNT(*) as order_count,
                        SUM(quantity) as quantity,
                        ROUND(SUM(buyer_payment), 2) as sales,
                        ROUND(AVG(buyer_payment), 2) as avg_price
                    FROM py_baby
                    WHERE 
                        order_status NOT IN ('交易关闭', '已退款')
                        AND title IS NOT NULL
                    GROUP BY title
                    ORDER BY sales DESC
                    LIMIT 10
                """)
                return cursor.fetchall()

    def get_promotion_stats(self):
        """获取推广数据统计"""
        with db.get_connection() as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        DATE_FORMAT(date, '%m-%d') as date,
                        ROUND(SUM(cost), 2) as cost,
                        SUM(clicks) as clicks,
                        SUM(impressions) as impressions,
                        SUM(total_transaction_count) as transaction_count,
                        ROUND(SUM(total_transaction_amount), 2) as transaction_amount,
                        ROUND(SUM(total_transaction_amount) / NULLIF(SUM(cost), 0) * 100, 2) as roi,
                        ROUND(SUM(total_transaction_count) / NULLIF(SUM(clicks), 0) * 100, 2) as conversion
                    FROM py_promotion
                    GROUP BY date
                    ORDER BY date DESC
                    LIMIT 30
                """)
                data = cursor.fetchall()
                
                # 格式化数据
                formatted_data = []
                for item in data:
                    formatted_data.append({
                        'date': item['date'],
                        'cost': float(item['cost'] or 0),
                        'roi': float(item['roi'] or 0),
                        'conversion': float(item['conversion'] or 0)
                    })
                
                return formatted_data

    def get_dashboard_stats(self):
        """获取仪表盘所需的所有统计数据"""
        with db.get_connection() as conn:
            with conn.cursor() as cursor:
                # 获取概览数据
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_orders,
                        COALESCE(SUM(total_amount), 0) as total_sales,
                        COALESCE(AVG(total_amount), 0) as avg_order_value,
                        COUNT(DISTINCT product_title) as total_products
                    FROM py_order
                """)
                overview = cursor.fetchone()

                # 获取销售趋势
                cursor.execute("""
                    SELECT 
                        DATE(order_create_time) as date,
                        COUNT(*) as order_count,
                        COALESCE(SUM(total_amount), 0) as total_amount
                    FROM py_order
                    GROUP BY DATE(order_create_time)
                    ORDER BY date ASC
                """)
                trend = cursor.fetchall()

                # 获取支付方式统计
                cursor.execute("""
                    SELECT 
                        COALESCE(payment_detail, '其他') as payment_method,
                        COUNT(*) as count,
                        COALESCE(SUM(total_amount), 0) as amount
                    FROM py_order
                    GROUP BY payment_detail
                    ORDER BY count DESC
                """)
                payment = cursor.fetchall()

                # 获取品类统计
                cursor.execute("""
                    SELECT 
                        SUBSTRING_INDEX(product_title, ' ', 1) as category,
                        COUNT(*) as count,
                        COALESCE(SUM(total_amount), 0) as amount,
                        COUNT(DISTINCT product_title) as product_count
                    FROM py_order
                    WHERE product_title IS NOT NULL
                    GROUP BY SUBSTRING_INDEX(product_title, ' ', 1)
                    ORDER BY amount DESC
                    LIMIT 10
                """)
                category = cursor.fetchall()

                # 获取时段分布
                cursor.execute("""
                    SELECT 
                        HOUR(order_create_time) as hour,
                        COUNT(*) as count,
                        COALESCE(SUM(total_amount), 0) as amount
                    FROM py_order
                    GROUP BY HOUR(order_create_time)
                    ORDER BY hour
                """)
                hourly = cursor.fetchall()

                return {
                    'overview': overview,
                    'trend': trend,
                    'payment': payment,
                    'category': category,
                    'hourly': hourly
                }

    def get_order_status_stats(self):
        """获取订单状态统计"""
        with db.get_connection() as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        order_status as status,
                        COUNT(*) as count,
                        ROUND(SUM(total_amount), 2) as amount
                    FROM py_order
                    WHERE order_create_time >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                    GROUP BY order_status
                    ORDER BY count DESC
                """)
                return cursor.fetchall()

    def get_region_stats(self):
        """获取销售地域分布"""
        with db.get_connection() as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        COALESCE(store_name, '未知地区') as region,
                        COUNT(*) as count,
                        ROUND(SUM(total_amount), 2) as amount
                    FROM py_order
                    WHERE order_create_time >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                    GROUP BY store_name
                    HAVING count > 0
                    ORDER BY count DESC
                """)
                return cursor.fetchall()
