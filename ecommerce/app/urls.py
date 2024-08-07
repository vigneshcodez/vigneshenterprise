from django.urls import path
from . import views
from .authenticationviews import (
    signup_view,
    login_view,
    logout_view,
    ActivateAccountView,
    RequestResetEmailView,
    SetNewPasswordView,
)

from .cartviews import (add_to_cart,update_cart_item,cart_detail,remove_from_cart)

urlpatterns = [

    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('signup/', signup_view, name='signup_view'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    path('password-reset/', RequestResetEmailView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/', SetNewPasswordView.as_view(), name='set_new_password'),

    # 
    path('shop/<str:name>', views.shop, name='shop'),
    path('productdetial/<int:id>', views.productdetial, name='productdetial'),
    
    #
    path('cart/', cart_detail, name='cart_detail'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),  # Ensure the trailing slash
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('update_cart_item/<int:product_id>/<str:action>/', update_cart_item, name='update_cart_item'), 
    
]
