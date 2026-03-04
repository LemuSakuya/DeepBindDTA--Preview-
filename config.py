"""
项目配置文件
统一管理所有配置项
"""
import os


class Config:
    """项目配置类"""
    
    # 数据库配置
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '12345')
    DB_NAME = os.getenv('DB_NAME', 'drug_discovery')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_CHARSET = 'utf8mb4'
    
    @classmethod
    def get_db_config(cls):
        """获取数据库配置字典"""
        return {
            'host': cls.DB_HOST,
            'user': cls.DB_USER,
            'password': cls.DB_PASSWORD,
            'database': cls.DB_NAME,
            'port': cls.DB_PORT,
            'charset': cls.DB_CHARSET
        }
    
    # 文件路径配置
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    MODELS_DIR = os.path.join(BASE_DIR, 'savemodel')
    OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
    PIC_DIR = os.path.join(BASE_DIR, 'pic')
    CASE_DIR = os.path.join(BASE_DIR, 'Case')
    
    # 软件信息
    SOFTWARE_NAME = '基于有向符号图与LLM的药物数据分析系统'
    
    # 模型配置
    DEFAULT_MODEL_VERSION = "LLMDTA_v1"
    
    # GUI配置
    MAIN_WINDOW_SIZE = '700x500'
    START_WINDOW_SIZE = '993x663'
    
    # MySQL路径（用于导入SQL）
    MYSQL_PATHS = [
        r"C:\Program Files\MySQL\MySQL Server 9.5\bin\mysql.exe",
        r"C:\Program Files (x86)\MySQL\MySQL Server 9.5\bin\mysql.exe",
        r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
        r"C:\Program Files (x86)\MySQL\MySQL Server 8.0\bin\mysql.exe",
    ]


# 创建必要的目录
for dir_path in [Config.DATA_DIR, Config.OUTPUT_DIR]:
    os.makedirs(dir_path, exist_ok=True)

