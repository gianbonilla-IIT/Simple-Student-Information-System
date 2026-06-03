#!/usr/bin/env python3
"""Test display transformations with actual NULL values."""

import sys
sys.path.insert(0, '.')

from core import college, program

# Delete a college that has programs
try:
    college.delete('COE')
    print('✓ Deleted COE')
except Exception as e:
    print(f'Error: {e}')

# Check programs with NULL college
programs = program.list_all()
null_programs = [p for p in programs if not p['college']]
print(f'\nPrograms with NULL college:')
for p in null_programs:
    print(f'  {p["code"]}: college="{p["college"]}" (UI displays as "N/A")')

# Show all programs with transformation
print(f'\nAll programs (with display transformation):')
for p in programs:
    display_college = p["college"] if p["college"] else "N/A"
    print(f'  {p["code"]}: college="{p["college"]}" → displays as "{display_college}"')

# Revert
try:
    college.create('COE', 'College of Engineering')
    program.update('BSCHE', 'BSCHE', 'Bachelor of Science in Chemical Engineering', 'COE')
    program.update('BSMINING', 'BSMINING', 'Bachelor of Science in Mining Engineering', 'COE')
    print('\n✓ Reverted changes')
except Exception as e:
    print(f'Revert error: {e}')
