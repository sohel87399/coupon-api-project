from typing import Dict
from datetime import datetime
# Import models from the models file
from models import Coupon, UserContext, Cart

# In-memory storage
coupon_db: Dict[str, Coupon] = {}

class CouponService:
    @staticmethod
    def create_coupon(coupon: Coupon):
        coupon.code = coupon.code.upper()
        coupon_db[coupon.code] = coupon
        return coupon.code

    @staticmethod
    def list_all():
        return list(coupon_db.values())

    @staticmethod
    def is_eligible(coupon: Coupon, user: UserContext, cart: Cart) -> bool:
        now = datetime.now()
        
        # 1. Date Validity
        if not (coupon.startDate <= now <= coupon.endDate):
            return False

        # 2. Usage Limit
        if coupon.usageLimitPerUser is not None:
            usage_count = user.pastCouponUsage.get(coupon.code, 0)
            if usage_count >= coupon.usageLimitPerUser:
                return False

        rules = coupon.eligibility
        if not rules:
            return True 

        # 3. User Attributes
        if rules.allowedUserTiers and user.tier not in rules.allowedUserTiers:
            return False
        if rules.minLifetimeSpend and user.lifetimeSpend < rules.minLifetimeSpend:
            return False
        if rules.minOrdersPlaced and user.ordersPlaced < rules.minOrdersPlaced:
            return False
        if rules.firstOrderOnly and user.ordersPlaced > 0:
            return False
        if rules.allowedCountries and user.countryCode not in rules.allowedCountries:
            return False

        # 4. Cart Attributes
        if rules.minCartValue and cart.total_value < rules.minCartValue:
            return False
        if rules.minItemsCount and cart.total_items < rules.minItemsCount:
            return False
        
        cart_cats = cart.unique_categories
        if rules.applicableCategories:
            if not any(cat in rules.applicableCategories for cat in cart_cats):
                return False
        if rules.excludedCategories:
            if any(cat in rules.excludedCategories for cat in cart_cats):
                return False

        return True

    @staticmethod
    def calculate_discount(coupon: Coupon, cart_value: float) -> float:
        if coupon.discountType == "FLAT":
            return min(coupon.discountValue, cart_value)
        elif coupon.discountType == "PERCENT":
            discount = (cart_value * coupon.discountValue) / 100.0
            if coupon.maxDiscountAmount:
                discount = min(discount, coupon.maxDiscountAmount)
            return discount
        return 0.0

    @staticmethod
    def find_best_coupon(user: UserContext, cart: Cart):
        valid_coupons = []
        for code, coupon in coupon_db.items():
            if CouponService.is_eligible(coupon, user, cart):
                discount = CouponService.calculate_discount(coupon, cart.total_value)
                valid_coupons.append({
                    "coupon": coupon,
                    "discount": discount
                })
        
        if not valid_coupons:
            return None

        # Sort: High Discount -> Earliest End Date -> A-Z Code
        valid_coupons.sort(key=lambda x: (
            -x["discount"],
            x["coupon"].endDate,
            x["coupon"].code
        ))
        return valid_coupons[0]