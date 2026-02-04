from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save,post_delete
from .models import Loan,Book

@receiver(pre_save,sender=Loan)
def store_prev_returned_state(sender,instance,**kwargs):
        if instance.pk:
            instance._prev_returned=sender.objects.get(pk=instance.pk).returned
        else:
            instance._prev_returned=None

@receiver(post_save,sender=Loan)
def update_available_copies_on_save(sender,instance,created,**kwargs):
    book=instance.book

    # New loan
    if created:
        if book.available_copies <=0:
            raise ValueError("No copies available for this book")
        book.available_copies -= 1
        book.save()
    elif instance._prev_returned is False and instance.returned is True:
        book.available_copies += 1
        book.save()

@receiver(post_delete,sender=Loan)
def restore_available_copies_on_delete(sender,instance,**kwargs):
     book=instance.book
     if not instance.returned:
            book.available_copies += 1
            book.save()