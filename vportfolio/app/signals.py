from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
import os
from .models import Blog,Testimonial

def delete_old_image(instance, old_image_field, **kwargs):
    """Delete old image file when the image is updated."""
    if old_image_field and os.path.isfile(old_image_field.path):
        os.remove(old_image_field.path)

@receiver(pre_save, sender=Blog)
def delete_old_blog_image_on_update(sender, instance, **kwargs):
    """Delete old blog image when a new image is uploaded."""
    try:
        old_instance = Blog.objects.get(pk=instance.pk)
    except Blog.DoesNotExist:
        return
    old_image = old_instance.image
    new_image = instance.image
    if old_image and old_image != new_image:
        delete_old_image(instance, old_image)

@receiver(pre_save, sender=Testimonial)
def delete_old_testimonial_image_on_update(sender, instance, **kwargs):
    """Delete old testimonial image when a new image is uploaded."""
    try:
        old_instance = Testimonial.objects.get(pk=instance.pk)
    except Testimonial.DoesNotExist:
        return
    old_image = old_instance.image
    new_image = instance.image
    if old_image and old_image != new_image:
        delete_old_image(instance, old_image)

@receiver(post_delete, sender=Blog)
def delete_blog_image_on_delete(sender, instance, **kwargs):
    """Delete blog image file when a blog instance is deleted."""
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)

@receiver(post_delete, sender=Testimonial)
def delete_testimonial_image_on_delete(sender, instance, **kwargs):
    """Delete testimonial image file when a testimonial instance is deleted."""
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)






