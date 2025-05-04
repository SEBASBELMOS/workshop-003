import pandas as pd

def df_brief(data: dict) -> pd.DataFrame:
    """
    Assemble a concise overview DataFrame from a mapping of years to DataFrames,
    reporting for each year the count of rows, columns, missing values and duplicate entries.

    Parameters:
        data (dict):
            A dictionary whose keys are years (e.g. 2015–2019) and whose values
            are pandas DataFrames for those respective years.

    Returns:
        pd.DataFrame:
            A summary table with columns:
            - Year
            - Number of rows
            - Number of columns
            - Total missing values
            - Total duplicate entries
    """
    summary_list = []
    for year, df in data.items():
        row_count = df.shape[0]
        col_count = df.shape[1]
        missing_count = df.isnull().sum().sum()
        duplicate_count = df.duplicated().sum()

        summary_list.append({
            "Year": year,
            "Number of rows": row_count,
            "Number of columns": col_count,
            "Total missing values": missing_count,
            "Total duplicate entries": duplicate_count
        })

    return pd.DataFrame(summary_list)



def compare_names_bool(data: dict) -> pd.DataFrame:
    """
    Build a boolean comparison table of column names across multiple years.

    Parameters:
        data (dict):
            A dictionary where keys are years (e.g. 2015–2019) and values are
            pandas DataFrames for those years.

    Returns:
        pd.DataFrame:
            An index of every column name found, with one column per year.
            Cells contain True if that column exists in the year’s DataFrame,
            or False if it does not.
    """
    
    all_columns = set().union(*(df.columns for df in data.values()))

    bool_map = {
        col: {
            year: (col in df.columns)
            for year, df in data.items()
        }
        for col in all_columns
    }

    bool_df = pd.DataFrame(bool_map).T
    bool_df.index.name = "Column Name"
    return bool_df
