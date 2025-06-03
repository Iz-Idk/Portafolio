import pandas as pd
import json
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

# Specify the path to your JSON file
file_path = r"C:\Users\izelm\Desktop\Izel\C++\First-Practice\Portafolio\output_data_US.json"

# Load the JSON file into a Python object
with open(file_path, 'r',encoding='utf-8') as file:
    data = json.load(file)

# Convert the loaded JSON data to a pandas DataFrame
df = pd.DataFrame(data)
replace_dict = {
    'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
    'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
    'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u',
    'À': 'A', 'È': 'E', 'Ì': 'I', 'Ò': 'O', 'Ù': 'U',
    'ä': 'a', 'ë': 'e', 'ï': 'i', 'ö': 'o', 'ü': 'u',
    'Ä': 'A', 'Ë': 'E', 'Ï': 'I', 'Ö': 'O', 'Ü': 'U',
    'ã': 'a', 'õ': 'o', 'Ã': 'A', 'Õ': 'O'
}

# Function to convert text to uppercase and replace accented vowels
def clean_text(text):
    if isinstance(text, str):
        text = text.upper()  # Convert to uppercase
        for key, value in replace_dict.items():
            text = text.replace(key, value)  # Replace accented vowels
    return text

# Apply the transformation to the entire DataFrame
df = df.applymap(clean_text)
df = df.drop(columns="URL")
df["MX"] = df["Ticker"] + ".MX"
# Display the DataFrame
print(df.size)
print(df.duplicated())
df = df.drop_duplicates()
print(df.size)
table = pa.Table.from_pandas(df)
pq.write_table(table, 'sp500.parquet')
#df.to_excel("dataframe_investing.xlsx")  