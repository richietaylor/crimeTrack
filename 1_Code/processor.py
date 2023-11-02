import pdfplumber
import pandas as pd
import os
import datetime

def extract_and_clean_data(pdf_path):
    # Initialize a list to store the extracted tables
    extracted_tables = []
    
    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        # Iterate through the pages
        for page in pdf.pages:
            # Extract tables from the page
            tables = page.extract_tables()
            
            # If tables are found, add them to the list
            if tables:
                for table in tables:
                    extracted_tables.append(table)
                    
    # Extracting and cleaning data from the tables
    combined_data = pd.DataFrame()
    for i in range(5, len(extracted_tables), 2):
        df = pd.DataFrame(extracted_tables[i])
        df_cleaned = df.dropna(how='all').dropna(axis=1, how='all')
        df_cleaned.columns = ["Offence", "Date", "Day of Week", "Time Begin", "Time End", "Street Name", "CAS Block", "Comments"]
        combined_data = pd.concat([combined_data, df_cleaned], ignore_index=True)
    
    return combined_data

# Directory path
dir_path = "./Crime Wrap/"

# Initialize a DataFrame to store the combined data from all PDFs
all_data = pd.DataFrame()

# Iterate through all PDF files in the folder
for filename in os.listdir(dir_path):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(dir_path, filename)
        print(f"Processing {filename}...")
        data = extract_and_clean_data(pdf_path)
        all_data = pd.concat([all_data, data], ignore_index=True)
        break

# Saving the combined data from all PDFs to a CSV file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
csv_filename = f"combined_crime_data_{timestamp}.csv"
csv_filepath = f"./Outputs/{csv_filename}"
all_data.to_csv(csv_filepath, index=False)

# Displaying the path to the saved CSV file
print("The combined crime data from all PDFs has been saved to:", csv_filepath)
