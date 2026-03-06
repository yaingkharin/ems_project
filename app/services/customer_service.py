from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone
from app.models.customer import Customer
from app.dto.responses.customer_response import CustomerResponse


class CustomerService:
    @staticmethod
    def create_customer(request_data: dict) -> dict:
        customer = Customer.objects.create(
            username=request_data['username'],
            gmail=request_data['gmail'],
            password=request_data['password']
        )
        return CustomerResponse(customer).data

    @staticmethod
    def get_customer_by_id(customer_id: int) -> Optional[dict]:
        try:
            customer = Customer.objects.get(id=customer_id)
            return CustomerResponse(customer).data
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all_customers() -> List[dict]:
        customers = Customer.objects.all()
        return [CustomerResponse(c).data for c in customers]

    @staticmethod
    def update_customer(customer_id: int, request_data: dict) -> Optional[dict]:
        try:
            customer = Customer.objects.get(id=customer_id)
            customer.username = request_data.get('username', customer.username)
            customer.gmail = request_data.get('gmail', customer.gmail)
            customer.password = request_data.get('password', customer.password)
            customer.save()
            return CustomerResponse(customer).data
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_customer(customer_id: int) -> bool:
        try:
            customer = Customer.objects.get(id=customer_id)
            customer.is_deleted = True
            customer.deleted_at = timezone.now()
            customer.save()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def force_delete_customer(customer_id: int) -> bool:
        """
        Permanently delete a customer from the database.
        Use with caution - this action cannot be undone.
        """
        try:
            customer = Customer.objects.get(id=customer_id)
            customer.delete()  # Hard delete
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def get_paginated_customers(validated_data: dict) -> dict:
        page = validated_data.get('page', 1)
        limit = validated_data.get('limit', 100)
        sort_by = validated_data.get('sort_by', 'id')
        sort_order = validated_data.get('sort_order', 'asc')
        search = validated_data.get('search', None)

        queryset = Customer.objects.all()

        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(gmail__icontains=search)
            )

        if sort_order.lower() == 'desc':
            sort_by = f'-{sort_by}'
        queryset = queryset.order_by(sort_by)

        paginator = Paginator(queryset, limit)
        try:
            paginated = paginator.page(page)
        except PageNotAnInteger:
            paginated = paginator.page(1)
        except EmptyPage:
            paginated = paginator.page(paginator.num_pages)

        data = [CustomerResponse(c).data for c in paginated.object_list]

        return {
            'data': data,
            'total': paginator.count,
            'page': paginated.number,
            'limit': limit,
        }
