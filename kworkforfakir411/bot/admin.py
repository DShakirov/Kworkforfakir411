from django.contrib import admin
from django.utils.safestring import mark_safe

from .handlers.replys import send_reply_message, send_reply_photo
from .models import User, Product, Comment, Message, Reply


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['chat_id', 'user_login', 'registered_at', 'is_registered']
    list_display_links = ['chat_id', 'user_login']
    search_fields = ['chat_id', 'user_login', 'registered_at']
    readonly_fields = ['chat_id', 'user_login', 'user_password', 'is_registered']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'created_at', 'is_published', 'get_photo']
    list_display_links = [ 'name']
    search_fields = ['name', 'price']

    def get_photo(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="75">')
        else:
            return '-'
    get_photo.short_description = 'Миниатюра'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'created_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'text', 'created_at', 'get_photo']

    def get_photo(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="75">')
        else:
            return '-'
    get_photo.short_description = 'Миниатюра'


@admin.register(Reply)

class ReplyAdmin(admin.ModelAdmin):
    list_display = ['message', 'get_photo', 'created_at', 'get_photo']
    list_display_links = ['message']

# при сохранении в админке ответа, он отсылается в телеграм пользователю
    def save_model(self, request, obj, form, change):
        if not obj.image:
            send_reply_message(obj.message.user.chat_id, obj.message.message_id, obj.text)
        else:
            send_reply_photo(obj.message.user.chat_id, obj.message.message_id, obj.text, obj.image)
        super().save_model(request, obj, form, change)
    def get_photo(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="75">')
        else:
            return '-'
    get_photo.short_description = 'Миниатюра'



