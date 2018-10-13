from django.urls import path, re_path

from . import views

urlpatterns = [
    path('home/', views.home, name = 'home'),

    re_path('market/(\d+)/(\d+)/(\d+)/', views.market, name = 'market'),
    re_path('market/', views.market, name = 'market'),

    path('cart/', views.cart, name = 'cart'),
    re_path('changecart/(\d+)/', views.changecart, name = 'changecart'),
    path('saveorder/', views.saveorder, name = 'saveorder'),

    path('mine/', views.mine, name = 'mine'),
    path('login/', views.login, name = 'login'),
    path('register/', views.register, name = 'register'),
    # 验证账号是否被注册
    path('checkuserid/', views.checkuserid, name = 'checkuserid'),

    path('quit/', views.quit, name = 'quit'),

]