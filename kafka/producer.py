from kafka import KafkaProducer
from json import dumps
import pandas as pd
import datetime as dt
import sys
import os
import time
from sklearn.model_selection import train_test_split
from kafka.errors import KafkaConnectionError, KafkaTimeoutError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utilities.data_preprocessing import continent, delete_columns

def create_dummy_vars(df):
    df = pd.get_dummies(df, columns=["continent"])
    new_columns = {
        "continent_North America": "continent_North_America",
        "continent_Central America": "continent_Central_America",
        "continent_South America": "continent_South_America"
    }
    df = df.rename(columns=new_columns)
    return df

def test_data():
    df = pd.read_csv("data/processed/world_happiness_report.csv")
    
    if 'continent' not in df.columns:
        raise ValueError("Column 'continent' not found in world_happiness_report.csv. Please preprocess the data first.")
    
    df_train, df_test = train_test_split(df, test_size=0.3, random_state=200)
    
    print(f"Total rows: {len(df)}, Test rows: {len(df_test)}")
    
    if 'country' in df_test.columns:
        print("Country column present, but continent is precomputed from CSV.")
    else:
        raise ValueError("Column 'country' not found in DataFrame.")
    
    df_test = delete_columns(df_test)
    
    df_test = create_dummy_vars(df_test)
    
    continent_columns = [
        'continent_Africa', 'continent_America', 'continent_Asia',
        'continent_Central_America', 'continent_Europe', 'continent_North_America',
        'continent_Oceania', 'continent_South_America'
    ]
    for col in continent_columns:
        if col not in df_test.columns:
            df_test[col] = 0
    
    original_continent = df.loc[df_train.index, 'continent'].value_counts()
    print("Original continent distribution in df_test (based on train split):")
    print(original_continent)
    print("Dummy variable sums in df_test:")
    for col in continent_columns:
        print(f"{col}: {df_test[col].sum()}")
    
    return df_test

def producer_kafka(df_test):
    max_retries = 5
    retry_delay = 15 
    for attempt in range(max_retries):
        try:
            producer = KafkaProducer(
                value_serializer=lambda m: dumps(m).encode('utf-8'),
                bootstrap_servers=['localhost:9092'], 
                batch_size=16384,
                linger_ms=10,
                api_version=(2, 6, 0),
                retries=5,
                request_timeout_ms=60000,
                max_block_ms=60000
            )
            print(f"Connected to Kafka on attempt {attempt + 1}")
            break
        except KafkaConnectionError as e:
            print(f"Failed to connect to Kafka (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise Exception("Max retries reached. Could not connect to Kafka.")
    
    batch_size = 50
    send_retries = 3
    send_retry_delay = 5
    
    for start in range(0, len(df_test), batch_size):
        end = min(start + batch_size, len(df_test))
        batch = df_test.iloc[start:end]
        
        for i in range(len(batch)):
            row_json = batch.iloc[i].to_json()
            for send_attempt in range(send_retries):
                try:
                    producer.send("test-data", value=row_json)
                    break
                except KafkaTimeoutError as e:
                    print(f"Failed to send message (attempt {send_attempt + 1}/{send_retries}): {e}")
                    if send_attempt < send_retries - 1:
                        print(f"Retrying send in {send_retry_delay} seconds...")
                        time.sleep(send_retry_delay)
                    else:
                        raise Exception("Max send retries reached. Failed to send message.")
        
        producer.flush()
        print(f"Sent batch of {end - start} messages at {dt.datetime.now(dt.UTC)}")

    print("The rows were sent successfully!")
    producer.close()

if __name__ == '__main__':
    df_test = test_data()
    producer_kafka(df_test)