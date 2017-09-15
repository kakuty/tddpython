import json
from django.http import HttpResponse

from .models import Item, List

def list(request, list_id):
    list_ = List.objects.get(id=list_id)
    if request.method == 'POST':
        Item.objects.create(list=list_, text = request.POST.get('text'))
        return HttpResponse(status=201)
    item_dicts = [
        {'id': item.id, 'text': item.text} for item in list_.item_set.all()
    ]
    
    return HttpResponse(
        json.dumps(item_dicts),
        content_type='application/json'
    )
