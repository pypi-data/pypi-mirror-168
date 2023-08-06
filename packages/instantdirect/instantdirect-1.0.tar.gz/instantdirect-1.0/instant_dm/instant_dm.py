import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException,ElementClickInterceptedException,ElementNotInteractableException,StaleElementReferenceException,NoSuchElementException
import time
import random
import datetime
import colorama
import threading
from termcolor import colored
import asyncio
import pyperclip
import getpass
import pickle
from cryptography import fernet
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import sys
import platform
from tinydb import TinyDB, Query,where

user=getpass.getuser()

account_creds = fr'C:\Users\{user}\instagram_database'

if not os.path.exists(account_creds):
    os.mkdir(account_creds)


full_cred_path=os.path.join(account_creds,'instagram_db.json')

db = TinyDB(full_cred_path)
User = Query()

colorama.init()

encryption_key = b'aJMvlGq62kjpx8o1tNwIRxW4CMqWBuvWyFZsa4XBzNU='


print(colored(f"[  {datetime.datetime.now()}  ] your instagram credentials along with database are located at {full_cred_path}","green"))


class Scraper:
    def __init__(self,window,target_user,user_count,shared_post,message_path,logout=False):

        full_msg_path=os.path.join(message_path,"message.txt")
        with open(full_msg_path,"r",encoding="utf-8") as message:

            self.message=message.read()

        self.shared_post=shared_post

        self.target_user=target_user
        self.user_count=user_count

        self.logout=logout
        self.scraped_users=[]

        self.exit_program = False

        self.block_thread = False

        self.save_login_credentials()

        self.liked_today = 0
        self.comment_today = 0
        self.now = datetime.datetime.today()

        self.tasks=0

        self.main_tasks=0

        if window=="Y":
            self.stealth=False
        else:
            self.stealth = True

        self.seconds=time.perf_counter()
        self.sleep_=3
        self.status="Starting bot"

        self.options = webdriver.ChromeOptions()
        os_detected=""
        if platform.system() == "Darwin":
            chrome_data=fr"Users/{getpass.getuser()}/Library/Application Support/Google/Chrome/Default"
            os_detected="MAC OS"

        if platform.system()=="Windows":
            chrome_data=fr"C:\Users\{getpass.getuser()}\AppData\Local\Google\Chrome\User Data\Default"

            os_detected="WINDOWS OS"
        if platform.system()=="Linux":
            chrome_data =fr"/home/{getpass.getuser()}/.config/google-chrome/default"
            os_detected="LINUX OS"

        if not os_detected:
            print("Can't detect your operating system")

        else:
            print(colored(f"\n[{datetime.datetime.now()}] {os_detected} Detected ","green"))
            self.options.add_argument(fr"--user-data-dir={chrome_data}")

        self.options.add_argument("--lang=en_US")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation","enable-logging"])

        self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_argument("disable-infobars")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--start-maximized")

        prefs = {"credentials_enable_service": False,
                 "profile.password_manager_enabled": False,
                 "profile.default_content_setting_values.notifications": 2}

        self.options.add_experimental_option("prefs", prefs)

        if self.stealth:
            print(colored("\nbrowser window mode disabled", "green"))
            # self.options.add_argument(
            #     'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36')
            self.options.add_argument("--headless")
        else:
            print(colored("\nbrowser window mode is enabled", "red"))

        chrome_service=Service(ChromeDriverManager().install())

        self.driver = webdriver.Chrome(service=chrome_service, options=self.options)

        self.driver.set_window_size(900,700)

        self.action = ActionChains(self.driver)

        def login_thread():
            asyncio.run(self.main_login())

        th=threading.Thread(target=login_thread)
        th.start()
        while True:
            #  check if login thread is running

            if not th.is_alive():
                if self.logout:
                    break
                else:
                    self.block_thread = False
                    asyncio.run(self.main())
                    break

    def save_login_credentials(self):
        encrypt_creds = fernet.Fernet(encryption_key)
        # db.update({"credentials": "true", "username": "jack", "password": "mypassword"})
        # db.insert({"credentials":"true","username":"jack","password":"mypassword"})
        # deleting user from db
        #db.remove(where('username') == 'jack')

        credentials=db.search(User.credentials == 'true')
        if credentials:
            # print(credentials)
            decrypt_credentials=credentials[0].get("encrypted").encode()

            decrypt_cryptography = encrypt_creds.decrypt(decrypt_credentials)
            decrypt_pickle2 = pickle.loads(decrypt_cryptography)
            self.username = decrypt_pickle2.get("username", "specify a username")
            self.password = decrypt_pickle2.get("password", "specify a password")

        else:
            print(colored(f"[{time.perf_counter()}] no logged in users found in database", "green"))
            print(colored(f"[{time.perf_counter()}] !password may not show on console as you type,hit Enter when done "
                          f"for each field", "cyan"), end="\n")

            self.username = input("Enter your username: ")
            self.password = getpass.getpass("Enter your password: ")

            credentials = {"username": self.username, "password": self.password}
            pickled_credentials = pickle.dumps(credentials)
            encrypted = encrypt_creds.encrypt(pickled_credentials)
            db.insert({"encrypted":encrypted.decode("utf-8"),"credentials":"true"})

    async def login(self,username,password):
        try:
            self.driver.get("https://www.instagram.com/")

            self.sleep_ = random.randrange(1,4)
            self.seconds = time.perf_counter()
            self.status = "Getting instagram login page"

            await asyncio.sleep(self.sleep_)

            username_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
            self.sleep_ = random.randrange(1,5)
            self.seconds = time.perf_counter()
            self.status = "Sending username to login page"
            await asyncio.sleep(self.sleep_)
            username_field.send_keys(username)

            password_field = WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.NAME, "password")))
            self.sleep_ = random.randrange(1, 5)
            self.seconds = time.perf_counter()
            self.status = "Sending password to login page"
            await asyncio.sleep(self.sleep_)
            password_field.send_keys(password)

            login_button = WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(),'Log In')]")))
            self.sleep_ = random.randrange(1, 5)
            self.seconds = time.perf_counter()
            self.status = "Logging in"
            await asyncio.sleep(self.sleep_)
            login_button.click()

            try:
                WebDriverWait(self.driver,5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'check your username')]")))

                print(colored(f"\n\nThe username you entered doesn't belong to an account. Please check your username and try again","red"))

                db.remove(where('credentials') == 'true')

            except (TimeoutException, ElementClickInterceptedException, ElementNotInteractableException,
                    StaleElementReferenceException, NoSuchElementException) as e:
                pass

            try:
                WebDriverWait(self.driver,5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'password was incorrect')]")))

                print(colored(f"\n\n your password was incorrect. Please double-check your password.","red"))
                db.remove(where('credentials') == 'true')

            except (TimeoutException, ElementClickInterceptedException, ElementNotInteractableException,
                    StaleElementReferenceException, NoSuchElementException) as e:
                pass

            await self.click_save_creds()

        except (TimeoutException, ElementClickInterceptedException, ElementNotInteractableException,
                StaleElementReferenceException, NoSuchElementException) as e:
            pass

        if self.logout:
            await self.logout_my_account()
            self.driver.quit()
            self.exit_program=True
        else:
            await self.my_account()

            self.block_thread=True

    async def click_save_creds(self):

        save_button = WebDriverWait(self.driver, 200).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Not Now')]")))
        self.sleep_ = random.randrange(1, 5)
        self.seconds = time.perf_counter()
        self.status = "Getting pop up window"
        await asyncio.sleep(self.sleep_)
        save_button.click()
        #
        # try:
        #
        #     floating_win = WebDriverWait(self.driver,50).until(
        #         EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Cancel')]")))
        #     self.sleep_ = random.randrange(1, 5)
        #     self.seconds = time.perf_counter()
        #     self.status = "clicked cancel popup window"
        #     await asyncio.sleep(self.sleep_)
        #     floating_win.click()
        #
        # except (TimeoutException, ElementClickInterceptedException, ElementNotInteractableException,
        #         StaleElementReferenceException, NoSuchElementException) as e:
        #
        #     self.sleep_ = random.randrange(1, 5)
        #     self.seconds = time.perf_counter()
        #     self.status = f"{e}"
        #     await asyncio.sleep(self.sleep_)

    async def logout_my_account(self):
        account_tag = "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]"
        account = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.XPATH, account_tag)))
        self.sleep_ = random.randrange(1, 5)
        self.seconds = time.perf_counter()
        self.status = f"Getting my account ( {self.username} ) info"
        await asyncio.sleep(self.sleep_)
        account.click()

        account_profile = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Log Out')]")))
        self.sleep_ = random.randrange(2, 7)
        self.seconds = time.perf_counter()
        self.status = f"Logging out of {self.username}"
        await asyncio.sleep(self.sleep_)
        account_profile.click()

    async def my_account(self):
        account_tag="/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]"
        account = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.XPATH,account_tag)))
        self.sleep_ = random.randrange(1, 5)
        self.seconds = time.perf_counter()
        self.status = f"Getting my account ( {self.username} ) info"
        await asyncio.sleep(self.sleep_)
        account.click()

        account_profile = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Profile')]")))
        self.sleep_ = random.randrange(2,7)
        self.seconds = time.perf_counter()
        self.status = f"Getting {self.username} profile"
        await asyncio.sleep(self.sleep_)
        account_profile.click()

        self.sleep_ = random.randrange(10, 17)
        self.seconds = time.perf_counter()
        self.status = f" {self.username} profile"
        await asyncio.sleep(self.sleep_)

        posts = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'posts')]")))

        posts_count = posts.text

        followers_tag = "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[2]/a/div/span"
        following_tag = "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[3]/a/div/span"

        followers = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.XPATH,followers_tag)))

        following = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.XPATH,following_tag)))

        total_followers = followers.get_attribute("title")
        total_following = following.text

        print(colored(f"\n {self.username}  [  {posts_count} ]  [ {total_followers} followers ] [ {total_following} following ]","green"))

        print(" ")

    async def search(self, search_key, hashtag=True):
        print(f"\nsearching {search_key}")

        search_tag = "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/nav/div[2]/div/div/div[2]/div[1]"

        search = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.XPATH, search_tag)))

        self.sleep_ = random.randrange(1, 5)
        self.seconds = time.perf_counter()
        self.status = f"searching {search_key}"
        await asyncio.sleep(self.sleep_)
        search.click()

        send_search = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            "input[aria-label='Search input']")))
        self.sleep_ = random.randrange(1, 5)
        self.seconds = time.perf_counter()
        self.status = "sending search keyword"
        await asyncio.sleep(self.sleep_)

        if "#" not in search_key and hashtag:
            search_key = f"#{search_key}"

        if search_key in send_search.text:
            search_key.clear()

        send_search.send_keys(search_key)
        time.sleep(random.randrange(1, 4))

        attempts = 0

        while True:
            try:
                first_result = "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]"

                latest_result = WebDriverWait(self.driver, 200).until(
                    EC.presence_of_element_located((By.XPATH, first_result)))

                self.sleep_ = random.randrange(1, 5)
                self.seconds = time.perf_counter()
                self.status = f"navigating to {search_key} page"
                await asyncio.sleep(self.sleep_)

                if search_key in latest_result.text:
                    print(colored(f"\n{latest_result.text}\n found", "yellow"))
                    latest_result.click()
                    break
                else:
                    attempts += 1

            except (TimeoutException, ElementClickInterceptedException, ElementNotInteractableException,
                    StaleElementReferenceException, NoSuchElementException) as e:
                attempts += 1

            if attempts >= 5:
                print(colored(" \n[  ] Something went wrong", "red"))
                break

    async def user_(self, username):

        await self.search(username, False)

        try:
            posts = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'posts')]")))

            self.sleep_ = random.randrange(5, 15)
            self.seconds = time.perf_counter()
            self.status = f"Getting {username} posts count "

            await asyncio.sleep(self.sleep_)

            posts_count = posts.text

            followers = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'followers')]")))

            self.sleep_ = random.randrange(5, 15)
            self.seconds = time.perf_counter()
            self.status = f"Getting {username} followers count "

            await asyncio.sleep(self.sleep_)

            followers_count = followers.text

            following = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'following')]")))

            self.sleep_ = random.randrange(1, 5)
            self.seconds = time.perf_counter()
            self.status = f"Getting {username} following count "

            await asyncio.sleep(self.sleep_)

            following_count = following.text

            print(f"\n {username} {posts_count} {followers_count} {following_count}")

            followers.click()
            self.sleep_ = random.randrange(1, 5)
            self.seconds = time.perf_counter()
            self.status = f"Getting {username} followers "

            await asyncio.sleep(self.sleep_)

            follow_max = self.user_count
            for follower in range(1, follow_max):
                follower_tag = f"/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[{follower}]"

                user_follower = WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, follower_tag)))
                # self.action.move_to_element(user_follower)
                self.driver.execute_script("arguments[0].scrollIntoView();", user_follower)

                self.sleep_ = random.randrange(1, 5)
                self.seconds = time.perf_counter()
                self.status = f"Fetching {follower} follower {user_follower.text} "
                print(colored(f"[ {datetime.datetime.now()} ] {self.status}", "yellow"))
                # await asyncio.sleep(self.sleep_)

            close = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "svg[aria-label='Close']")))

            close.click()

            print(f"Finished interacting with {username} recent posts")
        except Exception as e:
            posts = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'posts')]")))

            self.sleep_ = random.randrange(5, 15)
            self.seconds = time.perf_counter()
            self.status = f"Getting {username} posts count "

            await asyncio.sleep(self.sleep_)

            posts_count = posts.text

            followers = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'followers')]")))

            self.sleep_ = random.randrange(5, 15)
            self.seconds = time.perf_counter()
            self.status = f"Getting {username} followers count "

            await asyncio.sleep(self.sleep_)

            followers_count = followers.text

            following = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'following')]")))

            self.sleep_ = random.randrange(1, 5)
            self.seconds = time.perf_counter()
            self.status = f"Getting {username} following count "

            await asyncio.sleep(self.sleep_)

            following_count = following.text

            print(f"\n {username} {posts_count} {followers_count} {following_count}")

            followers.click()
            self.sleep_ = random.randrange(4,10)
            self.seconds = time.perf_counter()
            self.status = f"Getting {username} followers "

            await asyncio.sleep(self.sleep_)

            follow_max = self.user_count
            try:
                start_time = time.perf_counter()
                for follower in range(1, follow_max):
                    follower_tag = f"/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[{follower}]"

                    user_follower = WebDriverWait(self.driver, 50).until(
                        EC.presence_of_element_located((By.XPATH, follower_tag)))
                    # self.action.move_to_element(user_follower)
                    self.driver.execute_script("arguments[0].scrollIntoView();", user_follower)

                    self.sleep_ = random.randrange(1, 5)
                    self.seconds = time.perf_counter()
                    backslash_=r'\n'
                    _user_=str(user_follower.text).replace('Follow','').split("\n")
                    # _name_=str(user_follower.text).replace('Follow','').split(backslash_)[1]
                    self.status = f"Fetching {follower} follower {_user_[0]} {_user_[1]}"
                    self.scraped_users.append(_user_[0])

                    print(colored(f"[ {datetime.datetime.now()} ] {self.status}","green"))
                    # await asyncio.sleep(self.sleep_)

                close = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "svg[aria-label='Close']")))

                close.click()
                print(f"[ {datetime.datetime.now()} ] Finished interacting with {username} recent posts")

            except Exception as e:
                print(f"End of {username} users ")

            end_time=time.perf_counter()

            print(f"[ ] scraped {len(self.scraped_users)} in {datetime.timedelta(seconds=end_time-start_time)} ")

            self.send_dm()

    def coro_status(self,timer_,status,color_):
            print("\n")
            for o in range(timer_):
                o=o+1
                sys.stdout.write(colored(f"\r[ ] {status} [ {round(o/timer_*100,4)} % ] ",color_))
                sys.stdout.flush()
                time.sleep(1)

    def send_dm(self):
        self.driver.get(self.shared_post)
        for k,scraped_user in enumerate(self.scraped_users):
            self.coro_status(random.randrange(5,10),f"sharing post to {scraped_user}","cyan")

            send_users = db.search(User.send_dm == 'true')
            if send_users:
                # print(credentials)
                seen_users = send_users[0].get("users")

                if scraped_user in seen_users:
                    self.coro_status(random.randrange(5, 10), f"you've send a message to {scraped_user} before",
                                     "red")
                    seen_=True

                else:
                   seen_=False
            else:
                seen_users=[]
                db.insert({"send_dm": "true", "users": seen_users})
                seen_=False

            if not seen_:

                try:
                    share_tag="/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[1]/span[3]/button"

                    share = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, share_tag)))

                    share.click()

                    if k==0:
                        WebDriverWait(self.driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Share to Direct')]"))).click()

                        self.coro_status(random.randrange(5, 15), f"loading ...", "green")

                    user_search_input = WebDriverWait(self.driver, 50).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,'input[name="queryBox"]')))

                    user_search_input.send_keys(scraped_user)

                    self.coro_status(random.randrange(5, 15), f"getting  {scraped_user} ", "green")

                    toggle_user = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR,'svg[aria-label="Toggle selection"]')))

                    toggle_user[0].click()

                    self.coro_status(random.randrange(5,15), f"selecting  {scraped_user} username", "green")

                    message_input = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,"input[name='shareCommentText']")))

                    pyperclip.copy(self.message)

                    message_input.send_keys(Keys.CONTROL,"v")
                    self.coro_status(random.randrange(5,25), f"sending message to {scraped_user}", "green")

                    WebDriverWait(self.driver, 50).until(
                        EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Send')]"))).click()

                    self.coro_status(random.randrange(25,75),f"successfully send message to {scraped_user}","magenta")

                    seen_users.append(scraped_user)

                    db.update({"send_dm": "true", "users": seen_users})

                except (TimeoutException, ElementClickInterceptedException, ElementNotInteractableException,
                        StaleElementReferenceException, NoSuchElementException) as e:

                    close = WebDriverWait(self.driver, 20).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "svg[aria-label='Close']")))

                    for elem_ in close:
                        elem_.click()

                    self.coro_status(random.randrange(5,10),f"message send Failed {scraped_user}","yellow")

        quit()

    async def art(self):
        self.spinner = "..::::.."
        color = "yellow"

        while True:
            now_ = time.perf_counter() - self.seconds
            mins = datetime.timedelta(seconds=self.sleep_ - now_)
            char_ = ""

            if self.exit_program or self.block_thread:
                break
            for k, char in enumerate(self.spinner):
                try:
                    char_ += char
                    if "liked" in self.status:
                        color = "green"

                    if "you've liked" in self.status:
                        color = "cyan"
                    if "comment" in self.status:
                        color = "yellow"

                    sys.stdout.write(
                        colored(f"\r {char}{char}{char} ", color) + colored(f"{self.status} {str(mins)} ",
                                                                            color) + colored(
                            f"{char_.replace('.', f'{char}')}", color))
                    sys.stdout.flush()

                    await asyncio.sleep(0.1)
                except Exception as e:
                    await asyncio.sleep(0.01)

    async def main_login(self):
        task1 = asyncio.create_task(self.login(self.username, self.password))
        task2 = asyncio.create_task(self.art())

        await task1
        await task2

    async def main(self):
        # "Running second thread "
        task2 = asyncio.create_task(self.art())
        task3 = asyncio.create_task(self.user_(self.target_user))
        # task4 = asyncio.create_task(self.target_hashtags_task())
        await task2
        await task3
        # await task4


def start():
    target_user=input("Enter a target to scrape users:")
    user_count=int(input("How many users do want to scrape:"))
    post=input("\nEnter post link:")
    message_=input("Enter folder path containing message.txt: ")

    Scraper("Y",target_user,user_count,post,message_)