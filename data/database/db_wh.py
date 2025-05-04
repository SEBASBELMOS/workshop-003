import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'env', '.env')
print(f"Attempting to load .env file from: {env_path}")
load_dotenv(env_path)

db_config = {
    "dbname": os.getenv("PG_DATABASE"),
    "user": os.getenv("PG_USER"),
    "password": os.getenv("PG_PASSWORD"),
    "host": os.getenv("PG_HOST"),
    "port": os.getenv("PG_PORT") 
}

print("Loaded database configuration:")
for key, value in db_config.items():
    if key != "password":
        print(f"{key}: {value}")

for key, value in db_config.items():
    if value is None:
        raise ValueError(f"Environment variable for {key} not set. Check .env file.")

def connection():
    """Establish a connection to the PostgreSQL database using environment variables."""
    try:
        print("Attempting to connect to the database...")
        conn = psycopg2.connect(**db_config)
        print("Successfully connected to the database!")
        return conn
    except psycopg2.Error as err:
        print(f"Error connecting to the database: {err}")
        return None

def create_table():
    """Create the happiness table if it doesn't exist."""
    try:
        conn = connection()
        if conn is None:
            raise Exception("Failed to connect to the database.")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS happiness (
                id SERIAL PRIMARY KEY,
                year INT,
                social_support FLOAT,
                gdp_per_capita FLOAT,
                healthy_life_expectancy FLOAT,
                freedom FLOAT,
                generosity FLOAT,
                government_corruption FLOAT,
                continent_North_America INT,
                continent_Central_America INT,
                continent_South_America INT,
                happiness_score FLOAT,
                predicted_happiness_score FLOAT
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Table created successfully!")
    except (psycopg2.Error, Exception) as err:
        print(f"Error creating the table: {err}")

def load_data(data):
    """Insert a single row of data into the happiness table, ensuring the table exists."""
    try:
        create_table()
        
        conn = connection()
        if conn is None:
            raise Exception("Failed to connect to the database.")
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO happiness (year, social_support, gdp_per_capita, healthy_life_expectancy, freedom, generosity, 
                                  government_corruption, continent_North_America, continent_Central_America, 
                                  continent_South_America, happiness_score, predicted_happiness_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            float(data['year']),
            float(data['social_support']),
            float(data['gdp_per_capita']),
            float(data['healthy_life_expectancy']),
            float(data['freedom']),
            float(data['generosity']),
            float(data['government_corruption']),
            int(data['continent_North_America']),
            int(data['continent_Central_America']),
            int(data['continent_South_America']),
            float(data['happiness_score']),
            float(data['predicted_happiness_score'])
        )
        cursor.execute(insert_query, values)
        conn.commit()
        cursor.close()
        conn.close()
        print("Row inserted successfully!")
    except (psycopg2.Error, Exception) as err:
        print(f"Error inserting data: {err}")

def get_happiness_data():
    """Retrieve all data from the happiness table."""
    try:
        create_table()
        
        conn = connection()
        if conn is None:
            raise Exception("Failed to connect to the database.")
        cursor = conn.cursor()
        query = "SELECT * FROM happiness"
        cursor.execute(query)
        data = cursor.fetchall()
        columns = ['id', 'year', 'social_support', 'gdp_per_capita', 'healthy_life_expectancy', 'freedom', 'generosity',
                   'government_corruption', 'continent_North_America', 'continent_Central_America', 'continent_South_America',
                   'happiness_score', 'predicted_happiness_score']
        df = pd.DataFrame(data, columns=columns)
        conn.commit()
        cursor.close()
        conn.close()
        print("Data successfully obtained")
        return df
    except (psycopg2.Error, Exception) as err:
        print(f"Error getting data: {err}")
        return None

if __name__ == "__main__":
    create_table()