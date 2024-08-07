from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

from .models import Category,SubCategory,Product

@receiver(post_delete, sender=Category)
def delete_image_on_model_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(post_delete, sender=SubCategory)
def delete_image_on_model_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(post_delete, sender=Product)
def delete_image_on_model_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

