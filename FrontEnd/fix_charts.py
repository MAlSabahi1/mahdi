import re

with open('src/views/Reports/GraphicalReports.vue', 'r') as f:
    content = f.read()

# Fix Workforce Chart Categories
content = re.sub(
    r"xaxis: {\n    labels: { style: { colors: getLabelColor\(\), fontSize: '13px', fontFamily, fontWeight: 'bold' } },\n    axisBorder: { show: false },\n    title: { text: 'الكثافة العددية', style: { color: getLabelColor\(\), fontFamily, fontWeight: 'bold' } }\n  },",
    r"xaxis: {\n    categories: workforceLabels.value,\n    labels: { style: { colors: getLabelColor(), fontSize: '13px', fontFamily, fontWeight: 'bold' } },\n    axisBorder: { show: false }\n  },",
    content
)

content = re.sub(
    r"yaxis: {\n    categories: workforceLabels.value,\n    labels: { style: { colors: getLabelColor\(\), fontFamily, fontSize: '13px', fontWeight: 'bold' }, minWidth: 150 },\n  },",
    r"yaxis: {\n    title: { text: 'الكثافة العددية', style: { color: getLabelColor(), fontFamily, fontWeight: 'bold' } },\n    labels: { style: { colors: getLabelColor(), fontFamily, fontSize: '13px', fontWeight: 'bold' }, minWidth: 150 }\n  },",
    content
)

# Fix Overall Ranks Chart Categories
content = re.sub(
    r"xaxis: {\n    labels: { style: { colors: getLabelColor\(\), fontFamily, fontSize: '11px' } },\n    axisBorder: { show: false }\n  },",
    r"xaxis: {\n    categories: overallRanksLabels.value,\n    labels: { style: { colors: getLabelColor(), fontFamily, fontSize: '12px', fontWeight: 'bold' } },\n    axisBorder: { show: false }\n  },",
    content
)

content = re.sub(
    r"yaxis: {\n    categories: overallRanksLabels.value,\n    labels: { style: { colors: getLabelColor\(\), fontFamily, fontSize: '12px', fontWeight: 'bold' } }\n  },",
    r"yaxis: {\n    labels: { style: { colors: getLabelColor(), fontFamily, fontSize: '11px' } }\n  },",
    content
)

# Fix Dynamic Height
content = content.replace("Math.max(500, workforceLabels.value.length * 45)", "Math.max(150, workforceLabels.value.length * 60)")

# Fix bar height for Overall Ranks
content = content.replace("barHeight: '50%'", "barHeight: '70%', distributed: true")

# Make donut charts look 3D using gradients
content = content.replace("chart: { type: 'donut', ...commonChartConfig, toolbar: { show: false } },", "chart: { type: 'donut', ...commonChartConfig, toolbar: { show: false } },\n  fill: { type: 'gradient', gradient: { shade: 'dark', type: 'vertical', shadeIntensity: 0.5, gradientToColors: ['#38bdf8', '#34d399', '#fcd34d', '#c084fc', '#f43f5e'], inverseColors: true, opacityFrom: 1, opacityTo: 1, stops: [0, 100] } },")
content = content.replace("chart: { type: 'pie', ...commonChartConfig, toolbar: { show: false } },", "chart: { type: 'pie', ...commonChartConfig, toolbar: { show: false } },\n  fill: { type: 'gradient', gradient: { shade: 'dark', type: 'vertical', shadeIntensity: 0.5, gradientToColors: ['#60a5fa', '#34d399', '#fbbf24', '#a78bfa', '#94a3b8', '#f87171'], inverseColors: true, opacityFrom: 1, opacityTo: 1, stops: [0, 100] } },")


with open('src/views/Reports/GraphicalReports.vue', 'w') as f:
    f.write(content)

print("Fixed!")
