from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render,redirect
from .models import Category, SubCategory, Product,Slider,Address,Wishlist,Advertisment
from django.http import JsonResponse
from django.core.paginator import Paginator
from .forms import AddressForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


def index(request):
    categories = Category.objects.all()
    slider = Slider.objects.all()
    featured_product = Product.objects.filter(featured=True)
    try:
        ad1 = Advertisment.objects.get(id=1)
        ad2 = Advertisment.objects.get(id=2)
        ad3 = Advertisment.objects.get(id=3)
        ad4 = Advertisment.objects.get(id=4)
        return render(request, 'pages/index.html',{"categories":categories,"slider":slider,"featured_product":featured_product,'ad1':ad1,'ad2':ad2,'ad3':ad3,'ad4':ad4})

    except :
        return render(request, 'pages/index.html',{"categories":categories,"slider":slider,"featured_product":featured_product})
        


def about(request):
    categories = Category.objects.all()
    return render(request, 'pages/about.html',{'categories':categories})


# def shop(request,name=None):
#     category = get_object_or_404(Category, name=name)
#     subcategories = SubCategory.objects.filter(category=category)
#     products = Product.objects.filter(category=category)

#     print(category)
#     print(subcategories)
#     print(products)

#     context = {
#         'category': category,
#         'subcategories': subcategories,
#         'products': products
#     }
#     return render(request, 'pages/shop.html', context)



# def shop(request, name=None):
#     category = get_object_or_404(Category, name=name)
#     subcategories = SubCategory.objects.filter(category=category)
    
#     # Check if the request is AJAX
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         subcategory_id = request.GET.get('subcategory_id')
#         page_number = request.GET.get('page', 1)
        
#         # Filter products by subcategory if provided
#         if subcategory_id:
#             products = Product.objects.filter(subcategory_id=subcategory_id, category=category)
#         else:
#             products = Product.objects.filter(category=category)

#         # Paginate products
#         paginator = Paginator(products, 3)  # Show 3 products per page
#         page = paginator.get_page(page_number)

#         # Prepare data for JSON response
#         data = {
#             'products': list(page.object_list.values('name', 'price', 'image','id','discount','price','discounted_price')),
#             'has_next': page.has_next(),
#             'has_previous': page.has_previous(),
#             'page_number': page.number,
#             'num_pages': paginator.num_pages,
#         }
#         return JsonResponse(data)
    
#     # Handle regular requests
#     products = Product.objects.filter(category=category)
#     context = {
#         'category': category,
#         'subcategories': subcategories,
#         'products': products
#     }
#     return render(request, 'pages/shop.html', context)

def shop(request, name=None):
    categories = Category.objects.all()
    category = get_object_or_404(Category, name=name)
    subcategories = SubCategory.objects.filter(category=category)

    # Calculate product count for each subcategory
    subcategories_with_counts = []
    total_product_count = 0
    for subcategory in subcategories:
        product_count = Product.objects.filter(subcategory=subcategory, category=category).count()
        subcategories_with_counts.append((subcategory, product_count))
        total_product_count += product_count

    # Check if the request is AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        subcategory_id = request.GET.get('subcategory_id')
        page_number = request.GET.get('page', 1)

        # Filter products by subcategory if provided
        if subcategory_id:
            products = Product.objects.filter(subcategory_id=subcategory_id, category=category)
        else:
            products = Product.objects.filter(category=category)

        # Paginate products
        paginator = Paginator(products, 3)  # Show 3 products per page
        page = paginator.get_page(page_number)

        # Prepare data for JSON response
        data = {
            'products': list(page.object_list.values('name', 'price', 'image', 'id', 'discount', 'price', 'discounted_price')),
            'has_next': page.has_next(),
            'has_previous': page.has_previous(),
            'page_number': page.number,
            'num_pages': paginator.num_pages,
        }
        return JsonResponse(data)

    # Handle regular requests
    products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'subcategories_with_counts': subcategories_with_counts,
        'total_product_count': total_product_count,
        'products': products,
        'categories':categories
    }
    return render(request, 'pages/shop.html', context)



def productdetial(request, id):
    categories = Category.objects.all()
    # product = get_object_or_404(Product, id=id)
    product = Product.objects.get(id=id)

    context = {
        'product': product,
        'categories':categories
    }
    return render(request, 'pages/productdetial.html', context)

def address(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            # Save the form with the user
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request,'address added succesfully')
            return redirect('address')  # Replace 'success_url' with your actual success URL
    else:
        form = AddressForm()
        data = Address.objects.filter(user=request.user)
    
    return render(request, 'pages/address.html', {'form': form,'data':data,'categories':categories})


def product_search(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('query', '')
        products = Product.objects.filter(name__icontains=query)[:10]  # Limit to 10 results for performance
        results = list(products.values('id', 'name', 'price', 'image'))
        return JsonResponse({'products': results})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required(login_url='login_view')
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if created:
        message = "Product added to wishlist"
    else:
        message = "Product is already in your wishlist"
    messages.success(request, message)
    return redirect('view_wishlist')

@login_required(login_url='login_view')
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    return JsonResponse({'message': "Product removed from wishlist"})

@login_required(login_url='login_view')
def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    if wishlist_items.count() == 0:
        return render(request, 'pages/wishlist.html', {'wishlist_items': []})
    return render(request, 'pages/wishlist.html', {'wishlist_items': wishlist_items})

def myshop(request):
    categories = Category.objects.all()
    return render(request,'pages/myshop.html',{'categories':categories})