import pandas as pd

# Automatically sorts company.xlsx file
def sort_company_data():
    file_path = 'company.xlsx'

    # Load the data without specifying a sheet name
    df = pd.read_excel(file_path)

    # Creating the condition to move rows to the bottom
    condition = (df['지속가능경영보고서'] == 'X') & (df['기업지배구조보고서'] == 'X') & (df['채권발행이력수'] == 0)

    # Adding a temporary sorting column based on the condition
    df['Sort_Order'] = condition

    # Sorting and removing the temporary column
    sorted_df = df.sort_values(by='Sort_Order').drop(columns=['Sort_Order']).reset_index(drop=True)

    # Save the sorted data back to the original Excel file
    sorted_df.to_excel(file_path, index=False)

    print(f"Sorted file saved as: {file_path}")

# Example usage:
sort_company_data()
