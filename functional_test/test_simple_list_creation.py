from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.live_server_url)

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute(
            'placeholder'), 'Enter a to-do item')
        # self.fail('Finish the test')

        inputbox.send_keys('Buy some tea')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy some tea')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table(
            '2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy some tea')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy coffee')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy coffee')

        unique_list_url = self.browser.current_url
        self.assertRegex(unique_list_url, '/lists/.+')

        # New user
        self.browser.quit()
        self.browser = webdriver.Firefox(
            executable_path=os.path.join(os.getcwd(), 'geckodriver'))

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy coffe', page_text)

        # start new list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # get unique url
        new_unique_list_url = self.browser.current_url
        self.assertRegex(new_unique_list_url, '/lists/.+')
        self.assertNotEqual(unique_list_url, new_unique_list_url)

        # Test to make sure there are no traces from prevous user's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy coffee', page_text)
        self.assertIn('Buy milk', page_text)