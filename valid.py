from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import time
import csv

# Set up the Selenium WebDriver (for Chrome, for example)
path = './chromedriver.exe'  # Ensure the path is correct

# Initialize the WebDriver with the Service class
service = Service(path)
driver = webdriver.Chrome(service=service)
# Read the existing CSV file containing course details
input_csv = 'udemy_courses.csv'
output_csv = 'udemy_courses_with_status.csv'

# Open the input CSV file to read data and output CSV to write results
with open(input_csv, mode='r', newline='', encoding='utf-8') as infile, open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    # Read the header of the CSV and add a new column for "Coupon Status"
    header = next(reader)
    writer.writerow(header + ['Coupon Status'])
    
    # Iterate through each row in the CSV containing course data
    for row in reader:
        course_name, course_url, coupon_code = row

        # Open each course link from the CSV URL using Selenium
        try:
            # Navigate to the course URL
            driver.get(course_url)
            time.sleep(3)  # Wait for the page to load

            # Try to locate the price element on the course page
            try:
                price_element = driver.find_element(By.XPATH, "//div[@class='base-price-text-module--price-part---xQlz ud-clp-discount-price ud-heading-xxl']/span/span")
                price_text = price_element.text.strip()

                # Determine if the coupon is valid based on the price text
                if "Free" in price_text:
                    coupon_status = "valid"
                else:
                    coupon_status = "not valid"
            
            except Exception as e:
                # If the price element is not found, mark as not valid
                coupon_status = "not valid"
                print(f"Error finding price for {course_url}: {e}")

        except Exception as e:
            # Handle any errors when opening the course page (e.g., network issues, wrong URL)
            coupon_status = "not valid"
            print(f"Error opening course page {course_url}: {e}")
        
        # Write the row with the coupon status to the new CSV file
        writer.writerow(row + [coupon_status])

        # Sleep to avoid getting blocked by the website
        time.sleep(1)

# Close the browser after processing all courses
driver.quit()

print("Data with coupon status saved to udemy_courses_with_status.csv")
