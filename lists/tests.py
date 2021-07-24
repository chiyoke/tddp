from django.test import TestCase
from lists.models import Item

class HomePageTest(TestCase):
	"""
	def test_only_saves_items_when_necessary(self):
		self.client.get('/')
		self.assertEqual(Item.objects.count(), 0)
	"""

class ItemModelTest(TestCase):
	
	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second' 
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(second_saved_item.text, 'Item the second')


class ListViewTest(TestCase):

	def test_uses_list_template(self):
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response, 'list.html')


	def test_displays_all_items(self):
		Item.objects.create(text='itemey 1')
		Item.objects.create(text='itemey 2')

		response = self.client.get('/lists/the-only-list-in-the-world/')

		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')


class NewListTest(TestCase):
	
	def test_can_save_a_POST_request(self):
		self.client.post('/lists/new', data={'item_text':'A new list item'})
		##检查是否把一个新Item对象存入数据空
		##objects.count()是objects.all().count()的简写形式
		self.assertEqual(Item.objects.count(), 1) 
		##objects.first()等价于objects.all()[0]
		new_item = Item.objects.first()	
		self.assertEqual(new_item.text, 'A new list item')
		
	def test_redirect_after_POST(self):
		##/new后面不加斜线，作者HJWP一般不在修改数据库的“操作”后加斜线
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
		#self.assertEqual(response.status_code, 302)
		#self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
		##上面两个assertEqual断言可以精简成以下一条
		self.assertRedirects(response, '/lists/the-only-list-in-the-world/')