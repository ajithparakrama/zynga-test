from django.contrib import admin

from .models import record, Plan_Type, Functional_area, Investment_priority, Assets_Type, Capex_Type, Expected_Servince, Status,Approve_Status,User

admin.site.register(User)
admin.site.register(record)
admin.site.register(Plan_Type)
admin.site.register(Functional_area)
admin.site.register(Investment_priority)
admin.site.register(Assets_Type)
admin.site.register(Capex_Type)
admin.site.register(Expected_Servince)
admin.site.register(Status)
admin.site.register(Approve_Status)
