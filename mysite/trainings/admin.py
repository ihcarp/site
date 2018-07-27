from django.contrib import admin
from .models import Language,Topic, Post,Feedback

admin.site.register(Language)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Feedback)
