import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import os
from datetime import datetime, timedelta
import joblib
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, date_format, to_date
from pyspark.sql.types import StructType, StructField, StringType, FloatType, TimestampType

class SalesPredictive:
    def __init__(self):
        # 定义模型和scaler保存路径
        self.MODEL_PATH = 'static/models/lstm_sales_model.keras'
        self.SCALER_PATH = 'static/models/sales_scaler.pkl'
        
        # 初始化Spark会话
        self.spark = SparkSession.builder \
            .appName("SalesPrediction") \
            .master("local[*]") \
            .getOrCreate()

    def _process_with_spark(self, historical_data):
        """使用Spark处理历史数据"""
        # 定义schema
        schema = StructType([
            StructField("date", StringType(), True),
            StructField("total_amount", FloatType(), True)
        ])
        
        # 转换数据格式
        data = []
        for day in historical_data:
            date_str = day['date']
            if isinstance(date_str, datetime):
                date_str = date_str.strftime('%Y-%m-%d')
            amount = float(day['total_amount'])
            data.append((date_str, amount))
        
        # 创建DataFrame并处理
        df = self.spark.createDataFrame(data, schema)
        df = df.withColumn("date", to_date(col("date")))
        df = df.orderBy("date")
        
        # 转换回Python数据
        processed_data = df.collect()
        return [(row['date'], row['total_amount']) for row in processed_data]

    def create_lstm_model(self, input_shape):
        """创建LSTM模型"""
        model = tf.keras.Sequential([
            tf.keras.layers.LSTM(50, activation='relu', input_shape=input_shape, return_sequences=True),
            tf.keras.layers.LSTM(50, activation='relu'),
            tf.keras.layers.Dense(25),
            tf.keras.layers.Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

    def prepare_data(self, data, lookback=7):
        """准备LSTM训练数据"""
        X, y = [], []
        for i in range(len(data) - lookback):
            X.append(data[i:(i + lookback)])
            y.append(data[i + lookback])
        return np.array(X), np.array(y)

    def train_and_save_model(self, historical_data):
        """训练LSTM模型并保存"""
        try:
            print(f"训练数据条数: {len(historical_data)}")
            
            # 使用Spark预处理数据
            processed_data = self._process_with_spark(historical_data)
            
            # 转换为numpy数组
            amounts = np.array([amount for _, amount in processed_data])
            
            # 数据标准化
            scaler = MinMaxScaler()
            scaled_data = scaler.fit_transform(amounts.reshape(-1, 1))
            
            # 保存scaler
            os.makedirs(os.path.dirname(self.SCALER_PATH), exist_ok=True)
            joblib.dump(scaler, self.SCALER_PATH)
            
            # 准备训练数据
            lookback = 7
            X, y = self.prepare_data(scaled_data, lookback)
            
            print(f"训练数据形状: X={X.shape}, y={y.shape}")
            
            # 创建和训练模型
            model = self.create_lstm_model((lookback, 1))
            model.fit(X, y, epochs=100, batch_size=32, verbose=1)
            
            # 保存模型
            os.makedirs(os.path.dirname(self.MODEL_PATH), exist_ok=True)
            model.save(self.MODEL_PATH)
            
            print("模型训练完成并保存")
            return True
            
        except Exception as e:
            print(f"模型训练失败: {str(e)}")
            return False

    def load_model_and_predict(self, last_sequence):
        """加载模型并进行预测"""
        try:
            # 加载模型和scaler
            model = tf.keras.models.load_model(self.MODEL_PATH)
            scaler = joblib.load(self.SCALER_PATH)
            
            # 生成预测
            forecast_data = []
            current_sequence = last_sequence.reshape(-1, 1)
            
            for i in range(7):
                input_seq = current_sequence[-7:].reshape(1, 7, 1)
                predicted_scaled = model.predict(input_seq, verbose=0)[0][0]
                predicted_amount = scaler.inverse_transform([[predicted_scaled]])[0][0]
                
                original_values = scaler.inverse_transform(current_sequence)
                pred_std = np.std(original_values) * 0.1
                
                forecast_date = datetime.now() + timedelta(days=i+1)
                
                forecast_data.append({
                    'date': forecast_date.strftime('%m-%d'),
                    'predicted_amount': round(float(predicted_amount), 2),
                    'lower_bound': round(max(0, predicted_amount - 1.96 * pred_std), 2),
                    'upper_bound': round(predicted_amount + 1.96 * pred_std, 2),
                    'confidence': 95
                })
                
                current_sequence = np.append(current_sequence[1:], [[predicted_scaled]], axis=0)
                
            return forecast_data
            
        except Exception as e:
            print(f"预测失败: {str(e)}")
            return None

    def __del__(self):
        """析构函数，确保Spark会话被正确关闭"""
        if hasattr(self, 'spark'):
            self.spark.stop()
