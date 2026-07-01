#!/usr/bin/env python3
"""
Script to fix imports in copied shadcn-admin files
"""

import os
import re
from pathlib import Path

def fix_imports_in_file(filepath):
    """Fix imports in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix @tanstack/react-router to react-router-dom
        content = content.replace("from '@tanstack/react-router'", "from 'react-router-dom'")
        content = content.replace('from "@tanstack/react-router"', 'from "react-router-dom"')
        
        # Remove 'use client' directives (not needed in Vite)
        content = re.sub(r"'use client'\s*\n", '', content)
        content = re.sub(r'"use client"\s*\n', '', content)
        
        # Fix getCookie import if cookies.ts doesn't exist
        if 'getCookie' in content and not os.path.exists('frontend/src/lib/cookies.ts'):
            # Create a simple getCookie function inline or import from utils
            pass
        
        # Only write if content changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Fixing imports in copied files...")
    print("")
    
    # Directories to process
    dirs_to_process = [
        'frontend/src/components/ui',
        'frontend/src/components/layout',
        'frontend/src/components',
        'frontend/src/context',
        'frontend/src/hooks',
    ]
    
    files_fixed = 0
    files_processed = 0
    
    for dir_path in dirs_to_process:
        if not os.path.exists(dir_path):
            continue
            
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith(('.tsx', '.ts')) and not file.endswith('.d.ts'):
                    filepath = os.path.join(root, file)
                    files_processed += 1
                    if fix_imports_in_file(filepath):
                        files_fixed += 1
                        print(f"✅ Fixed: {filepath}")
    
    print("")
    print(f"🎉 Done! Fixed {files_fixed} out of {files_processed} files")

if __name__ == '__main__':
    main()
