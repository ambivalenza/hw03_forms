from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Post, Group


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "pub_date", "author")
    search_fields = ("text",)
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"


class GroupAdmin(ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug', 'description')
    search_fields = ('title', 'description')
    empty_value_display = "-пусто-"


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
