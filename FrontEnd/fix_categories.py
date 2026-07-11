import re

with open('src/views/Reports/GraphicalReports.vue', 'r') as f:
    content = f.read()

content = content.replace("categories: workforceLabels.value,", "")
content = content.replace("categories: overallRanksLabels.value,", "")

with open('src/views/Reports/GraphicalReports.vue', 'w') as f:
    f.write(content)

print("Removed explicit categories!")
