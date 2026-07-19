with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'r') as f:
    content = f.read()

new_content = content.replace('class="relative z-50 flex h-11', 'class="relative z-10 flex h-11')
# For MultiSelect.vue as well:
with open('FrontEnd/src/components/common/MultiSelect.vue', 'r') as f2:
    content2 = f2.read()
new_content2 = content2.replace('class="relative z-50 flex h-11', 'class="relative z-10 flex h-11')

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'w') as f:
    f.write(new_content)
with open('FrontEnd/src/components/common/MultiSelect.vue', 'w') as f2:
    f2.write(new_content2)

print("Done Z-index")
