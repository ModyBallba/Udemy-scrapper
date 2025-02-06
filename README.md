# README

## Overview

This project consists of three Python scripts that work together to extract, validate, and manage course registration data. The system allows users to extract data, validate it, and register for courses through a graphical user interface (GUI). All actions are logged, and user registrations are stored in a structured format.
All screeshots were observed in the PDF 

---

## Files

1. **`main.py`**:  
   This script extracts data and saves it into a `.csv` file.

2. **`valid.py`**:  
   This script validates the extracted data and outputs it into a new file.  
   *Note: This file is not required for the current task.*

3. **`testing.py`**:  
   This script is the core of the new task. It:
   - Opens the `.csv` file created by `main.py`.
   - Provides a GUI for users to select courses and register with their email.
   - Saves the course and email data into a new `.csv` file named `audit.csv`.
   - Logs all transactions in a `transactions.log` file.

---

## How It Works

### Step 1: Data Extraction (`main.py`)
- The `main.py` script extracts data from a source and saves it into a `.csv` file.
- This file serves as the input for the next steps.

### Step 2: Data Validation (`valid.py`)
- The `valid.py` script checks the extracted data for errors or inconsistencies.
- It outputs the validated data into a new file.  
  *Note: This step is optional and not required for the current task.*

### Step 3: Course Registration (`testing.py`)
- The `testing.py` script opens the `.csv` file created by `main.py`.
- It provides a GUI where users can:
  - Select a course from the available options.
  - Register for the course using their email.
- The script saves the course and email data into a new `.csv` file named `audit.csv`.
- All transactions are logged in a `transactions.log` file for tracking purposes.

---

## Prerequisites

- Python 3.x
- Required Python libraries:
  - `pandas` (for handling `.csv` files)
  - `tkinter` (for the GUI)

Install the required libraries using pip:
```bash
pip install pandas
