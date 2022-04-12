import django_tables2 as tables 
from django_tables2.export.views import ExportMixin

from .models import record

class RecordTable(tables.Table):
    name = tables.Column()
   # selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
   
    class Meta:
        model = record
        template_name = "django_tables2/bootstrap4.html"
        fields = ("record_id","company_code","functional_area","cost_center","investment_priority","assets_type","capex_type","preview_number","asset_to_be_replace","expected_inverstment_value","expected_servince_category","expected_savings_value","project_start_date","project_end_date","status","approve_status")

 