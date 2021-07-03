from django.shortcuts import render,redirect
from django.http import HttpResponse
from lists.models import Item

def home_page(request):

	"""
	item = Item()
	item.text = request.POST.get('item_text', '')
	item.save()
	"""


	if request.method == 'POST':

		Item.objects.create(text=request.POST['item_text'])
		return redirect('/')
	

	return render(request, 'home.html')