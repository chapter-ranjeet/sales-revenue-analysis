"""
Synthetic Sales Data Generator
Generates 1,500+ realistic rows of sales data spanning 2025-2026
with seasonal patterns, regional variance, and product-level granularity.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# ---------------------------------------------------------------------------
# Product catalogue with base pricing & margin bands
# ---------------------------------------------------------------------------
PRODUCT_CATALOGUE = {
    "Electronics": {
        "products": [
            ("Wireless Earbuds Pro", 79.99, 0.32),
            ("4K Smart Monitor", 449.99, 0.22),
            ("Mechanical Keyboard", 129.99, 0.38),
            ("USB-C Docking Station", 189.99, 0.28),
            ("Portable SSD 1TB", 109.99, 0.30),
            ("Noise-Cancelling Headphones", 249.99, 0.26),
        ],
        "seasonality": [0.8, 0.7, 0.75, 0.85, 0.9, 0.85, 0.8, 0.9, 1.0, 1.1, 1.4, 1.6],
    },
    "Furniture": {
        "products": [
            ("Ergonomic Office Chair", 399.99, 0.25),
            ("Standing Desk Electric", 549.99, 0.20),
            ("Bookshelf Walnut", 219.99, 0.35),
            ("Filing Cabinet Steel", 179.99, 0.30),
            ("Monitor Arm Dual", 89.99, 0.40),
        ],
        "seasonality": [0.9, 0.85, 0.95, 1.0, 1.0, 0.95, 0.85, 1.0, 1.1, 1.05, 1.1, 1.15],
    },
    "Clothing": {
        "products": [
            ("Performance Hoodie", 64.99, 0.45),
            ("Slim Fit Chinos", 49.99, 0.50),
            ("Merino Wool Sweater", 89.99, 0.42),
            ("Waterproof Jacket", 129.99, 0.35),
            ("Running Shoes Elite", 159.99, 0.30),
        ],
        "seasonality": [1.1, 0.9, 1.0, 1.05, 1.0, 0.8, 0.7, 0.85, 1.0, 1.1, 1.3, 1.5],
    },
    "Office Supplies": {
        "products": [
            ("Premium Notebook Set", 24.99, 0.55),
            ("Gel Pen Pack (12)", 14.99, 0.60),
            ("Desk Organizer Bamboo", 34.99, 0.48),
            ("Whiteboard 48x36", 89.99, 0.35),
            ("Label Maker Pro", 59.99, 0.40),
        ],
        "seasonality": [1.2, 1.0, 0.9, 0.85, 0.85, 0.8, 0.8, 1.3, 1.4, 1.0, 0.95, 1.0],
    },
    "Health & Beauty": {
        "products": [
            ("Vitamin D3 Supplements", 19.99, 0.55),
            ("Electric Toothbrush", 69.99, 0.38),
            ("Organic Face Serum", 44.99, 0.52),
            ("Massage Gun Pro", 149.99, 0.28),
            ("Air Purifier Compact", 199.99, 0.24),
        ],
        "seasonality": [1.2, 1.1, 1.0, 0.95, 0.9, 0.85, 0.85, 0.9, 0.95, 1.0, 1.1, 1.3],
    },
}

REGIONS = ["North", "South", "East", "West", "Central"]
REGION_WEIGHTS = [0.25, 0.20, 0.22, 0.18, 0.15]  # Market-share proxy


def generate_synthetic_data(
    start_date: str = "2025-01-01",
    end_date: str = "2026-12-31",
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate a realistic synthetic sales dataset.

    Returns a DataFrame with columns:
        Order_Date, Category, Product, Region, Units_Sold, Revenue, Profit
    """
    rng = np.random.default_rng(seed)

    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)
    total_days = (end - start).days + 1

    rows: list[dict] = []

    for day_offset in range(total_days):
        current_date = start + pd.Timedelta(days=day_offset)
        month_idx = current_date.month - 1  # 0-based
        dow = current_date.dayofweek  # Mon=0 … Sun=6

        # Fewer orders on weekends
        weekend_factor = 0.5 if dow >= 5 else 1.0

        # Year-over-year growth for 2026
        yoy_factor = 1.0 if current_date.year == 2025 else 1.12

        # Determine how many orders this day (Poisson-distributed)
        base_orders = 3.0 * weekend_factor * yoy_factor
        n_orders = rng.poisson(lam=base_orders)

        for _ in range(n_orders):
            # Pick category weighted by seasonality strength
            cat_names = list(PRODUCT_CATALOGUE.keys())
            cat_season_weights = np.array(
                [PRODUCT_CATALOGUE[c]["seasonality"][month_idx] for c in cat_names]
            )
            cat_season_weights /= cat_season_weights.sum()
            category = rng.choice(cat_names, p=cat_season_weights)

            # Pick product within category
            products = PRODUCT_CATALOGUE[category]["products"]
            prod_name, base_price, base_margin = products[
                rng.integers(0, len(products))
            ]

            # Pick region
            region = rng.choice(REGIONS, p=REGION_WEIGHTS)

            # Units (1-15, skewed low)
            units = int(rng.lognormal(mean=0.8, sigma=0.6)) + 1
            units = min(units, 20)

            # Price jitter ±8 %
            price = base_price * rng.uniform(0.92, 1.08)

            # Revenue
            revenue = round(units * price, 2)

            # Profit with margin jitter ±5 pp
            margin = base_margin + rng.uniform(-0.05, 0.05)
            profit = round(revenue * margin, 2)

            rows.append(
                {
                    "Order_Date": current_date.strftime("%Y-%m-%d"),
                    "Category": category,
                    "Product": prod_name,
                    "Region": region,
                    "Units_Sold": units,
                    "Revenue": revenue,
                    "Profit": profit,
                }
            )

    df = pd.DataFrame(rows)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df.sort_values("Order_Date", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df
