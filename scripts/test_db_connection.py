import pymysql

def test_db_connection():
    """测试数据库连接"""
    try:
        # 使用与app.py相同的连接配置
        sql_connection = pymysql.connect(host='localhost', user='root', password='12345',
                                        db='drug_discovery', port=3306, autocommit=False, charset='utf8mb4')

        # 测试查询
        with sql_connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"[SUCCESS] 数据库连接成功！找到 {len(tables)} 个表")

            # 显示表名
            for table in tables:
                print(f"  - {table[0]}")

        sql_connection.close()
        return True

    except Exception as e:
        print(f"[ERROR] 数据库连接失败: {e}")
        return False

if __name__ == "__main__":
    test_db_connection()
