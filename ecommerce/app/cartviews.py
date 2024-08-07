from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from .models import Product
from django.http import JsonResponse

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart = Cart.objects.get(user=request.user)
    return render(request, 'pages/cart.html', {'cart': cart})

@login_required
def remove_from_cart(request, product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    cart_item.delete()
    return redirect('cart_detail')


# def update_cart_item(request, product_id, quantity):
#     cart = Cart.objects.get(user=request.user)
#     cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
#     cart_item.quantity = quantity
#     cart_item.save()
#     return redirect('cart_detail')

# @login_required
# def update_cart_item(request, product_id, action):
#     cart = Cart.objects.get(user=request.user)  # Adjust this line according to your cart retrieval logic
#     product = get_object_or_404(Product, id=product_id)
#     cart_item = cart.items.get(product=product)
    
#     if action == 'increase':
#         cart_item.quantity += 1
#     elif action == 'decrease' and cart_item.quantity > 1:
#         cart_item.quantity -= 1

#     cart_item.save()
    
#     response_data = {
#         'quantity': cart_item.quantity,
#         'total_price': cart_item.get_total_price,
#         'cart_total': cart.get_total
#     }
    
#     return JsonResponse(response_data)


@login_required
def update_cart_item(request, product_id, action):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()
            response_data = {
                'quantity': 0,
                'total_price': 0,
                'cart_total': cart.get_total()
            }
            return JsonResponse(response_data)
    
    cart_item.save()
    
    response_data = {
        'quantity': cart_item.quantity,
        'total_price': cart_item.get_total_price(),  # Ensure this returns a number
        'cart_total': cart.get_total()  # Ensure this returns a number
    }

    # Debug print statement
    # print(json.dumps(response_data))

    return JsonResponse(response_data)