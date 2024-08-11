from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import razorpay
from .models import Order, Address, OrderItem,Product
from .models import Cart,Address  # Adjust based on your cart implementation
from django.contrib.auth.decorators import login_required

client = razorpay.Client(auth=("YOUR_KEY_ID", "YOUR_KEY_SECRET"))

@login_required(login_url='login_view')
def checkoutpage(request):
    user = request.user
    address = Address.objects.filter(user=user)
    return render(request,'pages/checkout.html',{'addresses':address})

@login_required(login_url='login_view')
@require_POST
def checkout(request):
    address_id = request.POST.get('address_id')
    payment_method = request.POST.get('payment_method')

    try:
        address = Address.objects.get(id=address_id)
    except Address.DoesNotExist:
        return JsonResponse({'error': 'Invalid address'}, status=400)

    cart = Cart.objects.get(user=request.user)
    total_amount = cart.get_total() + 10  # Add shipping cost

    # Create the order
    order = Order.objects.create(
        user=request.user,
        address=address,
        total_amount=total_amount,
        payment_method=payment_method
    )
    
    # Create OrderItem entries
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.discounted_price
        )

    # Clear the cart after the order is placed
    cart.delete()
    cart.save()

    if payment_method == 'RAZORPAY':
        razorpay_order = client.order.create(dict(amount=total_amount*100, currency='INR', payment_capture='1'))
        order.razorpay_order_id = razorpay_order['id']
        order.save()
        return JsonResponse({'razorpay_order_id': razorpay_order['id'], 'amount': total_amount})

    # For Cash on Delivery
    order.update_status('PENDING')
    return JsonResponse({'message': 'Order placed successfully', 'order_id': order.id})
@login_required(login_url='login_view')
@require_POST
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status in ['DELIVERED', 'CANCELLED']:
        return JsonResponse({'error': 'Cannot cancel this order'}, status=400)

    order.update_status('CANCELLED')
    return JsonResponse({'message': 'Order cancelled and stock restored'})
@login_required(login_url='login_view')
@csrf_exempt
def razorpay_webhook(request):
    if request.method == 'POST':
        payload = request.body.decode('utf-8')
        signature = request.headers.get('X-Razorpay-Signature')
        try:
            client.utility.verify_webhook_signature(payload, signature, "YOUR_WEBHOOK_SECRET")
            event = json.loads(payload)
            if event['event'] == 'order.paid':
                order_id = event['payload']['order']['id']
                order = Order.objects.get(razorpay_order_id=order_id)
                order.update_status('PROCESSING')
                return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=400)

@login_required(login_url='login_view')
def orders(request):
    placedorders = Order.objects.filter(user=request.user)
    content = []
    for i in placedorders:
        cartdata = {
            'orderid':i.id,
            'paymentmethod':i.payment_method,
            'status':i.status,
            'total':i.total_amount,
            'products':[]
        }
        data = OrderItem.objects.filter(order_id=i.id)

        for j in data:
            print(j.product_id,'qty',j.quantity)
            product = Product.objects.get(id=j.product_id)
            p = {
            'productname':product.name,
            'quantity':j.quantity,
            'price':product.price
            }
            cartdata['products'].append(p)

        
        content.append(cartdata)
        content.reverse()
        print(content)
    return render(request,'pages/orders.html',{'data':content})