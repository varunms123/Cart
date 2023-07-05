from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name="index"),
    path('login/',login,name="login"),
    path('register/',register,name="register"),
    path('post/',post_product,name="post"),
    path('category/',category,name="category"),
    path('get',get_product,name="get"),
    path('men/',men_product,name="men_product"),
    path('women/',women_product,name="women_product"),
    path('laptops/',laptops,name="laptops"),
    path('kitchen/',kitchen,name="kitchen"),
    path('headphones/',headphones,name="headphones"),
    path('books/',books,name="books"),
    path('mobiles/',mobiles,name="mobiles"),
    path('shoes/',shoes,name="shoes"),
    path('contact/',contact,name="contact"),
    path('add_product/<id>/',add_product,name="add_product"),
    path('cart/<id>/',cart,name="cart"),
    path('view/',view,name="view"),
    path('checkout/',checkout,name="checkout"),
    path('remove/<id>',remove,name="remove"),
    path('place_order/',place_order,name="place_order"),
    path('order_received/<str:payment_method>/',order_received,name="order_received"),
    path('review/',review,name="review")
]
