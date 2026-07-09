import os
import re

reports_dir = 'src/views/Reports/'

back_button_code = """
        <button @click="$router.push('/reports')" class="flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm hover:bg-slate-50 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700 transition-all focus:outline-none print:hidden">
          <svg class="h-4.5 w-4.5 rtl:rotate-180" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          عودة للوحة التقارير
        </button>
        """

for filename in os.listdir(reports_dir):
    if filename.endswith('Report.vue') and filename != 'ActiveForceReport.vue':
        filepath = os.path.join(reports_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the print button tag
        # Usually it looks like: <button @click="printReport" ...>
        # We can use regex to inject the back button right before it
        
        pattern = r'(<button\s+[^>]*@click="printReport"[^>]*>)'
        
        # Let's insert the back_button_code right before the pattern matches
        if re.search(pattern, content):
            new_content = re.sub(pattern, lambda m: back_button_code + m.group(1), content)
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Added back button to {filename}")

