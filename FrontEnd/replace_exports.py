import os
import glob
import re

files = glob.glob('src/views/Reports/*.vue')

for file in files:
    with open(file, 'r') as f:
        content = f.read()
    
    if "alert('ميزة التصدير" in content:
        # Add import if missing
        if "exportToCSV" not in content:
            # find first import
            content = re.sub(r'(import .* from .*' + '\n' + ')', r'\1import { exportToCSV } from "@/utils/export"\n', content, count=1)
        
        # Replace alert with export function
        # Check if the data array is named filteredData or reportData
        data_var = "filteredData.value" if "filteredData =" in content or "filteredData" in content else "reportData.value"
        # Wait, computed might not have .value in template, but in script it does.
        # Actually in script setup it's filteredData.value or reportData.value.
        
        report_name = os.path.basename(file).replace('.vue', '')
        
        # Use regex to replace the alert line
        content = re.sub(
            r"alert\('ميزة التصدير[^']*'\)", 
            f"exportToCSV([], {data_var}, '{report_name}_Export.csv')", 
            content
        )
        
        with open(file, 'w') as f:
            f.write(content)
        print(f"Updated {file}")

