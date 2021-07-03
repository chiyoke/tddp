from django.test import TestCase
from lists.models import Item

class HomePageTest(TestCase):

	def test_can_save_a_POST_request(self):
		response = self.client.post('/', data={'item_text':'A new list item'})

		#检查是否把一个新Item对象存入数据空
		self.assertEqual(Item.objects.count(), 1) #objects.count()是objects.all().count()的简写形式
		new_item = Item.objects.first()	#objects.first()等价于objects.all()[0]
		self.assertEqual(new_item.text, 'A new list item')

		self.assertIn('A new list item', response.content.decode())
		self.assertTemplateUsed(response, 'home.html')

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