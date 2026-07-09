import os
import re

reports_dir = 'src/views/Reports/'

back_button_code = """
          <button @click="$router.push('/reports')" class="flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm hover:bg-slate-50 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700 transition-all focus:outline-none">
            <svg class="h-4.5 w-4.5 rtl:rotate-180" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            عودة للوحة التقارير
          </button>
"""

for filename in os.listdir(reports_dir):
    if filename.endswith('.vue') and filename != 'ReportsDashboard.vue' and filename != 'AuditMovementReports.vue':
        filepath = os.path.join(reports_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for the toolbar buttons container: <div class="flex items-center gap-2"> or <div class="flex items-center gap-3">
        # that usually contains the print/refresh buttons.
        # We can also just replace '<div class="flex items-center gap-2">' with '<div class="flex items-center gap-2">' + back_button_code
        
        if '<div class="flex items-center gap-3">' in content:
            new_content = content.replace('<div class="flex items-center gap-3">', '<div class="flex items-center gap-3">' + back_button_code, 1)
        elif '<div class="flex items-center gap-2">' in content:
            new_content = content.replace('<div class="flex items-center gap-2">', '<div class="flex items-center gap-2">' + back_button_code, 1)
        else:
            new_content = content
            
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
                print(f"Added back button to {filename}")

