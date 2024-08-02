from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import urllib.request
import copy

def download_image(url, save_as):
    urllib.request.urlretrieve(url, save_as)

import instaloader
# Download the video
def instagram_download_video(post_url, username):
    try:
        video_download_path = os.path.join(os.getcwd(), 'temp', 'video_downloads')
        loader = instaloader.Instaloader(
            download_pictures=False,
            download_video_thumbnails=False,
            save_metadata=False,
            compress_json=False,
            dirname_pattern=video_download_path
        )
        post = instaloader.Post.from_shortcode(loader.context, post_url.split('/')[-2])
        if post.is_video:
            loader.download_post(post, target=username)
            print("Video downloaded successfully.")
        else:
            print("The post is not a video.")
        
    except Exception as e:
        print(f"An error occurred: {e}")


def load_browser(download_path=None,
                 video_download_path=None,
                 headless=False):
    '''browser load '''
    if not download_path:
        download_path = os.path.join(os.getcwd(), 'temp', 'browser_downloads')
        os.makedirs(download_path, exist_ok=True)
    if not video_download_path:
        video_download_path = os.path.join(os.getcwd(), 'temp', 'video_downloads')
        os.makedirs(video_download_path, exist_ok=True)

    options = Options()
    options.add_argument('--disable-infobars')
    options.add_argument('--start-fullscreen')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    if headless:
        options.add_argument("--headless")


    profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
                # Disable Chrome's PDF Viewer
                "download.default_directory": download_path,
                "download.extensions_to_open": "",
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "plugins.always_open_pdf_externally": True
    }
    options.add_experimental_option("prefs", profile)

    driver = webdriver.Chrome(options=options)
    driver.delete_all_cookies()
    return driver
  
class Instagram():
    def __init__(self, username, password):
        self.browser = load_browser()
        self.username = username
        self.password = password

    def signIn(self):
        self.browser.get("https://www.instagram.com/")
        time.sleep(3)

        emailInput = self.browser.find_elements(by='xpath',
                                                value='//*[@name="username"]')
        passwordInput = self.browser.find_elements(by='xpath',
                                            value='//*[@name="password"]')
        print(emailInput)
        emailInput[0].send_keys("" + self.username)
        passwordInput[0].send_keys("" + self.password)
        passwordInput[0].send_keys(Keys.ENTER)
        time.sleep(2)

        try:
            if self.browser.find_element_by_css_selector(".eiCW-"):
                print("Your password incorrect!")
                quit()
        except:
            print("Login successful.")
            
        time.sleep(10)

        

    def getFollowers(self, search_username):
        if not search_username:
            self.browser.get(
                f"https://www.instagram.com/{self.username}")
        else:
            self.browser.get(
                f"https://www.instagram.com/{search_username}")
        time.sleep(5)

        try:

            self.browser.find_elements(by='xpath',
                value="//header/section[3]/ul/li[2]")[0].click()
            time.sleep(5)
            WebDriverWait(self.browser, 30).until(
                EC.element_to_be_clickable((By.XPATH, 
                "//*[@class='x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3']/div//a")))
            
            followers = self.browser.find_elements(by='xpath',
                    value="//*[@class='x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3']/div//a")
            print(followers)
            unique_followers = set()
            number = 0
            for follower in followers:
                username_url = follower.get_attribute('href')
                follower_username = username_url.split('.com/')[1].replace('/','')
                number += 1
                print(f"{number}" + " --> " + follower_username)
                unique_followers.add(follower_username)
            
            with open("followers.txt", "w", encoding="utf8") as file:
                for follower in unique_followers:
                    file.write(f"{follower}\n")
        except Exception as err:
            print(err)
            print("No one is following you.")

    def getFollowing(self):
        self.browser.get(
            f"https://www.instagram.com/{self.username}")
        time.sleep(3)

        try:

            self.browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]").click()   

            following = self.browser.find_elements_by_css_selector(
                        ".FPmhX.notranslate._0imsa")
                
            list = []
            number = 0
            for follow in following:
                number += 1
                print(f"{number}" + " --> " + follow.text)
                list.append(follow.text)
            
            with open("following.txt", "w", encoding="utf8") as file:
                    for follower in list:
                        file.write(f"{follower}\n")
        except Exception:
            print("You aren't following anyone.")
    
    
    def whatchStory(self, username):
        time.sleep(2)
        self.browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(2)   

        try:
            self.browser.find_element_by_css_selector("._6q-tv").click()
        except Exception:
            print("Something went wrong.")
    
    def images_load(self, username):
        print('Start images download', datetime.now())
        self.browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(8)
        post_count = self.browser.find_element(By.XPATH, 
                "//header/section[3]/ul/li[1]/div/span/span").text
        try:
            print(post_count)
            main_post_count = copy.deepcopy(int(post_count.replace(',','')))
        except Exception as err:
            print(err)
            main_post_count = 10        

        set_data = set()
        main_count = 0
        while main_count<=main_post_count:
            try:
                wait_time = 30
                print('While loop', main_count)
                xpath = "//header/following-sibling::div[2]/div"
                element = WebDriverWait(self.browser, wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                img_element = element.find_elements(By.XPATH, "//img[@style='object-fit: cover;']")
                img_src= [(i.get_attribute("alt"), i.get_attribute("src")) for i in img_element if i.get_attribute("alt")]
                print("--len of elements", len(img_src))
                download_path = os.path.join(os.getcwd(), 'temp', 'browser_downloads')
                for save_as, image_url in img_src:
                    if image_url in set_data:
                        continue
                    cn = len(os.listdir(download_path)) + 1
                    download_image(image_url, f"{download_path}/{username}_images_{cn}.png")
                    time.sleep(1)
                    set_data.add(image_url)
                print('----main_count----', main_count)
                print('----file count----', len(os.listdir(download_path)))
                main_count = max(len(os.listdir(download_path)), main_count+10)
                self.browser.execute_script("window.scrollBy(0,900)")
                self.browser.execute_script("window.scrollBy(0,900)")
                time.sleep(1)
                self.browser.execute_script("window.scrollBy(0,900)")
                time.sleep(1)
                print(main_count<=main_post_count, main_post_count, post_count)
            except Exception as err:
                print(err)            
        
        print('End images download', datetime.now())
        # screenshot_path = "page_screenshot.png"
        # driver.save_screenshot(screenshot_path)

    def reels_load(self, username):
        print('Start Reels download', datetime.now())
        self.browser.get(f"https://www.instagram.com/{username}/reels/")
        time.sleep(8)
        post_count = self.browser.find_element(By.XPATH, 
                "//header/section[3]/ul/li[1]/div/span/span").text
        try:
            print(post_count)
            main_post_count = copy.deepcopy(int(post_count.replace(',','')))
        except Exception as err:
            print(err)
            main_post_count = 10
                
        set_data = set()
        main_count = 0
        while main_count<=main_post_count:
            try:
                wait_time = 30
                print('While loop', main_count)
                xpath = "//header/following-sibling::div[2]/div"
                element = WebDriverWait(self.browser, wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                video_element = element.find_elements(By.XPATH, "//a[@class='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd']")
                video_src= [i.get_attribute("href") for i in video_element[1:]]
                print("--len of elements", len(video_src))
                video_download_path = os.path.join(os.getcwd(), 'temp', 'video_downloads')
                for video_url in video_src:
                    if video_url in set_data:
                        continue
                    instagram_download_video(
                        post_url=video_url, username=username)
                    time.sleep(1)
                    set_data.add(video_url)
                print('----main_count----', main_count)
                print('----file count----', len(os.listdir(video_download_path)))
                main_count = max(len(os.listdir(video_download_path)), main_count+10)
                self.browser.execute_script("window.scrollBy(0,900)")
                self.browser.execute_script("window.scrollBy(0,900)")
                time.sleep(1)
                self.browser.execute_script("window.scrollBy(0,900)")
                time.sleep(1)
                print(main_count<=main_post_count, main_post_count, post_count)
            except Exception as err:
                print(err) 
                time.sleep(2)      
                     
        video_download_path = os.path.join(os.getcwd(), 'temp', 'video_downloads')
        test = os.listdir(video_download_path)
        for item in test:
            if item.endswith(".txt"):
                os.remove( os.path.join(video_download_path, item))
        print('End Videos download', datetime.now())
        # screenshot_path = "page_screenshot.png"
        # driver.save_screenshot(screenshot_path)        