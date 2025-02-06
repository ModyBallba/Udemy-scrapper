import requests
from bs4 import BeautifulSoup
import re
import csv

# Step 1: Fetch the page content
url = 'https://yofreesamples.com/courses/free-discounted-udemy-courses-list/'
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Open a CSV file to save the extracted data
    with open('udemy_courses.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header row
        writer.writerow(['Course Name', 'Course URL', 'Coupon Code'])
        
        # Step 2: Find all course containers with the specified class
        courses = soup.find_all('h4', class_='wp-block-heading')

        # Step 3: Extract name, URL, and coupon code
        for course in courses:
            # Extract course name
            course_name = course.get_text(strip=True)

            # Extract link
            link_tag = course.find('a', class_='external_link_title')
            if link_tag and 'href' in link_tag.attrs:
                course_url = link_tag['href']

                # Extract coupon code from the URL
                coupon_code_match = re.search(r'couponCode=([A-Z0-9]+)', course_url)
                coupon_code = coupon_code_match.group(1) if coupon_code_match else 'N/A'

                # Write the extracted information to the CSV file
                writer.writerow([course_name, course_url, coupon_code])

    print("Data saved to udemy_courses.csv")
else:
    print(f"Failed to retrieve page. Status code: {response.status_code}")
