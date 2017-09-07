from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import unittest


class TodoTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(executable_path= os.path.join(os.getcwd(), 'geckodriver'))
    
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        # self.fail('Finish the test')

        inputbox.send_keys('Buy some tea')

        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)


        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy some tea' for row in rows), 
            'New item to-do did not appear in table'
        )

        self.fail('Finish the test')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
