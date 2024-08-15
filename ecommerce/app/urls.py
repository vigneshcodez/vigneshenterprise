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
from .checkoutview import (
    checkout,
    cancel_order,
    razorpay_webhook,
    checkoutpage,
    checkout,
    orders
)

urlpatterns = [

    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('myshop', views.myshop, name='myshop'),
    path('signup/', signup_view, name='signup_view'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    path('password-reset/', RequestResetEmailView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/', SetNewPasswordView.as_view(), name='set_new_password'),
    path('address', views.address, name='address'),
    path('search/', views.product_search, name='product_search'),

    

    # 
    path('shop/<str:name>', views.shop, name='shop'),
    path('productdetial/<int:id>', views.productdetial, name='productdetial'),
    
    #
    path('cart/', cart_detail, name='cart_detail'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),  # Ensure the trailing slash
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('update_cart_item/<int:product_id>/<str:action>/', update_cart_item, name='update_cart_item'), 
    path('orders/', orders, name='orders'), 
    
    # 
    path('checkout/', checkout, name='checkout'),
    path('cancel_order/<int:order_id>/', cancel_order, name='cancel_order'),

    # Razorpay Webhook for Payment Confirmation
    path('payment/webhook/', razorpay_webhook, name='razorpay_webhook'),
    path('checkoutpage/', checkoutpage, name='checkoutpage'),

    # whishlist
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
]
