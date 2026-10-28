"""
04_Supply_Chain_DataCo: Power BI PBIR & TMDL Command Center Generator
Constructs modern Microsoft Fabric PBIR report files, TMDL semantic model with strict
tab indentation, relationships, report pages, and enterprise DAX repository.
"""

import os
import sys
import json

def build_pbi():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(base_dir)

    pbip_path = os.path.join(base_dir, "Supply_Chain_Command_Center.pbip")
    report_dir = os.path.join(base_dir, "Supply_Chain_Command_Center.Report")
    model_dir = os.path.join(base_dir, "Supply_Chain_Command_Center.SemanticModel")

    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)

    print("Generating Power BI PBIR and TMDL files...")

    # 1. PBIP Project File
    # CRITICAL: artifacts array must contain ONLY report
    pbip_content = {
        "version": "1.0",
        "artifacts": [
            { "report": { "path": "Supply_Chain_Command_Center.Report" } }
        ],
        "settings": {}
    }
    with open(pbip_path, "w", encoding="utf-8") as f:
        json.dump(pbip_content, f, indent=2)
    print(f"Created: {pbip_path}")

    # 2. Report Folder Structure
    with open(os.path.join(report_dir, ".platform"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
            "metadata": {
                "type": "Report",
                "displayName": "Supply_Chain_Command_Center"
            },
            "config": {
                "version": "2.0",
                "logicalId": "00000000-0000-0000-0000-000000000004"
            }
        }, f, indent=2)

    with open(os.path.join(report_dir, "definition.pbir"), "w", encoding="utf-8") as f:
        json.dump({
            "version": "4.0",
            "datasetReference": {
                "byPath": {
                    "path": "../Supply_Chain_Command_Center.SemanticModel"
                }
            }
        }, f, indent=2)

    rep_def_dir = os.path.join(report_dir, "definition")
    pages_dir = os.path.join(rep_def_dir, "pages")
    os.makedirs(pages_dir, exist_ok=True)

    with open(os.path.join(rep_def_dir, "version.json"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json",
            "version": "2.0.0"
        }, f, indent=2)

    with open(os.path.join(rep_def_dir, "report.json"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/1.2.0/schema.json",
            "themeCollection": {
                "baseTheme": {
                    "name": "CY24SU02",
                    "reportVersionAtImport": "5.55"
                }
            },
            "layoutOptimization": "None",
            "settings": {
                "useStylableVisualContainerHeader": True,
                "defaultDrillFilterOtherVisuals": True,
                "allowChangeFilterTypes": True,
                "useEnhancedTooltips": True,
                "useDefaultAggregateDisplayName": True
            }
        }, f, indent=2)

    # 4 Pages
    page_names = ["page_executive", "page_delivery", "page_profit_leakage", "page_predictive"]
    with open(os.path.join(pages_dir, "pages.json"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json",
            "pageOrder": page_names
        }, f, indent=2)

    pages_meta = [
        ("page_executive", "Executive Operations Command", [
            ("card_sales", "card", 20, 20, 100, 220, "Total Sales"),
            ("card_profit", "card", 260, 20, 100, 220, "Total Profit"),
            ("card_margin", "card", 500, 20, 100, 220, "Profit Margin %"),
            ("card_late_rate", "card", 740, 20, 100, 220, "Late Delivery Rate %"),
            ("chart_sales_profit_trend", "areaChart", 20, 140, 320, 680, "Monthly Net Sales & Profit YoY Trend"),
            ("gauge_otif", "gauge", 720, 140, 320, 520, "OTIF Fulfillment Rate (Target 85%)")
        ]),
        ("page_delivery", "Delivery Performance & Geospatial Intelligence", [
            ("map_regional_orders", "map", 20, 20, 380, 720, "Regional Orders & Late Delivery Concentration"),
            ("bar_delay_gap_by_mode", "clusteredBarChart", 760, 20, 380, 480, "Shipping Delay Gap: Scheduled vs Actual Days"),
            ("matrix_delay_by_market", "pivotTable", 20, 420, 260, 1220, "Shipping Delay Gap Days by Market and Shipping Mode")
        ]),
        ("page_profit_leakage", "Profit Leakage & Loss Elimination", [
            ("waterfall_revenue_to_profit", "waterfallChart", 20, 20, 360, 700, "Revenue-to-Profit Bridge & Leakage Walk"),
            ("scatter_discount_vs_margin", "scatterChart", 740, 20, 360, 500, "Discount Rate % vs Profit Margin % by Product Category"),
            ("table_loss_orders", "tableEx", 20, 400, 280, 1220, "Negative-Profit Order Detail Worklist")
        ]),
        ("page_predictive", "Predictive Dispatch Risk Worklist", [
            ("donut_risk_tiers", "donutChart", 20, 20, 320, 440, "Active Orders by Predicted Late Risk Tier"),
            ("slicer_risk_tier", "slicer", 480, 20, 120, 240, "Risk Tier Slicer"),
            ("table_dispatch_worklist", "tableEx", 20, 360, 320, 1220, "Proactive Dispatch Action Queue (Expedited Air Re-routing)")
        ])
    ]

    for p_id, p_title, visuals in pages_meta:
        p_dir = os.path.join(pages_dir, p_id)
        os.makedirs(os.path.join(p_dir, "visuals"), exist_ok=True)
        with open(os.path.join(p_dir, "page.json"), "w", encoding="utf-8") as f:
            json.dump({
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
                "name": p_id,
                "displayName": p_title,
                "displayOption": "FitToPage",
                "height": 720,
                "width": 1280
            }, f, indent=2)

        for v_id, v_type, x, y, h, w, title in visuals:
            v_dir = os.path.join(p_dir, "visuals", v_id)
            os.makedirs(v_dir, exist_ok=True)
            with open(os.path.join(v_dir, "visual.json"), "w", encoding="utf-8") as f:
                json.dump({
                    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
                    "name": v_id,
                    "position": {
                        "x": x,
                        "y": y,
                        "z": 1000,
                        "height": h,
                        "width": w,
                        "tabOrder": 1000
                    },
                    "visual": {
                        "visualType": v_type,
                        "drillFilterOtherVisuals": True
                    }
                }, f, indent=2)

    # 3. SemanticModel Folder & TMDL
    with open(os.path.join(model_dir, ".platform"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
            "metadata": {
                "type": "SemanticModel",
                "displayName": "Supply_Chain_Command_Center"
            },
            "config": {
                "version": "2.0",
                "logicalId": "00000000-0000-0000-0000-000000000004-sm"
            }
        }, f, indent=2)

    with open(os.path.join(model_dir, "definition.pbism"), "w", encoding="utf-8") as f:
        json.dump({
            "version": "4.1",
            "settings": {}
        }, f, indent=2)

    model_def_dir = os.path.join(model_dir, "definition")
    tables_dir = os.path.join(model_def_dir, "tables")
    os.makedirs(tables_dir, exist_ok=True)

    # model.tmdl (STRICT TAB INDENTATION)
    model_tmdl = (
        "model Model\n"
        "\tculture: en-US\n"
        "\tdefaultPowerBIDataSourceVersion: powerBI_V3\n"
        "\tsourceQueryCulture: en-US\n"
        "\tdataAccessOptions\n"
        "\t\tlegacyRedirects\n"
        "\t\treturnErrorValuesAsNull\n"
    )
    with open(os.path.join(model_def_dir, "model.tmdl"), "w", encoding="utf-8") as f:
        f.write(model_tmdl)

    # relationships.tmdl (STRICT TAB INDENTATION)
    rel_tmdl = (
        "relationship Rel_Fact_Customer\n"
        "\tfromColumn: Fact_Order_Items.customer_key\n"
        "\ttoColumn: Dim_Customer.customer_key\n\n"
        "relationship Rel_Fact_Product\n"
        "\tfromColumn: Fact_Order_Items.product_key\n"
        "\ttoColumn: Dim_Product.product_key\n\n"
        "relationship Rel_Fact_Shipping\n"
        "\tfromColumn: Fact_Order_Items.shipping_mode_key\n"
        "\ttoColumn: Dim_Shipping.shipping_mode_key\n\n"
        "relationship Rel_Fact_Geography\n"
        "\tfromColumn: Fact_Order_Items.geography_key\n"
        "\ttoColumn: Dim_Geography.geography_key\n\n"
        "relationship Rel_Fact_OrderDate\n"
        "\tfromColumn: Fact_Order_Items.order_date_key\n"
        "\ttoColumn: Dim_Date.date_key\n\n"
        "relationship Rel_Fact_Status\n"
        "\tfromColumn: Fact_Order_Items.order_status_key\n"
        "\ttoColumn: Dim_Order_Status.order_status_key\n"
    )
    with open(os.path.join(model_def_dir, "relationships.tmdl"), "w", encoding="utf-8") as f:
        f.write(rel_tmdl)

    # Table TMDLs
    # Dim_Customer.tmdl
    dim_cust_tmdl = (
        "table Dim_Customer\n"
        "\tlineageTag: 40000000-0000-0000-0000-000000000001\n\n"
        "\tcolumn customer_key\n"
        "\t\tdataType: int64\n"
        "\t\tisKey\n"
        "\t\tformatString: 0\n"
        "\t\tsourceColumn: customer_key\n\n"
        "\tcolumn customer_id\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: customer_id\n\n"
        "\tcolumn first_name\n"
        "\t\tdataType: string\n"
        "\t\tsourceColumn: first_name\n\n"
        "\tcolumn last_name\n"
        "\t\tdataType: string\n"
        "\t\tsourceColumn: last_name\n\n"
        "\tcolumn customer_segment\n"
        "\t\tdataType: string\n"
        "\t\tsourceColumn: customer_segment\n\n"
        "\tcolumn customer_city\n"
        "\t\tdataType: string\n"
        "\t\tsourceColumn: customer_city\n\n"
        "\tcolumn customer_state\n"
        "\t\tdataType: string\n"
        "\t\tsourceColumn: customer_state\n\n"
        "\tcolumn customer_country\n"
        "\t\tdataType: string\n"
        "\t\tsourceColumn: customer_country\n\n"
        "\tpartition Dim_Customer = m\n"
        "\t\tmode: import\n"
        "\t\tsource =\n"
        "\t\t\tlet\n"
        '\t\t\t\tSource = Csv.Document(File.Contents("data/clean/dim_customer.csv"),[Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),\n'
        '\t\t\t\t#"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true])\n'
        "\t\t\tin\n"
        '\t\t\t\t#"Promoted Headers"\n'
    )
    with open(os.path.join(tables_dir, "Dim_Customer.tmdl"), "w", encoding="utf-8") as f:
        f.write(dim_cust_tmdl)

    # Dim_Product.tmdl
    dim_prod_tmdl = (
        "table Dim_Product\n"
        "\tlineageTag: 40000000-0000-0000-0000-000000000002\n\n"
        "\tcolumn product_key\n"
        "\t\tdataType: int64\n"
        "\t\tisKey\n"
        "\t\tformatString: 0\n"
        "\t\tsourceColumn: product_key\n\n"
        "\tcolumn product_card_id\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: product_card_id\n\n"
        "\tcolumn product_name\n"
        "\t\tdataType: string\n"
        "\t\tsourceColumn: product_name\n\n"
        "\tcolumn category_id\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: category_id\n\n"
        "\tcolumn category_name\n"
        "\t\tdataType: string\n"
        "\t\tsourceColumn: category_name\n\n"
        "\tcolumn department_id\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: department_id\n\n"
        "\tcolumn department_name\n"
        "\t\tdataType: string\n"
        "\t\tsourceColumn: department_name\n\n"
        "\tcolumn product_price\n"
        "\t\tdataType: double\n"
        '\t\tformatString: "$#,##0.00"\n'
        "\t\tsourceColumn: product_price\n\n"
        "\tpartition Dim_Product = m\n"
        "\t\tmode: import\n"
        "\t\tsource =\n"
        "\t\t\tlet\n"
        '\t\t\t\tSource = Csv.Document(File.Contents("data/clean/dim_product.csv"),[Delimiter=",", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),\n'
        '\t\t\t\t#"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true])\n'
        "\t\t\tin\n"
        '\t\t\t\t#"Promoted Headers"\n'
    )
    with open(os.path.join(tables_dir, "Dim_Product.tmdl"), "w", encoding="utf-8") as f:
        f.write(dim_prod_tmdl)

    # Dim_Shipping.tmdl
    dim_ship_tmdl = (
        "table Dim_Shipping\n"
        "\tlineageTag: 40000000-0000-0000-0000-000000000003\n\n"
        "\tcolumn shipping_mode_key\n"
        "\t\tdataType: int64\n"
        "\t\tisKey\n"
        "\t\tformatString: 0\n"
        "\t\tsourceColumn: shipping_mode_key\n\n"
        "\tcolumn shipping_mode_name\n"
        "\t\tdataType: string\n"
        "\t\tsourceColumn: shipping_mode_name\n\n"
        "\tcolumn scheduled_days\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: scheduled_days\n\n"
        "\tcolumn target_sla_hours\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: target_sla_hours\n\n"
        "\tpartition Dim_Shipping = m\n"
        "\t\tmode: import\n"
        "\t\tsource =\n"
        "\t\t\tlet\n"
        '\t\t\t\tSource = Csv.Document(File.Contents("data/clean/dim_shipping.csv"),[Delimiter=",", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.None]),\n'
        '\t\t\t\t#"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true])\n'
        "\t\t\tin\n"
        '\t\t\t\t#"Promoted Headers"\n'
    )
    with open(os.path.join(tables_dir, "Dim_Shipping.tmdl"), "w", encoding="utf-8") as f:
        f.write(dim_ship_tmdl)

    # Dim_Geography.tmdl
    dim_geo_tmdl = (
        "table Dim_Geography\n"
        "\tlineageTag: 40000000-0000-0000-0000-000000000004\n\n"
        "\tcolumn geography_key\n"
        "\t\tdataType: int64\n"
        "\t\tisKey\n"
        "\t\tformatString: 0\n"
        "\t\tsourceColumn: geography_key\n\n"
        "\tcolumn market\n"
        "\t\tdataType: string\n"
        "\t\tsourceColumn: market\n\n"
        "\tcolumn order_region\n"
        "\t\tdataType: string\n"
        "\t\tsourceColumn: order_region\n\n"
        "\tcolumn order_country\n"
        "\t\tdataType: string\n"
        "\t\tsourceColumn: order_country\n\n"
        "\tcolumn order_state\n"
        "\t\tdataType: string\n"
        "\t\tsourceColumn: order_state\n\n"
        "\tcolumn order_city\n"
        "\t\tdataType: string\n"
        "\t\tsourceColumn: order_city\n\n"
        "\tpartition Dim_Geography = m\n"
        "\t\tmode: import\n"
        "\t\tsource =\n"
        "\t\t\tlet\n"
        '\t\t\t\tSource = Csv.Document(File.Contents("data/clean/dim_geography.csv"),[Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),\n'
        '\t\t\t\t#"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true])\n'
        "\t\t\tin\n"
        '\t\t\t\t#"Promoted Headers"\n'
    )
    with open(os.path.join(tables_dir, "Dim_Geography.tmdl"), "w", encoding="utf-8") as f:
        f.write(dim_geo_tmdl)

    # Dim_Date.tmdl
    dim_date_tmdl = (
        "table Dim_Date\n"
        "\tlineageTag: 40000000-0000-0000-0000-000000000005\n\n"
        "\tcolumn date_key\n"
        "\t\tdataType: int64\n"
        "\t\tisKey\n"
        "\t\tformatString: 0\n"
        "\t\tsourceColumn: date_key\n\n"
        "\tcolumn full_date\n"
        "\t\tdataType: dateTime\n"
        '\t\tformatString: "yyyy-MM-dd"\n'
        "\t\tsourceColumn: full_date\n\n"
        "\tcolumn day_of_month\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: day_of_month\n\n"
        "\tcolumn day_of_week_name\n"
        "\t\tdataType: string\n"
        "\t\tsourceColumn: day_of_week_name\n\n"
        "\tcolumn month_num\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: month_num\n\n"
        "\tcolumn month_name\n"
        "\t\tdataType: string\n"
        "\t\tsourceColumn: month_name\n\n"
        "\tcolumn quarter\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: quarter\n\n"
        "\tcolumn year\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: year\n\n"
        "\tcolumn is_weekend\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: is_weekend\n\n"
        "\tpartition Dim_Date = m\n"
        "\t\tmode: import\n"
        "\t\tsource =\n"
        "\t\t\tlet\n"
        '\t\t\t\tSource = Csv.Document(File.Contents("data/clean/dim_date.csv"),[Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),\n'
        '\t\t\t\t#"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true])\n'
        "\t\t\tin\n"
        '\t\t\t\t#"Promoted Headers"\n'
    )
    with open(os.path.join(tables_dir, "Dim_Date.tmdl"), "w", encoding="utf-8") as f:
        f.write(dim_date_tmdl)

    # Dim_Order_Status.tmdl
    dim_status_tmdl = (
        "table Dim_Order_Status\n"
        "\tlineageTag: 40000000-0000-0000-0000-000000000006\n\n"
        "\tcolumn order_status_key\n"
        "\t\tdataType: int64\n"
        "\t\tisKey\n"
        "\t\tformatString: 0\n"
        "\t\tsourceColumn: order_status_key\n\n"
        "\tcolumn order_status_name\n"
        "\t\tdataType: string\n"
        "\t\tsourceColumn: order_status_name\n\n"
        "\tpartition Dim_Order_Status = m\n"
        "\t\tmode: import\n"
        "\t\tsource =\n"
        "\t\t\tlet\n"
        '\t\t\t\tSource = Csv.Document(File.Contents("data/clean/dim_order_status.csv"),[Delimiter=",", Columns=2, Encoding=65001, QuoteStyle=QuoteStyle.None]),\n'
        '\t\t\t\t#"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true])\n'
        "\t\t\tin\n"
        '\t\t\t\t#"Promoted Headers"\n'
    )
    with open(os.path.join(tables_dir, "Dim_Order_Status.tmdl"), "w", encoding="utf-8") as f:
        f.write(dim_status_tmdl)

    # Fact_Order_Items.tmdl
    fact_tmdl = (
        "table Fact_Order_Items\n"
        "\tlineageTag: 40000000-0000-0000-0000-000000000007\n\n"
        "\tcolumn order_item_key\n"
        "\t\tdataType: int64\n"
        "\t\tisKey\n"
        "\t\tformatString: 0\n"
        "\t\tsourceColumn: order_item_key\n\n"
        "\tcolumn order_id\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: order_id\n\n"
        "\tcolumn customer_key\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: customer_key\n\n"
        "\tcolumn product_key\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: product_key\n\n"
        "\tcolumn geography_key\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: geography_key\n\n"
        "\tcolumn shipping_mode_key\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: shipping_mode_key\n\n"
        "\tcolumn order_date_key\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: order_date_key\n\n"
        "\tcolumn ship_date_key\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: ship_date_key\n\n"
        "\tcolumn order_status_key\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: order_status_key\n\n"
        "\tcolumn quantity\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: quantity\n\n"
        "\tcolumn product_price\n"
        "\t\tdataType: double\n"
        '\t\tformatString: "$#,##0.00"\n'
        "\t\tsourceColumn: product_price\n\n"
        "\tcolumn gross_sales\n"
        "\t\tdataType: double\n"
        '\t\tformatString: "$#,##0.00"\n'
        "\t\tsourceColumn: gross_sales\n\n"
        "\tcolumn discount_rate\n"
        "\t\tdataType: double\n"
        '\t\tformatString: "0.0%"\n'
        "\t\tsourceColumn: discount_rate\n\n"
        "\tcolumn discount_amount\n"
        "\t\tdataType: double\n"
        '\t\tformatString: "$#,##0.00"\n'
        "\t\tsourceColumn: discount_amount\n\n"
        "\tcolumn net_sales\n"
        "\t\tdataType: double\n"
        '\t\tformatString: "$#,##0.00"\n'
        "\t\tsourceColumn: net_sales\n\n"
        "\tcolumn profit_amount\n"
        "\t\tdataType: double\n"
        '\t\tformatString: "$#,##0.00"\n'
        "\t\tsourceColumn: profit_amount\n\n"
        "\tcolumn profit_margin_ratio\n"
        "\t\tdataType: double\n"
        '\t\tformatString: "0.0%"\n'
        "\t\tsourceColumn: profit_margin_ratio\n\n"
        "\tcolumn scheduled_days\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: scheduled_days\n\n"
        "\tcolumn actual_days\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: actual_days\n\n"
        "\tcolumn shipping_delay_days\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: shipping_delay_days\n\n"
        "\tcolumn is_late_delivery\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: is_late_delivery\n\n"
        "\tcolumn is_negative_profit\n"
        "\t\tdataType: int64\n"
        "\t\tsourceColumn: is_negative_profit\n\n"
        "\tcolumn predicted_late_prob\n"
        "\t\tdataType: double\n"
        '\t\tformatString: "0.0%"\n'
        "\t\tsourceColumn: predicted_late_prob\n\n"
        "\tmeasure 'Total Orders' = DISTINCTCOUNT(Fact_Order_Items[order_id])\n"
        "\t\tformatString: #,##0\n\n"
        "\tmeasure 'Total Sales' = SUM(Fact_Order_Items[net_sales])\n"
        '\t\tformatString: "$#,##0"\n\n'
        "\tmeasure 'Total Profit' = SUM(Fact_Order_Items[profit_amount])\n"
        '\t\tformatString: "$#,##0"\n\n'
        "\tmeasure 'Profit Margin %' = DIVIDE([Total Profit], [Total Sales], 0.0)\n"
        '\t\tformatString: "0.0%"\n\n'
        "\tmeasure 'Late Orders Count' = CALCULATE([Total Orders], Fact_Order_Items[is_late_delivery] = 1)\n"
        "\t\tformatString: #,##0\n\n"
        "\tmeasure 'Late Delivery Rate %' = DIVIDE([Late Orders Count], [Total Orders], 0.0)\n"
        '\t\tformatString: "0.0%"\n\n'
        "\tmeasure 'OTIF %' = 1 - [Late Delivery Rate %]\n"
        '\t\tformatString: "0.0%"\n\n'
        "\tpartition Fact_Order_Items = m\n"
        "\t\tmode: import\n"
        "\t\tsource =\n"
        "\t\t\tlet\n"
        '\t\t\t\tSource = Csv.Document(File.Contents("data/clean/fact_order_items.csv"),[Delimiter=",", Columns=23, Encoding=65001, QuoteStyle=QuoteStyle.None]),\n'
        '\t\t\t\t#"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true])\n'
        "\t\t\tin\n"
        '\t\t\t\t#"Promoted Headers"\n'
    )
    with open(os.path.join(tables_dir, "Fact_Order_Items.tmdl"), "w", encoding="utf-8") as f:
        f.write(fact_tmdl)

    # 4. Enterprise DAX Measures File (measures.dax)
    dax_measures = """-------------------------------------------------------------------------------
-- PROJECT 4: DATACO SUPPLY CHAIN - ENTERPRISE DAX MEASURES
-- Model Architecture: Star-Schema (Fact_Order_Items, Dim_Customer, Dim_Product,
-- Dim_Shipping, Dim_Geography, Dim_Date, Dim_Order_Status)
-------------------------------------------------------------------------------

// ============================================================================
// 1. Core Order Volume & Financial Metrics
// ============================================================================

[Total Orders] = 
DISTINCTCOUNT(Fact_Order_Items[order_id])

[Total Line Items] = 
COUNTROWS(Fact_Order_Items)

[Gross Sales] = 
SUM(Fact_Order_Items[gross_sales])

[Total Sales] = 
SUM(Fact_Order_Items[net_sales])

[Total Profit] = 
SUM(Fact_Order_Items[profit_amount])

[Profit Margin %] = 
DIVIDE(
    [Total Profit],
    [Total Sales],
    0.0
)

[Total Discount Amount] = 
SUM(Fact_Order_Items[discount_amount])

[Avg Discount Rate %] = 
AVERAGE(Fact_Order_Items[discount_rate])


// ============================================================================
// 2. Fulfillment SLA & Delivery Performance (OTIF)
// ============================================================================

[Late Orders Count] = 
CALCULATE(
    [Total Orders],
    Fact_Order_Items[is_late_delivery] = 1
)

[Late Delivery Rate %] = 
DIVIDE(
    [Late Orders Count],
    [Total Orders],
    0.0
)

[On-Time Delivery %] = 
1.0 - [Late Delivery Rate %]

[OTIF %] = 
[On-Time Delivery %]

[Avg Scheduled Days] = 
AVERAGE(Fact_Order_Items[scheduled_days])

[Avg Actual Days] = 
AVERAGE(Fact_Order_Items[actual_days])

[Shipping Delay Gap Days] = 
[Avg Actual Days] - [Avg Scheduled Days]


// ============================================================================
// 3. Profit Leakage & Loss Order Elimination
// ============================================================================

[Loss Orders Count] = 
CALCULATE(
    [Total Orders],
    Fact_Order_Items[profit_amount] < 0
)

[Loss Order Incidence %] = 
DIVIDE(
    [Loss Orders Count],
    [Total Orders],
    0.0
)

[Total Dollar Loss] = 
CALCULATE(
    ABS(SUM(Fact_Order_Items[profit_amount])),
    Fact_Order_Items[profit_amount] < 0
)

[Simulated 15% Cap Profit Recovery] = 
VAR RecoveredItemMargin = 
    SUMX(
        Fact_Order_Items,
        IF(
            Fact_Order_Items[discount_rate] > 0.15,
            (Fact_Order_Items[discount_rate] - 0.15) * Fact_Order_Items[gross_sales],
            0.0
        )
    )
RETURN
    [Total Profit] + RecoveredItemMargin


// ============================================================================
// 4. Time Intelligence & Growth Analytics (SAMEPERIODLASTYEAR)
// ============================================================================

[Sales SPLY] = 
CALCULATE(
    [Total Sales],
    SAMEPERIODLASTYEAR(Dim_Date[full_date])
)

[Sales YoY %] = 
DIVIDE(
    [Total Sales] - [Sales SPLY],
    [Sales SPLY],
    0.0
)

[Profit SPLY] = 
CALCULATE(
    [Total Profit],
    SAMEPERIODLASTYEAR(Dim_Date[full_date])
)

[Profit YoY %] = 
DIVIDE(
    [Total Profit] - [Profit SPLY],
    [Profit SPLY],
    0.0
)
"""
    measures_path = os.path.join(base_dir, "measures.dax")
    with open(measures_path, "w", encoding="utf-8") as f:
        f.write(dax_measures)
    print(f"Created: {measures_path}")

    print("Power BI PBIR & TMDL structure built successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(build_pbi())
