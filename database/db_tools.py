"""
统一的数据库工具模块
整合所有数据库相关功能
"""
import pymysql
import pandas as pd
import subprocess
import os
import tempfile
import re
from pymysql import Error


# 数据库配置（可以从环境变量或配置文件读取）
DB_CONFIG = {
    'host': 'localhost',
    'user': 'LemuSakuya',
    'password': 'Z17158806598z',
    'database': 'drug_discovery',
    'port': 3306,
    'charset': 'utf8mb4'
}


def get_connection(database=None):
    """获取数据库连接"""
    config = DB_CONFIG.copy()
    if database:
        config['database'] = database
    elif 'database' in config:
        del config['database']  # 不指定数据库，用于创建数据库等操作
    return pymysql.connect(**config)


def create_database_if_not_exists(db_name='drug_discovery'):
    """创建数据库（如果不存在）"""
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
            result = cursor.fetchone()
            
            if result:
                print(f"✅ 数据库 '{db_name}' 已存在")
            else:
                cursor.execute(f"CREATE DATABASE `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                print(f"✅ 数据库 '{db_name}' 创建成功")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ 创建数据库失败: {e}")
        return False


def test_connection():
    """测试数据库连接"""
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ MySQL连接成功！版本: {version[0]}")
            
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print("📊 可用数据库:")
            for db in databases:
                print(f"   - {db[0]}")
        conn.close()
        return True
    except Error as e:
        print(f"❌ 连接失败: {e}")
        return False


def read_table(table_name, database=None):
    """读取数据表"""
    try:
        db = database or DB_CONFIG['database']
        conn = get_connection(db)
        sql = f"SELECT * FROM `{db}`.`{table_name}`"
        df = pd.read_sql(sql, conn)
        conn.close()
        return df.values
    except Exception as e:
        print(f"❌ 读取表 '{table_name}' 失败: {e}")
        return None


def fix_sql_collation(content):
    """修复SQL文件中的排序规则兼容性问题"""
    replacement_map = {
        'utf8mb4_0900_ai_ci': 'utf8mb4_unicode_ci',
        'utf8mb4_0900_as_ci': 'utf8mb4_unicode_ci',
        'utf8mb4_0900_as_cs': 'utf8mb4_unicode_ci',
        'utf8mb4_0900_bin': 'utf8mb4_bin',
        'utf8mb4_unicode_520_ci': 'utf8mb4_unicode_ci',
        'utf8_0900_ai_ci': 'utf8_unicode_ci',
    }
    
    fixed_content = content
    changes_count = 0
    
    for old_collation, new_collation in replacement_map.items():
        count = fixed_content.count(old_collation)
        if count > 0:
            fixed_content = fixed_content.replace(old_collation, new_collation)
            changes_count += count
    
    if changes_count > 0:
        print(f"🔧 已修复 {changes_count} 处排序规则兼容性问题")
    
    return fixed_content


def find_mysql_path():
    """查找mysql命令的路径"""
    possible_paths = [
        r"E:\Study\XAMPP\mysql\bin\mysql.exe",
        r"E:\Study\XAMPP\mysql\bin\mysql",
        r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
        r"C:\Program Files (x86)\MySQL\MySQL Server 8.0\bin\mysql.exe",
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    for path in os.environ["PATH"].split(os.pathsep):
        mysql_path = os.path.join(path, "mysql.exe")
        if os.path.exists(mysql_path):
            return mysql_path

    return None


def import_sql_file(sql_file_path, db_name='drug_discovery'):
    """导入SQL文件（自动修复排序规则）"""
    print("🔍 检查数据库是否存在...")
    if not create_database_if_not_exists(db_name):
        return False
    
    mysql_path = find_mysql_path()
    if not mysql_path:
        print("❌ 找不到mysql命令")
        return False
    
    print(f"✅ 找到mysql: {mysql_path}")
    
    try:
        # 读取并修复SQL文件
        print("🔧 检查并修复SQL文件兼容性...")
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        fixed_content = fix_sql_collation(sql_content)
        
        # 使用临时文件保存修复后的SQL
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.sql', delete=False) as temp_file:
            temp_file.write(fixed_content)
            temp_sql_path = temp_file.name
        
        try:
            cmd = [
                mysql_path,
                '-h', DB_CONFIG['host'],
                '-u', DB_CONFIG['user'],
                f'-p{DB_CONFIG["password"]}',
                db_name
            ]

            print(f"🔄 导入SQL文件...")
            with open(temp_sql_path, 'r', encoding='utf-8') as f:
                result = subprocess.run(cmd, stdin=f, capture_output=True, text=True)

            if result.returncode == 0:
                print("✅ SQL文件导入成功！")
                return True
            else:
                print(f"❌ 导入失败: {result.stderr}")
                if result.stdout:
                    print(f"输出: {result.stdout}")
                return False
        finally:
            try:
                os.unlink(temp_sql_path)
            except:
                pass

    except Exception as e:
        print(f"❌ 导入过程出错: {e}")
        return False


if __name__ == "__main__":
    # 测试连接
    test_connection()

