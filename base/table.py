import django_tables2 as tables 
from django_tables2.export.views import ExportMixin
from django_filters import Filter
from django_tables2.utils import A
from .models import record, User
#from .filters import RecordsFilter

class RecordTable(tables.Table, Filter):
    Action =tables.LinkColumn('editrecord',text='Edit', args=[A('pk')], orderable=False)
   # selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
   
    class Meta:
        model = record 
        template_name = "django_tables2/bootstrap4.html"
        edit = tables.LinkColumn('base:editrecord', text='static text', orderable=False, args=[A('pk')])
        fields = ("record_id","create_by", "company_code","functional_area","cost_center","investment_priority","assets_type","capex_type","preview_number","asset_to_be_replace","expected_inverstment_value","expected_servince_category","expected_savings_value","project_start_date","project_end_date","status","created", "approve_status")

class RecordTableAdmin(tables.Table, Filter):
    Action =tables.LinkColumn('approverecord',text='Approve', args=[A('pk')], orderable=False)
   # selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
   
    class Meta:
        model = record
        attrs = {
            "th" : {
                "_ordering": {
                    "orderable": "sortable", # Instead of `orderable`
                    "ascending": "ascend",   # Instead of `asc`
                    "descending": "descend"  # Instead of `desc`
                }
            }
        }
        template_name = "django_tables2/bootstrap4.html"
        edit = tables.LinkColumn('base:editrecord', text='static text', orderable=False, args=[A('pk')])
        fields = ("record_id","create_by","company_code","functional_area","cost_center","investment_priority","assets_type","capex_type","preview_number","asset_to_be_replace","expected_inverstment_value","expected_servince_category","expected_savings_value","project_start_date","project_end_date","status","created", "approve_status")


class AdminUsers(tables.Table, Filter):
    model = User
    template_name =   "django_tables2/bootstrap4.html"
  #  edit = tables.LinkColumn('base:editrecord', text='static text', orderable=False, args=[A('pk')])
    fields =  ("username","username","first_name","last_name","email") 
    
class PersonTable(tables.Table): 
    Action =tables.LinkColumn('approverecord',text='Approve', args=[A('pk')], orderable=False)
    class Meta:
        model = record
        template_name = "django_tables2/bootstrap4.html" 
        fields = ("record_id","create_by","company_code","functional_area","cost_center","investment_priority","assets_type","capex_type","preview_number","asset_to_be_replace","expected_inverstment_value","expected_servince_category","expected_savings_value","project_start_date","project_end_date","status","created", "approve_status")

     