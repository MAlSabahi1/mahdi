import json

def log_to_file(data):
    with open('/app/logs/patch_log.txt', 'a') as f:
        f.write(json.dumps(data) + '\n')
