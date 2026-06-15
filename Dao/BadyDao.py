import pymysql
from datetime import datetime

class BadyDao:
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
        """添加订单
        Args:
            order_data: 订单数据字典，包含订单的各个字段
        Returns:
            新增订单的ID
        """
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
            print(f"添加订单失败: {str(e)}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()

    def delete_order(self, order_id):
        """删除订单
        Args:
            order_id: 订单ID
        Returns:
            是否删除成功
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            sql = "DELETE FROM py_order WHERE id = %s"
            cursor.execute(sql, (order_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"删除订单失败: {str(e)}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def update_order(self, order_id, order_data):
        """更新订单
        Args:
            order_id: 订单ID
            order_data: 要更新的订单数据字典
        Returns:
            是否更新成功
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # 构建更新字段
            update_fields = []
            values = []
            for key, value in order_data.items():
                update_fields.append(f"{key} = %s")
                values.append(value)
            values.append(order_id)  # WHERE条件的值

            sql = f"""
            UPDATE py_order SET 
            {', '.join(update_fields)}
            WHERE id = %s
            """
            cursor.execute(sql, tuple(values))
            conn.commit()
            return True
        except Exception as e:
            print(f"更新订单失败: {str(e)}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def get_order_by_id(self, order_id):
        """根据ID查询订单
        Args:
            order_id: 订单ID
        Returns:
            订单信息字典
        """
        conn = self.get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            sql = "SELECT * FROM py_order WHERE id = %s"
            cursor.execute(sql, (order_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"查询订单失败: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_orders_by_condition(self, conditions=None, page=1, page_size=10):
        """条件查询订单
        Args:
            conditions: 查询条件字典
            page: 页码
            page_size: 每页记录数
        Returns:
            订单列表和总记录数
        """
        conn = self.get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            # 构建WHERE子句
            where_clause = "WHERE 1=1"
            values = []
            if conditions:
                for key, value in conditions.items():
                    where_clause += f" AND {key} = %s"
                    values.append(value)

            # 查询总记录数
            count_sql = f"SELECT COUNT(*) as total FROM py_order {where_clause}"
            cursor.execute(count_sql, tuple(values))
            total = cursor.fetchone()['total']

            # 查询分页数据
            offset = (page - 1) * page_size
            sql = f"""
            SELECT * FROM py_order 
            {where_clause}
            ORDER BY order_create_time DESC
            LIMIT %s, %s
            """
            values.extend([offset, page_size])
            cursor.execute(sql, tuple(values))
            orders = cursor.fetchall()

            return orders, total
        except Exception as e:
            print(f"查询订单列表失败: {str(e)}")
            return [], 0
        finally:
            cursor.close()
            conn.close()

    def get_order_statistics(self, start_date=None, end_date=None):
        """获取订单统计信息
        Args:
            start_date: 开始日期
            end_date: 结束日期
        Returns:
            统计信息字典
        """
        conn = self.get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            where_clause = "WHERE 1=1"
            values = []
            if start_date:
                where_clause += " AND order_create_time >= %s"
                values.append(start_date)
            if end_date:
                where_clause += " AND order_create_time <= %s"
                values.append(end_date)

            sql = f"""
            SELECT 
                COUNT(*) as total_orders,
                SUM(total_amount) as total_amount,
                SUM(actual_payment) as total_actual_payment,
                COUNT(DISTINCT store_id) as store_count,
                AVG(total_amount) as avg_order_amount
            FROM py_order
            {where_clause}
            """
            cursor.execute(sql, tuple(values))
            return cursor.fetchone()
        except Exception as e:
            print(f"获取订单统计信息失败: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_product_statistics(self, start_date=None, end_date=None):
        """获取商品统计信息"""
        conn = self.get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            where_clause = "WHERE 1=1"
            values = []
            if start_date:
                where_clause += " AND create_time >= %s"
                values.append(start_date)
            if end_date:
                where_clause += " AND create_time <= %s"
                values.append(end_date)

            sql = f"""
            SELECT 
                COUNT(*) as total_products,
                COUNT(DISTINCT category) as category_count,
                SUM(stock) as total_stock,
                AVG(price) as avg_price
            FROM py_baby
            {where_clause}
            """
            cursor.execute(sql, tuple(values))
            return cursor.fetchone()
        except Exception as e:
            print(f"获取商品统计信息失败: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()
