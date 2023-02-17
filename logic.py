import pandas as pd


def integer(symbol):
    return ord(symbol.upper()) - 65


def load_from_excel(row, col1, col2):
    df = pd.read_excel('import.xlsx')
    result = df.to_dict('records')
    preview = result[row + 1]
    keys = list(preview.keys())
    data = []
    for d in range(row + 1, len(result)):
        data.append([result[d][keys[integer(col1)]], result[d][keys[integer(col2)]]])
    return data, preview
