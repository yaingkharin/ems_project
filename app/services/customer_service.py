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
            first_name=request_data.get('first_name'),
            last_name=request_data.get('last_name'),
            email=request_data['email'],
            picture=request_data.get('picture'),
            email_verified=request_data.get('email_verified', False)
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
            customer.first_name = request_data.get('first_name', customer.first_name)
            customer.last_name = request_data.get('last_name', customer.last_name)
            customer.email = request_data.get('email', customer.email)
            customer.picture = request_data.get('picture', customer.picture)
            customer.status = request_data.get('status', customer.status)
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
    def get_paginated_customers(validated_data: dict) -> dict:
        page = validated_data.get('page', 1)
        limit = validated_data.get('limit', 100)
        sort_by = validated_data.get('sort_by', 'id')
        sort_order = validated_data.get('sort_order', 'asc')
        search = validated_data.get('search', None)

        queryset = Customer.objects.all()

        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
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
