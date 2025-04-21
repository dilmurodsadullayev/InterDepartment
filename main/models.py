from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ImageField, ForeignKey
from phonenumber_field.modelfields import PhoneNumberField
import re
from django.core.exceptions import ValidationError
from datetime import date



# Create your models here
class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    birthdate = models.DateField()
    phone_number = PhoneNumberField(unique=True, region="UZ")

    def clean(self):
        super().clean()

        if self.birthdate > date.today():
            raise ValidationError("Tug'ilgan sana kelajakda bo'lishi mumkin emas.")

        min_age = 18
        age = date.today().year - self.birthdate.year
        if (date.today().month, date.today().day) < (self.birthdate.month, self.birthdate.day):
            age -= 1
        if age < min_age:
            raise ValidationError(f"Yosh kamida {min_age} yosh bo'lishi kerak.")



class Programme(models.Model):
    name = models.CharField(max_length=35)

    def __str__(self):
        return self.name


class Faculty(models.Model):
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    faculty_name = models.CharField(max_length=120)

    def __str__(self):
        return f"{str(self.programme.name)} | {self.faculty_name}"




def validate_passport(value):
    if not re.match(r'^[A-Z]{2}\d{7}$', value):
        raise ValidationError("Pasport seriyasi va raqami noto‘g‘ri formatda.")



# Faylning maksimal hajmini tekshirish funksiyasi
def validate_file_size(file):
    max_size_kb = 5120
    if file.size > max_size_kb * 1024:
        raise ValidationError(f"Fayl hajmi {max_size_kb} KB dan oshmasligi kerak.")

# Ruxsat etilgan fayl turlarini tekshirish funksiyasi
def validate_file_extension(file, allowed_extensions):
    ext = file.name.split('.')[-1].lower()
    if ext not in allowed_extensions:
        raise ValidationError(f"Fayl turi noto'g'ri. Faqat {', '.join(allowed_extensions)} ruxsat etiladi.")

# Ruxsat etilgan rasm formatlarini tekshirish
def validate_image_extension(file):
    validate_file_extension(file, allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])

# Ruxsat etilgan hujjat formatlarini tekshirish
def validate_document_extension(file):
    validate_file_extension(file, allowed_extensions=['pdf', 'jpg', 'png'])


class Application(models.Model):
    APPLICATION_STATUS = [
        ('submitted', 'Submitted'),
        ('under review', 'Under review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    programme = models.ForeignKey(Programme, on_delete=models.SET_NULL, null=True,blank=True)
    faculty = models.ForeignKey(Faculty,on_delete=models.SET_NULL, null=True,blank=True)
    passport_serial = models.CharField(
        max_length=9,
        validators=[validate_passport],
        help_text="Pasport seriyasi va raqami, masalan: AA1234567"
    )
    passport = models.FileField(
        upload_to='passport_images',
        validators=[validate_file_size, validate_document_extension]
    )
    diploma_transcript = models.FileField(
        upload_to='diplomas_transcripts',
        validators=[validate_file_size, validate_document_extension]
    )
    diploma_copy = models.FileField(
        upload_to='diplomas_copies',
        validators=[validate_file_size, validate_document_extension]
    )
    image = models.ImageField(
        upload_to='images',
        validators=[validate_file_size, validate_image_extension]
    )
    certificate = models.FileField(
        upload_to='certificates',
        validators=[validate_file_size, validate_document_extension],
    null = True, blank = True
    )
    status = models.CharField(max_length=50,choices=APPLICATION_STATUS,default='submitted')
    timestamp = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{'Ariza yuborildi' if self.passport_serial else 'None'}"


class ApplicationUser(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.user.username)} {'Ariza yubordi' if self.application else 'None'}"


class ApplicationIssue(models.Model):
    application_user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)
    message = models.TextField()  # Kamchilik matni
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)  # Hal qilindimi yoki yo‘q

    def __str__(self):
        return f"Kamchilik: {self.message[:30]}"