import pandas as pd
import pymysql
from datetime import datetime
import warnings

# 完全禁用所有警告
warnings.filterwarnings('ignore')
pd.options.mode.chained_assignment = None

def get_connection():
    """获取数据库连接"""
    return pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123456',
        db='py_ryp',
        charset='utf8'
    )

def create_promotion_table():
    """创建推广表"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # 先删除已存在的表
        cursor.execute("DROP TABLE IF EXISTS py_promotion")

        sql = """
        CREATE TABLE IF NOT EXISTS py_promotion (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE COMMENT '日期',
            scene_id INT COMMENT '场景ID',
            scene_name VARCHAR(50) COMMENT '场景名字',
            plan_id BIGINT COMMENT '计划ID',
            plan_name VARCHAR(100) COMMENT '计划名字',
            unit_id BIGINT COMMENT '单元ID',
            unit_name VARCHAR(255) COMMENT '单元名字',
            item_id BIGINT COMMENT '主体ID',
            item_type VARCHAR(50) COMMENT '主体类型',
            item_name VARCHAR(255) COMMENT '主体名称',
            impressions INT COMMENT '展现量',
            clicks INT COMMENT '点击量',
            cost DECIMAL(10,2) COMMENT '花费',
            click_rate DECIMAL(10,5) COMMENT '点击率',
            avg_click_cost DECIMAL(10,2) COMMENT '平均点击花费',
            cost_per_mille DECIMAL(10,2) COMMENT '千次展现花费',
            total_presale_amount DECIMAL(10,2) COMMENT '总预售成交金额',
            direct_transaction_amount DECIMAL(10,2) COMMENT '直接成交金额',
            indirect_transaction_amount DECIMAL(10,2) COMMENT '间接成交金额',
            total_transaction_amount DECIMAL(10,2) COMMENT '总成交金额',
            total_transaction_count INT COMMENT '总成交笔数',
            cart_count INT COMMENT '总购物车数',
            favorite_count INT COMMENT '总收藏数',
            uv INT COMMENT '引导访问人数',
            deep_visit_count INT COMMENT '深度访问量',
            new_customer_count INT COMMENT '成交新客数',
            natural_transaction_amount DECIMAL(10,2) COMMENT '自然流量转化金额',
            create_time DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        cursor.execute(sql)
        print("推广表创建成功")
    except Exception as e:
        print(f"创建推广表失败: {str(e)}")
    finally:
        cursor.close()
        conn.close()


def import_promotion_csv():
    """导入推广表CSV数据"""
    conn = None
    cursor = None
    try:
        # 尝试不同的编码方式读取CSV文件
        try:
            df = pd.read_csv('推广表.csv', encoding='gbk')
        except:
            try:
                df = pd.read_csv('推广表.csv', encoding='gb2312')
            except:
                df = pd.read_csv('推广表.csv', encoding='gb18030')
        
        print(f"读取到 {len(df)} 条推广数据")
        print("\nCSV文件的列名:", df.columns.tolist())
        
        conn = get_connection()
        cursor = conn.cursor()
        
        success_count = 0
        for _, row in df.iterrows():
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
                    pd.to_datetime(row['日期']).date(),
                    int(row['场景ID']),
                    str(row['场景名字']),
                    int(row['计划ID']),
                    str(row['计划名字']),
                    int(row['单元ID']),
                    str(row['单元名字']),
                    int(row['主体ID']),
                    str(row['主体类型']),
                    str(row['主体名称']),
                    int(row['展现量']),
                    int(row['点击量']),
                    float(row['花费']),
                    float(row['点击率']),
                    float(row['平均点击花费']),
                    float(row['千次展现花费']),
                    float(row['总预售成交金额']),
                    float(row['直接成交金额']),
                    float(row['间接成交金额']),
                    float(row['总成交金额']),
                    int(row['总成交笔数']),
                    int(row['总购物车数']),
                    int(row['总收藏数']),
                    int(row['引导访问人数']),
                    int(row['深度访问量']),
                    int(row['成交新客数']),
                    float(row['自然流量转化金额'])
                ))
                success_count += 1
                
                if success_count % 100 == 0:
                    conn.commit()
                    print(f"已导入 {success_count} 条推广数据")
                    
            except Exception as e:
                print(f"插入推广数据失败: {str(e)}")
                print(f"问题数据: {row.to_dict()}")
                continue
        
        conn.commit()
        print(f"成功导入 {success_count} 条推广数据")
        
    except Exception as e:
        print(f"导入推广数据过程发生错误: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def create_table():
    """创建订单表"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # 先删除已存在的表
        cursor.execute("DROP TABLE IF EXISTS py_baby")
        
        sql = """
        CREATE TABLE IF NOT EXISTS py_baby (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_no VARCHAR(50) COMMENT '订单编号',
            order_time DATETIME COMMENT '下单时间',
            payment_time DATETIME COMMENT '付款时间',
            buyer_name VARCHAR(100) COMMENT '买家昵称',
            store_name VARCHAR(100) COMMENT '店铺名称',
            product_name VARCHAR(255) COMMENT '商品名称',
            product_code VARCHAR(50) COMMENT '商品编码',
            product_spec VARCHAR(255) COMMENT '商品规格',
            unit_price DECIMAL(10,2) COMMENT '单价',
            quantity INT COMMENT '数量',
            total_amount DECIMAL(10,2) COMMENT '总金额',
            actual_payment DECIMAL(10,2) COMMENT '实付金额',
            payment_method VARCHAR(50) COMMENT '支付方式',
            order_status VARCHAR(50) COMMENT '订单状态',
            shipping_method VARCHAR(50) COMMENT '配送方式',
            receiver_name VARCHAR(100) COMMENT '收货人',
            receiver_phone VARCHAR(20) COMMENT '联系电话',
            receiver_address TEXT COMMENT '收货地址',
            buyer_message TEXT COMMENT '买家留言',
            create_time DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        cursor.execute(sql)
        print("订单表创建成功")
    except Exception as e:
        print(f"创建订单表失败: {str(e)}")
    finally:
        cursor.close()
        conn.close()

def import_excel():
    """导入Excel数据"""
    try:
        # 使用pandas读取Excel
        df = pd.read_excel('订单数据.xlsx')  # 请确保文件名正确
        print(f"读取到 {len(df)} 条订单数据")
        
        conn = get_connection()
        cursor = conn.cursor()
        
        success_count = 0
        for _, row in df.iterrows():
            try:
                sql = """
                INSERT INTO py_baby (
                    order_no, order_time, payment_time, buyer_name, store_name,
                    product_name, product_code, product_spec, unit_price, quantity,
                    total_amount, actual_payment, payment_method, order_status,
                    shipping_method, receiver_name, receiver_phone, receiver_address,
                    buyer_message
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """
                cursor.execute(sql, (
                    str(row['订单编号']),
                    pd.to_datetime(row['下单时间']),
                    pd.to_datetime(row['付款时间']),
                    str(row['买家昵称']),
                    str(row['店铺名称']),
                    str(row['商品名称']),
                    str(row['商品编码']),
                    str(row['商品规格']) if pd.notna(row['商品规格']) else None,
                    float(row['单价']),
                    int(row['数量']),
                    float(row['总金额']),
                    float(row['实付金额']),
                    str(row['支付方式']),
                    str(row['订单状态']),
                    str(row['配送方式']),
                    str(row['收货人']),
                    str(row['联系电话']),
                    str(row['收货地址']),
                    str(row['买家留言']) if pd.notna(row['买家留言']) else None
                ))
                success_count += 1
                
                if success_count % 100 == 0:
                    conn.commit()
                    print(f"已导入 {success_count} 条订单数据")
                    
            except Exception as e:
                print(f"插入订单数据失败: {str(e)}")
                print(f"问题数据: {row.to_dict()}")
                continue
        
        conn.commit()
        print(f"成功导入 {success_count} 条订单数据")
        
    except Exception as e:
        print(f"导入订单数据过程发生错误: {str(e)}")
    finally:
        cursor.close()
        conn.close()

def show_data():
    """显示导入的数据"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM py_baby")
        total = cursor.fetchone()[0]
        print(f"\n数据库中共有 {total} 条记录")
        
        cursor.execute("""
            SELECT product_name, unit_price, quantity, store_name 
            FROM py_baby LIMIT 5
        """)
        print("\n前5条数据:")
        for row in cursor.fetchall():
            print(f"商品名称: {row[0]}")
            print(f"单价: {row[1]}")
            print(f"数量: {row[2]}")
            print(f"店铺名称: {row[3]}")
            print("---")
            
    except Exception as e:
        print(f"查询数据失败: {str(e)}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    print("开始导入数据...")

    # 导入订单数据
    print("\n=== 导入订单数据 ===")
    create_table()
    import_excel()
    show_data()

    # 导入推广数据
    print("\n=== 导入推广数据 ===")
    create_promotion_table()
    import_promotion_csv()