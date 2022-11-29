from django.urls import path
from .views import *


urlpatterns = [
    path('',main_menu,name='main-menu'),
    path('stock-list/<int:id>/',stock_list,name='stock-list'),
    path('documents/',document,name='documents'),
    path('document-items/<int:id>/',docitems,name = 'docitems'),
    path('document-create/',create_document,name='create-document'),
    path('documentitems-create/<int:id>/',create_docitem,name='create-docitem')
]