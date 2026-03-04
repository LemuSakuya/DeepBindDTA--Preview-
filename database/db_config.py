import pymysql
import pandas as pd
import pickle


class DrugDiscoveryDB:
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': 'LemuSakuya',
            'password': 'Z17158806598z',  # 替换为实际密码
            'database': 'drug_discovery',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }

    def get_connection(self):
        """获取数据库连接"""
        return pymysql.connect(**self.config)

    def import_csv_data(self, csv_file_path, table_name):
        """导入CSV数据到数据库"""
        try:
            # 读取CSV文件
            df = pd.read_csv(csv_file_path)
            conn = self.get_connection()

            with conn.cursor() as cursor:
                # 动态构建插入语句
                for _, row in df.iterrows():
                    columns = ', '.join(row.index)
                    placeholders = ', '.join(['%s'] * len(row))

                    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                    cursor.execute(sql, tuple(row.values))

            conn.commit()
            conn.close()
            print(f"✅ 成功导入数据到 {table_name}")

        except Exception as e:
            print(f"❌ 导入数据失败: {e}")

    def save_model_prediction(self, drug_id, target_id, prediction, model_version="LLMDTA_v1"):
        """保存模型预测结果"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                      INSERT INTO model_predictions
                          (drug_id, target_id, predicted_affinity, model_version)
                      VALUES (%s, %s, %s, %s) \
                      """
                cursor.execute(sql, (drug_id, target_id, prediction, model_version))

            conn.commit()
            print(f"✅ 预测结果已保存: {drug_id}-{target_id}")

        except Exception as e:
            print(f"❌ 保存预测结果失败: {e}")
        finally:
            conn.close()


# 创建全局数据库实例
db = DrugDiscoveryDB()