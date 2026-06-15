import pymysql
from datetime import datetime



# 数据库连接
def get_connection():
    return pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123456',
        db='py_ryp',
        charset='utf8'
    )

# 管理员登陆
def loginDao(username,password,role):
    conn = get_connection()
    cursor3=conn.cursor()
    cursor3.execute('select * from `py_user` where username = %s and password = %s and role = %s' ,(username,password,role))
    res = cursor3.fetchall()
    conn.commit()
    conn.close()
    return res

# 注册检测
def GetuserDao(username):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = "SELECT * FROM py_user WHERE username = %s"
        cursor.execute(sql, (username,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# 用户注册
def Addregister(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO py_user (username, password, role) VALUES (%s, %s, 'user')"
        cursor.execute(sql, (username, password))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"注册失败: {str(e)}")
        return False
    finally:
        cursor.close()
        conn.close()

# 查询用户列表
def ListDao(username='', page=1, limit=20):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        role_expr = "TRIM(CONVERT(role USING utf8mb4)) COLLATE utf8mb4_general_ci"
        # 兼容不同角色命名，用户列表默认排除管理员数据
        where_clause = (
            "WHERE (role IS NULL OR "
            f"{role_expr} = '' OR "
            f"{role_expr} = 'user' OR "
            f"{role_expr} = '用户' OR "
            f"{role_expr} = '普通用户')"
        )
        if username:
            where_clause += " AND username LIKE %s"
            query_params = [f"%{username}%"]
        else:
            query_params = []
        
        # 计算偏移量
        offset = (page - 1) * limit
        
        # 查询总数
        count_sql = f"SELECT COUNT(*) FROM py_user {where_clause}"
        print("[ListDao] count_sql:", count_sql)
        print("[ListDao] count_params:", query_params)
        cursor.execute(count_sql, query_params)
        total = cursor.fetchone()[0]
        
        # 查询数据
        sql = f"""
            SELECT id, username, password, nickname, sex, age, phone, email, 
                   birthday, card, content, remarks, role 
            FROM py_user 
            {where_clause}
            LIMIT %s, %s
        """
        print("[ListDao] data_sql:", " ".join(sql.split()))
        print("[ListDao] data_params:", query_params + [offset, limit])
        cursor.execute(sql, query_params + [offset, limit])
        data = cursor.fetchall()
        print("[ListDao] total:", total)
        print("[ListDao] rows:", len(data))
        
        return {
            'total': total,
            'data': data
        }
    finally:
        cursor.close()
        conn.close()

# 删除用户
def DeleteUserDao(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM py_user WHERE id = %s "
        cursor.execute(sql, (user_id,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"删除用户失败: {str(e)}")
        return False
    finally:
        cursor.close()
        conn.close()

# 新增用户
def AddUserDao(username, password, nickname, sex, age, phone, email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = """
            INSERT INTO py_user (username, password, nickname, sex, age, phone, email, role) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'user')
        """
        cursor.execute(sql, (username, password, nickname, sex, age, phone, email))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"添加用户失败: {str(e)}")
        return False
    finally:
        cursor.close()
        conn.close()

# 获取用户详情
def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = """
            SELECT id, username, password, nickname, sex, age, phone, email 
            FROM py_user 
            WHERE id = %s AND role = 'user'
        """
        cursor.execute(sql, (user_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

# 更新用户信息
def update_user(user_id, username, password, nickname, sex, age, phone, email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = """
            UPDATE py_user 
            SET username = %s, password = %s, nickname = %s, 
                sex = %s, age = %s, phone = %s, email = %s 
            WHERE id = %s AND role = 'user'
        """
        cursor.execute(sql, (username, password, nickname, sex, age, phone, email, user_id))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"更新用户失败: {str(e)}")
        return False
    finally:
        cursor.close()
        conn.close()

# 查询管理员列表
def ListAdminDao(username=None, page=1, limit=20):
    conn = get_connection()
    cursor4 = conn.cursor()
    
    # 计算偏移量
    offset = (page - 1) * limit
    
    # 构建基础查询语句
    role_expr = "TRIM(CONVERT(role USING utf8mb4)) COLLATE utf8mb4_general_ci"
    base_sql = f"select * from py_user where ({role_expr} = 'admin' or {role_expr} = '管理员')"
    count_sql = f"select count(*) from py_user where ({role_expr} = 'admin' or {role_expr} = '管理员')"

    # 如果有用户名参数,添加搜索条件
    if username:
        base_sql += " and username like %s"
        count_sql += " and username like %s"
        search_param = f"%{username}%"
        
        # 执行分页查询
        print("[ListAdminDao] data_sql:", " ".join((base_sql + " LIMIT %s,%s").split()))
        print("[ListAdminDao] data_params:", (search_param, offset, limit))
        cursor4.execute(base_sql + " LIMIT %s,%s", (search_param, offset, limit))
        # 获取总数
        print("[ListAdminDao] count_sql:", count_sql)
        print("[ListAdminDao] count_params:", (search_param,))
        cursor4.execute(count_sql, (search_param,))
    else:
        # 无搜索条件的查询
        print("[ListAdminDao] data_sql:", " ".join((base_sql + " LIMIT %s,%s").split()))
        print("[ListAdminDao] data_params:", (offset, limit))
        cursor4.execute(base_sql + " LIMIT %s,%s", (offset, limit))
        print("[ListAdminDao] count_sql:", count_sql)
        print("[ListAdminDao] count_params:", ())
        cursor4.execute(count_sql)
    
    # 获取总记录数
    total = cursor4.fetchone()[0]
    
    # 执行分页查询
    if username:
        cursor4.execute(base_sql + " LIMIT %s,%s", (search_param, offset, limit))
    else:
        cursor4.execute(base_sql + " LIMIT %s,%s", (offset, limit))
    data = cursor4.fetchall()
    print("[ListAdminDao] total:", total)
    print("[ListAdminDao] rows:", len(data))
    
    conn.commit()
    conn.close()
    
    return {
        "total": total,
        "data": data
    }

# 添加管理员
def AddAdminDao(username, password, nickname, sex, age, phone, email, birthday, card, content, remarks):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """insert into py_user(username, password, nickname, sex, age, phone, email, birthday, card, content, remarks, role) 
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'admin')"""
    cursor.execute(sql, (username, password, nickname, sex, age, phone, email, birthday, card, content, remarks))
    conn.commit()
    conn.close()
    return True