from django.contrib import admin

from .models import Subscriber, Tag, User, Message


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("pk",
                    "user_id",
                    "username",
                    "phone",
                    "company",
                    )
    list_filter = ("username",
                   "updated_date",
                   "company",
                   )
    search_fields = ("user_id",
                     "created_date",
                     "updated_date",
                    )
    empty_value_display = "-пусто-"


class MessageAdmin(admin.ModelAdmin):
    list_display = ("pk",
                    "author",
                    "text",
                    "status"
                    )
    list_filter = ("tag", "status", )
    search_fields = ("tag",
                     "created_date",
                     "updated_date",
                    )
    empty_value_display = "-пусто-"


class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "tag", )
    list_filter = ("tag", )
    search_fields = ("tag", "created_date", "updated_date", )
    empty_value_display = "-пусто-"
    

admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(User)