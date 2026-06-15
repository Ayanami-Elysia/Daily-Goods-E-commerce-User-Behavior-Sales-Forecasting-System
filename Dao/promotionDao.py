import pymysql
from datetime import datetime

class PromotionDao:
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

    def add_promotion(self, promotion_data):
        """添加推广数据"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
            INSERT INTO py_promotion (
                date, scene_id, scene_name, plan_id, plan_name,
                unit_id, unit_name, item_id, item_type, item_name,
                impressions, clicks, cost, click_rate, avg_click_cost,
                cost_per_mille, total_presale_amount, direct_transaction_amount,
                indirect_transaction_amount, total_transaction_amount,
                total_transaction_count, cart_count, favorite_count,
                uv, deep_visit_count, new_customer_count, natural_transaction_amount
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """
            cursor.execute(sql, (
                promotion_data.get('date'),
                promotion_data.get('scene_id'),
                promotion_data.get('scene_name'),
                promotion_data.get('plan_id'),
                promotion_data.get('plan_name'),
                promotion_data.get('unit_id'),
                promotion_data.get('unit_name'),
                promotion_data.get('item_id'),
                promotion_data.get('item_type'),
                promotion_data.get('item_name'),
                promotion_data.get('impressions'),
                promotion_data.get('clicks'),
                promotion_data.get('cost'),
                promotion_data.get('click_rate'),
                promotion_data.get('avg_click_cost'),
                promotion_data.get('cost_per_mille'),
                promotion_data.get('total_presale_amount'),
                promotion_data.get('direct_transaction_amount'),
                promotion_data.get('indirect_transaction_amount'),
                promotion_data.get('total_transaction_amount'),
                promotion_data.get('total_transaction_count'),
                promotion_data.get('cart_count'),
                promotion_data.get('favorite_count'),
                promotion_data.get('uv'),
                promotion_data.get('deep_visit_count'),
                promotion_data.get('new_customer_count'),
                promotion_data.get('natural_transaction_amount')
            ))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            print(f"添加推广数据失败: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()

    def delete_promotion(self, promotion_id):
        """删除推广数据"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            sql = "DELETE FROM py_promotion WHERE id = %s"
            cursor.execute(sql, (promotion_id,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"删除推广数据失败: {str(e)}")
            return False
        finally:
            cursor.close()
            conn.close()

    def update_promotion(self, promotion_id, promotion_data):
        """更新推广数据"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
            UPDATE py_promotion SET
                date = %s, scene_id = %s, scene_name = %s,
                plan_id = %s, plan_name = %s, unit_id = %s,
                unit_name = %s, item_id = %s, item_type = %s,
                item_name = %s, impressions = %s, clicks = %s,
                cost = %s, click_rate = %s, avg_click_cost = %s,
                cost_per_mille = %s, total_presale_amount = %s,
                direct_transaction_amount = %s, indirect_transaction_amount = %s,
                total_transaction_amount = %s, total_transaction_count = %s,
                cart_count = %s, favorite_count = %s, uv = %s,
                deep_visit_count = %s, new_customer_count = %s,
                natural_transaction_amount = %s
            WHERE id = %s
            """
            cursor.execute(sql, (
                promotion_data.get('date'),
                promotion_data.get('scene_id'),
                promotion_data.get('scene_name'),
                promotion_data.get('plan_id'),
                promotion_data.get('plan_name'),
                promotion_data.get('unit_id'),
                promotion_data.get('unit_name'),
                promotion_data.get('item_id'),
                promotion_data.get('item_type'),
                promotion_data.get('item_name'),
                promotion_data.get('impressions'),
                promotion_data.get('clicks'),
                promotion_data.get('cost'),
                promotion_data.get('click_rate'),
                promotion_data.get('avg_click_cost'),
                promotion_data.get('cost_per_mille'),
                promotion_data.get('total_presale_amount'),
                promotion_data.get('direct_transaction_amount'),
                promotion_data.get('indirect_transaction_amount'),
                promotion_data.get('total_transaction_amount'),
                promotion_data.get('total_transaction_count'),
                promotion_data.get('cart_count'),
                promotion_data.get('favorite_count'),
                promotion_data.get('uv'),
                promotion_data.get('deep_visit_count'),
                promotion_data.get('new_customer_count'),
                promotion_data.get('natural_transaction_amount'),
                promotion_id
            ))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"更新推广数据失败: {str(e)}")
            return False
        finally:
            cursor.close()
            conn.close()

    def get_promotion_by_id(self, promotion_id):
        """根据ID获取推广数据"""
        conn = self.get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            sql = "SELECT * FROM py_promotion WHERE id = %s"
            cursor.execute(sql, (promotion_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"获取推广数据失败: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_promotions_by_condition(self, conditions, page=1, page_size=10):
        """条件查询推广数据"""
        conn = self.get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            # 构建WHERE子句
            where_clause = "WHERE 1=1"
            values = []
            
            if conditions.get('date_start'):
                where_clause += " AND date >= %s"
                values.append(conditions['date_start'])
            if conditions.get('date_end'):
                where_clause += " AND date <= %s"
                values.append(conditions['date_end'])
            if conditions.get('scene_name'):
                where_clause += " AND scene_name LIKE %s"
                values.append(f"%{conditions['scene_name']}%")
            if conditions.get('plan_name'):
                where_clause += " AND plan_name LIKE %s"
                values.append(f"%{conditions['plan_name']}%")
            if conditions.get('item_name'):
                where_clause += " AND item_name LIKE %s"
                values.append(f"%{conditions['item_name']}%")

            # 获取总记录数
            count_sql = f"SELECT COUNT(*) as total FROM py_promotion {where_clause}"
            cursor.execute(count_sql, tuple(values))
            total = cursor.fetchone()['total']

            # 获取分页数据
            sql = f"""
            SELECT * FROM py_promotion 
            {where_clause}
            ORDER BY date DESC, id DESC
            LIMIT %s OFFSET %s
            """
            values.extend([page_size, (page - 1) * page_size])
            cursor.execute(sql, tuple(values))
            promotions = cursor.fetchall()

            return promotions, total
        except Exception as e:
            print(f"查询推广数据失败: {str(e)}")
            return [], 0
        finally:
            cursor.close()
            conn.close()

    def get_promotion_statistics(self, start_date=None, end_date=None):
        """获取推广统计信息"""
        conn = self.get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            where_clause = "WHERE 1=1"
            values = []
            if start_date:
                where_clause += " AND date >= %s"
                values.append(start_date)
            if end_date:
                where_clause += " AND date <= %s"
                values.append(end_date)

            sql = f"""
            SELECT 
                SUM(impressions) as total_impressions,
                SUM(clicks) as total_clicks,
                SUM(cost) as total_cost,
                AVG(click_rate) as avg_click_rate,
                SUM(total_transaction_amount) as total_amount,
                SUM(total_transaction_count) as total_orders,
                SUM(new_customer_count) as total_new_customers
            FROM py_promotion
            {where_clause}
            """
            cursor.execute(sql, tuple(values))
            return cursor.fetchone()
        except Exception as e:
            print(f"获取推广统计信息失败: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_promotion_rank(self, start_date=None, end_date=None, limit=10):
        """获取推广效果排行"""
        conn = self.get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            where_clause = "WHERE 1=1"
            values = []
            if start_date:
                where_clause += " AND date >= %s"
                values.append(start_date)
            if end_date:
                where_clause += " AND date <= %s"
                values.append(end_date)

            sql = f"""
            SELECT 
                plan_name,
                SUM(clicks) as total_clicks,
                AVG(click_rate) as avg_click_rate,
                SUM(total_transaction_amount) as total_amount
            FROM py_promotion
            {where_clause}
            GROUP BY plan_name
            ORDER BY total_clicks DESC
            LIMIT %s
            """
            values.append(limit)
            cursor.execute(sql, tuple(values))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
