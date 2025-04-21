from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from .models import Application

@receiver(pre_delete, sender=Application)
def delete_files_on_delete(sender, instance, **kwargs):
    file_fields = [instance.passport, instance.diploma_transcript, instance.diploma_copy, instance.image, instance.certificate]

    for file_field in file_fields:
        if file_field and file_field.name:
            if default_storage.exists(file_field.name):
                default_storage.delete(file_field.name)
