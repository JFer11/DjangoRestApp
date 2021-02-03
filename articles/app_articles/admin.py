from django.contrib import admin

"""
There are two ways to load our CustomUser to the Admin page, as a Django User.
1)
from django.contrib.auth import get_user_model
User = get_user_model()
admin.site.register(User)

2)
"""
from .models import CustomUser
admin.site.register(CustomUser)
