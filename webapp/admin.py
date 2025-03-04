from django.contrib import admin


# Register your models here.

from . models import Record

admin.site.register(Record)


from django.contrib import admin
from .models import Question, Answer

admin.site.register(Question)
admin.site.register(Answer)








