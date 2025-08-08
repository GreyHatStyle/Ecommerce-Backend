from typing import Dict

from account.models import AddressTypeChoices, User, UserAddress


def get_delivery_address(user: User, address_data: Dict | None) -> str | None:
    """
    Will return a formatted address for `delivery_address` field in **Order** table.\n
    If `address_data` is empty then use the default address of user.

    Args:
        user (User): User who is ordering.
        address_data (Dict): Address data of user from **UserAddress** Table

    Returns:
        str: Either formatted address in *string* form. or..\n
        None: (if address not found or some unexpected error occur)
    """
    if address_data:
        return f"{address_data['main_address']}, {address_data['city']}, {address_data['state']}, {address_data['country']} - {address_data['pincode']}"
        
    try:
        user_address = UserAddress.objects.filter(
            user=user, 
            address_type=AddressTypeChoices.HOME
        ).first()
        
        if user_address:
            return f"{user_address.main_address}, {user_address.city}, {user_address.state}, {user_address.country} - {user_address.pincode}"
        
        
        # If no Home address, get any address
        user_address = UserAddress.objects.filter(user=user).first()
        if user_address:
            return f"{user_address.main_address}, {user_address.city}, {user_address.state}, {user_address.country} - {user_address.pincode}"
        
        return None
    
    except Exception as e:
        print(f"System error in checkout_utils.py -> get_delivery_address method: {e}")
        return None