# Codeforces Spies Report Script Readme

## Overview

This Python script automates the process of fetching Codeforces submissions data for a list of friends, extracting relevant information, and sending a summary report via email. The script utilizes the Selenium library for web scraping, Jinja2 for email templating and Sendgrid for sending emails.

## Workflow

1. **Web Scraping with Selenium:**

   - Configures a headless Chrome browser using Selenium and initiates with configured options.
   - Navigates to each friend's Codeforces profile and fetches their recent correct submissions.

2. **Data Extraction:**

   - Extracts information about submissions made by friends yesterday.
   - Uses Jinja2 templates to format the HTML content of the email body dynamically.

3. **Email Sending:**

   - Uses the Sendgrid API to send emails.
