from django.contrib import admin
from .models import Tag, Category, PublicAPI


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(PublicAPI)
class PublicAPIAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'auth',
        'is_free',
        'api_url',
    )

    list_filter = (
        'category',
        'auth',
        'is_free',
    )

    search_fields = (
        'name',
        'description',
    )

    prepopulated_fields = {'slug': ('name',)}

    filter_horizontal = ('tags',)

    ordering = ('-created_at',)

    readonly_fields = ('created_at',)
