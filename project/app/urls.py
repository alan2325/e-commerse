from django.urls import path
from . import views
urlpatterns = [
path('',views.login),
path('logout',views.logout),
path('register',views.register),
path('adminhome',views.adminhome),
path('user_home',views.user_home),
path('profile',views.profile),
path('upload',views.upload),
path('viewuser',views.viewuser),
path('addpro',views.addpro),
path('viewpro',views.viewpro),
path('bookinghistory',views.bookinghistory),
path('cart/<int:id>',views.user_cart),
path('deletes/<int:id>',views.deletes),
path('user_view_cart',views.user_view_cart),
path('qty_incri/<int:id>',views.qty_incri),
path('qty_decri/<int:id>',views.qty_decri),
path('order_details',views.order_details),
path('proupdate/<int:id>',views.proupdate),
path('prodetails/<int:id>',views.prodetails),
path('viewproduct',views.viewproduct),
path('delete/<int:id>',views.delete),
path('buys/<int:id>',views.buys),

]