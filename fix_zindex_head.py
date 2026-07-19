with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'r') as f:
    content = f.read()

new_content = content.replace('class="relative z-50 flex h-11', 'class="relative z-10 flex h-11')

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'w') as f:
    f.write(new_content)
