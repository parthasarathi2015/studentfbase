from django.contrib import admin
from .models import Student, Classroom,Subject, MarksObtain

# Register your models here.
admin.site.register(Student)
admin.site.register(Classroom)
admin.site.register(Subject)
admin.site.register(MarksObtain)
