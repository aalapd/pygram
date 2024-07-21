# Instagram Scheduled Poster

## Overview
This Python script automates the process of posting images to Instagram on a scheduled basis. It's designed to mimic human behavior by posting images at random times throughout the day, with built-in safeguards against rate limiting and session management.

## Features
- Automatic login and session management
- Random daily scheduling of posts
- Exponential backoff for rate limit handling
- Image posting with captions
- Automatic removal of posted images
- Comprehensive logging

## Usage
- Create a folder called 'images' in the same directory as the script.
- Run the script with:
`python ./post_to_ig.py`

The script will generate a daily schedule for all images in the 'images' folder and post them at random times. It will continue running until all images have been posted.

## Notes
- This script is intended for personal use and should be used responsibly and in compliance with Instagram's terms of service.
- Excessive automated posting may lead to account restrictions or bans.

## Disclaimer
Use this script at your own risk. I will not be responsible for any consequences resulting from the use of this script.
