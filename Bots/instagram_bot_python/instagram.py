from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import urllib.request

def download_image(url, save_as):
    urllib.request.urlretrieve(url, save_as)



def load_browser(download_path=None, headless=False):
    '''browser load '''
    if not download_path:
        download_path = os.path.join(os.getcwd(), 'temp', 'browser_downloads')
        os.makedirs(download_path, exist_ok=True)

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

            WebDriverWait(self.browser, 30).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 
                "xyi19xy x1ccrb07 xtf3nb5 x1pc53ja x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6")))
            
            followers = self.browser.find_elements(by="class",
                    value="xyi19xy x1ccrb07 xtf3nb5 x1pc53ja x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6")
            print(followers)
            list = []
            number = 0
            for follower in followers:
                number += 1
                print(f"{number}" + " --> " + follower.text)
                list.append(follower.text)
            
            with open("followers.txt", "w", encoding="utf8") as file:
                for follower in list:
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

            Instagram.scrollDown(self)
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
    
    def followUser(self, username): 
        self.browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(4)
                 
        
        try:
            try:
                self.browser.find_element_by_css_selector("._5f5mN.jIbKX._6VtSN.yZn4P").click()
            except:     
                self.browser.find_element_by_css_selector(".sqdOP.L3NKy.y3zKF").click()
            print(f"{username} is following.")
            
        except Exception:
            button = self.browser.find_element_by_css_selector("._5f5mN.-fzfL._6VtSN.yZn4P")
            print(f"Already follow {username}.")

    def unFollowUser(self,username):
        self.browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(4)
         
        try:
            self.browser.find_element_by_css_selector("._5f5mN.jIbKX._6VtSN.yZn4P")
            print(f"You don't already follow {username}.")
        except:
            try:
                self.browser.find_element_by_css_selector("._5f5mN.-fzfL._6VtSN.yZn4P").click()
            except:
                self.browser.find_element_by_css_selector(".qF0y9.Igw0E.IwRSH.eGOV_._4EzTm.soMvl").click()
                   
            unFollow = self.browser.find_element_by_css_selector(".aOOlW.-Cab_")
            time.sleep(3)
            unFollow.click()
            print(f"{username} unfollowed.")

    def whoDontFollowMe(self):
        self.followers = []
        self.following = []
        self.dontfollow = []
        
        with open("followers.txt", "r") as file:
            for i in file:
                self.followers.append(i.strip())
        with open("following.txt", "r") as file2:
            for i in file2:
                self.following.append(i.strip())

        print("Users who do not follow you:".center(25,"*"))
        print()
        for user in self.following:
            if not user in self.followers:
                self.dontfollow.append(user)
                print(user)
                
        result = input("Would you like to unfollow people who don't follow you(all)?(Y/N): ")
        if result == "Y":
            for user in self.dontfollow:
                Instagram.unFollowUser(self,user)
        else:
            print("I haven't unfollowed anyone.")
    
    def whatchStory(self, username):
        time.sleep(2)
        self.browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(2)   

        try:
            self.browser.find_element_by_css_selector("._6q-tv").click()
        except Exception:
            print("Something went wrong.")
    
    def scrollDown(self):
        # Javascript commands

        jsCommand = """
        page = document.querySelector(".isgrP");
        page.scrollTo(0,page.scrollHeight);
        var pageDown = page.scrollHeight;
        return pageDown;
        """
        pageDown = self.browser.execute_script(jsCommand)

        while True:
            end = pageDown
            time.sleep(1)
            pageDown = self.browser.execute_script(jsCommand)
            if end == pageDown:
                break   
    
    def images_load(self, username):
        self.browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(8)

        set_data = set()
        main_count = 0
        i = 0
        while True:
            wait_time = 30
            print('While loop', main_count)
            xpath = "//header/following-sibling::div[2]/div"
            element = WebDriverWait(self.browser, wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            img_element = element.find_elements(By.XPATH, "//img[@style='object-fit: cover;']")
            img_src= [(i.get_attribute("alt"), i.get_attribute("src")) for i in img_element if i.get_attribute("alt")]
            if main_count>=len(img_src):
                break
            download_path = os.path.join(os.getcwd(), 'temp', 'browser_downloads')
            for save_as, image_url in img_src:
                if image_url in set_data:
                    continue
                i+=1
                download_image(image_url, f"{download_path}/{username}_images_{i}.png")
                time.sleep(1)
                set_data.add(image_url)
            main_count += 1
            self.browser.execute_script("window.scrollBy(0,900)")
            time.sleep(3)            
        
        print(img_src)
        # screenshot_path = "page_screenshot.png"
        # driver.save_screenshot(screenshot_path)
        