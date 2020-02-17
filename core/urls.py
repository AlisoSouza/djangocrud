from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('',views.list_products,name='list_products'),
    path('new', views.create_products,name='create_products'),
    path('update/<int:id>/', views.update_product,name='update_product'),
    path('delete/<int:id>/', views.delete_product, name='delete_product'),

]
