from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.response import Response

from .models import *
from .serializers import *

from django.db.models import Q
from django.shortcuts import get_object_or_404

from django.utils import timezone
from datetime import datetime, timedelta

class ItemView(APIView):
    def get(self, request):
        category_name = request.GET.get('category_name', None)
        items = Item.objects.filter(category__name=category_name)
        # items = Category.objects.prefetch_related('item_set').get(name=category).item_set

        if items.exists():
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        item_serializer = ItemSerializer(data=request.data, context={"request": request})
        
        if item_serializer.is_valid():
            request.data['category_id']
            category_instance = get_object_or_404(Category, id=request.data['category_id'])
            item_serializer.save(category=category_instance)
            return Response(item_serializer.data, status=status.HTTP_200_OK)
        
        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ItemOrderView(APIView):
    def get(self, request):

        order_id = self.request.query_params.get('order_id')
        item_order = ItemOrder.objects.filter(
            Q(order__order_date__gt=timezone.now()-timedelta(days=7)) &
            Q(order_id=order_id)
        )

        # item_order = ItemOrder.objects.filter(
        #     Q(order__order_date__range=(timezone.now()-timedelta(days=7), timezone.now())) &
        #     Q(order_id=order_id)
        # )

        if item_order.exists():
            serializer = ItemOrderSerializer(item_order, many=True)
            return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)
        