from django.contrib import admin
from .models import Loan,Staff, StaffFile


class LoanAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'duration', 'approval_status', 'payment_status', 'create_time']


class StaffAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'department', 'created_at']


class StaffFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'file_name', 'uploaded_at']


admin.site.register(Loan, LoanAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(StaffFile, StaffFileAdmin)

