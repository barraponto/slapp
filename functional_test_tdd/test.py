
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys




class ItemListTest(LiveServerTestCase):


    def setUp(self):
        self.browser=webdriver.Chrome('/Users/LeeX/Dropbox/Programming/Thinkfull/python/django/slapp/sla_app/chromedriver')  # Optional argument, if not specified will search path.


    def tearDown(self):
        self.browser.quit()
        print(self.live_server_url)


    def check_item_in_row(self,item_name):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(item_name,[row.text for row in rows])


    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        #self.browser.get('http://localhost:8000/tdd/pag_inicio')
        self.browser.get(self.live_server_url+'/tdd/pag_inicio')

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        #import time
        #time.sleep(10)

        inputbox.send_keys(Keys.ENTER)


        table = self.browser.find_element_by_id('id_list_table')

        #table = self.browser.find_element(by=By.ID, value="id_list_table")
        rows = table.find_elements_by_tag_name('tr')
        self.check_item_in_row('1: Buy peacock feathers')
    

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)


        # The page updates again, and now shows both items on her list
        table = self.browser.find_element_by_id('id_list_table')

        #table = self.browser.find_element(by=By.ID, value="id_list_table")
        rows = table.find_elements_by_tag_name('tr')
        self.check_item_in_row('1: Buy peacock feathers')
        self.check_item_in_row('2: Use peacock feathers to make a fly')
        import time
        time.sleep(5)
        
        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep
        self.fail('Finish the test!')

