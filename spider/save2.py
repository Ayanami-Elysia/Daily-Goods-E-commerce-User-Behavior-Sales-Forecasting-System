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

def create_table():
    """创建订单表"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # 先删除已存在的表
        cursor.execute("DROP TABLE IF EXISTS py_order")
        
        sql = """
        CREATE TABLE IF NOT EXISTS py_order (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_no BIGINT COMMENT '订单编号',
            payment_no VARCHAR(50) COMMENT '支付单号',
            payment_detail TEXT COMMENT '支付详情',
            buyer_payment DECIMAL(10,2) COMMENT '买家应付货款',
            shipping_fee DECIMAL(10,2) COMMENT '买家应付邮费',
            total_amount DECIMAL(10,2) COMMENT '总金额',
            points_earned INT COMMENT '返点积分',
            actual_payment DECIMAL(10,2) COMMENT '买家实付金额',
            points_paid INT COMMENT '买家实付积分',
            order_status VARCHAR(50) COMMENT '订单状态',
            buyer_message TEXT COMMENT '买家留言',
            order_create_time DATETIME COMMENT '订单创建时间',
            order_payment_time DATETIME COMMENT '订单付款时间',
            product_title VARCHAR(500) COMMENT '商品标题',
            product_count INT COMMENT '宝贝种类',
            tracking_no VARCHAR(255) COMMENT '物流单号',
            shipping_company VARCHAR(50) COMMENT '物流公司',
            note_tags TEXT COMMENT '备注标签',
            merchant_note TEXT COMMENT '商家备注',
            total_quantity INT COMMENT '宝贝总数量',
            store_id BIGINT COMMENT '店铺ID',
            store_name VARCHAR(100) COMMENT '店铺名称',
            product_sku TEXT COMMENT '商品属性SKU',
            receive_time DATETIME COMMENT '确认收货时间',
            receive_amount DECIMAL(10,2) COMMENT '确认收货打款金额',
            points_payment INT COMMENT '买家支付积分',
            old_total_amount DECIMAL(10,2) COMMENT '总金额(旧版)',
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
        df = pd.read_excel('订单表.xlsx')
        print(f"读取到 {len(df)} 条订单数据")
        print("\nExcel文件的列名:", df.columns.tolist())
        
        conn = get_connection()
        cursor = conn.cursor()
        
        success_count = 0
        for _, row in df.iterrows():
            try:
                # 处理日期时间字段的空值
                order_payment_time = pd.to_datetime(row['订单付款时间']) if pd.notna(row['订单付款时间']) else None
                receive_time = pd.to_datetime(row['确认收货时间']) if pd.notna(row['确认收货时间']) else None
                
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
                    int(row['订单编号']),
                    str(row['支付单号']),
                    str(row['支付详情']),
                    float(row['买家应付货款']),
                    float(row['买家应付邮费']),
                    float(row['总金额']),
                    int(row['返点积分']),
                    float(row['买家实付金额']),
                    int(row['买家实付积分']),
                    str(row['订单状态']),
                    str(row['买家留言']) if pd.notna(row['买家留言']) else None,
                    pd.to_datetime(row['订单创建时间']),
                    order_payment_time,  # 使用处理后的日期时间
                    str(row['商品标题']) if pd.notna(row['商品标题']) else None,
                    int(row['宝贝种类']),
                    str(row['物流单号']) if pd.notna(row['物流单号']) else None,
                    str(row['物流公司']) if pd.notna(row['物流公司']) else None,
                    str(row['备注标签']) if pd.notna(row['备注标签']) else None,
                    str(row['商家备注']) if pd.notna(row['商家备注']) else None,
                    int(row['宝贝总数量']),
                    int(row['店铺ID']),
                    str(row['店铺名称']),
                    str(row['商品属性SKU']),
                    receive_time,  # 使用处理后的日期时间
                    float(row['确认收货打款金额']),
                    int(row['买家支付积分']),
                    float(row['总金额(旧版)'])
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
        cursor.execute("SELECT COUNT(*) FROM py_order")
        total = cursor.fetchone()[0]
        print(f"\n数据库中共有 {total} 条记录")
        
        cursor.execute("""
            SELECT product_title, total_amount, total_quantity, store_name, 
                   order_create_time, order_payment_time 
            FROM py_order LIMIT 5
        """)
        print("\n前5条数据:")
        for row in cursor.fetchall():
            print(f"商品标题: {row[0]}")
            print(f"总金额: {row[1]}")
            print(f"数量: {row[2]}")
            print(f"店铺名称: {row[3]}")
            print(f"下单时间: {row[4]}")
            print(f"付款时间: {row[5]}")
            print("---")
            
    except Exception as e:
        print(f"查询数据失败: {str(e)}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    print("开始导入订单数据...")
    create_table()
    import_excel()
    show_data()
