from selenium import webdriver
from random import choice
from time import sleep
from datetime import datetime


class InstaBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.driver_path = './chromedriver'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.bot = webdriver.Chrome(self.driver_path, options=self.options)

    def acess_site(self):
        self.bot.get('https://www.instagram.com/')

    def login(self):
        self.bot.implicitly_wait(20)
        user_field = self.bot.find_element_by_name('username')
        pass_field = self.bot.find_element_by_name('password')

        user_field.send_keys(self.username)
        pass_field.send_keys(self.password)

        btn_login = self.bot.find_element_by_tag_name('button div')
        btn_login.click()

    def acess_profile_page(self):
        sleep(3)
        self.bot.get(f'https://www.instagram.com/{self.username}')

    def _get_names(self):
        self.bot.implicitly_wait(20)
        scroll_box = self.bot.find_element_by_xpath(
            "/html/body/div[4]/div/div/div[2]")

        print('Getting users...')
        lh, h = 0, 1
        while lh != h:
            lh = h

            sleep(3)
            h = self.bot.execute_script(
                """
            arguments[0].scrollTo(0, arguments[0].scrollHeight);
            return arguments[0].scrollHeight;
            """, scroll_box)

        links = scroll_box.find_elements_by_tag_name('div a')
        names = [
            name.text for name in links if name.text != '' and name is not None
        ]

        self.bot.find_element_by_xpath(
            '/html/body/div[4]/div/div/div[1]/div/div[2]/button').click()

        return names

    def dont_follow_me(self):

        nums = self.bot.find_elements_by_css_selector('.g47SY')

        num_followers = int(nums[1].text.replace(',', ''))
        num_following = int(nums[2].text.replace(',', ''))

        sleep(5)

        following = []
        followers = []

        while len(following) != num_following or len(
                followers) != num_followers:

            self.bot.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a'
            ).click()

            sleep(5)

            following = self._get_names()

            print(len(following), num_following)
            sleep(5)

            self.bot.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a'
            ).click()

            sleep(5)

            followers = self._get_names()

            print(len(followers), num_followers)

            sleep(5)

        sleep(5)

        dont_follow_back = [
            user for user in following if user not in followers
        ]

        return dont_follow_back

    def unfollow_func(self, user):
        self.bot.get(f'https://www.instagram.com/{user}/')
        self.bot.implicitly_wait(20)
        self.bot.find_element_by_css_selector('.YBx95').click()
        self.bot.implicitly_wait(20)
        self.bot.find_element_by_css_selector(
            'body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.-Cab_'
        ).click()

    def unfollow(self):
        print('\nStarting unfollow process...')

        unfollow_list = self.dont_follow_me()
        unfollow_list.reverse()

        for user in unfollow_list:
            print(f'\nStop following {user}...')

            self.unfollow_func(user)

            print(datetime.now().strftime('Operation realized %d/%b %H:%M'))
            sleep(choice([50, 100, 20, 120]))

    def exit(self):
        self.bot.quit()


user = input("User Instagram: ")
password = input("Password Instagram: ")

bot = InstaBot(user, password)
bot.acess_site()

bot.login()

bot.acess_profile_page()

bot.unfollow()

bot.exit()
