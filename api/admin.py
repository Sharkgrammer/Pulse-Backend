from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms

from .models import User, Post, Follow, Like


# USER ADMIN
class AddUserForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        else:
            print("test thing")

        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password2"))
        if commit:
            user.save()
        return user


class UpdateUserForm(forms.ModelForm):
    """
    Update User Form. Doesn't allow changing password in the Admin.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'email', 'password', 'username', 'first_name', 'last_name', 'prof_image', 'prof_desc', 'followers',
            'following', 'is_active', 'is_staff', 'date_joined', 'last_login'
        )

    def clean_password(self):
        # Password can't be changed in the admin
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UpdateUserForm
    add_form = AddUserForm

    list_display = (
        'id', 'email', 'username', 'first_name', 'last_name', 'followers', 'following', 'is_active', 'is_staff',
        'date_joined', 'last_login')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        ('Personal Info', {'fields': ('first_name', 'last_name', 'username', 'email', 'password')}),
        ('Profile Data', {'fields': ('followers', 'following', 'prof_image', 'prof_desc')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
        ('Spare Data', {'fields': ('field1', 'field2', 'field3', 'field4', 'field5')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email', 'first_name', 'last_name', 'username', 'prof_desc', 'password1',
                    'password2'
                )
            }
        ),
    )
    search_fields = ('id', 'username', 'email', 'first_name', 'last_name')
    ordering = ('-id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login')


admin.site.register(User, UserAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'created_by', 'content', 'likes', 'comments', 'shares', 'image_post', 'status', 'created_date',
        'last_edit', 'last_update', 'deleted')
    search_fields = ('id', 'created_by', 'content', 'template_id')
    ordering = ('-id',)
    list_filter = ('image_post', 'status', 'deleted')

    fieldsets = (
        ('Post Data', {'fields': (
            'created_by', 'created_date', 'last_edit', 'last_update', 'content', 'likes', 'comments', 'shares',
            'status', 'image_post', 'image_contents', 'deleted')}),
        ('Spare Data', {'fields': ('field1', 'field2', 'field3', 'field4', 'field5')}),
    )


admin.site.register(Post, PostAdmin)


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'created_by', 'following', 'created_date', 'last_update', 'deleted')
    search_fields = ('id', 'created_by', 'following', 'created_date')
    list_filter = ("deleted",)
    ordering = ('-id',)

    fieldsets = (
        ('Follows Data', {'fields': (
            'created_by', 'following', 'created_date', 'last_update', 'deleted')}),
        ('Spare Data', {'fields': ('field1', 'field2', 'field3', 'field4', 'field5')}),
    )


admin.site.register(Follow, FollowAdmin)


class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'created_by', 'post', 'created_date', 'last_update', 'deleted')
    search_fields = ('id', 'created_by', 'post', 'created_date')
    list_filter = ("deleted",)
    ordering = ('-id',)

    fieldsets = (
        ('Likes Data', {'fields': (
            'created_by', 'post', 'created_date', 'last_update', 'deleted')}),
        ('Spare Data', {'fields': ('field1', 'field2', 'field3', 'field4', 'field5')}),
    )


admin.site.register(Like, LikeAdmin)
