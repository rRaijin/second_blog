from django.contrib import admin
from .models import *

# class PostComments(admin.TabularInline):
#     model = Comment
#     extra = 0

class PostInline(admin.TabularInline):
    model = Post
    extra = 0

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class PostCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PostCategory._meta.fields]
    inlines = [PostInline]

    class Meta:
        model = PostCategory

admin.site.register(PostCategory, PostCategoryAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "author", "created_date", "updated_date"]
    list_display_links = ["id", "updated_date"]
    list_editable = ["title"]
    list_filter = ["created_date", "updated_date"]
    search_fields = ["title"]

    inlines = [CommentInline]

    class Meta:
        model = Post
admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ["text", "created_date"]
    search_fields = ["created_date"]

admin.site.register(Comment, CommentAdmin)
# class PostStatisticAdmin(admin.ModelAdmin):
#     list_display = ["date", "views"]
#     search_fields = ["views"]
#
#     class Meta:
#         model = PostStatistic
# admin.site.register(PostStatistic, PostStatisticAdmin)


# class CommentAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Comment._meta.fields]
#
#     class Meta:
#         model = Comment
# admin.site.register(Comment,CommentAdmin)





