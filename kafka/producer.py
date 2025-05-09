from kafka import KafkaProducer
from json import dumps
import pandas as pd
import datetime as dt
import sys
import os
from sklearn.model_selection import train_test_split

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utilities.data_preprocessing import continent, delete_columns, convert_to_dummy

def test_data():
    df = pd.read_csv("data/processed/world_happiness_report.csv")
    
    df_train, df_test = train_test_split(df, test_size=0.3, random_state=200)
    
    print(f"Total rows: {len(df)}, Test rows: {len(df_test)}")
    
    if 'country' in df_test.columns:
        df_test['continent'] = df_test['country'].apply(continent) 
    else:
        raise ValueError("Column 'country' not found in DataFrame.")
    
    df_test = delete_columns(df_test)
    df_test = convert_to_dummy(df_test)

    continent_columns = [
        'continent_Africa', 'continent_America', 'continent_Asia',
        'continent_Central_America', 'continent_Europe', 'continent_North_America',
        'continent_Oceania', 'continent_South_America'
    ]
    for col in continent_columns:
        if col not in df_test.columns:
            df_test[col] = 0
    
    return df_test

def producer_kafka(df_test):
    producer = KafkaProducer(
        value_serializer=lambda m: dumps(m).encode('utf-8'),
        bootstrap_servers=['localhost:9092'],
        batch_size=16384,
        linger_ms=10
    )
    
    batch_size = 50
    
    for start in range(0, len(df_test), batch_size):
        end = min(start + batch_size, len(df_test))
        batch = df_test.iloc[start:end]
        
        for i in range(len(batch)):
            row_json = batch.iloc[i].to_json()
            producer.send("test-data", value=row_json)
        
        producer.flush()
        print(f"Sent batch of {end - start} messages at {dt.datetime.now(dt.UTC)}")

    print("The rows were sent successfully!")

if __name__ == '__main__':
    df_test = test_data()
    producer_kafka(df_test)