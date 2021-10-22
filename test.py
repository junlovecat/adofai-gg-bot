import openpyxl
wb=openpyxl.load_workbook('main.xlsx')
ws=wb['Levels by ID']
# This will fail if there is no hyperlink to target
value=[]
for row in ws.rows:
    rowb=[]
    for cell in row:
        print(ws.cell(cell).hyperlink)
print(value)