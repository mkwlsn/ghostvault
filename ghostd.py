#!/usr/bin/env python3
"""
ghostd v0.0.1 - Minimal Daemon for ghostOS

Processes ritual proposals from .ghost/output/, executes them,
and logs results according to the v0.0.1 specification.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
import shutil
import argparse
import re


def parse_simple_yaml(content):
    """
    Minimal YAML parser for ritual proposal format.
    Uses regex to extract the specific fields we need.
    """
    
    # Extract chain_id
    chain_match = re.search(r'chain_id:\s*["\']?([^"\'\n]+)["\']?', content)
    if not chain_match:
        raise ValueError("Missing chain_id field")
    
    # Extract reasoning (optional)
    reasoning_match = re.search(r'reasoning:\s*["\']?([^"\'\n]+)["\']?', content)
    reasoning = reasoning_match.group(1).strip() if reasoning_match else ""
    
    # Extract rituals - find all ritual blocks
    rituals = []
    
    # Find ritual blocks starting with "- name:"
    ritual_blocks = re.finditer(r'- name:\s*["\']?([^"\'\n]+)["\']?', content)
    
    for match in ritual_blocks:
        ritual_name = match.group(1).strip()
        ritual = {'name': ritual_name}
        
        # Find args section for this ritual
        start_pos = match.end()
        # Look for args: followed by indented content
        args_match = re.search(r'args:\s*\n((?:\s{6,}[^\n]+\n?)*)', content[start_pos:])
        
        if args_match:
            args_content = args_match.group(1)
            ritual['args'] = {}
            
            # Parse each arg line
            for line in args_content.split('\n'):
                line = line.strip()
                if line and ':' in line:
                    key, value = line.split(':', 1)
                    ritual['args'][key.strip()] = value.strip().strip('"\'')
        
        rituals.append(ritual)
    
    return {
        'ritual_proposal': {
            'chain_id': chain_match.group(1).strip(),
            'reasoning': reasoning,
            'rituals': rituals
        }
    }


def find_yaml_files(directory):
    """Find all YAML files in the given directory."""
    yaml_files = []
    directory = Path(directory)
    
    if directory.exists():
        for file_path in directory.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in ['.yaml', '.yml']:
                yaml_files.append(file_path)
    
    return sorted(yaml_files)


def load_ritual_proposal(file_path):
    """Load and parse a ritual proposal from a YAML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        data = parse_simple_yaml(content)
        
        # Validate required structure
        if 'ritual_proposal' not in data:
            raise ValueError("Missing 'ritual_proposal' section")
        
        proposal = data['ritual_proposal']
        
        if 'chain_id' not in proposal:
            raise ValueError("Missing 'chain_id' field")
        
        if 'rituals' not in proposal:
            raise ValueError("Missing 'rituals' field")
        
        return proposal
        
    except Exception as e:
        raise ValueError(f"Error loading {file_path}: {e}")


def execute_ritual(ritual):
    """
    Execute a single ritual and return result.
    Returns dict with status, result info, and any error details.
    """
    result = {
        'name': ritual.get('name', 'unknown'),
        'status': 'pending',
        'error': None
    }
    
    try:
        ritual_name = ritual.get('name', '').lower()
        args = ritual.get('args', {})
        
        if ritual_name == 'file_write':
            # Write content to path
            path = args.get('path', '')
            content = args.get('content', '')
            
            if not path:
                raise ValueError("file_write requires 'path' argument")
            
            # Ensure parent directory exists
            file_path = Path(path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            result['status'] = 'success'
            result['path'] = str(file_path)
            result['bytes_written'] = len(content.encode('utf-8'))
            
        elif ritual_name == 'mkdir':
            # Create directory
            path = args.get('path', '')
            
            if not path:
                raise ValueError("mkdir requires 'path' argument")
            
            dir_path = Path(path)
            dir_path.mkdir(parents=True, exist_ok=True)
            
            result['status'] = 'success'
            result['path'] = str(dir_path)
            
        elif ritual_name == 'echo':
            # Print message to stdout
            message = args.get('message', '')
            print(message)
            
            result['status'] = 'success'
            result['message'] = message
            
        else:
            raise ValueError(f"Unknown ritual type: {ritual_name}")
            
    except Exception as e:
        result['status'] = 'failed'
        result['error'] = str(e)
    
    return result


def execute_rituals(rituals):
    """
    Execute a list of rituals in sequence.
    Returns list of execution results.
    Stops on first failure.
    """
    results = []
    
    for ritual in rituals:
        result = execute_ritual(ritual)
        results.append(result)
        
        # Stop on failure
        if result['status'] == 'failed':
            break
    
    return results


def create_log_entry(chain_id, proposal, results):
    """
    Create a log entry in the format specified by the v0.0.1 spec.
    """
    # Determine overall status
    overall_status = "complete"
    for result in results:
        if result['status'] == 'failed':
            overall_status = "failed"
            break
    
    # Create the log entry
    log_entry = {
        'chain_id': chain_id,
        'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'status': overall_status,
        'rituals': []
    }
    
    # Add ritual results
    for result in results:
        ritual_log = {
            'name': result['name'],
            'status': result['status']
        }
        
        # Add specific result fields based on ritual type
        if result['status'] == 'success':
            if 'path' in result:
                ritual_log['path'] = result['path']
            if 'bytes_written' in result:
                ritual_log['bytes_written'] = result['bytes_written']
            if 'message' in result:
                ritual_log['message'] = result['message']
        else:
            ritual_log['error'] = result.get('error', 'Unknown error')
        
        log_entry['rituals'].append(ritual_log)
    
    return log_entry


def write_log_entry(log_entry):
    """
    Write a log entry to .ghost/logs/<chain_id>.yaml
    """
    log_file = Path('.ghost/logs') / f"{log_entry['chain_id']}.yaml"
    
    # Convert to YAML format manually (since we're not using yaml library)
    yaml_content = f"""chain_id: {log_entry['chain_id']}
timestamp: {log_entry['timestamp']}
status: {log_entry['status']}
rituals:"""
    
    for ritual in log_entry['rituals']:
        yaml_content += f"\n  - name: {ritual['name']}"
        yaml_content += f"\n    status: {ritual['status']}"
        
        for key, value in ritual.items():
            if key not in ['name', 'status']:
                if isinstance(value, str):
                    yaml_content += f"\n    {key}: \"{value}\""
                else:
                    yaml_content += f"\n    {key}: {value}"
    
    yaml_content += "\n"
    
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    
    return log_file


def archive_processed_file(yaml_file):
    """
    Move processed file to .ghost/archive/
    """
    archive_dir = Path('.ghost/archive')
    archive_path = archive_dir / yaml_file.name
    
    # Move the file
    shutil.move(str(yaml_file), str(archive_path))
    
    return archive_path


def update_context(chain_id, status, results):
    """
    Update .ghost/context/last.yaml with execution summary
    """
    context_file = Path('.ghost/context/last.yaml')
    
    context_data = {
        'last_execution': {
            'chain_id': chain_id,
            'status': status,
            'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'rituals_run': len(results)
        }
    }
    
    # Convert to YAML format manually
    yaml_content = f"""last_execution:
  chain_id: {context_data['last_execution']['chain_id']}
  status: {context_data['last_execution']['status']}
  timestamp: {context_data['last_execution']['timestamp']}
  rituals_run: {context_data['last_execution']['rituals_run']}
"""
    
    with open(context_file, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    
    return context_file


def main():
    """Main entry point for ghostd script."""
    parser = argparse.ArgumentParser(description='ghostd v0.0.1 - Process ritual proposals')
    parser.add_argument('--verbose', '-v', action='store_true', 
                        help='Enable verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        print("ghostd v0.0.1 starting...")
    
    # Validate the directory structure exists
    ghost_dir = Path('.ghost')
    required_dirs = ['output', 'logs', 'context', 'daemon', 'archive']
    
    for dir_name in required_dirs:
        dir_path = ghost_dir / dir_name
        if not dir_path.exists():
            print(f"Error: Required directory {dir_path} does not exist")
            sys.exit(1)
    
    if args.verbose:
        print("Directory structure validated")
    
    # Find and process YAML files
    output_dir = ghost_dir / 'output'
    yaml_files = find_yaml_files(output_dir)
    
    if args.verbose:
        print(f"Found {len(yaml_files)} YAML files to process")
    
    for yaml_file in yaml_files:
        if args.verbose:
            print(f"Processing {yaml_file.name}...")
        
        try:
            proposal = load_ritual_proposal(yaml_file)
            if args.verbose:
                print(f"  Chain ID: {proposal['chain_id']}")
                print(f"  Rituals: {len(proposal['rituals'])}")
            
            # Execute the rituals
            results = execute_rituals(proposal['rituals'])
            
            # Create and write log entry
            log_entry = create_log_entry(proposal['chain_id'], proposal, results)
            log_file = write_log_entry(log_entry)
            
            # Move processed file to archive
            archive_path = archive_processed_file(yaml_file)
            
            # Update context with execution summary
            context_file = update_context(proposal['chain_id'], log_entry['status'], results)
            
            if args.verbose:
                print(f"  Logged to: {log_file}")
                print(f"  Archived to: {archive_path}")
                print(f"  Updated context: {context_file}")
                for i, result in enumerate(results):
                    print(f"    Ritual {i+1} ({result['name']}): {result['status']}")
                    if result['status'] == 'failed':
                        print(f"      Error: {result['error']}")
                
        except Exception as e:
            print(f"Error processing {yaml_file.name}: {e}")
            
            # Still move malformed files to archive so they don't get processed again
            try:
                archive_path = archive_processed_file(yaml_file)
                if args.verbose:
                    print(f"  Moved malformed file to: {archive_path}")
            except Exception as archive_error:
                print(f"  Warning: Could not archive malformed file: {archive_error}")
            
            continue
    
    if args.verbose:
        print("ghostd processing complete")


if __name__ == '__main__':
    main()