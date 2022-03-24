from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NewUser

# Register your models here.
class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('username', 'email', 'first_name', 'tz')
    list_filer = ('username', 'email', 'first_name', 'is_active','is_staff', 'tz')
    ordering = ('-start_date',)
    list_display = ('username','email','first_name','is_active','is_staff', 'tz')
    fieldsets = (
        (None, {'fields':('username','email','first_name')}),
        ('Permissions', {'fields':('is_staff', 'is_active')}),
        ('Personal', {'fields':('tz',)}),
    )
    add_fiedsets = (
        (None, {
            'classes' : ('wide',),
            'fields' : ('username', 'email', 'first_name', 'password1', 'password2', 'is_active', 'is_staff')
        })
    )

admin.site.register(NewUser, UserAdminConfig)
    