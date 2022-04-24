import django_filters

from .models import record

class RecordsFilter(django_filters.FilterSet):
    class Meta:
        model = record
        #fields = ['record_id',]
        fields = ["record_id","create_by","company_code","functional_area","cost_center","investment_priority","assets_type","capex_type","preview_number","asset_to_be_replace","expected_inverstment_value","expected_servince_category","expected_savings_value","project_start_date","project_end_date","status","created", "approve_status"]
