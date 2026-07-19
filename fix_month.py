with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'r') as f:
    content = f.read()

target = "const resetAllFilters = () => {\n  selectedMonths.value = []"
replacement = "const resetAllFilters = () => {\n  selectedMonths.value = [new Date().getMonth() + 1]"
new_content = content.replace(target, replacement)

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'w') as f:
    f.write(new_content)

print("Done Month")
