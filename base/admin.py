from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import record, Plan_Type, Functional_area, Investment_priority, Assets_Type, Capex_Type, Expected_Servince, Status,Approve_Status,User

admin.site.register(User,SimpleHistoryAdmin)
admin.site.register(record,SimpleHistoryAdmin)
admin.site.register(Plan_Type,SimpleHistoryAdmin)
admin.site.register(Functional_area,SimpleHistoryAdmin)
admin.site.register(Investment_priority,SimpleHistoryAdmin)
admin.site.register(Assets_Type,SimpleHistoryAdmin)
admin.site.register(Capex_Type,SimpleHistoryAdmin)
admin.site.register(Expected_Servince,SimpleHistoryAdmin)
admin.site.register(Status,SimpleHistoryAdmin)
admin.site.register(Approve_Status,SimpleHistoryAdmin)
