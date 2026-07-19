import re

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'r') as f:
    content = f.read()

# We need to find <div class="relative"> followed by <div v-if="showXXXDropdown" ... class="fixed inset-0 z-40"></div>
# and replace <div class="relative"> with <div class="relative" :class="{'z-50': showXXXDropdown}">

def repl(match):
    show_var = match.group(1)
    return f'<div class="relative" :class="{{\'z-50\': {show_var}}}">\n              <div v-if="{show_var}"'

new_content = re.sub(r'<div class="relative">\n\s*<div v-if="([a-zA-Z0-9_]+)"', repl, content)

# But wait, there's also the month dropdown, which is coded exactly like that.
# Let's check how many were replaced.
import sys
if content == new_content:
    print("No changes made!")
    sys.exit(1)

with open('FrontEnd/src/views/Reports/MonthlyServicesReport.vue', 'w') as f:
    f.write(new_content)
print(f"Replaced {len(re.findall(r'<div class=\"relative\">\\n\\s*<div v-if=\"([a-zA-Z0-9_]+)\"', content))} occurrences.")
