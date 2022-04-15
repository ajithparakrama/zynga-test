import django_tables2 as tables 
from django_tables2.export.views import ExportMixin
from django_filters import Filter
from django_tables2.utils import A
from .models import record
from .filters import RecordsFilter

class RecordTable(tables.Table, Filter):
    Action =tables.LinkColumn('editrecord',text='Edit', args=[A('pk')], orderable=False)
   # selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
   
    class Meta:
        model = record
        template_name = "django_tables2/bootstrap4.html"
        edit = tables.LinkColumn('base:editrecord', text='static text', orderable=False, args=[A('pk')])
        fields = ("record_id","company_code","functional_area","cost_center","investment_priority","assets_type","capex_type","preview_number","asset_to_be_replace","expected_inverstment_value","expected_servince_category","expected_savings_value","project_start_date","project_end_date","status","approve_status")

class RecordTableAdmin(tables.Table, Filter):
    Action =tables.LinkColumn('approverecord',text='Approve', args=[A('pk')], orderable=False)
   # selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
   
    class Meta:
        model = record
        template_name = "django_tables2/bootstrap4.html"
        edit = tables.LinkColumn('base:editrecord', text='static text', orderable=False, args=[A('pk')])
        fields = ("record_id","company_code","functional_area","cost_center","investment_priority","assets_type","capex_type","preview_number","asset_to_be_replace","expected_inverstment_value","expected_servince_category","expected_savings_value","project_start_date","project_end_date","status","approve_status")
