from decimal import Decimal
def calculate_cart_total(cart_dict, movies_qs):
    total = Decimal('0.00')
    for m in movies_qs:
        qty = int(cart_dict.get(str(m.id), 0))
        total += (m.price * qty)
    return total
