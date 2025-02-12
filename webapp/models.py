from django.db import models

from django.db import models

class Record(models.Model):

    creation_date = models.DateTimeField(auto_now_add=True)

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    email = models.CharField(max_length=225)

    phone = models.CharField(max_length=20)

    address = models.CharField(max_length=300)

    city = models.CharField(max_length=225)

    province = models.CharField(max_length=200)

    country = models.CharField(max_length=125)


from django.contrib.auth.hashers import make_password, check_password

class Admin(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)  # You should hash passwords
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Hash only when creating a new user
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username






class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    attachment = models.FileField(upload_to='assignments/', blank=True, null=True)  # Allow document uploads
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
