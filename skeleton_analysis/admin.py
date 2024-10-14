# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, GaitParameter, HistoryRecord, IssueAndSuggestion
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class CustomUserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'date_of_birth', 'gender', 'role', 'is_active')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on the user, but replaces the password field with admin's password hash display field."""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'date_of_birth', 'gender', 'role', 'is_active')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value. This is done here, so that the password won't be changed in the admin.
        return self.initial["password"]

class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # The fields to be used in displaying the User model.
    list_display = ('username', 'date_of_birth', 'gender', 'role', 'is_active')
    list_filter = ('is_active', 'role')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('date_of_birth', 'gender', 'role', 'notes')}),
        ('Permissions', {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'date_of_birth', 'gender', 'role', 'notes', 'password1', 'password2', 'is_active'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()

# Now register the new CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(GaitParameter)
class GaitParameterAdmin(admin.ModelAdmin):
    list_display = ['gait_parameter_id', 'measurement_time', 'video_name', 'json_name', 'user_name', 
                    'average_step_time', 'average_stride_length', 'movement_speed', 'stance', 'health_value']
    search_fields = ['user_name', 'video_name']
    list_filter = ['measurement_time']


@admin.register(HistoryRecord)
class HistoryRecordAdmin(admin.ModelAdmin):
    list_display = ['record_id', 'user', 'gait_parameter', 'issue_id', 'record_time']
    search_fields = ['user__username', 'gait_parameter__video_name']
    list_filter = ['record_time']

@admin.register(IssueAndSuggestion)
class IssueAndSuggestionAdmin(admin.ModelAdmin):
    list_display = ['issue_id', 'issue_name', 'record', 'suggestion']
    search_fields = ['issue_name']
    list_filter = ['record__record_time']
