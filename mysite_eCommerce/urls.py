from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.home, name="Home" ),
    path('cart/',views.cart, name="Cart"),
    path('shopbybrand/',views.shopbybrand, name="shopbybrand"),
    path('shopbycatagory/',views.shopbycatagory, name="shopbycatagory"),
    path('view/<str:brand>',views.brandview, name="brandview"),
    path('productview/<int:id>',views.productview, name="productview"),
    path('search/',views.search, name = "search"),
    path('checkout/',views.checkout, name= "checkout"),
    path('login/',views.loginpage,name= "Login"),
    path('signin/',views.registrationpage, name= "signin"),
    path('logout/',views.logoutpage, name= "logout"),
    path('viewprofile/',views.viewprofile, name="viewprofile"),
    path('editprofile/',views.editprofile, name="editprofile"),
    path('updateitem/',views.updateItem, name="updateitem"),
    path('test',views.test, name="test"),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)