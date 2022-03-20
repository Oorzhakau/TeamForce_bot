from django.contrib import admin

from .models import Subscriber, Tag, User, Message, Group


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("pk",
                    "username",
                    "first_name",
                    "last_name",
                    "phone",
                    "company",
                    "tags",)
    list_filter = ("username", "company",)
    search_fields = ("user_id", "username")
    empty_value_display = "-пусто-"


class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "tag", )
    list_filter = ("tag", )
    search_fields = ("tag", )


class MessageAdmin(admin.ModelAdmin):
    list_display = ("pk",
                    "author",
                    "text",
                    "tag",
                    "status",)
    list_filter = ("tag", "status", )
    search_fields = ("text", "created_date", )
    list_editable = ("status", )


admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(User)
admin.site.register(Group)