from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from .models import Category, SubCategory, Product,Slider
# Create your views here.


def index(request):
    categories = Category.objects.all()
    slider = Slider.objects.all()
    featured_product = Product.objects.filter(featured=True)
    return render(request, 'pages/index.html',{"categories":categories,"slider":slider,"featured_product":featured_product})


def about(request):
    return render(request, 'pages/about.html')


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

from django.http import JsonResponse
from django.core.paginator import Paginator

def shop(request, name=None):
    category = get_object_or_404(Category, name=name)
    subcategories = SubCategory.objects.filter(category=category)
    
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
            'products': list(page.object_list.values('name', 'price', 'image','id','discount','price','discounted_price')),
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
        'subcategories': subcategories,
        'products': products
    }
    return render(request, 'pages/shop.html', context)


def productdetial(request, id):
    # product = get_object_or_404(Product, id=id)
    product = Product.objects.get(id=id)

    context = {
        'product': product
    }
    return render(request, 'pages/productdetial.html', context)