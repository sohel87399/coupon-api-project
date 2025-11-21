# E-Commerce Coupon Engine API

## 1. Project Overview
This project is a RESTful API designed to manage e-commerce coupons. It allows administrators to create coupons with complex eligibility rules (such as minimum cart value, user tiers, and specific categories). It also features a logic engine that accepts a User and a Cart, evaluates all available coupons, and automatically selects the "best" coupon based on the highest discount amount.

## 2. Tech Stack
* **Language:** Python 3.10+
* **Framework:** FastAPI
* **Validation:** Pydantic
* **Server:** Uvicorn
* **Architecture:** MVC (Model-View-Controller) separation

## 3. How to Run

### Prerequisites
* Python 3.10 or higher installed.
* `pip` (Python package manager).

### Setup Steps
1.  Clone or download this repository.
2.  Open a terminal in the project root folder.
3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Start the Service
Run the following command to start the development server:
```bash
uvicorn main:app --reload
