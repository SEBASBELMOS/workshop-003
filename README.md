# Workshop #3: Machine Learning and Data Streaming 💻
 
## Overview  

This project implements a machine learning pipeline to predict happiness scores for different countries using data from five CSV files, as part of Workshop 3: Machine Learning and Data Streaming.
---

## Project Structure

| Folder/File            | Description |
|------------------------|------------|
| **assets/**             | Static resources (images, documentation, etc.) |
| **dashboard/**                   | Dashboard script | 
| **data/**             | Data used in the project (ignored in .gitignore) |
| ├── database/                 |	Database Script  |
| ├── raw/                 |	World Happiness CSV files  |
| ├── processed/                 |	World Happiness Report file  |
| **docs/**              | Documentation, Guides and workshop PDFs |
| **env/**               | Environment variables (ignored in .gitignore) |
| ├── .env                 |	Stores credentials and paths  |
| **kafka/**                   | Python scripts for Apache Kafka   | 
| **model/**              | AI Model |
| **notebooks/**        | Jupyter Notebooks |
| ├── 01_EDA.ipynb | Exploratory Data Analysis of CSV files  |  
| ├── 02_model-training.ipynb   | Model Selection and Training   |  
| ├── 03_model-performance.ipynb   | Model Performance / Metrics  |  
| **docker-compose.yml**         | Docker configuration |
| **pyproject.toml**    | Poetry dependency management file |
| **README.md**         | This file |

## Tools and Libraries

- Python 3.13 -> [Download here](https://www.python.org/downloads/)
- PostgreSQL -> [Download here](https://www.postgresql.org/download/)
- Apache Kafka -> [Documentation here](https://kafka.apache.org/documentation/)
- Jupyter Notebook -> [VSCode tool used](https://code.visualstudio.com/docs/datascience/jupyter-notebooks)
- Docker -> [Documentation here](https://docs.docker.com/desktop)

All the libraries are included in the Poetry project config file (_pyproject.toml_).

---

## Installation and Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/SEBASBELMOS/workshop-003.git
   cd workshop-001
   ````

2. **Installing the dependencies with _Poetry_**
    - Windows: 
        - In Powershell, execute this command: 
            ```powershell
            (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
            ```
            <img src="https://github.com/SEBASBELMOS/workshop-003/blob/main/assets/poetry_installation.png" width="600"/>
        - Press Win + R, type _sysdm.cpl_, and press **Enter**. 
        - Go to the _Advanced_ tab, select _environment variable_.
        - Under System variables, select Path → Click Edit.
        - Click _Edit_ and set the path provided during the installation in **PATH** so that the `poetry` command works. ("C:\Users\username\AppData\Roaming\Python\Scripts")
        - Restart Powershell and execute _poetry --version_.

        
    - Linux
        - In a terminal, execute this command:
            ```bash
            curl -sSL https://install.python-poetry.org | python3 -
            ```
            <img src="https://github.com/SEBASBELMOS/workshop-003/blob/main/assets/poetry_linux.png" width="600"/>
        -  Now, execute:
            ```bash
            export PATH = "/home/user/.locar/bin:$PATH"
            ```
        -Finally, restart the terminal and execute _poetry --version_.


        <img src="https://github.com/SEBASBELMOS/workshop-003/blob/main/assets/poetry_linux_installed.png" width="400"/>

3. **Poetry Shell**
    - Enter the Poetry shell with _poetry shell_.
    - Then, execute _poetry init_, it will create a file called _pyproject.toml_
    - To add all the dependencies, execute this: 
        ```bash
        poetry add pandas matplotlib psycopg2-binary sqlalchemy python-dotenv seaborn ipykernel dotenv kafka-python
        ```
    - Install the dependencies with: 
        ```bash
        poetry install
        ```
        In case of error with the .lock file, just execute _poetry lock_ to fix it.
    - Create the kernel with this command (You must choose this kernel when running the notebooks):
        ```bash
        poetry run python -m ipykernel install --user --name workshop-003 --display-name "Python (workshop-003)"
        ```

4. **Enviromental variables**
    >Realise this in VS Code.

    1. Inside the cloned repository, create a new directory named *env/*.
    2. Within that directory, create a file called *.env*.
    3. In the *.env file*, define the following six environment variables (without double quotes around values):
        ```python
        PG_HOST = #host address, e.g. localhost or 127.0.0.1
        PG_PORT = #PostgreSQL port, e.g. 5432

        PG_USER = #your PostgreSQL user
        PG_PASSWORD = #your user password
        
        PG_DATABASE = #your database name, e.g. postgres
        ```
    4. Create the database with this command:
        ```bash
        psql -U your_username -c "CREATE DATABASE happiness_db;"
        ```

5. **Execution**

    1. Run all the notebooks to create the EDA, transformations and model.
    2. Run this command to start the Docker Containers for Kafka and Zookeeper.
        ```bash
        docker-compose up -d
        ```
    3. To check if the container are correctly running, use this command:
        ```bash
        docker ps
        ```
        <img src="https://github.com/SEBASBELMOS/workshop-003/blob/main/assets/docker_ps.png" width="300"/>

    4. Now we can create a `Kafka Topic` with this command:
        ```bash
        docker exec -it kafka_w3 kafka-topics --create --topic wh_kafka_topic --bootstrap-server localhost:9092
        ```
        <img src="https://github.com/SEBASBELMOS/workshop-003/blob/main/assets/kafka_topic_creation.png" width="300"/>

    5. To check if it was created, run this command:
        ```bash
        docker exec -it kafka_w3 kafka-topics --list --bootstrap-server localhost:9092
        ```
        <img src="https://github.com/SEBASBELMOS/workshop-003/blob/main/assets/kafka_topic_list.png" width="300"/>

    6. Finally, run the files from the kafka directory (`producer.py` and `consumer.py`, in the same order) with the following commands:

        ```bash
        python kafka/producer.py
        ```

        ```bash
        python kafka/consumer.py
        ```

        <img src="https://github.com/SEBASBELMOS/workshop-003/blob/main/assets/kafka_execution.png" width="300"/>

        <img src="https://github.com/SEBASBELMOS/workshop-003/blob/main/assets/kafka_execution_all_data.png" width="300"/>

    7. Optional Cleanup (After executing everything)

        ```bash
        docker-compose down
        psql -h localhost -U postgres -d happiness_db -c "DELETE FROM happiness;"
        psql -h localhost -U postgres -d happiness_db -c "ALTER SEQUENCE happiness_id_seq RESTART WITH 1;"
        ```

---

## **Conclusions**

This project successfully implemented a machine learning pipeline to predict happiness scores, fulfilling the objectives of Workshop 3: Machine Learning and Data Streaming. The pipeline integrated exploratory data analysis (EDA), model training, data streaming with Apache Kafka, and performance evaluation, with predictions stored in a PostgreSQL database.

### **Model Performance**
- Four regression models were evaluated: Linear Regression, Random Forest Regressor, an Alternative Random Forest Regressor, and Gradient Boosting Regressor. The Alternative Random Forest Regressor, configured with 100 estimators and a random state of 0, achieved the best performance with a Mean Squared Error (MSE) of 0.1721, a Mean Absolute Error (MAE) of 0.3246, and a Coefficient of Determination (R²) of 0.8639. This indicates that the model explains 86.39% of the variance in happiness scores, outperforming the other models and demonstrating the effectiveness of ensemble techniques with increased estimators. The Explained Variance Score of 0.8650 further confirms the model's ability to capture the variance in the target variable, with a Root Mean Squared Error (RMSE) of approximately 0.4149, suggesting an average prediction error of 0.4149 on a 0–10 scale.

- The Linear Regression model produced an MSE of 0.2103 and an R² of 0.8337, explaining 83.37% of the variance, which is a reasonable but improvable fit. The Random Forest Regressor (50 estimators) improved upon this with an MSE of 0.1755 and an R² of 0.8612, while the Gradient Boosting Regressor achieved an MSE of 0.1749 and an R² of 0.8617, both showing strong performance but falling short of the Alternative Random Forest Regressor.

- The expected model features include: ['year', 'gdp_per_capita', 'health_life_expectancy', 'social_support', 'freedom', 'government_corruption', 'generosity', 'continent_Africa', 'continent_America', 'continent_Asia', 'continent_Central_America', 'continent_Europe', 'continent_North_America', 'continent_Oceania', 'continent_South_America'], and these were successfully aligned with the database columns.

### **Data Streaming and Storage**
- The pipeline streamed the 30% test set (235 rows) from a total dataset of 782 rows, aligning with the 70/30 train-test split. The Kafka producer and consumer successfully processed and stored these predictions in the `happiness` database table, with each row including input features, actual happiness scores, and predicted happiness scores. The dummy variable values in the database were: `continent_Central_America`: 14, `continent_North_America`: 3, and `continent_South_America`: 18, with a continent distribution of `Other`: 200, `South America`: 18, `Central America`: 14, and `North America`: 3.

### **Visual and Analytical Insights**
- **Actual vs Predicted Happiness Scores**: A scatter plot of actual versus predicted happiness scores closely follows the ideal line (y=x), indicating high predictive accuracy. Most predictions deviate by less than 0.5 points from the actual scores, consistent with the RMSE of 0.4149, demonstrating the model’s reliability.

- **Average Predicted Happiness Score by Continent**: Analysis by continent revealed distinct regional patterns. North America exhibited the highest average predicted happiness score at 6.448847, followed by South America at 6.038931, Central America at 5.544421, and the "Other" category (encompassing Africa, Asia, Europe, Oceania, and America) at 5.337529. These values align with socio-economic conditions and highlight regional happiness variations.

- **Original vs Predicted Happiness Scores by Continent**: A bar chart comparing original and predicted average happiness scores showed strong alignment. For instance, Central America’s original average of 5.804705 was predicted as 5.544421, North America’s 7.024867 as 6.448847, and South America’s 6.126091 as 6.038931. The "Other" category averaged 5.6 originally and 5.337529 predicted, with minor differences (less than 0.5 on average) confirming the model’s robustness across diverse regions.

- **Feature Importance**: The model identified `gdp_per_capita` and `health_life_expectancy` as the most influential predictors, followed by `freedom`, `social_support`, `generosity`, and `government_corruption`.
---

## **Author**  
Created by **Sebastian Belalcazar Mosquera**. Connect with me on [LinkedIn](https://www.linkedin.com/in/sebasbelmos/) for feedback, suggestions, or collaboration opportunities!

---