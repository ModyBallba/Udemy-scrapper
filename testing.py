import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import random
import re
from selenium import webdriver
import time
import logging

# Set up logging to log all transactions
def setup_logging():
    logging.basicConfig(
        filename='transactions.log', 
        level=logging.INFO, 
        format='%(asctime)s - %(message)s', 
        filemode='a'
    )

# Function to read data from the CSV file and choose a random course
def select_random_course():
    try:
        with open('udemy_courses.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            courses = list(reader)
            if courses:
                return random.choice(courses)
            else:
                messagebox.showerror("Error", "No courses found in udemy_courses.csv.")
                return None
    except FileNotFoundError:
        messagebox.showerror("Error", "The file 'udemy_courses.csv' was not found.")
        return None

# Function to save selected course with email to a new CSV file
def save_selection(email, course_name, course_url):
    try:
        with open('audit.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([email, course_name, course_url])  # Save email, course name, and URL
        messagebox.showinfo("Success", f"Course saved for {email}")
        # Log the transaction in the log file
        log_transaction(email, course_name, course_url)
    except Exception as e:
        messagebox.showerror("Error", f"Error saving data: {e}")

# Log the transaction in the log file
def log_transaction(email, course_name, course_url):
    logging.info(f"Email: {email}, Course: {course_name}, URL: {course_url}")

# Function to open the course link using Selenium
def open_course_link(url):
    driver = webdriver.Chrome()  # Ensure ChromeDriver is in your PATH or provide its path here
    driver.get(url)  # Just open the URL without clicking anything
    time.sleep(20)  # Wait for a few seconds to ensure the page loads fully
    
    driver.quit()  # Close the browser after opening the link

# Function to update the combo box with the available course names
def update_combobox():
    try:
        with open('udemy_courses.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            courses = list(reader)
            course_names = [course['Course Name'] for course in courses]
            url_mapping = {course['Course Name']: course['Course URL'] for course in courses}
            url_combobox['values'] = course_names  # Populate the combobox with course names
            if course_names:
                url_combobox.set(course_names[0])  # Set the default value of the combobox
            else:
                messagebox.showerror("Error", "No course names found in udemy_courses.csv.")
            return url_mapping
    except FileNotFoundError:
        messagebox.showerror("Error", "The file 'udemy_courses.csv' was not found.")
        return {}

# Button function to process the email, validate, and open the course link
def process_email():
    email = email_entry.get().strip()
    if not re.match(r'^[\w\.-]+@gmail\.com$', email):
        messagebox.showerror("Invalid Email", "Please enter a valid Gmail address ending with @gmail.com.")
        return
    
    # Save the Gmail address when validated
    global user_email
    user_email = email

    selected_course_name = url_combobox.get()  # Get the selected course name from the combobox
    if not selected_course_name:
        messagebox.showerror("Error", "Please select a valid course.")
        return
    
    # Find the course with the selected name
    course_url = url_mapping.get(selected_course_name)
    if not course_url:
        messagebox.showerror("Error", "Could not find the selected course.")
        return
    
    # Open the course link without clicking anything
    open_course_link(course_url)

    # Save the selected course along with the email and course URL to the CSV file
    save_selection(user_email, selected_course_name, course_url)

# Setting up the Tkinter GUI
root = tk.Tk()
root.title("Udemy Course Selector")
root.geometry("500x350")
root.config(bg="#f0f0f0")  # Light gray background

# Adding a title label with a larger font
title_label = tk.Label(root, text="Udemy Course Selector", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
title_label.pack(pady=20)

# Frame for better layout management
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=20)

# Label and entry for email input with custom styling
email_label = tk.Label(frame, text="Enter your Gmail address:", font=("Helvetica", 12), bg="#f0f0f0")
email_label.grid(row=0, column=0, padx=10, pady=10)

email_entry = tk.Entry(frame, width=30, font=("Helvetica", 12), bd=2)
email_entry.grid(row=0, column=1, padx=10, pady=10)

# Label for combobox
url_label = tk.Label(frame, text="Select a course:", font=("Helvetica", 12), bg="#f0f0f0")
url_label.grid(row=1, column=0, padx=10, pady=10)

# Combobox for selecting a course name
url_combobox = ttk.Combobox(frame, width=30, font=("Helvetica", 12))
url_combobox.grid(row=1, column=1, padx=10, pady=10)

# Button to submit email and select a course with a hover effect
def on_enter(event):
    submit_button.config(bg="#4CAF50")

def on_leave(event):
    submit_button.config(bg="#45a049")

submit_button = tk.Button(root, text="Select Course", font=("Helvetica", 14), bg="#45a049", fg="white", command=process_email, relief="flat", height=2, width=20)
submit_button.pack(pady=20)
submit_button.bind("<Enter>", on_enter)
submit_button.bind("<Leave>", on_leave)

# Footer Label for additional information or instructions
footer_label = tk.Label(root, text="Powered by Udemy Course Selector | Made with Tkinter", font=("Helvetica", 8), bg="#f0f0f0")
footer_label.pack(side="bottom", pady=10)

# Update the combobox with the course names when the program starts
url_mapping = update_combobox()

# Initialize logging at the start
setup_logging()

# Keep the window open until the user manually closes it
root.mainloop()
