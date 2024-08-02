from django.contrib import admin
from users.models import User, EmailVerification

# Register your models here.
admin.site.register(User)

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('created', )
    