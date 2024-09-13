import pandas as pd
import sys

def excel_to_json(excel_path, json_path):
    try:
        # Load the Excel file
        df = pd.read_excel(excel_path, engine='openpyxl')

        # Convert the DataFrame to JSON
        json_data = df.to_json(orient='records', indent=4)

        # Write the JSON data to a file
        with open(json_path, 'w') as json_file:
            json_file.write(json_data)

        print(f"JSON file has been created at: {json_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <excel_file_path> <json_file_ppipath>")
    else:
        excel_file_path = sys.argv[1]
        json_file_path = sys.argv[2]
        excel_to_json(excel_file_path, json_file_path)
