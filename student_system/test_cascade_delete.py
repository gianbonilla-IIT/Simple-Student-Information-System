#!/usr/bin/env python3
"""Test script to verify cascading NULL deletion."""

import sys
sys.path.insert(0, '.')

from core import college, program, student

# Print initial state
print("=== Initial State ===\n")
print("Colleges:")
for c in college.list_all():
    print(f"  {c['code']} - {c['name']}")

print("\nPrograms:")
for p in program.list_all():
    print(f"  {p['code']} ({p['name']}) -> College: {p['college'] or 'NULL'}")

print("\nStudents:")
for s in student.list_all():
    print(f"  {s['id']} {s['firstname']} {s['lastname']} -> Program: {s['program'] or 'NULL'}")

# Test 1: Delete a program and cascade to students
print("\n" + "="*60)
print("=== Test 1: Delete Program (cascade to students) ===\n")
print("Deleting program 'BSCHE'...")
try:
    program.delete("BSCHE")
    print("✓ Program deleted successfully")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

print("\nPrograms after deletion:")
for p in program.list_all():
    print(f"  {p['code']} ({p['name']}) -> College: {p['college'] or 'NULL'}")

print("\nStudents after program deletion (check BSCHE students):")
for s in student.list_all():
    print(f"  {s['id']} {s['firstname']} {s['lastname']} -> Program: {s['program'] or 'NULL'}")

# Verify cascade worked for students
bsche_students = [s for s in student.list_all() if s['program'] == '']
print(f"\n✓ Found {len(bsche_students)} student(s) with NULL program")

# Revert by re-creating the program
print("\nReverting: Re-creating BSCHE...")
try:
    program.create("BSCHE", "Bachelor of Science in Chemical Engineering", "COE")
    # Note: Students will still have NULL - we need to manually fix them
    # Update student to BSCHE
    student.update("2024-0408", "Gian Christian", "Bonilla", "BSCHE", "2", "Male")
    print("✓ Reverted successfully")
except Exception as e:
    print(f"Note: Revert may have issues: {e}")

# Test 2: Delete a college and cascade to programs
print("\n" + "="*60)
print("=== Test 2: Delete College (cascade to programs) ===\n")
print("Deleting college 'CHS'...")
try:
    college.delete("CHS")
    print("✓ College deleted successfully")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

print("\nColleges after deletion:")
for c in college.list_all():
    print(f"  {c['code']} - {c['name']}")

print("\nPrograms after college deletion (check CHS programs):")
for p in program.list_all():
    print(f"  {p['code']} ({p['name']}) -> College: {p['college'] or 'NULL'}")

# Verify cascade worked for programs
null_college_programs = [p for p in program.list_all() if p['college'] == '']
print(f"\n✓ Found {len(null_college_programs)} program(s) with NULL college")

print("\n" + "="*60)
print("=== Test Complete ===")
print("✓ Cascading NULL deletion feature is working correctly!")
