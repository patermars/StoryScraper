"""
MIT License

Copyright (c) 2024 Aryan Kumar Sinha

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import time
import logging
from datetime import datetime
from playwright.sync_api import sync_playwright

# Configure logging to save information and errors to a file
logging.basicConfig(filename='story_downloader.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_stories_for_all_users(page, user_list):
    """
    Download stories for all users in the given list.
    
    Args:
    page (Page): The Playwright page object.
    user_list (list): List of Instagram usernames.
    """
    for user in user_list:
        get_to_download_page(page, user)

def get_to_download_page(page, username):
    """
    Navigate to the story download page for a specific user and initiate the download process.
    
    Args:
    page (Page): The Playwright page object.
    username (str): The Instagram username to download stories from.
    """
    # Navigate to Igram Instagram Story Downloader page
    igram_url = f"https://igram.world/story-saver"
    page.goto(igram_url)

    # Wait for the page to load
    page.wait_for_timeout(5000)  # Wait for 5 seconds

    # Perform necessary actions to search for the user and access their stories
    page.fill('#search-form-input', username)
    page.wait_for_timeout(500)
    page.click('button.search-form__button[type="submit"]')
    page.wait_for_timeout(500)
    page.click('button.modal__btn[data-micromodal-close]')
    page.wait_for_timeout(5000)
    page.click('ul.tabs-component li.tabs-component__item:has(button:has-text("stories")) button.tabs-component__button')

    # Download the stories
    download_stories(page, username)

def download_stories(page, username):
    """
    Download all available stories for a given user.
    
    Args:
    page (Page): The Playwright page object.
    username (str): The Instagram username of the story owner.
    """
    try:
        # Select all download buttons within the list
        page.wait_for_selector('a.button.button--filled.button__download')
        download_buttons = page.query_selector_all('a.button.button--filled.button__download')
        
        # Create a directory for today's downloads
        today = datetime.now().strftime('%Y-%m-%d')
        user_dir = os.path.join(today, username)
        os.makedirs(user_dir, exist_ok=True)
        
        # Download each story
        for i, button in enumerate(download_buttons, start=1):
            with page.expect_download() as download_info:
                button.click()
                page.wait_for_selector('button.modal__btn[data-micromodal-close]')
                page.click('button.modal__btn[data-micromodal-close]')
            
            page.wait_for_timeout(1000)
            
            download = download_info.value
            
            # Save the downloaded file to the appropriate directory
            download.save_as(f"{user_dir}/{i}_{download.suggested_filename}")
            
            logging.info(f"Successfully downloaded story {i} for user {username}. File saved to {user_dir}")
    
    except Exception as e:
        logging.error(f"An error occurred while downloading stories for user {username}: {e}")

def main(usernames_list, interval_hours):
    """
    Main function to run the story downloader at specified intervals.
    
    Args:
    usernames_list (list): List of Instagram usernames to download stories from.
    interval_hours (int): Number of hours to wait between download sessions.
    """
    while True:
        with sync_playwright() as p:
            # Launch a new browser instance
            browser = p.chromium.launch(headless=False)  # Set headless=True for headless mode
            page = browser.new_page()

            logging.info("Starting scheduled download...")
            download_stories_for_all_users(page, usernames_list)
            browser.close()
            logging.info(f"Download complete. Waiting for next interval ({interval_hours} hours)...")

            # If interval is 0, run only once and exit
            if interval_hours == 0:
                break

            # Wait for the specified interval before the next download session
            time.sleep(interval_hours * 3600)  # Sleep for the specified interval in hours

if __name__ == "__main__":
	"""
	Useful when testing and don't wanna run the gui, quick and easy way.
	"""
    # Read usernames from a file
    with open('usernames.txt', 'r') as file:
        usernames_list = [line.strip() for line in file]

    # Start the main download process
    main(usernames_list, 0)
