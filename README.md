# Workshop #3: Machine Learning and Data Streaming 💻
 
## Overview  

This project implements a machine learning pipeline to predict happiness scores for different countries using data from five CSV files, as part of Workshop 3: Machine Learning and Data Streaming.
---

## Project Structure

| Folder/File            | Description |
|------------------------|------------|
| **assets/**             | Static resources (images, documentation, etc.) |
| **data/**             | Dataset used in the project (ignored in .gitignore) |
| **docs/**              | Documentation, Guides and workshop PDFs |
| **model/**              | AI Model and Training |
| **notebooks/**        | Jupyter Notebooks with analysis |
| ├── 01_EDA.ipynb | Exploratory Data Analysis of CSV files  |  
| ├── 02_model-training.ipynb   | Model Selection and Training   |  
| **kafka/**                   | Python scripts for tasks and utilities   | 
| **Dashboard/**                   | Dashboard script | 
| **venv/**              | Virtual environment (ignored in .gitignore) |
| **env/**               | Environment variables (ignored in .gitignore) |
| ├── .env                 |	Stores credentials and paths  |
| **docker-compose.yml**         | Docker configuration |
| **requirements.txt**         | All the libraries required to execute this project properly |
| **pyproject.toml**    | Poetry dependency management file |
| **README.md**         | This file |

## Tools and Libraries

- Python 3.13 -> [Download here](https://www.python.org/downloads/)
- PostgreSQL -> [Download here](https://www.postgresql.org/download/)
- Power BI Desktop -> [Download here](https://www.microsoft.com/es-es/power-platform/products/power-bi/desktop)
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
        poetry add pandas matplotlib psycopg2-binary sqlalchemy python-dotenv seaborn ipykernel dotenv
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

---

## **Author**  
Created by **Sebastian Belalcazar Mosquera**. Connect with me on [LinkedIn](https://www.linkedin.com/in/sebasbelmos/) for feedback, suggestions, or collaboration opportunities!

---