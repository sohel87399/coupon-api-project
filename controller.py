from fastapi import APIRouter, HTTPException
from models import Coupon, BestCouponRequest
from service import CouponService

# Create a Router (a mini-app)
router = APIRouter()

@router.post("/coupons", status_code=201)
def create_coupon(coupon: Coupon):
    """Create a new coupon"""
    code = CouponService.create_coupon(coupon)
    return {"message": "Coupon created", "code": code}

@router.get("/coupons")
def list_coupons():
    """List all coupons"""
    return CouponService.list_all()

@router.post("/best-coupon")
def get_best_coupon(request: BestCouponRequest):
    """Find the best coupon for a cart"""
    best = CouponService.find_best_coupon(request.user, request.cart)
    
    if not best:
        return {"best_coupon": None, "message": "No eligible coupons found."}

    return {
        "code": best["coupon"].code,
        "discount_amount": best["discount"],
        "final_cart_price": request.cart.total_value - best["discount"],
        "description": best["coupon"].description
    }