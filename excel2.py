import pandas as pd
import FinanceDataReader as fdr

def sort_company_data():
    file_path = 'company.xlsx'
    save_path = 'company_last.xlsx'

    # Load the data without specifying a sheet name
    df = pd.read_excel(file_path)

    # Fetch top market cap data from KOSPI
    kospi = fdr.StockListing('KOSPI')
    kospi_sorted = kospi.sort_values(by="Marcap", ascending=False)

    # Merge market cap data with the existing dataset using the company name
    merged_df = pd.merge(df, kospi_sorted[['Name', 'Marcap']], left_on='회사명', right_on='Name', how='left')

    # Sorting by market cap in descending order, ensuring the entire row is moved together
    sorted_df = merged_df.sort_values(by='Marcap', ascending=False).drop(columns=['Name']).reset_index(drop=True)

    # Save the sorted data back to a new Excel file
    sorted_df.to_excel(save_path, index=False)

    print(f"Sorted file saved as: {save_path}")

# Example usage:
sort_company_data()
