from django.db import transaction

def update_cart(cart, product_id, quantity, action):
    """
    Update the user's shopping cart by adding or removing items.

    Parameters:
    - cart: The Cart object for the user.
    - product_id: The product to add or remove.
    - quantity: The number of items to add or remove.
    - action: "add" to add the item, "remove" to remove the item.
    """
    from .models import CartItem  # Import CartItem model

    with transaction.atomic():
        try:
            # Check if the item already exists in the cart
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)

            if action == "add":
                cart_item.quantity += quantity
                cart_item.save()

            elif action == "remove":
                cart_item.quantity -= quantity
                if cart_item.quantity <= 0:
                    cart_item.delete()
                else:
                    cart_item.save()

        except CartItem.DoesNotExist:
            # If the item doesn't exist and action is "add", create a new one
            if action == "add":
                CartItem.objects.create(cart=cart, product_id=product_id, quantity=quantity)
            elif action == "remove":
                raise ValueError("Item not found in the cart to remove.")

    return cart


