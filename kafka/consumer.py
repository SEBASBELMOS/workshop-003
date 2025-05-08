from json import loads
import joblib
from kafka import KafkaConsumer
import pandas as pd
import os
import sys
import time
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.database.db_wh import create_table, load_data

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

model = joblib.load('model/alternative_rf_model.pkl')

def predict(m):
    s = loads(m.value)
    df = pd.DataFrame(s, index=[0])
    
    feature_columns = [
        'year', 'gdp_per_capita', 'health_life_expectancy', 'social_support',
        'freedom', 'government_corruption', 'generosity',
        'continent_Africa', 'continent_America', 'continent_Asia',
        'continent_Central_America', 'continent_Europe', 'continent_North_America',
        'continent_Oceania', 'continent_South_America'
    ]
    
    required_columns = ['happiness_score']
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0
    
    df = df[feature_columns + ['happiness_score']]
    
    prediction = model.predict(df[feature_columns])
    df['predicted_happiness_score'] = prediction
    
    if (df['predicted_happiness_score'] < 0).any() or (df['predicted_happiness_score'] > 10).any():
        raise ValueError("Predicted happiness score out of expected range (0-10)")
    
    df = df.rename(columns={'health_life_expectancy': 'healthy_life_expectancy'})
    
    db_columns = [
        'year', 'social_support', 'gdp_per_capita', 'healthy_life_expectancy', 'freedom',
        'generosity', 'government_corruption', 'continent_North_America',
        'continent_Central_America', 'continent_South_America', 'happiness_score',
        'predicted_happiness_score'
    ]
    return df[db_columns]

def kafka_consumer():
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            consumer = KafkaConsumer(
                'test-data',
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id='my-group-1',
                value_deserializer=lambda m: loads(m.decode('utf-8')),
                bootstrap_servers=['localhost:9092'],
                consumer_timeout_ms=5000,
                session_timeout_ms=30000,
                heartbeat_interval_ms=10000
            )
            
            logger.info("Successfully connected to Kafka")
            
            batch = []
            batch_size = 50
            processed_rows = 0
            
            while True:
                try:
                    messages = consumer.poll(timeout_ms=1000)
                    if not messages:
                        if batch:
                            for row in batch:
                                load_data(row.iloc[0].to_dict())
                                processed_rows += 1
                                logger.info(f"Processed and stored row {processed_rows}")
                            batch = []
                        logger.info("No messages received in the last 1 second")
                        continue
                    
                    for _, msgs in messages.items():
                        for m in msgs:
                            try:
                                row = predict(m)
                                batch.append(row)
                                if len(batch) >= batch_size or not msgs:
                                    for row in batch:
                                        load_data(row.iloc[0].to_dict())
                                        processed_rows += 1
                                        logger.info(f"Processed and stored row {processed_rows}")
                                    batch = []
                            except Exception as e:
                                logger.error(f"Error processing message: {str(e)}")
                                raise
                                
                except Exception as e:
                    logger.error(f"Error polling messages: {str(e)}")
                    break
                    
        except Exception as e:
            retry_count += 1
            logger.error(f"Failed to connect to Kafka (attempt {retry_count}/{max_retries}): {str(e)}")
            if retry_count < max_retries:
                logger.info("Retrying in 10 seconds...")
                time.sleep(10)
            else:
                logger.error("Max retries reached. Exiting...")
                break
        finally:
            if batch:
                for row in batch:
                    load_data(row.iloc[0].to_dict())
                    processed_rows += 1
                    logger.info(f"Processed and stored row {processed_rows}")

if __name__ == '__main__':
    create_table()
    kafka_consumer()