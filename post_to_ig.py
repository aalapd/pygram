import os
import traceback
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from datetime import datetime, timedelta
import schedule
import time
import logging
import random

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Instagram credentials
USERNAME = os.getenv('INSTAGRAM_USERNAME')
PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

def exponential_backoff(attempt, max_delay=3600):
    delay = min(30 * (2 ** attempt), max_delay)
    time.sleep(delay + random.uniform(0, 10))

def login_user():
    cl = Client()
    cl.delay_range = [10, 30]  # Increase delay to 10-30 seconds between requests
    
    session_file = "session.json"
    max_attempts = 5
    
    for attempt in range(max_attempts):
        try:
            if os.path.exists(session_file):
                session = cl.load_settings(session_file)
                cl.set_settings(session)
                cl.login(USERNAME, PASSWORD)
                cl.get_timeline_feed()  # Test if session is valid
            else:
                cl.login(USERNAME, PASSWORD)
            
            logger.info("Successfully logged in")
            return cl
        except Exception as e:
            logger.warning(f"Login attempt {attempt + 1} failed: {str(e)}")
            if "Please wait a few minutes before you try again" in str(e):
                exponential_backoff(attempt)
            elif attempt == max_attempts - 1:
                raise Exception("Max login attempts reached")
    
    raise Exception("Couldn't login user")

def post_image(cl, image_path, caption):
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            cl.photo_upload(path=image_path, caption=caption)
            logger.info(f"Posted image: {image_path}")
            return
        except Exception as e:
            logger.error(f"Error uploading image (attempt {attempt + 1}): {str(e)}")
            if "Please wait a few minutes before you try again" in str(e):
                exponential_backoff(attempt)
            elif attempt == max_attempts - 1:
                raise

def generate_daily_schedule(image_folder, start_time):
    images = os.listdir(image_folder)
    schedule_times = []
    
    current_time = start_time
    for _ in images:
        schedule_times.append(current_time.strftime("%H:%M"))
        
        # Add a random interval between 30 minutes to 2 hours for the next post
        interval = random.randint(30, 120)
        current_time += timedelta(minutes=interval)
        
        # If we've passed midnight, break the loop
        if current_time.day != start_time.day:
            break
    
    return schedule_times

def schedule_and_post():
    try:
        cl = login_user()

        image_folder = 'images'
        images = os.listdir(image_folder)

        if images:
            image = images[0]
            caption = os.path.splitext(image)[0] + "\n #midjourney #aiart #promptengineering #chaos #midjourneychaos"
            image_path = os.path.join(image_folder, image)
            post_image(cl, image_path, caption)
            
            os.remove(image_path)
            logger.info(f"Posted and removed image: {image_path}")

            cl.dump_settings("session.json")
            return True
        else:
            logger.info("No images left to post")
            return False

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        traceback.print_exc()
        return False

# Calculate the start time (1 minute from now)
start_time = datetime.now() + timedelta(minutes=1)

# Generate the daily schedule
image_folder = 'images'

# Create the 'images' folder if it doesn't exist
if not os.path.exists(image_folder):
    os.makedirs(image_folder)
    print(f"Created folder: {image_folder}")

# Now proceed with listing images and generating the schedule
images = os.listdir(image_folder)
daily_schedule = generate_daily_schedule(image_folder, start_time)
images_to_post = len(images)

# Schedule the posting function to run at the calculated times
for post_time in daily_schedule:
    schedule.every().day.at(post_time).do(schedule_and_post)

logger.info(f"Scheduled {len(daily_schedule)} posts starting at: {daily_schedule[0]}")
logger.info(f"Full schedule: {', '.join(daily_schedule)}")

# Keep the script running until all images are posted
while images_to_post > 0:
    for job in schedule.jobs:
        if job.should_run:
            if job.run():
                images_to_post -= 1
                logger.info(f"Images left to post: {images_to_post}")
            else:
                logger.info("No more images to post. Exiting.")
                images_to_post = 0
                break
    
    if images_to_post > 0:
        time.sleep(60)  # Check every minute

logger.info("All images have been posted. Script is ending.")