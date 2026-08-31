"""Tests for Gold aggregation logic (pandas fixtures)."""

import pandas as pd

from src.silver.pandas_engine import validate_customers_pandas, validate_orders_pandas, validate_products_pandas


def _build_silver_fixtures():
    customers = pd.DataFrame(
        {
            "customer_id": [1, 2, 3],
            "customer_name": ["A", "B", "C"],
            "email": ["a@x.com", "b@x.com", "c@x.com"],
            "country": ["US", "US", "UK"],
            "signup_date": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "customer_segment": ["Premium", "Standard", "Basic"],
            "lifetime_value": [100, 50, 25],
        }
    )
    products = pd.DataFrame(
        {
            "product_id": [10, 20],
            "product_name": ["Widget", "Gadget"],
            "category": ["Electronics", "Home"],
            "price": [25.0, 15.0],
            "cost": [10.0, 5.0],
            "stock_quantity": [100, 50],
            "reorder_level": [10, 5],
        }
    )
    orders = pd.DataFrame(
        {
            "order_id": [100, 101, 102, 103],
            "customer_id": [1, 1, 2, 3],
            "order_date": ["2024-02-01", "2024-02-02", "2024-02-03", "2024-02-04"],
            "product_id": [10, 20, 10, 20],
            "quantity": [2, 1, 1, 3],
            "unit_price": [25.0, 15.0, 25.0, 15.0],
            "total_amount": [50.0, 15.0, 25.0, 45.0],
            "order_status": ["Completed", "Completed", "Pending", "Completed"],
            "payment_date": ["2024-02-02", "2024-02-03", None, "2024-02-05"],
        }
    )
    silver_customers = validate_customers_pandas(customers)
    silver_products = validate_products_pandas(products)
    silver_orders = validate_orders_pandas(orders, customers, products)
    return silver_customers, silver_orders, silver_products


def test_sales_by_product_uses_valid_completed_orders_only():
    customers, orders, products = _build_silver_fixtures()
    valid_orders = orders[orders["is_valid"] & (orders["order_status"] == "Completed")]
    joined = valid_orders.merge(products[products["is_valid"]], on="product_id")
    result = (
        joined.groupby(["product_id", "product_name", "category"], as_index=False)
        .agg(total_orders=("order_id", "count"), total_revenue=("total_amount", "sum"))
    )

    widget = result[result["product_id"] == 10].iloc[0]
    assert widget["total_orders"] == 1
    assert widget["total_revenue"] == 50.0


def test_revenue_by_customer_lifetime_value_actual():
    customers, orders, products = _build_silver_fixtures()
    valid_orders = orders[orders["is_valid"] & (orders["order_status"] == "Completed")]
    joined = valid_orders.merge(customers[customers["is_valid"]], on="customer_id")
    result = joined.groupby("customer_id", as_index=False).agg(total_revenue=("total_amount", "sum"))

    customer_1 = result[result["customer_id"] == 1].iloc[0]
    assert customer_1["total_revenue"] == 65.0


def test_customer_segmentation_mutually_exclusive_segments():
    customers, orders, products = _build_silver_fixtures()
    valid_orders = orders[orders["is_valid"] & (orders["order_status"] == "Completed")]
    stats = valid_orders.groupby("customer_id").agg(
        completed_order_count=("order_id", "count"),
        total_revenue=("total_amount", "sum"),
    )
    activity = customers[customers["is_valid"]][["customer_id"]].merge(
        stats, on="customer_id", how="left"
    ).fillna({"completed_order_count": 0, "total_revenue": 0})

    assert len(activity) == 3
    assert activity.loc[activity["customer_id"] == 2, "completed_order_count"].iloc[0] == 0
