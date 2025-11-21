from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal
from datetime import datetime

# --- Configuration Models ---
class Eligibility(BaseModel):
    allowedUserTiers: Optional[List[str]] = None
    minLifetimeSpend: Optional[float] = None
    minOrdersPlaced: Optional[int] = None
    firstOrderOnly: Optional[bool] = None
    allowedCountries: Optional[List[str]] = None
    minCartValue: Optional[float] = None
    applicableCategories: Optional[List[str]] = None
    excludedCategories: Optional[List[str]] = None
    minItemsCount: Optional[int] = None

class Coupon(BaseModel):
    code: str
    description: Optional[str] = None
    discountType: Literal["FLAT", "PERCENT"]
    discountValue: float
    maxDiscountAmount: Optional[float] = None
    startDate: datetime
    endDate: datetime
    usageLimitPerUser: Optional[int] = None
    eligibility: Optional[Eligibility] = Field(default_factory=Eligibility)

# --- Input Models ---
class CartItem(BaseModel):
    productId: str
    category: str
    unitPrice: float
    quantity: int

class Cart(BaseModel):
    items: List[CartItem]

    @property
    def total_value(self) -> float:
        return sum(item.unitPrice * item.quantity for item in self.items)

    @property
    def total_items(self) -> int:
        return sum(item.quantity for item in self.items)
    
    @property
    def unique_categories(self) -> set:
        return {item.category for item in self.items}

class UserContext(BaseModel):
    userId: str
    tier: Optional[str] = "REGULAR"
    lifetimeSpend: Optional[float] = 0.0
    ordersPlaced: Optional[int] = 0
    countryCode: Optional[str] = "IN"
    pastCouponUsage: Optional[Dict[str, int]] = Field(default_factory=dict) 

class BestCouponRequest(BaseModel):
    user: UserContext
    cart: Cart