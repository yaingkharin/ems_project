from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from app.models.test import Test
from app.dto.requests.test_request import CreateTestRequest
from app.dto.responses.test_response import TestResponse


class TestService:
    @staticmethod
    def create_test(data: dict) -> TestResponse:
        test = Test.objects.create(**data)
        return TestResponse(test).data

    @staticmethod
    def get_test_by_id(test_id: int) -> Optional[TestResponse]:
        try:
            test = Test.objects.get(id=test_id)
            return TestResponse(test).data
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all_tests() -> List[TestResponse]:
        tests = Test.objects.all()
        return [TestResponse(test).data for test in tests]

    @staticmethod
    def update_test(test_id: int, data: dict) -> Optional[TestResponse]:
        try:
            test = Test.objects.get(id=test_id)
            for key, value in data.items():
                if value is not None:
                    setattr(test, key, value)
            test.save()
            return TestResponse(test).data
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_test(test_id: int) -> bool:
        try:
            test = Test.objects.get(id=test_id)
            test.delete()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def get_paginated_tests(validated_data: dict) -> dict:
        """
        Get paginated tests with optional filtering and searching.
        """
        page = validated_data.get('page', 1)
        limit = validated_data.get('limit', 100)
        sort_by = validated_data.get('sort_by', 'id')
        sort_order = validated_data.get('sort_order', 'asc')
        search = validated_data.get('search', None)
        filters = validated_data.get('filters', {})

        queryset = Test.objects.all()

        # Apply filters
        if filters:
            queryset = queryset.filter(**filters)

        # Searching
        if search:
            queryset = queryset.filter(
                Q(test_name__icontains=search) |
                Q(description__icontains=search)
            )

        # Sorting
        if sort_order.lower() == 'desc':
            sort_by = f'-{sort_by}'
        queryset = queryset.order_by(sort_by)

        paginator = Paginator(queryset, limit)
        try:
            paginated_tests = paginator.page(page)
        except PageNotAnInteger:
            paginated_tests = paginator.page(1)
        except EmptyPage:
            paginated_tests = paginator.page(paginator.num_pages)

        tests_data = [TestResponse(t).data for t in paginated_tests.object_list]

        return {
            'data': tests_data,
            'total': paginator.count,
            'page': paginated_tests.number,
            'limit': limit,
        }