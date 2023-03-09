from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Count

from .utils import  ViewModelContextMixin

from .models import Inventory

def index(request):
    return render(request, 'bases/base.html',
                  context={'title': 'Template', 'content':'<p>Some content</p>'})



class InventoryView(ViewModelContextMixin, ListView):
    # TODO Empty model page 
    # FIXME object_list is not empty on context_object_name definition
    # need check docs
    model = Inventory
    template_name = 'inventory_list.html'
    stored_context = {}

    def get_context_data(self, **kwargs):

        su_context = super().get_context_data(**kwargs)
        mix_context = self.get_user_context()        


        # FIXME refactor. Move to Mixin.
        if self.request.GET.get("products", False):
            self.set_product_context()
            print("Products")
        elif self.request.GET.get("storages", False):
            print("Storages")
            self.set_storage_context()
        else:
            print("Default")
            self.set_default_context()

        context = dict(
            list(su_context.items()) +
            list(mix_context.items()) +
            list(self.stored_context.items())
        )

            
        return context

    def set_product_context(self):
        self.stored_context['field_titles'] = ['Product name', 'Now avaliable']

        prod_uniq = self.model.objects.values_list(
            "product_prototype__name",
            "product_prototype__model__name"
        ).distinct()

        self.stored_context['items'] = []
        for prod in prod_uniq:
            count = self.model.objects.filter(
                write_off=False,
                on_employee=None,
                product_prototype__name=prod[0],
                product_prototype__model__name=prod[1]
            ).aggregate(group=Count('id'))

            if None not in prod:
                group_name = ' '.join(prod)
            else:
                group_name = prod[0]

            self.stored_context['items'].append([group_name, count['group']])


    def set_storage_context(self):
        # Try use regroup
        pass


    def set_default_context(self):
        self.stored_context['field_titles'] = [
                'Inventory ID',
                'Product name',
                'Storage location',
                'User',
                'Write off'
            ]
        # FIXME to refactoring.
        self.stored_context['items'] = []
        for row in self.model.objects.all():
            self.stored_context['items'].append([
                    row.id,
                    row.product_prototype,
                    row.storage,
                    row.on_employee,
                    row.write_off
                ]
            )
            


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
        
