import os
from pprint import pprint

import django
from django.db import connection
from django.db.models import Sum, Count, Max, Q, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Product, Category, Customer, Order, OrderProduct


def product_quantity_ordered():
    result = []

    total_quantity = (Product.objects
                      .annotate(total_ordered_quantity=Sum('orderproduct__quantity'))
                      .exclude(total_ordered_quantity=None)
                      .order_by('-total_ordered_quantity'))

    for product in total_quantity:
        result.append(f'Quantity ordered of {product.name}: {product.total_ordered_quantity}')

    return '\n'.join(result)


def count_product_categories():
    categories = Product.objects.values('category').annotate(categories_count=Count('category'))

    return categories


def max_price():
    max_price_product = Product.objects.aggregate(max_price=Max('price'))

    return max_price_product


def ordered_products_per_customer():
    result = []

    orders = Order.objects.prefetch_related('orderproduct_set__product__category')

    for order in orders:
        result.append(f'Order ID: {order.id}, Customer: {order.customer.username}')
        for order_product in order.orderproduct_set.all():
            result.append(f'- Product: {order_product.product.name}, Category: {order_product.product.category.name}')

    return '\n'.join(result)


def filter_products():
    result = []

    filtered_products = Product.objects.filter(
        Q(is_available=True) & Q(price__gt=3.00)
    ).order_by('-price', 'name')

    for p in filtered_products:
        result.append(f"{p.name}: {p.price}lv.")

    return '\n'.join(result)


def give_discount():
    result = []

    query = Q(is_available=True) & Q(price__gt=3.00)

    filtered_products = Product.objects.filter(query).order_by('-price', 'name')

    filtered_products.update(price=F('price') * 0.70)

    for product in filtered_products:
        result.append(f'{product.name}: {product.price}lv.')

    return '\n'.join(result)

























