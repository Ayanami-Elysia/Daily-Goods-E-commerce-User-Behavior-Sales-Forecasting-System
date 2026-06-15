import pandas as pd
import pymysql
from datetime import datetime

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
    """创建数据宝贝表"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = """
        CREATE TABLE IF NOT EXISTS py_baby (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sub_order_no VARCHAR(50) COMMENT '子订单编号',
            main_order_no VARCHAR(50) COMMENT '主订单编号',
            title VARCHAR(255) COMMENT '商品标题',
            price DECIMAL(10,2) COMMENT '商品价格',
            quantity INT COMMENT '购买数量',
            shop_code VARCHAR(50) COMMENT '外部系统编号',
            attributes TEXT COMMENT '商品属性',
            package_info TEXT COMMENT '套餐信息',
            contact_note TEXT COMMENT '联系方式备注',
            order_status VARCHAR(50) COMMENT '订单状态',
            merchant_code VARCHAR(50) COMMENT '商家编码',
            payment_no VARCHAR(100) COMMENT '支付单号',
            buyer_payment DECIMAL(10,2) COMMENT '买家应付货款',
            buyer_actual_payment DECIMAL(10,2) COMMENT '买家实付金额',
            refund_status VARCHAR(50) COMMENT '退款状态',
            refund_amount VARCHAR(50) COMMENT '退款金额',
            order_create_time DATETIME COMMENT '订单创建时间',
            order_payment_time DATETIME COMMENT '订单付款时间',
            fresh_channel VARCHAR(10) COMMENT '淘鲜达渠道',
            product_id BIGINT COMMENT '商品ID',
            stage_info TEXT COMMENT '分阶段信息',
            note_tags TEXT COMMENT '备注标签',
            merchant_note TEXT COMMENT '商家备注',
            buyer_message TEXT COMMENT '主订单买家留言',
            is_active_compensation VARCHAR(10) COMMENT '是否主动赔付',
            compensation_amount DECIMAL(10,2) COMMENT '主动赔付金额',
            compensation_time DATETIME COMMENT '主动赔付出账时间',
            create_time DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        cursor.execute(sql)
        print("数据表创建成功")
    except Exception as e:
        print(f"创建表失败: {str(e)}")
    finally:
        cursor.close()
        conn.close()

def import_excel():
    """导入Excel数据到数据库"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # 先删除已存在的表
        cursor.execute("DROP TABLE IF EXISTS py_baby")
        
        # 创建新表
        create_table()
        
        df = pd.read_excel('baobei.xlsx')
        
        success_count = 0
        for _, row in df.iterrows():
            print(row)
            try:
                sql = """
                INSERT INTO py_baby (
                    sub_order_no, main_order_no, title, price, quantity, shop_code, 
                    attributes, package_info, contact_note, order_status, 
                    merchant_code, payment_no, buyer_payment, buyer_actual_payment,
                    refund_status, refund_amount, order_create_time, order_payment_time,
                    fresh_channel, product_id, stage_info, note_tags, merchant_note,
                    buyer_message, is_active_compensation, compensation_amount, 
                    compensation_time
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """
                cursor.execute(sql, (
                    str(row['子订单编号']),
                    str(row['主订单编号']),
                    str(row['商品标题']),
                    float(row['商品价格']),
                    int(row['购买数量']),
                    str(row['外部系统编号']),
                    str(row['商品属性']),
                    str(row['套餐信息']) if pd.notna(row['套餐信息']) else None,
                    str(row['联系方式备注']) if pd.notna(row['联系方式备注']) else None,
                    str(row['订单状态']),
                    str(row['商家编码']),
                    str(row['支付单号']),
                    float(row['买家应付货款']),
                    float(row['买家实付金额']),
                    str(row['退款状态']),
                    str(row['退款金额']),
                    pd.to_datetime(row['订单创建时间']),
                    pd.to_datetime(row['订单付款时间']),
                    str(row['淘鲜达渠道']),
                    int(row['商品ID']) if pd.notna(row['商品ID']) else None,
                    str(row['分阶段信息']) if pd.notna(row['分阶段信息']) else None,
                    str(row['备注标签']) if pd.notna(row['备注标签']) else None,
                    str(row['商家备注']) if pd.notna(row['商家备注']) else None,
                    str(row['主订单买家留言']) if pd.notna(row['主订单买家留言']) else None,
                    str(row['是否主动赔付']),
                    float(row['主动赔付金额']) if pd.notna(row['主动赔付金额']) else None,
                    pd.to_datetime(row['主动赔付出账时间']) if pd.notna(row['主动赔付出账时间']) else None
                ))
                success_count += 1
            except Exception as e:
                print(f"导入行数据失败: {str(e)}")
                print(f"问题数据: {row.to_dict()}")
                continue
        
        conn.commit()
        print(f"成功导入 {success_count} 条数据")
        
    except Exception as e:
        print(f"导入过程发生错误: {str(e)}")
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
        
        cursor.execute("SELECT title, price, quantity, shop_code FROM py_baby LIMIT 5")
        print("\n前5条数据:")
        for row in cursor.fetchall():
            print(f"商品标题: {row[0]}")
            print(f"价格: {row[1]}")
            print(f"数量: {row[2]}")
            print(f"店铺编号: {row[3]}")
            print("---")
            
    except Exception as e:
        print(f"查询数据失败: {str(e)}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    print("开始导入数据...")
    # 不需要单独调用create_table()，因为已经在import_excel()中调用了
    import_excel()
    show_data()