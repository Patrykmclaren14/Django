from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.registration_view, name='register'),
    path('add_product', views.add_product, name='add-product'),
    path('profile/<user_id>', views.profile, name='profile'),
    path('edit_profile/<user_id>', views.edit_profile, name='edit_profile'),
    path('users_page', views.users_page, name='users_page'),
    path('profile_page/<user_id>', views.profile_page, name='profile_page'),
    path('show_product/<product_id>', views.show_product, name='show_product'),
    path('cart', views.cart, name='cart'),
]
