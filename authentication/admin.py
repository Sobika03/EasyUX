# authentication/admin.py
from email.quoprimime import unquote
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect, render
from django.core.exceptions import PermissionDenied
from django.urls import path
from django.contrib.admin.utils import quote

class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('must_change_password',)
    readonly_fields = UserAdmin.readonly_fields + ('must_change_password',)

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('organization', 'must_change_password')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('organization',)}),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/password/',
                self.admin_site.admin_view(self.change_password),
                name='authentication_customuser_password_change',
            ),
        ]
        return custom_urls + urls

    def change_password(self, request, object_id, form_url=''):
        user = self.get_object(request, object_id)
        if not self.has_change_permission(request, user):
            raise PermissionDenied

        if request.method == 'POST':
            form = AdminPasswordChangeForm(user, request.POST)
            if form.is_valid():
                form.save()
                if request.user.is_staff:
                    user.must_change_password = True
                    user.save()
                messages.success(request, _('Password changed successfully.'))
                return redirect('admin:authentication_customuser_changelist')
        else:
            form = AdminPasswordChangeForm(user)

        context = {
            'title': _('Change password: %s') % user.get_username(),
            'form': form,
            'is_popup': False,
            'add': False,
            'change': True,
            'has_view_permission': self.has_view_permission(request, user),
            'has_add_permission': self.has_add_permission(request),
            'has_change_permission': self.has_change_permission(request, user),
            'has_delete_permission': self.has_delete_permission(request, user),
            'original': user,
            'show_save': True,

            # ✅ Add these:
            'opts': self.model._meta,
            'object_id': quote(object_id),
        }

        return render(request, 'admin/auth/user/change_password.html', context)

admin.site.register(CustomUser, CustomUserAdmin)