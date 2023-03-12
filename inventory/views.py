from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Count, QuerySet

from typing import Any, Dict

from .utils import  ViewModelContextMixin

from .models import Inventory, ProductPrototype

def index(request):
    return render(request, 'bases/base.html',
                  context={'title': 'Home', 'content':'<p>Some content</p>'})



class InventoryView(ViewModelContextMixin, ListView):
    # FIXME duplicate field in items
    #   field_titles must be a dict.
    #   on iter fields_titles from dict call it from items or ect.
    # TODO pagination
    # NOTE May be reserve another key for view with add 1:1 key to origin context items.

    model = Inventory
    template_name = 'inventory_list.html'
    context_object_name = 'items'



    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = 'Inventory'
        
        context['field_titles'] = [
            'Inventory_ID',
            'Product_name',
            'Storage_location',
            'User',
            'Write_off'
        ]
        context['items'] = [
            {
                'Inventory_ID': item.id,
                'Product_name': item.product_prototype,
                'Storage_location': item.storage,
                'User': item.on_employee if item.on_employee is not None else "",
                'Write_off': item.write_off if item.write_off == True else "" 
            }
            for item in context['items'].order_by('storage')
        ]
        
        return context
        

class ProductsAvaliableView(ListView):
    model = Inventory
    template_name = 'inventory_list.html'
    context_object_name = 'items'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products avaliable'
        context['items'] = [
            {
                'product_id': item['product_prototype__pk'],
                'Product':"{product_name} {product_model}".format(
                    product_name = item['product_prototype__name'],
                    product_model= (
                        ''
                        if item['product_prototype__model__name'] is None
                        else item['product_prototype__model__name']
                    )
                ),
                'Count':item['count']
            }
            for item in context['items']
        ]

        context['field_titles'] = ['Product', 'Count']
        return context


    def get_queryset(self):
        qs = self.model.objects.filter(
            on_employee=None,
            write_off=False
        ).values(
            'product_prototype__pk',
            'product_prototype__name',
            'product_prototype__model__name'
            ).annotate(
            count = Count('id')
            )
        return qs
    

class StorageContainsView(InventoryView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'On Storages'
        return context


    def get_queryset(self):
        qs = super().get_queryset().filter(
            on_employee=None,
            write_off=False
        )
        return qs
        


class ShowInventory(ViewModelContextMixin, DetailView):
    # TODO 404
    model = Inventory
    template_name = "inventory_detail.html"
    pk_url_kwarg = 'id'
    
    context_object_name = "item"


    def get_context_data(self, **kwargs):
        su_context = super().get_context_data(**kwargs)
        mix_context = self.get_user_context()
        context = dict(list(su_context.items()) + list(mix_context.items()))
        return context
        
