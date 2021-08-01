from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
from selenium import webdriver
import unittest
import time
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
	
	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	#定义辅助方法
	def wait_for_row_in_list_table(self,row_text):

		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)
		

	def test_can_start_a_list_for_one_user(self):
		#self.browser.get('http://localhost:8000')
		self.browser.get(self.live_server_url)
		self.assertIn('To-Do' , self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		#应用邀请伊迪斯输入一个待办事项
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
			)
		
		#伊迪斯在一个文本框中输入了“Buy peacock feathers”（购买孔雀羽毛）
		inputbox.send_keys('Buy peacock feathers')
		#伊迪斯按回车键后，页面更新了
		#待办事项表格中显示了“1：Buy peacock feathers”
		inputbox.send_keys(Keys.ENTER)
		#time.sleep(1)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')		

		
		#页面中又显示了一个文本框，可以输入其它的待办事项
		#伊迪斯输入了“Use peacock feathers to make a fly”（使用孔雀羽毛做假蝇）
		#伊迪丝做事很有条理
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)
		#time.sleep(1)

		self.wait_for_row_in_list_table('1: Buy peacock feathers')
		self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')


	def test_multiple_users_can_start_lists_at_different_urls(self):
		#伊迪斯新建一个待办事项清单
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		#伊迪斯注意到清单有个唯一的URL
		edith_list_url = self.browser.current_url
		#assertRegex是unittest提供的辅助函数，用户检查字符串是否匹配正则表达式，此处检查新的REST式设计能否实现
		self.assertRegex = (edith_list_url, '/lists/.+')

		#现在一名叫做弗朗西斯的新用户访问了网站
		##我们使用一个新的浏览器会话
		##确保伊迪斯的信息不会从cookie中泄露出去(两个##叫元注释，说明测试的工作方式及为什么这么做)
		self.browser.quit()
		self.browser = webdriver.Firefox()

		#弗朗西斯访问首页，页面看不到伊迪斯的清单
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)

		#弗朗西斯输入一个新待办事项，新建一个清单
		#他不像伊迪斯那样兴趣盎然
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		#弗朗西斯获得了他的唯一URL
		francis_list_url = self.browser.current_url
		self.assertRegexpMatches(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)

		#这个页面还是没有伊迪斯的清单
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)



"""
if __name__ == '__main__':
	unittest.main(warnings='ignore')
"""