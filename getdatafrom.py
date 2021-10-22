from openpyxl import load_workbook
def getvalue():
    load_wb = load_workbook("main.xlsx", data_only=True)
    load_ws = load_wb['Levels by ID']
    value=[]
    for row in load_ws.rows:
        rowb=[]
        for cell in row:
            rowb.append(cell.value)
        value.append(rowb)
    return value
if __name__=='__main__':
    print()