# Codeforces Spies Report Script Readme

## Overview

This Python script automates the process of fetching Codeforces submissions data for a list of friends, extracting relevant information, and sending a summary report via email. The script utilizes the Selenium library for web scraping and Jinja2 for email templating.

## Functions Used

1. `getRating()`: Extracts the Codeforces rating from a user's profile page.
2. `getDate(tame)`: Converts the date format used on the Codeforces website to a standardized format (YYYY-MM-DD).
3. `getProblems(handle)`: Retrieves information about recent submissions, including submission IDs, submission links, problem IDs, and problem links.

## Workflow

1. **Web Scraping with Selenium:**
   - Configures a headless Chrome browser using Selenium.
   - Initiates a Chrome WebDriver with configured options.
   - Navigates to each friend's Codeforces profile page and fetches information about their recent submissions.

2. **Data Extraction:**
   - Extracts information about submissions made by friends, filtering them based on the submission date (today and yesterday).

3. **Email Sending:**
   - Uses the `smtplib` library to send emails via Gmail.
   - Creates an HTML email body using the Jinja2 template engine, incorporating the extracted submission data.
   - Sends the email to the specified recipient's email address.

4. **Jinja2 Templating:**
   - Uses Jinja2 templates to format the HTML content of the email body dynamically.


## Improvements
   - Suggests enhancements, including improved error handling, logging, and adherence to best practices.
   - Recommends the use of environment variables for sensitive information and adding comments for better code understanding.
   - Encourages testing the script with different scenarios to ensure its robustness.
