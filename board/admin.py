from django.contrib import admin
from .models import Bb, Category, AdvUser


class BbAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'published', 'category')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content')


admin.site.register(Bb, BbAdmin)
admin.site.register(Category)
admin.site.register(AdvUser)
