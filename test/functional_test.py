from selenium import webdriver
import os
import unittest


class TodoTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(executable_path= os.path.join(os.getcwd(), 'geckodriver'))
    
    def tearDown(self):
        self.browser.quit()

    def test_start(self):
        self.browser.get('http://localhost:8000')
        
        self.assertIn('Django', self.browser.title)
        # self.fail('Finish the test')

    def test_equal(self):
        self.assertEqual(3,3)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
