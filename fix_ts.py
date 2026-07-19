import re

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'r') as f:
    content = f.read()

content = content.replace("groups.push({", "groups.push({") # Just ensuring it exists
content = content.replace("const groups = []", "const groups: any[] = []")
content = content.replace("const validVals = groupedWorkplaces.value.flatMap(g => g.options.map(o => o.value))", 
                          "const validVals = groupedWorkplaces.value.flatMap((g: any) => g.options.map((o: any) => o.value))")

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'w') as f:
    f.write(content)

print("TS fixed.")
