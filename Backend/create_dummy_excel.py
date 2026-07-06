import openpyxl

workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "Personnel Data"

# Headers
headers = [
    'الرقم العسكري الصحيح', 'الرقم العسكري', 'الأسم', 'الرقم الوطني', 
    'تاريخ الميلاد', 'تاريخ الالتحاق'
]
sheet.append(headers)

# Dummy Data
data = [
    [None, '1111111', 'أحمد محمد علي', '12345678901', '1990-01-01', '2010-01-01'],
    [None, '2222222', 'صالح حسين سعيد', '12345678902', '1988-05-15', '2008-03-20'],
    [None, '3333333', 'عبدالله قاسم ناصر', '12345678903', '1995-10-10', '2015-08-01'],
    [None, '4444444', 'علي بن علي سالم', '12345678904', '1985-12-05', '2005-02-11'],
    [None, '5555555', 'يوسف أحمد عوض', '12345678905', '1992-07-22', '2012-09-30'],
]

for row in data:
    sheet.append(row)

# Save
file_path = "d:/Programming/2026/HumenResorse/Backend/dummy_personnel_data.xlsx"
workbook.save(file_path)
print(f"Created {file_path} successfully!")
