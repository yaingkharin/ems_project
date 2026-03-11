from rest_framework import serializers

class PaginationResponse(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    limit = serializers.IntegerField()
    data = serializers.ListField(child=serializers.DictField())
