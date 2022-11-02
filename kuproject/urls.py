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
    path('', kuproject.views.main, name='index'),
    path('main.html/', kuproject.views.main, name='main'),
    path('nowstock.html/', kuproject.views.nowstock, name='nowstock'),
    path('favorite.html/', kuproject.views.favorite, name='favorite'),
    path('stockindex.html/', kuproject.views.stockindex, name='stockindex'),
    path('test1.html/',kuproject.views.test1,name='test1'),
    path('test2', kuproject.views.test2, name='test2'),
    path('test4.html/', kuproject.views.test3, name='test4'),
    path('login.html/',kuproject.views.login, name='login'),
    path('register.html/', kuproject.views.register, name='register'),
    path('com_search_ajax/',kuproject.views.com_search_ajax, name='com_search_ajax'),
    path('alter.html', kuproject.views.alter, name='alter'),
    path('FS.html',kuproject.views.FS, name='FS'),
    path('investor.html',kuproject.views.investor, name="investor"),
    path('news.html',kuproject.views.news, name="news"),
    path('test3.html',kuproject.views.test3,name="test3"),
    path('opin.html',kuproject.views.opin,name="opin"),
    path('community.html', kuproject.views.commu, name="commu"),
    path('write.html', kuproject.views.write, name="write"),
    path('comment.html', kuproject.views.comment, name="comment"),
    path('detail/<int:pk>/', kuproject.views.comm_detail, name='comm_detail'),
    path('detail/<int:pk>/delete/', kuproject.views.comm_delete, name='comm_delete'),
    path('comment_write/<int:pk>', kuproject.views.comment_write, name='comment_write'),
    path('board.html', kuproject.views.board, name='board'),
    path('write.html', kuproject.views.board_write, name="board_write"),
    path('board_detail/<int:pk>/', kuproject.views.board_detail, name='board_detail'),
    path('board_detail/<int:pk>/delete/', kuproject.views.board_delete, name='board_delete'),
    path('board_comment_write/<int:pk>', kuproject.views.board_comment_write, name='board_comment_write')
]
