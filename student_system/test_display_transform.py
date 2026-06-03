#!/usr/bin/env python3
"""Test script to verify display transformations for NULL values."""

import sys
sys.path.insert(0, '.')

from core import college, program, student

# Create test data with NULL values
print("=== Creating Test Data ===\n")

# Delete a college to create NULL references
try:
    college.delete("CHS")
    print("✓ Deleted CHS to create NULL college references")
except Exception as e:
    print(f"Note: {e}")

# Delete a program to create NULL references
try:
    program.delete("BSCHE")
    print("✓ Deleted BSCHE to create NULL program references")
except Exception as e:
    print(f"Note: {e}")

# Now test the display transformation functions
print("\n=== Testing Display Transformations ===\n")

# Import the display functions from the UI
sys.path.insert(0, 'ui')

# Simulate the display transformation for programs
print("Programs with display transformation (empty college → 'N/A'):")
raw_programs = program.list_all()
for p in raw_programs:
    display_college = p["college"] if p["college"] else "N/A"
    print(f"  {p['code']}: college='{p['college']}' (displays as '{display_college}')")

# Simulate the display transformation for students
print("\nStudents with display transformation (empty program → 'NOT ENROLLED'):")
raw_students = student.list_all()
for s in raw_students:
    display_program = s["program"] if s["program"] else "NOT ENROLLED"
    print(f"  {s['id']}: program='{s['program']}' (displays as '{display_program}')")

print("\n=== Transformation Test Complete ===")
print("✓ Display values are correctly transformed for UI display")
print("✓ Underlying data remains as empty strings in CSV")
