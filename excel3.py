import pandas as pd

def remove_xx0_rows():
    file_path = 'company_last.xlsx'

    # Load the already sorted data
    df = pd.read_excel(file_path)

    # Remove rows where BCD columns are X, X, and 0
    filtered_df = df[~((df['지속가능경영보고서'] == 'X') & 
                       (df['기업지배구조보고서'] == 'X') & 
                       (df['채권발행이력수'] == 0))]

    # Save the cleaned data back to the same Excel file
    filtered_df.to_excel(file_path, index=False)

    print(f"Cleaned file saved as: {file_path}")

# Example usage:
remove_xx0_rows()