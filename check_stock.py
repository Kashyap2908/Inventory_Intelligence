from inventory.models import ExpiryStock, Product
from django.contrib.auth.models import User

p = Product.objects.first()
print(f'Product: {p.name}')
print(f'Total Stock: {p.total_stock}')

stocks = ExpiryStock.objects.filter(product=p)
print(f'\nTotal ExpiryStock entries: {stocks.count()}')

for s in stocks[:10]:
    print(f'  - Quantity: {s.quantity}, User: {s.user}, Expiry: {s.expiry_date}')

print(f'\nUser-specific stock:')
for user in User.objects.all()[:5]:
    user_stock = p.get_user_stock(user)
    if user_stock > 0:
        print(f'  {user.username}: {user_stock} units')
