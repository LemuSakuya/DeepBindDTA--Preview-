import pymysql
import subprocess
import os
import re
import tempfile
from pathlib import Path
import sys


def create_database_if_not_exists(db_name='drug_discovery', host='localhost', user='root', password='12345'):
    """创建数据库（如果不存在）"""
    try:
        # 连接到MySQL服务器（不指定数据库）
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            charset='utf8mb4'
        )
        
        with conn.cursor() as cursor:
            # 检查数据库是否存在
            cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
            result = cursor.fetchone()
            
            if result:
                print(f"✅ 数据库 '{db_name}' 已存在")
            else:
                # 创建数据库
                cursor.execute(f"CREATE DATABASE `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                print(f"✅ 数据库 '{db_name}' 创建成功")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ 创建数据库失败: {e}")
        return False


def fix_sql_collation(content):
    """
    修复SQL文件中的排序规则兼容性问题
    将 MySQL 8.0 的排序规则替换为兼容的版本
    """
    # 替换映射：MySQL 8.0 -> MySQL 5.7/MariaDB 兼容
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
        r"C:\Program Files\MySQL\MySQL Server 9.5\bin\mysql.exe",
        r"C:\Program Files (x86)\MySQL\MySQL Server 9.5\bin\mysql.exe",
        r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
        r"C:\Program Files (x86)\MySQL\MySQL Server 8.0\bin\mysql.exe",
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    # 在PATH环境变量中查找
    for path in os.environ["PATH"].split(os.pathsep):
        mysql_path = os.path.join(path, "mysql.exe")
        if os.path.exists(mysql_path):
            return mysql_path

    return None


def import_sql_file(sql_file_path, db_name='drug_discovery'):
    """导入SQL文件"""
    # 首先确保数据库存在
    print("🔍 检查数据库是否存在...")
    if not create_database_if_not_exists(db_name):
        return False
    
    mysql_path = find_mysql_path()

    if mysql_path:
        print(f"✅ 找到mysql: {mysql_path}")
        try:
            # 读取并修复SQL文件
            print("🔧 检查并修复SQL文件兼容性...")
            with open(sql_file_path, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # 修复排序规则
            fixed_content = fix_sql_collation(sql_content)
            
            # 使用临时文件保存修复后的SQL
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.sql', delete=False) as temp_file:
                temp_file.write(fixed_content)
                temp_sql_path = temp_file.name
            
            try:
                cmd = [
                    mysql_path,
                    '-h', 'localhost',
                    '-u', 'root',
                    '-p12345',
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
                # 清理临时文件
                try:
                    os.unlink(temp_sql_path)
                except:
                    pass

        except Exception as e:
            print(f"❌ 导入过程出错: {e}")
            return False
    else:
        print("❌ 找不到mysql命令，请确保MySQL已安装并在PATH中")
        return False


def analyze_sql_file(sql_file_path):
    """分析SQL文件内容"""
    try:
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        print("🔍 分析SQL文件内容...")
        print(f"📁 文件大小: {len(content)} 字符")
        print(f"📁 文件大小: {len(content) / 1024 / 1024:.2f} MB")

        # 统计表数量
        table_creates = content.count('CREATE TABLE')
        print(f"📊 包含的表数量: {table_creates}")

        # 显示表名
        import re
        table_names = re.findall(r'CREATE TABLE `?(.*?)`? \(', content)
        if table_names:
            print("📋 包含的表:")
            for table in table_names:
                print(f"   - {table}")

        return True

    except Exception as e:
        print(f"❌ 分析文件失败: {e}")
        return False


if __name__ == "__main__":
    default_sql_file_path = Path(__file__).resolve().parent / 'test_fixed.sql'
    sql_file_path = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else default_sql_file_path

    if sql_file_path.exists():
        if analyze_sql_file(str(sql_file_path)):
            choice = input("\n是否导入这个SQL文件到数据库？ (y/n): ")
            if choice.lower() == 'y':
                import_sql_file(str(sql_file_path))
    else:
        print(f"❌ SQL文件不存在: {sql_file_path}")