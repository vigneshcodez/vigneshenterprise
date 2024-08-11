from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from ckeditor.fields import RichTextField

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, mobilenumber, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, mobilenumber=mobilenumber, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, mobilenumber, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, mobilenumber, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    mobilenumber = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobilenumber']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='categories/')
    product_count = models.IntegerField(default=0)
    subcategory_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='subcategories/')
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    product_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Slider(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='slider/')
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    specification = RichTextField(blank=True, null=True)
    information = RichTextField(blank=True, null=True)
    discount = models.IntegerField()
    stock = models.IntegerField()
    price = models.IntegerField()
    discounted_price = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"

    def get_total(self):
        total = sum(item.get_total_price() for item in self.items.all())
        return total

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_price(self):
        return self.product.discounted_price * self.quantity

@receiver(post_save, sender=Product)
def update_product_count(sender, instance, created, **kwargs):
    if created:
        category = instance.category
        category.product_count += 1
        category.save()

        subcategory = instance.subcategory
        if subcategory:
            subcategory.product_count += 1
            subcategory.save()
    else:
        old_instance = Product.objects.get(pk=instance.pk)
        if old_instance.category != instance.category:
            old_category = old_instance.category
            old_category.product_count -= 1
            old_category.save()

            new_category = instance.category
            new_category.product_count += 1
            new_category.save()

        if old_instance.subcategory != instance.subcategory:
            if old_instance.subcategory:
                old_subcategory = old_instance.subcategory
                old_subcategory.product_count -= 1
                old_subcategory.save()

            if instance.subcategory:
                new_subcategory = instance.subcategory
                new_subcategory.product_count += 1
                new_subcategory.save()

@receiver(pre_save, sender=Product)
def calculate_discounted_price(sender, instance, **kwargs):
    if instance.price and instance.discount:
        instance.discounted_price = instance.price - (instance.price * instance.discount / 100)
    else:
        instance.discounted_price = instance.price

@receiver(post_delete, sender=Product)
def decrease_product_count(sender, instance, **kwargs):
    category = instance.category
    category.product_count -= 1
    category.save()

    subcategory = instance.subcategory
    if subcategory:
        subcategory.product_count -= 1
        subcategory.save()

@receiver(post_save, sender=SubCategory)
def update_subcategory_count(sender, instance, created, **kwargs):
    if created:
        category = instance.category
        category.subcategory_count += 1
        category.save()

@receiver(post_delete, sender=SubCategory)
def decrease_subcategory_count(sender, instance, **kwargs):
    category = instance.category
    category.subcategory_count -= 1
    category.save()

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    postal_code = models.CharField(max_length=20)


    def __str__(self):
        return f"{self.address_line1}, {self.city}, {self.postal_code}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)

    def update_status(self, new_status):
        if self.status == 'CANCELLED' and new_status != 'CANCELLED':
            raise ValueError('Cannot change status from CANCELLED')
        elif self.status != 'CANCELLED' and new_status == 'CANCELLED':
            self._restore_stock()
        self.status = new_status
        self.save()

    def _restore_stock(self):
        for item in self.order_items.all():
            item.product.stock += item.quantity
            item.product.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.pk is None:  # If this is a new order item
            self.product.stock -= self.quantity
            self.product.save()
        super().save(*args, **kwargs)