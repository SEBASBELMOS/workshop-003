import country_converter as coco
import pandas as pd

def continent(country):
    cc = coco.CountryConverter()
    try:
        base_continent = cc.convert(names=country, to='continent')
        
        continent_mapping = {
            "Argentina": "South America",
            "Belize": "Central America",
            "Bolivia": "South America",
            "Brazil": "South America",
            "Canada": "North America",
            "Chile": "South America",
            "Colombia": "South America",
            "Costa Rica": "Central America",
            "Dominican Republic": "Central America",
            "Ecuador": "South America",
            "El Salvador": "Central America",
            "Guatemala": "Central America",
            "Honduras": "Central America",
            "Haiti": "Central America",
            "Jamaica": "Central America",
            "Mexico": "North America",
            "Panama": "Central America",
            "Paraguay": "South America",
            "Peru": "South America",
            "Puerto Rico": "Central America",
            "Trinidad and Tobago": "South America",
            "Trinidad & Tobago": "South America",
            "United States": "North America",
            "Uruguay": "South America",
            "Venezuela": "South America"
        }
        
        return continent_mapping.get(country, base_continent)
    except:
        return None

def convert_to_dummy(df):

    df = pd.get_dummies(df, columns=['continent'], prefix='continent')

    df.columns = [
        col.replace('continent_', 'continent_').replace(' ', '_')
        for col in df.columns
    ]
    
    expected = [
        'continent_Africa', 'continent_America', 'continent_Asia',
        'continent_Central_America', 'continent_Europe',
        'continent_North_America', 'continent_Oceania',
        'continent_South_America'
    ]
    for c in expected:
        if c not in df.columns:
            df[c] = 0

    for col in expected:
        df[col] = df[col].astype(int)
    return df

def delete_columns(df):
    df.drop(columns=['country', 'happiness_rank'], inplace=True, errors='ignore')
    return df
