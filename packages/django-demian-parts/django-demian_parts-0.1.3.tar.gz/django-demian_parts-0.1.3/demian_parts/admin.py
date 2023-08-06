from django.contrib import admin
from .models import Type4, Type3, Type2, Type1


class Type4Admin(admin.ModelAdmin):
    list_display = ('h1', 'activate')


class Type3Admin(admin.ModelAdmin):
    list_display = ('h2', 'activate')


class Type2Admin(admin.ModelAdmin):
    list_display = ('h2', 'activate')


class Type1Admin(admin.ModelAdmin):
    list_display = ('h2', 'activate')


admin.site.register(Type4, Type4Admin)
admin.site.register(Type3, Type3Admin)
admin.site.register(Type2, Type2Admin)
admin.site.register(Type1, Type1Admin)
