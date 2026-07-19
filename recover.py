import re
import sys
import os

log_file = os.path.expanduser('~/.gemini/antigravity/brain/da401edf-d656-4e8c-b2ec-c067d18c4a75/.system_generated/logs/overview.txt')

if not os.path.exists(log_file):
    print("Log file not found.")
    sys.exit(1)

with open(log_file, 'r') as f:
    lines = f.readlines()

recovered_lines = {}

pattern = re.compile(r'^(\d+):\s(.*)$')

for line in lines:
    match = pattern.match(line.rstrip('\n'))
    if match:
        line_num = int(match.group(1))
        content = match.group(2)
        
        # In case the overview text includes other output that matches \d+: format,
        # we can assume the file we want has up to 1809 lines
        if 1 <= line_num <= 1809:
            recovered_lines[line_num] = content

print(f"Recovered {len(recovered_lines)} lines.")
missing = []
for i in range(1, 1601):
    if i not in recovered_lines:
        missing.append(i)

print(f"Missing between 1-1600: {len(missing)} lines.")
if len(missing) > 0:
    print(f"Missing example: {missing[:10]} ... {missing[-10:] if len(missing)>10 else ''}")

# Let's save the recovered lines to a file to inspect
with open('recovered_part.txt', 'w') as f:
    for i in sorted(recovered_lines.keys()):
        f.write(f"{i}: {recovered_lines[i]}\n")

