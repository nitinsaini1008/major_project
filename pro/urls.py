from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('main_page',views.home,name='home'),
    path('',views.main_page,name='main_page'),
    path('search_name',views.search_name,name='search_name'),
    path('buy',views.buy,name='buy'),
    path('sign_in',views.sign_in,name='sign_in'),
    path('log_in',views.log_in,name='log_in'),
    path('log_out',views.log_out,name='log_out'),
    path('my_cart',views.my_cart,name='my_cart'),
    path('delete_cart',views.delete_cart,name='delete_cart'),
    path('about',views.about,name='about'),
    path('sub_page',views.sub_page,name='sub_page'),
    path('pre_buy',views.pre_buy,name='pre_buy'),
    path('account',views.account,name='account'),
    path('details/<id>',views.details,name='details'),
    path('save_reviews/<id>',views.save_reviews,name='save_reviews'),
    path('post_sign',views.post_sign,name='post_sign'),
    path('sign_2',views.sign_2,name='sign_2'),
    path('result',views.result,name='result'),
    path("accounts/login/", views.sign_in, name='sign_in'),
    path("clear_cart/", views.clear_cart, name="clear_cart"),
    path('callback/', views.callback, name="callback"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)