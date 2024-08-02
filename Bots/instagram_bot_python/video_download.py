from instaloader import Instaloader, Profile
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from instagram import load_browser, Instagram
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def download_video(username):
    L = Instaloader(download_pictures=False)
    PROFILE = username
    profile = Profile.from_username(L.context, PROFILE)

    posts_sorted_by_likes = sorted(profile.get_posts(), key=lambda post: post.likes,reverse=True)

    for post in posts_sorted_by_likes:
        if post.is_video:
            L.download_post(post, PROFILE)
        
