import os
import django
from django.db.models import Q, Count, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Order, Product


# Create queries within functions
def get_profiles(search_string=None):
    if search_string is None:
        return ''

    full_name_query = Q(full_name__icontains=search_string)
    email_query = Q(email__icontains=search_string)
    phone_number_query = Q(phone_number__icontains=search_string)

    profiles = Profile.objects.filter(
        full_name_query | email_query | phone_number_query
    ).order_by('full_name')

    if not profiles.exists():
        return ''

    return '\n'.join(
        [f'Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.profile_orders.count()}' for p
         in profiles])


def get_loyal_profiles():
    loyal_profiles = Profile.objects.get_regular_customers()

    if not loyal_profiles.exists():
        return ''

    return '\n'.join([f'Profile: {p.full_name}, orders: {p.count_orders}' for p in loyal_profiles])


def get_last_sold_products():
    latest_order_with_products = (Order.objects
                                  .prefetch_related('products')
                                  .order_by('products__name')
                                  .last())

    if not latest_order_with_products or not latest_order_with_products.products.exists():
        return ''

    products = ', '.join([p.name for p in latest_order_with_products.products.all()])

    return f"Last sold products: {products}"


def get_top_products():
    top_products = (Product.objects
                    .prefetch_related('orders')
                    .annotate(order_count=Count('orders'))
                    .filter(order_count__gt=0)
                    .order_by('-order_count', 'name'))

    if not top_products or not top_products[0].orders.exists():
        return ''

    length_top_products = len(top_products)

    result = ['Top products:']

    if length_top_products >= 5:
        top_5_products = top_products[:5]

        result.extend(f'{p.name}, sold {p.order_count} times' for p in top_5_products)
    else:
        result.extend(f'{p.name}, sold {p.order_count} times' for p in top_products)

    return '\n'.join(result)


def apply_discounts():
    orders_to_apply = (Order.objects
                       .prefetch_related('products')
                       .annotate(count_products=Count('products'))
                       .filter(is_completed=False, count_products__gt=2))

    orders_to_apply.update(total_price=F('total_price') * 0.90)

    if not orders_to_apply:
        num_of_updated_orders = 0
    else:
        num_of_updated_orders = len(orders_to_apply)

    return f"Discount applied to {num_of_updated_orders} orders."


def complete_order():
    # Get the oldest order that is not completed
    oldest_order = Order.objects.prefetch_related('products').filter(is_completed=False).first()

    if not oldest_order:
        return ''

    # Make the order completed
    oldest_order.is_completed = True
    oldest_order.save()

    # Take all the products that have quantity and decrease it
    products_to_decrease = oldest_order.products.filter(in_stock__gt=0)
    products_to_decrease.update(in_stock=F('in_stock') - 1)

    # Get all the products without quantity and make then unavailable
    not_available_products = oldest_order.products.filter(in_stock=0)
    not_available_products.update(is_available=False)

    return "Order has been completed!"



