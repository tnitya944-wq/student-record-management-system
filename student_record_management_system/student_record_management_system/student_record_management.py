import csv
import json
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent
CSV_FILE = DATA_DIR / "students.csv"
JSON_FILE = DATA_DIR / "students.json"
FIELDS = ["student_id", "name", "age", "course", "email"]


def read_records(file_format="csv"):
    """Load student records from CSV or JSON."""
    try:
        if file_format == "csv":
            if not CSV_FILE.exists():
                return []
            with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
                return list(csv.DictReader(file))
        elif file_format == "json":
            if not JSON_FILE.exists():
                return []
            with open(JSON_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                if not isinstance(data, list):
                    raise ValueError("JSON data must be a list of student records.")
                return data
        else:
            raise ValueError("Unsupported format. Choose 'csv' or 'json'.")
    except (OSError, json.JSONDecodeError, csv.Error, ValueError) as error:
        print(f"Could not read records: {error}")
        return []


def save_records(records, file_format="csv"):
    """Save all records to CSV or JSON."""
    try:
        if file_format == "csv":
            with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(records)
        elif file_format == "json":
            with open(JSON_FILE, "w", encoding="utf-8") as file:
                json.dump(records, file, indent=4)
        else:
            raise ValueError("Unsupported format. Choose 'csv' or 'json'.")
    except (OSError, csv.Error, TypeError, ValueError) as error:
        print(f"Could not save records: {error}")


def validate_student(student_id, name, age, course, email, records, editing_id=None):
    """Validate input and prevent duplicate IDs."""
    if not all(value.strip() for value in [student_id, name, age, course, email]):
        raise ValueError("All fields are required.")
    if not age.isdigit() or not 1 <= int(age) <= 120:
        raise ValueError("Age must be a number between 1 and 120.")
    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValueError("Enter a valid email address.")
    if any(
        str(record["student_id"]) == student_id and student_id != editing_id
        for record in records
    ):
        raise ValueError("A student with this ID already exists.")


def add_student(file_format):
    records = read_records(file_format)
    try:
        student = {
            "student_id": input("Student ID: ").strip(),
            "name": input("Full name: ").strip(),
            "age": input("Age: ").strip(),
            "course": input("Course/branch: ").strip(),
            "email": input("Email: ").strip(),
        }
        validate_student(**student, records=records)
        student["age"] = str(int(student["age"]))
        records.append(student)
        save_records(records, file_format)
        print("Student added successfully.")
    except ValueError as error:
        print(f"Invalid input: {error}")


def list_students(file_format):
    records = read_records(file_format)
    if not records:
        print("No student records found.")
        return
    print("\nSTUDENT RECORDS")
    print("-" * 82)
    print(f"{'ID':<12}{'Name':<22}{'Age':<8}{'Course':<18}{'Email'}")
    print("-" * 82)
    for student in records:
        print(
            f"{student.get('student_id', ''):<12}"
            f"{student.get('name', ''):<22}"
            f"{student.get('age', ''):<8}"
            f"{student.get('course', ''):<18}"
            f"{student.get('email', '')}"
        )


def search_student(file_format):
    records = read_records(file_format)
    search_id = input("Enter student ID to search: ").strip()
    student = next(
        (record for record in records if str(record.get("student_id")) == search_id),
        None,
    )
    if student:
        for key, value in student.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
    else:
        print("Student not found.")


def update_student(file_format):
    records = read_records(file_format)
    student_id = input("Enter ID of student to update: ").strip()
    student = next(
        (record for record in records if str(record.get("student_id")) == student_id),
        None,
    )
    if not student:
        print("Student not found.")
        return

    print("Press Enter to keep the current value.")
    try:
        name = input(f"Name [{student['name']}]: ").strip() or student["name"]
        age = input(f"Age [{student['age']}]: ").strip() or student["age"]
        course = input(f"Course [{student['course']}]: ").strip() or student["course"]
        email = input(f"Email [{student['email']}]: ").strip() or student["email"]
        validate_student(student_id, name, age, course, email, records, editing_id=student_id)
        student.update({
            "name": name,
            "age": str(int(age)),
            "course": course,
            "email": email,
        })
        save_records(records, file_format)
        print("Student updated successfully.")
    except ValueError as error:
        print(f"Invalid input: {error}")


def delete_student(file_format):
    records = read_records(file_format)
    student_id = input("Enter ID of student to delete: ").strip()
    student = next(
        (record for record in records if str(record.get("student_id")) == student_id),
        None,
    )
    if not student:
        print("Student not found.")
        return
    confirmation = input(f"Delete {student['name']}? (y/n): ").strip().lower()
    if confirmation == "y":
        records.remove(student)
        save_records(records, file_format)
        print("Student deleted successfully.")
    else:
        print("Deletion cancelled.")


def choose_format():
    while True:
        file_format = input("Storage format (csv/json): ").strip().lower()
        if file_format in ("csv", "json"):
            return file_format
        print("Please enter either 'csv' or 'json'.")


def main():
    print("=== Student Record Management System ===")
    file_format = choose_format()

    actions = {
        "1": ("Add student", lambda: add_student(file_format)),
        "2": ("View all students", lambda: list_students(file_format)),
        "3": ("Search student", lambda: search_student(file_format)),
        "4": ("Update student", lambda: update_student(file_format)),
        "5": ("Delete student", lambda: delete_student(file_format)),
    }

    while True:
        print("\n1. Add student\n2. View all students\n3. Search student")
        print("4. Update student\n5. Delete student\n6. Change storage format\n0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        elif choice == "6":
            file_format = choose_format()
            # Rebuild actions so they use the newly selected format.
            actions = {
                "1": ("Add student", lambda: add_student(file_format)),
                "2": ("View all students", lambda: list_students(file_format)),
                "3": ("Search student", lambda: search_student(file_format)),
                "4": ("Update student", lambda: update_student(file_format)),
                "5": ("Delete student", lambda: delete_student(file_format)),
            }
        elif choice in actions:
            actions[choice][1]()
        else:
            print("Invalid choice. Select 0–6.")


if __name__ == "__main__":
    main()
