"""kuproject URL Configuration

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
from django.urls import path ,include
import kuproject.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', kuproject.views.get, name='index'),
    path('main.html/', kuproject.views.main, name='main'),
    path('mystock.html/',kuproject.views.mystock, name='mystock'),
    path('nowstock.html/', kuproject.views.nowstock, name='nowstock'),
    path('favorite.html/', kuproject.views.favorite, name='favorite'),
    path('order.html/', kuproject.views.order, name='order'),
    path('profit.html/',kuproject.views.profit, name='profit'),
    path('stockindex.html/', kuproject.views.stockindex, name='stockindex'),
    path('input.html/',kuproject.views.SCinput, name='SCinput'),
    path('test1.html/',kuproject.views.test1,name= 'test1'),
    path('test2.html/', kuproject.views.test2, name='test2'),
    path('test3.html/', kuproject.views.test3, name='test3'),
]
