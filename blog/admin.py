from django.contrib import admin
from blog.models import *
from blog import models
# Register your models here.


class CourseRecordAdmin(admin.ModelAdmin):
    list_display = ("course", "day_num", 'teacher', 'date')


class MyCourse(admin.ModelAdmin):
    list_display = ('name', 'price', 'online_price', 'brief')
    search_fields = ['name','online_price']
    list_filter = ['price']
    ordering = ['id']


admin.site.register(models.UserProfile)
admin.site.register(models.School)
admin.site.register(models.Course, MyCourse)
admin.site.register(models.ClassList)
admin.site.register(models.Customer)
admin.site.register(models.ConsultRecord)
admin.site.register(models.CourseRecord, CourseRecordAdmin)
admin.site.register(models.StudyRecord)