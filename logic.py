import pandas as pd

import db


def integer(symbol):
    return ord(symbol.upper()) - 65


def load_from_excel(row, col1, col2, filename='import.xlsx'):
    df = pd.read_excel(filename)
    result = df.to_dict('records')
    preview = result[row + 1]
    keys = list(preview.keys())
    data = []
    for d in range(row + 1, len(result)):
        data.append([result[d][keys[integer(col1)]], result[d][keys[integer(col2)]]])
    return data, preview


def load_to_excel():
    items = db.get_items()
    df = pd.DataFrame(items)

    # Create a Pandas Excel writer using xlsx format
    writer = pd.ExcelWriter('export.xlsx', engine='xlsxwriter')

    # Write the DataFrame to a sheet called 'Sheet1'
    df.to_excel(writer, sheet_name='Sheet1', index=False)

    # Save the file
    writer.save()