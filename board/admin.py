from django.contrib import admin
from .models import Bb, Category, AdvUser
from .models import SuperCategory, SubRubric, AdditionalImage
from .forms import SubRubricForm


class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage


class BbAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'published', 'category', 'author', 'slug', 'views')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content')
    fields = (('category', 'author'), 'title', 'content', 'price', 'contacts', 'image', 'is_active', 'slug')
    inlines = (AdditionalImageInline,)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Bb, BbAdmin)
admin.site.register(Category)
admin.site.register(AdvUser)


class SubRubricInline(admin.TabularInline):
    model = SubRubric


class SuperCategoryAdmin(admin.ModelAdmin):
    exclude = ('super_category',)
    inlines = (SubRubricInline,)


admin.site.register(SuperCategory, SuperCategoryAdmin)


class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm


admin.site.register(SubRubric, SubRubricAdmin)
