from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
import os
from .models import Category, SubCategory, Product,Advertisment

def delete_old_image(instance, old_image_field, **kwargs):
    """Delete old image file when the image is updated."""
    if old_image_field and os.path.isfile(old_image_field.path):
        os.remove(old_image_field.path)

@receiver(pre_save, sender=Category)
def delete_old_category_image_on_update(sender, instance, **kwargs):
    """Delete old category image when a new image is uploaded."""
    try:
        old_instance = Category.objects.get(pk=instance.pk)
    except Category.DoesNotExist:
        return
    old_image = old_instance.image
    new_image = instance.image
    if old_image and old_image != new_image:
        delete_old_image(instance, old_image)

@receiver(pre_save, sender=SubCategory)
def delete_old_subcategory_image_on_update(sender, instance, **kwargs):
    """Delete old subcategory image when a new image is uploaded."""
    try:
        old_instance = SubCategory.objects.get(pk=instance.pk)
    except SubCategory.DoesNotExist:
        return
    old_image = old_instance.image
    new_image = instance.image
    if old_image and old_image != new_image:
        delete_old_image(instance, old_image)

@receiver(pre_save, sender=Product)
def delete_old_product_image_on_update(sender, instance, **kwargs):
    """Delete old product image when a new image is uploaded."""
    try:
        old_instance = Product.objects.get(pk=instance.pk)
    except Product.DoesNotExist:
        return
    old_image = old_instance.image
    new_image = instance.image
    if old_image and old_image != new_image:
        delete_old_image(instance, old_image)

@receiver(post_delete, sender=Category)
def delete_category_image_on_delete(sender, instance, **kwargs):
    """Delete category image file when a Category instance is deleted."""
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)

@receiver(post_delete, sender=SubCategory)
def delete_subcategory_image_on_delete(sender, instance, **kwargs):
    """Delete subcategory image file when a SubCategory instance is deleted."""
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)

@receiver(post_delete, sender=Product)
def delete_product_image_on_delete(sender, instance, **kwargs):
    """Delete product image file when a Product instance is deleted."""
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)


@receiver(pre_save, sender=Advertisment)
def delete_old_advertisment_image_on_update(sender, instance, **kwargs):
    """Delete old category image when a new image is uploaded."""
    try:
        old_instance = Advertisment.objects.get(pk=instance.pk)
    except Advertisment.DoesNotExist:
        return
    old_image = old_instance.image
    new_image = instance.image
    if old_image and old_image != new_image:
        delete_old_image(instance, old_image)

@receiver(post_delete, sender=Advertisment)
def delete_advertisement_image_on_delete(sender, instance, **kwargs):
    """Delete product image file when a Product instance is deleted."""
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)