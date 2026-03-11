from rest_framework import serializers

class PaginationRequest(serializers.Serializer):
    page = serializers.IntegerField(required=False, default=1, help_text="Page number")
    limit = serializers.IntegerField(required=False, default=100, help_text="Number of results per page")
    sort_by = serializers.CharField(required=False, default='id', help_text="Field to sort by")
    sort_order = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='asc', help_text="Sort order (asc/desc)")
    search = serializers.CharField(required=False, allow_blank=True, default=None, help_text="Search term")
    filters = serializers.JSONField(required=False, default=dict, help_text="JSON object for additional filter parameters")
