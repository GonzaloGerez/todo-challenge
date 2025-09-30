#!/usr/bin/env python
"""
Script to run tests with different configurations.
"""
import os
import sys
import subprocess
import argparse


def run_command(command, description):
    """Run a command and print the result."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print("STDOUT:")
        print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    print(f"Exit code: {result.returncode}")
    return result.returncode == 0


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Run tests with different configurations')
    parser.add_argument('--unit', action='store_true', help='Run only unit tests')
    parser.add_argument('--integration', action='store_true', help='Run only integration tests')
    parser.add_argument('--coverage', action='store_true', help='Run tests with coverage report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--parallel', '-n', type=int, help='Number of parallel workers')
    parser.add_argument('--pattern', '-k', help='Test pattern to match')
    
    args = parser.parse_args()
    
    # Base pytest command
    cmd_parts = ['python', '-m', 'pytest']
    
    # Add verbosity
    if args.verbose:
        cmd_parts.append('-v')
    
    # Add parallel execution
    if args.parallel:
        cmd_parts.extend(['-n', str(args.parallel)])
    
    # Add coverage
    if args.coverage:
        cmd_parts.extend(['--cov=src', '--cov-report=html', '--cov-report=term'])
    
    # Add test pattern
    if args.pattern:
        cmd_parts.extend(['-k', args.pattern])
    
    # Add test type filters
    if args.unit:
        cmd_parts.extend(['-m', 'unit'])
    elif args.integration:
        cmd_parts.extend(['-m', 'integration'])
    
    # Add test directory
    cmd_parts.append('tests/')
    
    command = ' '.join(cmd_parts)
    
    print("Test Runner")
    print("=" * 60)
    print(f"Command: {command}")
    print("=" * 60)
    
    success = run_command(command, "Running tests")
    
    if args.coverage and success:
        print(f"\nCoverage report generated in: htmlcov/index.html")
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
