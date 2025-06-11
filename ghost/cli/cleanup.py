#!/usr/bin/env python3
"""
Ghost environment cleanup utility
Removes traces of old PYTHONPATH pollution from shell RC files
"""

import os
import sys
from pathlib import Path

def find_shell_rc_files():
    """Find shell RC files that might contain ghost pollution"""
    home = Path.home()
    shell_files = []
    
    # Common shell RC files
    potential_files = [
        ".bashrc",
        ".zshrc", 
        ".bash_profile",
        ".profile",
        ".config/fish/config.fish"
    ]
    
    for filename in potential_files:
        rc_file = home / filename
        if rc_file.exists():
            shell_files.append(rc_file)
    
    return shell_files

def check_file_pollution(filepath):
    """Check if a file contains ghost PYTHONPATH pollution"""
    markers = [
        "# ghostOS path config",
        "export PYTHONPATH=",
        "/ghostvault/system",
        "/ghostvault/ghost"
    ]
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            
        pollution_found = []
        for marker in markers:
            if marker in content:
                pollution_found.append(marker)
        
        return pollution_found
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return []

def clean_file_pollution(filepath, dry_run=False):
    """Remove ghost pollution from a file"""
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        # Track what we're removing
        removed_lines = []
        clean_lines = []
        skip_next = False
        
        for i, line in enumerate(lines):
            # Check if this is a ghost marker line
            if "# ghostOS path config" in line:
                removed_lines.append(line.strip())
                skip_next = True  # Skip the export line that follows
                continue
                
            # Skip export line after marker
            if skip_next and "export PYTHONPATH=" in line and ("ghostvault/system" in line or "ghostvault/ghost" in line):
                removed_lines.append(line.strip())
                skip_next = False
                continue
                
            # Remove standalone ghost PYTHONPATH exports
            if "export PYTHONPATH=" in line and ("ghostvault/system" in line or "ghostvault/ghost" in line):
                removed_lines.append(line.strip())
                continue
                
            skip_next = False
            clean_lines.append(line)
        
        if removed_lines:
            print(f"\n📄 {filepath}:")
            print(f"   Found {len(removed_lines)} pollution lines:")
            for line in removed_lines[:3]:  # Show first 3
                print(f"   - {line}")
            if len(removed_lines) > 3:
                print(f"   ... and {len(removed_lines) - 3} more")
            
            if not dry_run:
                # Create backup
                backup_path = filepath.with_suffix(filepath.suffix + '.ghost-backup')
                filepath.rename(backup_path)
                
                # Write clean file
                with open(filepath, 'w') as f:
                    f.writelines(clean_lines)
                
                print(f"   ✅ Cleaned and backed up to {backup_path}")
            else:
                print("   🔍 (dry run - no changes made)")
                
        return len(removed_lines)
        
    except Exception as e:
        print(f"   ❌ Error cleaning {filepath}: {e}")
        return 0

def clean_ghostenv_files():
    """Remove .ghostenv files"""
    ghostenv_locations = [
        Path.home() / "ghostvault" / ".ghostenv",
        Path.cwd() / ".ghostenv"
    ]
    
    removed = 0
    for ghostenv in ghostenv_locations:
        if ghostenv.exists():
            print(f"\n🗑️  Found .ghostenv at {ghostenv}")
            try:
                ghostenv.unlink()
                print("   ✅ Removed")
                removed += 1
            except Exception as e:
                print(f"   ❌ Error removing: {e}")
    
    return removed

def main():
    print("🧹 Ghost Environment Cleanup Utility")
    print("=" * 40)
    
    # Parse args
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        print("🔍 Running in DRY RUN mode (no changes will be made)\n")
    
    # Find and clean shell RC files
    print("Checking shell RC files for PYTHONPATH pollution...")
    shell_files = find_shell_rc_files()
    
    total_pollution = 0
    for rc_file in shell_files:
        pollution = check_file_pollution(rc_file)
        if pollution:
            cleaned = clean_file_pollution(rc_file, dry_run)
            total_pollution += cleaned
    
    # Clean .ghostenv files
    print("\nChecking for .ghostenv files...")
    ghostenv_removed = clean_ghostenv_files() if not dry_run else 0
    
    # Summary
    print("\n" + "=" * 40)
    if total_pollution > 0 or ghostenv_removed > 0:
        print(f"🧹 Cleanup {'would remove' if dry_run else 'complete'}:")
        if total_pollution > 0:
            print(f"   - {total_pollution} PYTHONPATH pollution lines")
        if ghostenv_removed > 0:
            print(f"   - {ghostenv_removed} .ghostenv files")
            
        if dry_run:
            print("\n💡 Run without --dry-run to apply changes")
    else:
        print("✨ No ghost environment pollution found!")
    
    # Check current environment
    if "PYTHONPATH" in os.environ and "ghostvault" in os.environ["PYTHONPATH"]:
        print("\n⚠️  Warning: PYTHONPATH still contains ghost paths in current shell")
        print("   Restart your shell or run: unset PYTHONPATH")

if __name__ == "__main__":
    main()