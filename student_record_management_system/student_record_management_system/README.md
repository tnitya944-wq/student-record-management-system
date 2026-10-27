# Student Record Management System (Python)

A beginner-friendly command-line project that demonstrates Python functions, parameters, return values, file handling, CSV/JSON, exception handling, and CRUD operations.

## Features
- **Create:** Add a student record.
- **Read:** Display all records or search by student ID.
- **Update:** Edit an existing student's details.
- **Delete:** Remove a record after confirmation.
- Store data in either **CSV** or **JSON** format.
- Validate required fields, age, email, and duplicate student IDs.
- Handle common file and data errors with `try`/`except`.

## Requirements
- Python 3.9 or later
- No third-party packages required

## Run the project
1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run:

   ```bash
   python student_record_management.py
   ```

4. Choose `csv` or `json` when prompted.
5. Use the menu to add, view, search, update, or delete records.

The selected data file (`students.csv` or `students.json`) is created in the same folder when records are saved.

## Concepts demonstrated
- Functions and parameters: `add_student()`, `save_records()`, `validate_student()`
- Return values: `read_records()` returns a list of records.
- Exception handling: `try`/`except` for file errors, invalid JSON, and invalid input.
- File handling: Python `open()` with context managers (`with`).
- CSV: `csv.DictReader` and `csv.DictWriter`
- JSON: `json.load` and `json.dump`
- CRUD: Create, Read, Update, Delete

## Suggested manual test
1. Add a student with ID `101`.
2. View all students and confirm the record appears.
3. Search for ID `101`.
4. Update the student's course.
5. Delete the student and confirm it no longer appears.
6. Try an invalid age, a duplicate ID, and an invalid storage format.

## Repository contents
- `student_record_management.py` — application code
- `README.md` — project guide
- `students.csv` / `students.json` — generated automatically when data is saved
