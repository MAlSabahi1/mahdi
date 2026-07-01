"""
Script to compare old backend1 with new backend.
For each Python file in backend1, checks if its content exists in backend.
"""
import os
import hashlib
import difflib
OLD = '/home/mahdi/Desktop/POL/backend1'
NEW = '/home/mahdi/Desktop/POL/backend'
SKIP_DIRS = {'__pycache__', 'migrations', '.pytest_cache', 'media', 'staticfiles'}
SKIP_FILES = {'settings.py', 'settings_test.py', 'manage.py', 'celery.py', 
              'asgi.py', 'wsgi.py', 'middleware.py', '__init__.py',
              'yemen-info.json', 'test_api_phase4.py', 'test_rejections.py',
              'test_security.py', 'run_test_api_directly.py', 'pytest.ini'}
# Map old app names to new locations
APP_MAP = {
    'personnel': 'systems/personnel',
    'services': 'systems/services',
    'accounts': 'infra/accounts',
    'authorization': 'infra/authorization',
    'audit': 'infra/audit',
    'security': 'infra/security',
    'storage': 'infra/storage',
    'workflows': 'infra/workflows',
    'core': 'core',
    'hrms': 'config',
}
def get_py_files(root):
    """Get all .py files excluding skip dirs"""
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            if f.endswith('.py') and f not in SKIP_FILES:
                full = os.path.join(dirpath, f)
                rel = os.path.relpath(full, root)
                files.append((rel, full))
    return files
def file_hash(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()
def find_in_new(old_rel, old_full):
    """Try to find the equivalent file in the new backend"""
    old_basename = os.path.basename(old_rel)
    old_app = old_rel.split('/')[0]
    
    # Try direct mapped path
    if old_app in APP_MAP:
        mapped = APP_MAP[old_app]
        rest = '/'.join(old_rel.split('/')[1:])
        direct = os.path.join(NEW, mapped, rest)
        if os.path.exists(direct):
            return direct, 'direct_map'
    
    # Search all .py files in new backend for same basename
    matches = []
    for dirpath, dirnames, filenames in os.walk(NEW):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        if old_basename in filenames:
            full = os.path.join(dirpath, old_basename)
            matches.append(full)
    
    return matches, 'search'
def compare_content(old_path, new_path):
    """Compare file contents and return similarity ratio"""
    with open(old_path, 'r', errors='replace') as f:
        old_lines = f.readlines()
    with open(new_path, 'r', errors='replace') as f:
        new_lines = f.readlines()
    
    sm = difflib.SequenceMatcher(None, old_lines, new_lines)
    return sm.ratio(), len(old_lines), len(new_lines)
# Main analysis
old_files = get_py_files(OLD)
print(f"=== AUDIT: Backend1 → Backend Migration Completeness ===")
print(f"Total files to check in backend1: {len(old_files)}\n")
missing = []
partial = []
complete = []
redirected = []
for old_rel, old_full in sorted(old_files):
    result, method = find_in_new(old_rel, old_full)
    
    if method == 'direct_map' and isinstance(result, str):
        ratio, old_lines, new_lines = compare_content(old_full, result)
        new_rel = os.path.relpath(result, NEW)
        if ratio > 0.95:
            complete.append((old_rel, new_rel, ratio, old_lines, new_lines))
        elif ratio > 0.5:
            partial.append((old_rel, new_rel, ratio, old_lines, new_lines))
        else:
            # Check if file is a redirect stub
            with open(result, 'r') as f:
                content = f.read()
            if len(content) < 500 and ('import' in content or 'from' in content):
                redirected.append((old_rel, new_rel, len(content), old_lines))
            else:
                partial.append((old_rel, new_rel, ratio, old_lines, new_lines))
    elif isinstance(result, list) and len(result) > 0:
        # Found by basename search
        best_ratio = 0
        best_match = None
        for match in result:
            ratio, old_lines, new_lines = compare_content(old_full, match)
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = match
                best_old_lines = old_lines
                best_new_lines = new_lines
        
        new_rel = os.path.relpath(best_match, NEW)
        if best_ratio > 0.95:
            complete.append((old_rel, new_rel, best_ratio, best_old_lines, best_new_lines))
        elif best_ratio > 0.3:
            partial.append((old_rel, new_rel, best_ratio, best_old_lines, best_new_lines))
        else:
            # Check if it's a redirect stub
            with open(best_match, 'r') as f:
                content = f.read()
            if len(content) < 500:
                redirected.append((old_rel, new_rel, len(content), best_old_lines))
            else:
                missing.append((old_rel, best_old_lines if 'best_old_lines' in dir() else 0))
    else:
        with open(old_full, 'r', errors='replace') as f:
            lines = len(f.readlines())
        missing.append((old_rel, lines))
print("=" * 80)
print(f"✅ COMPLETE (>95% match): {len(complete)} files")
print("=" * 80)
for old, new, ratio, ol, nl in complete:
    print(f"  {old}")
    print(f"    → {new} ({ratio:.0%}, {ol}→{nl} lines)")
print(f"\n{'=' * 80}")
print(f"⚠️  PARTIAL match (50-95%): {len(partial)} files")
print("=" * 80)
for old, new, ratio, ol, nl in partial:
    print(f"  {old}")
    print(f"    → {new} ({ratio:.0%}, {ol}→{nl} lines)")
print(f"\n{'=' * 80}")
print(f"🔄 REDIRECT STUBS (file exists but is a small import redirect): {len(redirected)} files")
print("=" * 80)
for old, new, size, ol in redirected:
    print(f"  {old} ({ol} lines in old)")
    print(f"    → {new} (stub: {size} bytes) — NEEDS VERIFICATION")
print(f"\n{'=' * 80}")
print(f"❌ MISSING: {len(missing)} files")
print("=" * 80)
for old, lines in missing:
    print(f"  {old} ({lines} lines)")
# Summary
print(f"\n{'=' * 80}")
print("SUMMARY")
print("=" * 80)
print(f"  Complete:   {len(complete)}")
print(f"  Partial:    {len(partial)}")
print(f"  Redirects:  {len(redirected)}")
print(f"  Missing:    {len(missing)}")
print(f"  Total:      {len(old_files)}")
