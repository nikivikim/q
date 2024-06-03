from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from users.models import Indicator, IndicatorValue, Balance, ActivityType

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    pass

@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

admin.site.register(IndicatorValue)
admin.site.register(Balance)
admin.site.register(ActivityType)