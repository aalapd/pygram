import os
import traceback
from instagrapi import Client

# Log in to Instagram using environment variables
USERNAME = os.getenv('INSTAGRAM_USERNAME')
PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

try:
    cl = Client()
    cl.login(username=USERNAME, password=PASSWORD)

    # Path to the folder containing images
    image_folder = 'images'

    # Get the list of images
    images = os.listdir(image_folder)

    # Function to post an image
    def post_image(image_path, caption):
        try:
            cl.photo_upload(path=image_path, caption=caption)
        except Exception as e:
            print(f"Error uploading image: {str(e)}")
            traceback.print_exc()

    # Post the first image with its filename as the caption
    if images:
        test_image = images[0]
        caption = os.path.splitext(test_image)[0] + "#midjourney #aiart #promptengineering #chaos #midjourneychaos"
        post_image(os.path.join(image_folder, test_image), caption)
except Exception as e:
    print(f"An error occurred: {str(e)}")
    traceback.print_exc()
finally:
    # Log out
    cl.logout()