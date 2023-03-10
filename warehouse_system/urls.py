"""warehouse_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from inventory import views

inventory_patterns =[
    path('', views.InventoryView.as_view()),
    re_path(r'(?P<id>\d+)', views.ShowInventory.as_view()),
    path('products/', views.ProductsAvaliableView.as_view()),
    path('storages/', views.StorageContainsView.as_view()),
]

urlpatterns = [
    path('', views.index, name='home'),
    path('inventory/', include(inventory_patterns)),
    path('admin/', admin.site.urls),

    
]
