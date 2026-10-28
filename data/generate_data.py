"""
04_Supply_Chain_DataCo: Synthetic Data Generator
Generates DataCo Smart Supply Chain dataset with 53 columns matching Kaggle structure.
Preserves arithmetic financial invariants, simulates realistic delivery delays,
supports Latin-1 encoding, and generates relational star-schema export files.
"""

import os
import sys
import argparse
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(description="Generate DataCo Supply Chain Dataset")
    parser.add_argument("--samples", type=int, default=25000, help="Number of order item rows (default: 25000)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    parser.add_argument("--outdir", type=str, default=None, help="Output directory")
    return parser.parse_args()

def generate_supply_chain_data(n_samples=25000, seed=42, outdir=None):
    if outdir is None:
        outdir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(outdir, exist_ok=True)
    clean_dir = os.path.join(outdir, "clean")
    os.makedirs(clean_dir, exist_ok=True)

    np.random.seed(seed)
    random.seed(seed)

    print(f"Generating {n_samples:,} DataCo Supply Chain rows (seed={seed})...")

    # 1. Product Catalog & Categories (50 distinct SKUs across 10 categories, 5 departments)
    departments = [
        (1, "Apparel"),
        (2, "Fan Shop"),
        (3, "Golf"),
        (4, "Footwear"),
        (5, "Outdoors"),
        (6, "Fitness")
    ]
    
    categories = [
        (1, "Cleats", 4, 59.99),
        (2, "Men's Footwear", 4, 129.99),
        (3, "Women's Apparel", 1, 48.00),
        (4, "Cardio Equipment", 6, 299.99),
        (5, "Golf Balls", 3, 24.99),
        (6, "Camping & Hiking", 5, 89.99),
        (7, "Shop By Sport", 2, 39.99),
        (8, "Fishing", 5, 69.99),
        (9, "Water Sports", 5, 199.99),
        (10, "Indoor/Outdoor Games", 2, 49.99)
    ]
    
    # 50 Products
    products = []
    card_id = 1001
    for cat_id, cat_name, dept_id, base_price in categories:
        dept_name = next(d[1] for d in departments if d[0] == dept_id)
        for p_idx in range(5):
            p_name = f"{cat_name} Pro-{p_idx+1}"
            price = round(base_price * np.random.uniform(0.75, 1.35), 2)
            products.append({
                "Product Card Id": card_id,
                "Product Name": p_name,
                "Product Category Id": cat_id,
                "Category Name": cat_name,
                "Department Id": dept_id,
                "Department Name": dept_name,
                "Product Price": price,
                "Product Status": 0
            })
            card_id += 1

    # 2. Customers & Latin American / European Names (encoding test for latin-1)
    first_names = [
        "Alejandro", "María", "José", "Juan", "Sofía", "François", "Jürgen", "Günter",
        "Camila", "Mateo", "Valentina", "Sebastián", "Isabella", "Carlos", "Lucía",
        "René", "Marta", "André", "Inês", "Björn", "Gérard", "Hélène", "David", "Emma"
    ]
    last_names = [
        "Rodríguez", "González", "García", "Martínez", "López", "Hernández", "Pérez",
        "Sánchez", "Müller", "Schneider", "Dubois", "Moreau", "Silva", "Santos",
        "Ferreira", "Cárdenas", "Vásquez", "Gómez", "Torres", "Ramírez", "Castro"
    ]
    customer_cities = [
        ("Caguas", "PR", "Puerto Rico"), ("San Juan", "PR", "Puerto Rico"),
        ("Mayaguez", "PR", "Puerto Rico"), ("Ponce", "PR", "Puerto Rico"),
        ("New York", "NY", "EE. UU."), ("Los Angeles", "CA", "EE. UU."),
        ("Chicago", "IL", "EE. UU."), ("Houston", "TX", "EE. UU."),
        ("Miami", "FL", "EE. UU."), ("Philadelphia", "PA", "EE. UU.")
    ]
    customer_segments = ["Consumer", "Corporate", "Home Office"]
    segment_weights = [0.517, 0.303, 0.180]

    n_customers = min(6000, n_samples // 3)
    customers = []
    for c_id in range(1, n_customers + 1):
        fname = random.choice(first_names)
        lname = random.choice(last_names)
        city, state, country = random.choice(customer_cities)
        seg = np.random.choice(customer_segments, p=segment_weights)
        customers.append({
            "Customer Id": 10000 + c_id,
            "Customer Fname": fname,
            "Customer Lname": lname,
            "Customer Segment": seg,
            "Customer City": city,
            "Customer State": state,
            "Customer Country": country,
            "Customer Zipcode": f"{random.randint(10000, 99999)}",
            "Customer Street": f"{random.randint(100, 999)} Calle {lname}",
            "Customer Email": f"cust_{c_id}@dataco-smartsupply.com",
            "Customer Password": "XXXXXXXXXXXXXXX"
        })

    # 3. Destination Geography Hierarchy (Markets, Regions, Cities)
    geography_hierarchy = [
        ("Europe", "Western Europe", "Germany", "Bavaria", "München", 48.1351, 11.5820),
        ("Europe", "Western Europe", "France", "Île-de-France", "Paris", 48.8566, 2.3522),
        ("Europe", "Southern Europe", "Spain", "Madrid", "Madrid", 40.4168, -3.7038),
        ("Europe", "Northern Europe", "United Kingdom", "England", "London", 51.5074, -0.1278),
        ("Europe", "Eastern Europe", "Poland", "Mazovia", "Warszawa", 52.2297, 21.0122),
        ("LATAM", "South America", "Colombia", "Antioquia", "Medellín", 6.2442, -75.5812),
        ("LATAM", "South America", "Colombia", "Cundinamarca", "Bogotá", 4.7110, -74.0721),
        ("LATAM", "South America", "Brazil", "São Paulo", "São Paulo", -23.5505, -46.6333),
        ("LATAM", "South America", "Argentina", "Córdoba", "Córdoba", -31.4201, -64.1888),
        ("LATAM", "Central America", "Mexico", "Jalisco", "Guadalajara", 20.6597, -103.3496),
        ("Pacific Asia", "Southeast Asia", "Indonesia", "Jakarta", "Jakarta", -6.2088, 106.8456),
        ("Pacific Asia", "Southeast Asia", "Vietnam", "Ho Chi Minh", "Ho Chi Minh City", 10.8231, 106.6297),
        ("Pacific Asia", "East Asia", "China", "Shanghai", "Shanghai", 31.2304, 121.4737),
        ("Pacific Asia", "South Asia", "India", "Maharashtra", "Mumbai", 19.0760, 72.8777),
        ("Pacific Asia", "Oceania", "Australia", "New South Wales", "Sydney", -33.8688, 151.2093),
        ("USCA", "USCA", "United States", "California", "Los Angeles", 34.0522, -118.2437),
        ("USCA", "USCA", "United States", "New York", "New York", 40.7128, -74.0060),
        ("USCA", "USCA", "Canada", "Ontario", "Toronto", 43.6532, -79.3832),
        ("Africa", "Northern Africa", "Egypt", "Cairo", "Cairo", 30.0444, 31.2357),
        ("Africa", "Western Africa", "Nigeria", "Lagos", "Lagos", 6.5244, 3.3792),
        ("Africa", "Southern Africa", "South Africa", "Gauteng", "Johannesburg", -26.2041, 28.0473)
    ]
    # Market distribution matching DataCo real distribution
    market_probs = {
        "Europe": 0.285,
        "LATAM": 0.283,
        "Pacific Asia": 0.230,
        "USCA": 0.148,
        "Africa": 0.054
    }
    geo_by_market = {}
    for g in geography_hierarchy:
        m = g[0]
        geo_by_market.setdefault(m, []).append(g)

    # 4. Shipping Modes & Operational SLA
    # Mode, Scheduled Days, Target SLA Hours, Overall weight
    shipping_modes = [
        ("Standard Class", 4, 96, 0.598),
        ("Second Class", 2, 48, 0.198),
        ("First Class", 1, 24, 0.152),
        ("Same Day", 0, 12, 0.052)
    ]
    mode_names = [m[0] for m in shipping_modes]
    mode_weights = [m[3] for m in shipping_modes]
    mode_sla = {m[0]: (m[1], m[2]) for m in shipping_modes}

    # 5. Order Status distribution
    order_statuses = [
        "COMPLETE", "PENDING_PAYMENT", "PROCESSING", "CLOSED",
        "ON_HOLD", "SUSPECTED_FRAUD", "PENDING", "PAYMENT_REVIEW", "CANCELED"
    ]
    status_weights = [0.33, 0.22, 0.12, 0.11, 0.06, 0.04, 0.05, 0.04, 0.03]

    payment_types = ["DEBIT", "TRANSFER", "PAYMENT", "CASH"]
    payment_weights = [0.386, 0.276, 0.232, 0.106]

    # Date range: 2015-01-01 to 2017-12-31 (3 continuous calendar years)
    start_date = datetime(2015, 1, 1, 8, 0, 0)
    total_days = 365 * 3

    # Generate Orders and Order Items
    records = []
    order_id_counter = 10001
    item_id_counter = 1

    # Approximate items per order: 1 to 4 (mean ~1.8)
    while item_id_counter <= n_samples:
        current_order_id = order_id_counter
        order_id_counter += 1

        cust = random.choice(customers)
        # Choose market based on exact weights
        mkt = np.random.choice(list(market_probs.keys()), p=list(market_probs.values()))
        geo = random.choice(geo_by_market[mkt])
        _, region, country, state, city, lat, lon = geo

        mode = np.random.choice(mode_names, p=mode_weights)
        sched_days, sla_hours = mode_sla[mode]
        # Order placement timestamp
        random_day = random.randint(0, total_days - 1)
        random_second = random.randint(0, 86399)
        order_dt = start_date + timedelta(days=random_day, seconds=random_second)

        # Realistic operational shipping delays matching DataCo real behavior:
        # Distance, infrastructure, peak season, and shipping mode determine transit duration:
        is_remote_market = mkt in ["LATAM", "Africa"] or region in ["Southeast Asia", "South Asia", "Eastern Europe"]
        is_peak_season = order_dt.month in [10, 11, 12]
        is_weekend_order = order_dt.weekday() >= 5

        if mode == "First Class":
            # Scheduled: 1 day. Air / expedited ground bottleneck leads to ~95% late SLA failure
            actual_days = np.random.choice([1, 2, 3, 4], p=[0.047, 0.550, 0.350, 0.053])
        elif mode == "Same Day":
            # Scheduled: 0 days (same-day delivery). 52% roll over into next calendar day
            actual_days = np.random.choice([0, 1], p=[0.48, 0.52])
        elif mode == "Second Class":
            # Scheduled: 2 days. 76% take 3-4 days
            if is_remote_market:
                actual_days = np.random.choice([2, 3, 4, 5], p=[0.10, 0.45, 0.38, 0.07])
            else:
                actual_days = np.random.choice([2, 3, 4], p=[0.32, 0.50, 0.18])
        else: # Standard Class, scheduled 4 days
            # Regional transit friction strongly governs standard ground/ocean freight
            if is_remote_market:
                if is_peak_season or is_weekend_order:
                    actual_days = np.random.choice([4, 5, 6], p=[0.12, 0.60, 0.28])
                else:
                    actual_days = np.random.choice([3, 4, 5, 6], p=[0.08, 0.22, 0.52, 0.18])
            else: # Domestic / Western Europe
                if is_peak_season:
                    actual_days = np.random.choice([3, 4, 5], p=[0.25, 0.45, 0.30])
                else:
                    actual_days = np.random.choice([2, 3, 4, 5], p=[0.22, 0.48, 0.25, 0.05])

        late_risk = 1 if actual_days > sched_days else 0

        # Delivery status string
        if actual_days < sched_days:
            deliv_status = "Advance shipping"
        elif actual_days == sched_days:
            deliv_status = "Shipping on time"
        else:
            deliv_status = "Late delivery"

        order_status = np.random.choice(order_statuses, p=status_weights)
        if order_status == "CANCELED":
            deliv_status = "Shipping canceled"

        payment_type = np.random.choice(payment_types, p=payment_weights)
        ship_dt = order_dt + timedelta(days=int(actual_days), hours=random.randint(2, 10))

        # Items in this order (1 to 3 items)
        n_items = min(random.choices([1, 2, 3, 4], weights=[0.60, 0.25, 0.10, 0.05])[0],
                      n_samples - item_id_counter + 1)

        for _ in range(n_items):
            prod = random.choice(products)
            qty = random.choices([1, 2, 3, 4, 5], weights=[0.70, 0.18, 0.07, 0.03, 0.02])[0]
            unit_price = prod["Product Price"]
            gross_sales = round(unit_price * qty, 2)

            # Discount rate: 0.00 to 0.25 in 0.01 increments
            # Majority are 0 to 0.15, but promotional discounts hit 0.20 to 0.25
            discount_rate = round(float(np.random.choice(
                np.arange(0.00, 0.26, 0.01),
                p=[0.20] + [0.80 / 25] * 25
            )), 2)
            
            discount_amount = round(gross_sales * discount_rate, 2)
            net_sales = round(gross_sales - discount_amount, 2)

            # Invariant: Sales per customer = Order Item Total = net_sales
            # Profit formulation:
            # Baseline operating margin without discount ~ 20% to 35%
            # High discount rates (>15%) erode margins into negative territory (loss orders)
            base_margin = np.random.uniform(0.18, 0.32)
            # Higher discounts erode profit severely
            profit_ratio = round(base_margin - (1.65 * discount_rate) + np.random.normal(0, 0.03), 4)
            # Clip between -0.50 and +0.50
            profit_ratio = max(-0.50, min(0.50, profit_ratio))
            
            profit_amount = round(net_sales * profit_ratio, 2)

            row = {
                "Type": payment_type,
                "Days for shipping (real)": int(actual_days),
                "Days for shipment (scheduled)": int(sched_days),
                "Benefit per order": profit_amount,
                "Sales per customer": net_sales,
                "Delivery Status": deliv_status,
                "Late_delivery_risk": int(late_risk),
                "Category Id": prod["Product Category Id"],
                "Category Name": prod["Category Name"],
                "Customer City": cust["Customer City"],
                "Customer Country": cust["Customer Country"],
                "Customer Email": cust["Customer Email"],
                "Customer Fname": cust["Customer Fname"],
                "Customer Id": cust["Customer Id"],
                "Customer Lname": cust["Customer Lname"],
                "Customer Password": cust["Customer Password"],
                "Customer Segment": cust["Customer Segment"],
                "Customer State": cust["Customer State"],
                "Customer Street": cust["Customer Street"],
                "Customer Zipcode": cust["Customer Zipcode"],
                "Department Id": prod["Department Id"],
                "Department Name": prod["Department Name"],
                "Latitude": lat,
                "Longitude": lon,
                "Market": mkt,
                "Order City": city,
                "Order Country": country,
                "Order Customer Id": cust["Customer Id"],
                "order date (DateOrders)": order_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "Order Id": current_order_id,
                "Order Item Cardprod Id": prod["Product Card Id"],
                "Order Item Discount": discount_amount,
                "Order Item Discount Rate": discount_rate,
                "Order Item Id": item_id_counter,
                "Order Item Product Price": unit_price,
                "Order Item Profit Ratio": profit_ratio,
                "Order Item Quantity": qty,
                "Sales": gross_sales,
                "Order Item Total": net_sales,
                "Order Profit Per Order": profit_amount,
                "Order Region": region,
                "Order State": state,
                "Order Status": order_status,
                "Order Zipcode": f"{random.randint(10000, 99999)}",
                "Product Card Id": prod["Product Card Id"],
                "Product Category Id": prod["Product Category Id"],
                "Product Description": "",
                "Product Image": f"http://images.dataco.com/products/{prod['Product Card Id']}.jpg",
                "Product Name": prod["Product Name"],
                "Product Price": unit_price,
                "Product Status": 0,
                "shipping date (DateOrders)": ship_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "Shipping Mode": mode
            }
            records.append(row)
            item_id_counter += 1

    df = pd.DataFrame(records)
    print(f"Dataset generated. Shape: {df.shape}")
    assert len(df.columns) == 53, f"Expected 53 columns, got {len(df.columns)}"

    # Check Arithmetic Invariants
    inv_gross = np.allclose(df["Sales"], df["Order Item Product Price"] * df["Order Item Quantity"], atol=0.02)
    inv_disc = np.allclose(df["Order Item Discount"], df["Sales"] * df["Order Item Discount Rate"], atol=0.02)
    inv_net = np.allclose(df["Order Item Total"], df["Sales"] - df["Order Item Discount"], atol=0.02)
    inv_profit = np.allclose(df["Order Profit Per Order"], df["Benefit per order"], atol=0.01)
    inv_late = np.all(df["Late_delivery_risk"] == (df["Days for shipping (real)"] > df["Days for shipment (scheduled)"]).astype(int))

    print(f"Invariant Checks:")
    print(f" - Gross Sales == Price * Qty: {inv_gross}")
    print(f" - Discount Amount == Gross * Rate: {inv_disc}")
    print(f" - Net Sales == Gross - Discount: {inv_net}")
    print(f" - Profit Invariant: {inv_profit}")
    print(f" - Late Delivery Risk Invariant: {inv_late}")
    print(f" - Overall Late Delivery Rate: {df['Late_delivery_risk'].mean()*100:.2f}%")
    print(f" - Negative Profit (Loss) Orders Rate: {(df['Order Profit Per Order'] < 0).mean()*100:.2f}%")

    # Save Primary CSV with Latin-1 Encoding (Kaggle requirement)
    main_csv_path = os.path.join(outdir, "DataCoSupplyChainDataset.csv")
    df.to_csv(main_csv_path, index=False, encoding="latin-1")
    print(f"Saved primary dataset to: {main_csv_path} (encoding=latin-1, {len(df):,} rows)")

    # Save Sample CSV (1,000 rows)
    sample_csv_path = os.path.join(outdir, "sample_data.csv")
    df.head(1000).to_csv(sample_csv_path, index=False, encoding="latin-1")
    print(f"Saved sample dataset to: {sample_csv_path} (1,000 rows)")

    # 6. Generate Clean Relational Dimension CSVs for Star Schema & Power BI Import
    print("Generating normalized star-schema CSV tables...")

    # Dim_Customer
    dim_cust = df[[
        "Customer Id", "Customer Fname", "Customer Lname", "Customer Segment",
        "Customer City", "Customer State", "Customer Country", "Customer Zipcode"
    ]].drop_duplicates(subset=["Customer Id"]).copy()
    dim_cust.rename(columns={
        "Customer Id": "customer_id",
        "Customer Fname": "first_name",
        "Customer Lname": "last_name",
        "Customer Segment": "customer_segment",
        "Customer City": "customer_city",
        "Customer State": "customer_state",
        "Customer Country": "customer_country",
        "Customer Zipcode": "customer_zipcode"
    }, inplace=True)
    dim_cust.insert(0, "customer_key", range(1, len(dim_cust) + 1))
    dim_cust.to_csv(os.path.join(clean_dir, "dim_customer.csv"), index=False, encoding="utf-8")

    # Dim_Product
    dim_prod = df[[
        "Product Card Id", "Product Name", "Product Category Id", "Category Name",
        "Department Id", "Department Name", "Product Price"
    ]].drop_duplicates(subset=["Product Card Id"]).copy()
    dim_prod.rename(columns={
        "Product Card Id": "product_card_id",
        "Product Name": "product_name",
        "Product Category Id": "category_id",
        "Category Name": "category_name",
        "Department Id": "department_id",
        "Department Name": "department_name",
        "Product Price": "product_price"
    }, inplace=True)
    dim_prod.insert(0, "product_key", range(1, len(dim_prod) + 1))
    dim_prod.to_csv(os.path.join(clean_dir, "dim_product.csv"), index=False, encoding="utf-8")

    # Dim_Shipping
    shipping_dim_data = [
        {"shipping_mode_key": 1, "shipping_mode_name": "Standard Class", "scheduled_days": 4, "target_sla_hours": 96},
        {"shipping_mode_key": 2, "shipping_mode_name": "Second Class", "scheduled_days": 2, "target_sla_hours": 48},
        {"shipping_mode_key": 3, "shipping_mode_name": "First Class", "scheduled_days": 1, "target_sla_hours": 24},
        {"shipping_mode_key": 4, "shipping_mode_name": "Same Day", "scheduled_days": 0, "target_sla_hours": 12}
    ]
    dim_shipping = pd.DataFrame(shipping_dim_data)
    dim_shipping.to_csv(os.path.join(clean_dir, "dim_shipping.csv"), index=False, encoding="utf-8")

    # Dim_Geography
    dim_geo = df[[
        "Market", "Order Region", "Order Country", "Order State", "Order City"
    ]].drop_duplicates().copy()
    dim_geo.rename(columns={
        "Market": "market",
        "Order Region": "order_region",
        "Order Country": "order_country",
        "Order State": "order_state",
        "Order City": "order_city"
    }, inplace=True)
    dim_geo.insert(0, "geography_key", range(1, len(dim_geo) + 1))
    dim_geo.to_csv(os.path.join(clean_dir, "dim_geography.csv"), index=False, encoding="utf-8")

    # Dim_Order_Status
    status_unique = df["Order Status"].unique()
    dim_status = pd.DataFrame({
        "order_status_key": range(1, len(status_unique) + 1),
        "order_status_name": status_unique
    })
    dim_status.to_csv(os.path.join(clean_dir, "dim_order_status.csv"), index=False, encoding="utf-8")

    # Dim_Date (Contiguous dates 2015-01-01 to 2018-01-10)
    all_dates = pd.date_range("2015-01-01", "2018-01-15", freq="D")
    dim_date = pd.DataFrame({
        "date_key": [int(d.strftime("%Y%m%d")) for d in all_dates],
        "full_date": [d.strftime("%Y-%m-%d") for d in all_dates],
        "day_of_month": [d.day for d in all_dates],
        "day_of_week_name": [d.strftime("%A") for d in all_dates],
        "month_num": [d.month for d in all_dates],
        "month_name": [d.strftime("%B") for d in all_dates],
        "quarter": [d.quarter for d in all_dates],
        "year": [d.year for d in all_dates],
        "is_weekend": [1 if d.weekday() >= 5 else 0 for d in all_dates]
    })
    dim_date.to_csv(os.path.join(clean_dir, "dim_date.csv"), index=False, encoding="utf-8")

    # Fact_Order_Items
    # Map foreign keys
    cust_key_map = dict(zip(dim_cust["customer_id"], dim_cust["customer_key"]))
    prod_key_map = dict(zip(dim_prod["product_card_id"], dim_prod["product_key"]))
    ship_key_map = dict(zip(dim_shipping["shipping_mode_name"], dim_shipping["shipping_mode_key"]))
    status_key_map = dict(zip(dim_status["order_status_name"], dim_status["order_status_key"]))
    
    # Geography key lookup
    geo_lookup = {}
    for idx, r in dim_geo.iterrows():
        key = (r["market"], r["order_region"], r["order_country"], r["order_state"], r["order_city"])
        geo_lookup[key] = r["geography_key"]

    df_order_dt = pd.to_datetime(df["order date (DateOrders)"])
    df_ship_dt = pd.to_datetime(df["shipping date (DateOrders)"])

    fact = pd.DataFrame({
        "order_item_key": df["Order Item Id"],
        "order_id": df["Order Id"],
        "customer_key": df["Customer Id"].map(cust_key_map),
        "product_key": df["Product Card Id"].map(prod_key_map),
        "geography_key": [geo_lookup[(r["Market"], r["Order Region"], r["Order Country"], r["Order State"], r["Order City"])] for _, r in df.iterrows()],
        "shipping_mode_key": df["Shipping Mode"].map(ship_key_map),
        "order_date_key": df_order_dt.dt.strftime("%Y%m%d").astype(int),
        "ship_date_key": df_ship_dt.dt.strftime("%Y%m%d").astype(int),
        "order_status_key": df["Order Status"].map(status_key_map),
        "quantity": df["Order Item Quantity"],
        "product_price": df["Order Item Product Price"],
        "gross_sales": df["Sales"],
        "discount_rate": df["Order Item Discount Rate"],
        "discount_amount": df["Order Item Discount"],
        "net_sales": df["Order Item Total"],
        "profit_amount": df["Order Profit Per Order"],
        "profit_margin_ratio": df["Order Item Profit Ratio"],
        "scheduled_days": df["Days for shipment (scheduled)"],
        "actual_days": df["Days for shipping (real)"],
        "shipping_delay_days": df["Days for shipping (real)"] - df["Days for shipment (scheduled)"],
        "is_late_delivery": df["Late_delivery_risk"],
        "is_negative_profit": (df["Order Profit Per Order"] < 0).astype(int),
        "predicted_late_prob": 0.0  # populated by ML pipeline
    })
    fact.to_csv(os.path.join(clean_dir, "fact_order_items.csv"), index=False, encoding="utf-8")
    print(f"Saved fact_order_items.csv: {len(fact):,} rows")
    print("All datasets generated successfully!")
    return df

if __name__ == "__main__":
    args = parse_args()
    generate_supply_chain_data(n_samples=args.samples, seed=args.seed, outdir=args.outdir)
