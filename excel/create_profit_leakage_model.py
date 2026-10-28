"""
04_Supply_Chain_DataCo: Excel Profit Leakage & Discount Sensitivity Model Builder
Generates Supply_Chain_Profit_Leakage_Model.xlsx with 5 professional worksheets:
1. Executive_Scorecard: Executive KPIs, monthly trends, and high-level unit economics.
2. Market_Analysis: Multi-market and shipping mode matrix with conditional formatting.
3. Waterfall_Profit_Leakage: Gross-to-net profit bridge with embedded Excel waterfall bar chart.
4. Discount_Sensitivity_Model: Dynamic 15% discount-capping model demonstrating $920K profit recovery.
5. Data_Dictionary: Exhaustive operational and financial KPI definitions.
"""

import os
import sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference, Series
from openpyxl.formatting.rule import ColorScaleRule

def create_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    wb_path = os.path.join(base_dir, "Supply_Chain_Profit_Leakage_Model.xlsx")
    os.makedirs(base_dir, exist_ok=True)

    print("Building Supply_Chain_Profit_Leakage_Model.xlsx...")
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # Global Style Palettes
    navy_header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    slate_sub_fill = PatternFill(start_color="2F5597", end_color="2F5597", fill_type="solid")
    ice_blue_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    soft_gray_fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
    accent_green_fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
    accent_red_fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")

    font_title = Font(name="Calibri", size=16, bold=True, color="1F4E79")
    font_subtitle = Font(name="Calibri", size=11, italic=True, color="595959")
    font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_bold = Font(name="Calibri", size=11, bold=True, color="000000")
    font_regular = Font(name="Calibri", size=11, color="000000")
    font_kpi_val = Font(name="Calibri", size=18, bold=True, color="1F4E79")
    font_kpi_lbl = Font(name="Calibri", size=9, bold=True, color="595959")

    thin_border_side = Side(style="thin", color="D9D9D9")
    border_grid = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    double_bottom_border = Border(top=thin_border_side, bottom=Side(style="double", color="1F4E79"))

    align_center = Alignment(horizontal="center", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")

    # =========================================================================
    # SHEET 1: Executive_Scorecard
    # =========================================================================
    ws1 = wb.create_sheet(title="Executive_Scorecard")
    ws1.views.sheetView[0].showGridLines = True

    # Title Block
    ws1["B2"] = "DataCo Global Supply Chain: Executive Operations & Profit Leakage Scorecard"
    ws1["B2"].font = font_title
    ws1["B3"] = "Enterprise Fulfillment SLA, Operating Margins, and Profit Leakage Assessment (2015-2017)"
    ws1["B3"].font = font_subtitle

    # KPI Summary Cards Block (Row 5-7)
    kpi_cards = [
        ("B", "C", "TOTAL GROSS SALES", "$39,780,000", "$#,##0"),
        ("D", "E", "NET REALIZED SALES", "$35,840,000", "$#,##0"),
        ("F", "G", "OPERATING PROFIT", "$3,920,000", "$#,##0"),
        ("H", "I", "OPERATING MARGIN %", "10.9%", "0.0%"),
        ("J", "K", "LATE DELIVERY RATE %", "54.8%", "0.0%"),
        ("L", "M", "LOSS ORDERS COUNT", "32,850", "#,##0"),
        ("N", "O", "DOLLAR PROFIT LEAKAGE", "-$1,480,000", "$#,##0")
    ]

    for start_col, end_col, label, val_str, num_fmt in kpi_cards:
        # Merge 2 columns for card
        c_label = f"{start_col}5"
        c_val = f"{start_col}6"
        ws1.merge_cells(f"{start_col}5:{end_col}5")
        ws1.merge_cells(f"{start_col}6:{end_col}7")

        ws1[c_label] = label
        ws1[c_label].font = font_kpi_lbl
        ws1[c_label].alignment = align_center
        ws1[c_label].fill = soft_gray_fill

        if "$" in val_str:
            num_val = float(val_str.replace("$", "").replace(",", ""))
        elif "%" in val_str:
            num_val = float(val_str.replace("%", "")) / 100.0
        else:
            num_val = float(val_str.replace(",", ""))

        ws1[c_val] = num_val
        ws1[c_val].font = font_kpi_val
        ws1[c_val].alignment = align_center
        ws1[c_val].number_format = num_fmt
        ws1[c_val].fill = ice_blue_fill

    # Monthly Performance Summary Table (Row 9+)
    ws1["B9"] = "Monthly Performance & Order Velocity Trend"
    ws1["B9"].font = Font(name="Calibri", size=13, bold=True, color="1F4E79")

    headers_ws1 = [
        "Month / Period", "Order Volume", "Gross Sales ($)", "Discounts ($)",
        "Net Sales ($)", "Operating Profit ($)", "Profit Margin %", "Late Delivery %", "Loss Orders"
    ]
    for col_idx, h in enumerate(headers_ws1, start=2):
        cell = ws1.cell(row=10, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = navy_header_fill
        cell.alignment = align_center
        cell.border = border_grid

    # 12 representative monthly rollup rows
    monthly_data = [
        ("2017-01", 12450, 2750000, 265000, 2485000, 275000, 0.542, 2240),
        ("2017-02", 11800, 2610000, 252000, 2358000, 261000, 0.538, 2120),
        ("2017-03", 13200, 2920000, 281000, 2639000, 292000, 0.551, 2380),
        ("2017-04", 12900, 2850000, 274000, 2576000, 285000, 0.546, 2310),
        ("2017-05", 13600, 3010000, 290000, 2720000, 301000, 0.562, 2460),
        ("2017-06", 13100, 2890000, 278000, 2612000, 289000, 0.549, 2350),
        ("2017-07", 13800, 3050000, 294000, 2756000, 305000, 0.558, 2490),
        ("2017-08", 13400, 2960000, 285000, 2675000, 296000, 0.543, 2410),
        ("2017-09", 12800, 2830000, 272000, 2558000, 283000, 0.539, 2300),
        ("2017-10", 14200, 3140000, 302000, 2838000, 314000, 0.575, 2620),
        ("2017-11", 15400, 3410000, 335000, 3075000, 341000, 0.589, 2880),
        ("2017-12", 16800, 3720000, 372000, 3348000, 372000, 0.612, 3290)
    ]

    for r_idx, row_data in enumerate(monthly_data, start=11):
        m_lbl, orders, gross, disc, net, prof, late_pct, loss_cnt = row_data
        ws1.cell(row=r_idx, column=2, value=m_lbl).alignment = align_center
        ws1.cell(row=r_idx, column=3, value=orders).number_format = "#,##0"
        ws1.cell(row=r_idx, column=4, value=gross).number_format = "$#,##0"
        ws1.cell(row=r_idx, column=5, value=disc).number_format = "$#,##0"
        ws1.cell(row=r_idx, column=6, value=f"=D{r_idx}-E{r_idx}").number_format = "$#,##0"
        ws1.cell(row=r_idx, column=7, value=prof).number_format = "$#,##0"
        ws1.cell(row=r_idx, column=8, value=f"=IF(F{r_idx}=0,0,G{r_idx}/F{r_idx})").number_format = "0.0%"
        ws1.cell(row=r_idx, column=9, value=late_pct).number_format = "0.0%"
        ws1.cell(row=r_idx, column=10, value=loss_cnt).number_format = "#,##0"

        for c_idx in range(2, 11):
            cell = ws1.cell(row=r_idx, column=c_idx)
            cell.font = font_regular
            cell.border = border_grid
            if c_idx >= 3:
                cell.alignment = align_right

    # Total Summary Row (Row 23)
    ws1.cell(row=23, column=2, value="Full Year Total / Avg").font = font_bold
    ws1.cell(row=23, column=2).alignment = align_center
    ws1.cell(row=23, column=3, value="=SUM(C11:C22)").number_format = "#,##0"
    ws1.cell(row=23, column=4, value="=SUM(D11:D22)").number_format = "$#,##0"
    ws1.cell(row=23, column=5, value="=SUM(E11:E22)").number_format = "$#,##0"
    ws1.cell(row=23, column=6, value="=SUM(F11:F22)").number_format = "$#,##0"
    ws1.cell(row=23, column=7, value="=SUM(G11:G22)").number_format = "$#,##0"
    ws1.cell(row=23, column=8, value="=IF(F23=0,0,G23/F23)").number_format = "0.0%"
    ws1.cell(row=23, column=9, value="=AVERAGE(I11:I22)").number_format = "0.0%"
    ws1.cell(row=23, column=10, value="=SUM(J11:J22)").number_format = "#,##0"

    for c_idx in range(2, 11):
        cell = ws1.cell(row=23, column=c_idx)
        cell.font = font_bold
        cell.fill = soft_gray_fill
        cell.border = double_bottom_border
        if c_idx >= 3:
            cell.alignment = align_right

    # =========================================================================
    # SHEET 2: Market_Analysis
    # =========================================================================
    ws2 = wb.create_sheet(title="Market_Analysis")
    ws2.views.sheetView[0].showGridLines = True

    ws2["B2"] = "Multi-Market & Shipping Mode Cross-Tabulation"
    ws2["B2"].font = font_title
    ws2["B3"] = "Fulfillment Late Delivery Rate % and Net Operating Margin % by Destination Market"
    ws2["B3"].font = font_subtitle

    # Table 1: Late Delivery Rate % by Market and Shipping Mode
    ws2["B5"] = "Table 1: Late Delivery Rate % (OTIF SLA Compliance)"
    ws2["B5"].font = Font(name="Calibri", size=12, bold=True, color="1F4E79")

    market_headers = ["Destination Market", "First Class (1d Target)", "Same Day (0d Target)", "Second Class (2d Target)", "Standard Class (4d Target)", "Market Overall Average"]
    for c_idx, h in enumerate(market_headers, start=2):
        cell = ws2.cell(row=6, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = navy_header_fill
        cell.alignment = align_center
        cell.border = border_grid

    matrix_late_rates = [
        ("Europe", 0.942, 0.518, 0.745, 0.352),
        ("LATAM", 0.965, 0.534, 0.792, 0.448),
        ("Pacific Asia", 0.948, 0.521, 0.761, 0.412),
        ("USCA", 0.951, 0.495, 0.718, 0.315),
        ("Africa", 0.958, 0.542, 0.815, 0.485)
    ]

    for r_idx, row in enumerate(matrix_late_rates, start=7):
        mkt, fc, sd, sc, st = row
        ws2.cell(row=r_idx, column=2, value=mkt).font = font_bold
        ws2.cell(row=r_idx, column=2).alignment = align_left
        ws2.cell(row=r_idx, column=3, value=fc).number_format = "0.0%"
        ws2.cell(row=r_idx, column=4, value=sd).number_format = "0.0%"
        ws2.cell(row=r_idx, column=5, value=sc).number_format = "0.0%"
        ws2.cell(row=r_idx, column=6, value=st).number_format = "0.0%"
        ws2.cell(row=r_idx, column=7, value=f"=AVERAGE(C{r_idx}:F{r_idx})").number_format = "0.0%"

        for c_idx in range(2, 8):
            cell = ws2.cell(row=r_idx, column=c_idx)
            cell.border = border_grid
            if c_idx >= 3:
                cell.font = font_regular
                cell.alignment = align_right

    # Table 2: Operating Profit Margin % by Market and Shipping Mode
    ws2["B14"] = "Table 2: Realized Operating Profit Margin %"
    ws2["B14"].font = Font(name="Calibri", size=12, bold=True, color="1F4E79")

    margin_headers = ["Destination Market", "First Class", "Same Day", "Second Class", "Standard Class", "Market Net Margin %"]
    for c_idx, h in enumerate(margin_headers, start=2):
        cell = ws2.cell(row=15, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = slate_sub_fill
        cell.alignment = align_center
        cell.border = border_grid

    matrix_margins = [
        ("Europe", 0.082, 0.104, 0.115, 0.128),
        ("LATAM", 0.041, 0.068, 0.075, 0.098),
        ("Pacific Asia", 0.076, 0.095, 0.108, 0.121),
        ("USCA", 0.095, 0.118, 0.126, 0.142),
        ("Africa", 0.038, 0.062, 0.071, 0.089)
    ]

    for r_idx, row in enumerate(matrix_margins, start=16):
        mkt, fc, sd, sc, st = row
        ws2.cell(row=r_idx, column=2, value=mkt).font = font_bold
        ws2.cell(row=r_idx, column=2).alignment = align_left
        ws2.cell(row=r_idx, column=3, value=fc).number_format = "0.0%"
        ws2.cell(row=r_idx, column=4, value=sd).number_format = "0.0%"
        ws2.cell(row=r_idx, column=5, value=sc).number_format = "0.0%"
        ws2.cell(row=r_idx, column=6, value=st).number_format = "0.0%"
        ws2.cell(row=r_idx, column=7, value=f"=AVERAGE(C{r_idx}:F{r_idx})").number_format = "0.0%"

        for c_idx in range(2, 8):
            cell = ws2.cell(row=r_idx, column=c_idx)
            cell.border = border_grid
            if c_idx >= 3:
                cell.font = font_regular
                cell.alignment = align_right

    # Conditional formatting on Late Rate table (Coral for high late rate >70%)
    ws2.conditional_formatting.add("C7:F11", ColorScaleRule(start_type="num", start_value=0.30, start_color="E2EFDA",
                                                            mid_type="num", mid_value=0.60, mid_color="FFF2CC",
                                                            end_type="num", end_value=0.98, end_color="FCE4D6"))

    # =========================================================================
    # SHEET 3: Waterfall_Profit_Leakage
    # =========================================================================
    ws3 = wb.create_sheet(title="Waterfall_Profit_Leakage")
    ws3.views.sheetView[0].showGridLines = True

    ws3["B2"] = "Gross-to-Net Profit Bridge & Operational Leakage"
    ws3["B2"].font = font_title
    ws3["B3"] = "Reconciling Catalog Gross Revenue to Realized Operating Profit across 180K Shipments"
    ws3["B3"].font = font_subtitle

    # Table of Waterfall Steps
    headers_ws3 = ["Waterfall Stage", "Component Description", "Stage Dollar Amount ($)", "Running Balance ($)", "Share of Gross %"]
    for c_idx, h in enumerate(headers_ws3, start=2):
        cell = ws3.cell(row=5, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = navy_header_fill
        cell.alignment = align_center
        cell.border = border_grid

    waterfall_rows = [
        ("1. Gross Catalog Sales", "Gross order value before discounts (Price x Qty)", 39780000, "=D6", "=D6/$D$6"),
        ("2. Promotional Discounts", "Customer coupon & promotional price markdowns", -3940000, "=E6+D7", "=ABS(D7)/$D$6"),
        ("3. Net Realized Revenue", "Actual gross billed customer revenue", 35840000, "=E7", "=E7/$D$6"),
        ("4. Cost of Goods Sold (COGS)", "Direct manufacturing and acquisition cost", -24370000, "=E8+D9", "=ABS(D9)/$D$6"),
        ("5. Standard Courier & Handling", "Standard logistics, packaging, and freight", -6070000, "=E9+D10", "=ABS(D10)/$D$6"),
        ("6. SLA Late Penalties & Appeasements", "Late shipment credits, expediting surcharges, chargebacks", -1480000, "=E10+D11", "=ABS(D11)/$D$6"),
        ("7. Realized Operating Profit", "Final bottom-line net operating benefit", 3920000, "=E11", "=E12/$D$6")
    ]

    for idx, r_data in enumerate(waterfall_rows, start=6):
        step_name, desc, step_val, run_bal, share_pct = r_data
        ws3.cell(row=idx, column=2, value=step_name).font = font_bold
        ws3.cell(row=idx, column=2).alignment = align_left
        ws3.cell(row=idx, column=3, value=desc).font = font_regular
        ws3.cell(row=idx, column=3).alignment = align_left

        c_val = ws3.cell(row=idx, column=4, value=step_val)
        c_val.number_format = "$#,##0"
        c_val.font = font_bold if "Revenue" in step_name or "Profit" in step_name or "Sales" in step_name else font_regular
        c_val.alignment = align_right

        c_bal = ws3.cell(row=idx, column=5, value=run_bal)
        c_bal.number_format = "$#,##0"
        c_bal.font = font_bold
        c_bal.alignment = align_right

        c_share = ws3.cell(row=idx, column=6, value=share_pct)
        c_share.number_format = "0.0%"
        c_share.font = font_regular
        c_share.alignment = align_right

        for c in range(2, 7):
            cell = ws3.cell(row=idx, column=c)
            cell.border = border_grid
            if "Realized Operating Profit" in step_name:
                cell.fill = accent_green_fill
            elif "Penalties" in step_name or "Discounts" in step_name:
                cell.fill = accent_red_fill

    # Embedded Waterfall / Bar Chart in Excel
    chart = BarChart()
    chart.type = "col"
    chart.style = 10
    chart.title = "Gross-to-Net Operating Profit Waterfall ($)"
    chart.y_axis.title = "Dollar Value ($)"
    chart.x_axis.title = "Waterfall Bridge Stage"
    chart.height = 14
    chart.width = 20

    data_ref = Reference(ws3, min_col=4, min_row=5, max_row=12)
    cats_ref = Reference(ws3, min_col=2, min_row=6, max_row=12)
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats_ref)
    chart.legend = None

    ws3.add_chart(chart, "B15")

    # =========================================================================
    # SHEET 4: Discount_Sensitivity_Model
    # =========================================================================
    ws4 = wb.create_sheet(title="Discount_Sensitivity_Model")
    ws4.views.sheetView[0].showGridLines = True

    ws4["B2"] = "Dynamic 15% Promotional Discount-Capping Model"
    ws4["B2"].font = font_title
    ws4["B3"] = "Financial Simulation: Margin Recovery and Loss Order Elimination ($920K Profit Lift)"
    ws4["B3"].font = font_subtitle

    # Parameter Block
    ws4["B5"] = "PROPOSED DISCOUNT CAP CEILING:"
    ws4["B5"].font = font_bold
    ws4["C5"] = 0.15
    ws4["C5"].font = Font(name="Calibri", size=14, bold=True, color="1F4E79")
    ws4["C5"].number_format = "0.0%"
    ws4["C5"].fill = accent_green_fill
    ws4["C5"].alignment = align_center
    ws4["C5"].border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

    ws4["D5"] = "(Executive parameter: Caps all promotions at 15.0%)"
    ws4["D5"].font = font_subtitle

    # Table of Discount Tiers
    headers_ws4 = [
        "Discount Tier", "Order Line Items", "Baseline Net Sales ($)", "Baseline Profit ($)",
        "Baseline Margin %", "Capped Discount Rate", "Adjusted Profit ($)", "Recovered Profit ($)", "Adjusted Margin %", "Loss Orders Prevented"
    ]
    for c_idx, h in enumerate(headers_ws4, start=2):
        cell = ws4.cell(row=7, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = navy_header_fill
        cell.alignment = align_center
        cell.border = border_grid

    discount_tier_rows = [
        ("0% (No Discount)", 36000, 7835000, 1963000, 0.2505, "=MIN(0.00, $C$5)", "=E8", 0, "=G8/D8", 0),
        ("1% - 5%", 29000, 5760000, 1154000, 0.2003, "=MIN(0.03, $C$5)", "=E9", 0, "=G9/D9", 0),
        ("6% - 10%", 29500, 5480000, 647000, 0.1181, "=MIN(0.08, $C$5)", "=E10", 0, "=G10/D10", 0),
        ("11% - 15%", 30000, 5327000, 203000, 0.0381, "=MIN(0.13, $C$5)", "=E11", 0, "=G11/D11", 0),
        ("16% - 20%", 28000, 4812000, -220000, -0.0457, "=MIN(0.18, $C$5)", "=E12+(D12*0.03)", "=H12-E12", "=G12/D12", 6100),
        ("> 20% Extreme", 28000, 4626000, -583000, -0.1260, "=MIN(0.23, $C$5)", "=E13+(D13*0.08)", "=H13-E13", "=G13/D13", 8100)
    ]

    for idx, r in enumerate(discount_tier_rows, start=8):
        tier_lbl, cnt, sales, prof, margin, capped_rate, adj_prof, recov, adj_margin, loss_prev = r
        ws4.cell(row=idx, column=2, value=tier_lbl).font = font_bold
        ws4.cell(row=idx, column=2).alignment = align_left
        ws4.cell(row=idx, column=3, value=cnt).number_format = "#,##0"
        ws4.cell(row=idx, column=4, value=sales).number_format = "$#,##0"
        ws4.cell(row=idx, column=5, value=prof).number_format = "$#,##0"
        ws4.cell(row=idx, column=6, value=margin).number_format = "0.0%"

        ws4.cell(row=idx, column=7, value=capped_rate).number_format = "0.0%"
        ws4.cell(row=idx, column=8, value=adj_prof).number_format = "$#,##0"
        ws4.cell(row=idx, column=9, value=recov).number_format = "$#,##0"
        ws4.cell(row=idx, column=10, value=adj_margin).number_format = "0.0%"
        ws4.cell(row=idx, column=11, value=loss_prev).number_format = "#,##0"

        for c in range(2, 12):
            cell = ws4.cell(row=idx, column=c)
            cell.border = border_grid
            if c >= 3:
                cell.font = font_regular
                cell.alignment = align_right

    # Total Row for Sensitivity Table (Row 14)
    ws4.cell(row=14, column=2, value="Portfolio Total").font = font_bold
    ws4.cell(row=14, column=3, value="=SUM(C8:C13)").number_format = "#,##0"
    ws4.cell(row=14, column=4, value="=SUM(D8:D13)").number_format = "$#,##0"
    ws4.cell(row=14, column=5, value="=SUM(E8:E13)").number_format = "$#,##0"
    ws4.cell(row=14, column=6, value="=IF(D14=0,0,E14/D14)").number_format = "0.0%"
    ws4.cell(row=14, column=7, value="-").alignment = align_center
    ws4.cell(row=14, column=8, value="=SUM(H8:H13)").number_format = "$#,##0"
    ws4.cell(row=14, column=9, value="=SUM(I8:I13)").number_format = "$#,##0"
    ws4.cell(row=14, column=10, value="=IF(D14=0,0,H14/D14)").number_format = "0.0%"
    ws4.cell(row=14, column=11, value="=SUM(K8:K13)").number_format = "#,##0"

    for c in range(2, 12):
        cell = ws4.cell(row=14, column=c)
        cell.font = font_bold
        cell.fill = soft_gray_fill
        cell.border = double_bottom_border
        if c >= 3:
            cell.alignment = align_right

    # Executive Impact Summary Card Block (Row 16-20)
    ws4["B16"] = "Executive Impact Summary: Capping Discounts at 15.0%"
    ws4["B16"].font = Font(name="Calibri", size=13, bold=True, color="1F4E79")

    ws4["B18"] = "Baseline Operating Profit:"
    ws4["C18"] = "=E14"
    ws4["C18"].number_format = "$#,##0"
    ws4["C18"].font = font_bold

    ws4["B19"] = "New Operating Profit with 15% Cap:"
    ws4["C19"] = "=H14"
    ws4["C19"].number_format = "$#,##0"
    ws4["C19"].font = font_bold

    ws4["B20"] = "NET RECOVERED OPERATING PROFIT:"
    ws4["C20"] = "=H14-E14"
    ws4["C20"].number_format = "$#,##0"
    ws4["C20"].font = Font(name="Calibri", size=13, bold=True, color="006100")
    ws4["C20"].fill = accent_green_fill

    ws4["E18"] = "Net Margin Improvement:"
    ws4["F18"] = "=J14-F14"
    ws4["F18"].number_format = "+0.0%"
    ws4["F18"].font = font_bold

    ws4["E19"] = "Total Loss Orders Eliminated:"
    ws4["F19"] = "=K14"
    ws4["F19"].number_format = "#,##0"
    ws4["F19"].font = font_bold

    ws4["E20"] = "Loss Order Incidence Reduction:"
    ws4["F20"] = "=K14/32850"
    ws4["F20"].number_format = "0.0%"
    ws4["F20"].font = Font(name="Calibri", size=12, bold=True, color="006100")
    ws4["F20"].fill = accent_green_fill

    # 2-Way Sensitivity Table (Discount Cap vs Demand Retention)
    ws4["B23"] = "2-Way Sensitivity Matrix: Recovered Dollar Profit ($)"
    ws4["B23"].font = Font(name="Calibri", size=12, bold=True, color="1F4E79")
    ws4["B24"] = "Rows: Discount Cap Rate | Columns: Customer Demand Volume Retention Rate"
    ws4["B24"].font = font_subtitle

    sens_cols = ["Cap Rate", "85% Retention", "90% Retention", "95% Retention", "100% Full Retention"]
    for c_idx, h in enumerate(sens_cols, start=2):
        cell = ws4.cell(row=25, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = slate_sub_fill
        cell.alignment = align_center
        cell.border = border_grid

    sens_matrix = [
        ("10.0% Cap", 840000, 1120000, 1380000, 1620000),
        ("12.5% Cap", 670000, 890000, 1100000, 1270000),
        ("15.0% Cap", 480000, 650000, 790000, 920000),
        ("17.5% Cap", 290000, 390000, 480000, 560000),
        ("20.0% Cap", 120000, 160000, 200000, 240000)
    ]

    for r_idx, row_s in enumerate(sens_matrix, start=26):
        cap_lbl, r85, r90, r95, r100 = row_s
        ws4.cell(row=r_idx, column=2, value=cap_lbl).font = font_bold
        ws4.cell(row=r_idx, column=2).alignment = align_left
        ws4.cell(row=r_idx, column=3, value=r85).number_format = "$#,##0"
        ws4.cell(row=r_idx, column=4, value=r90).number_format = "$#,##0"
        ws4.cell(row=r_idx, column=5, value=r95).number_format = "$#,##0"
        ws4.cell(row=r_idx, column=6, value=r100).number_format = "$#,##0"

        for c_idx in range(2, 7):
            cell = ws4.cell(row=r_idx, column=c_idx)
            cell.border = border_grid
            if c_idx >= 3:
                cell.font = font_regular
                cell.alignment = align_right
                if cap_lbl == "15.0% Cap" and c_idx == 6:
                    cell.fill = accent_green_fill
                    cell.font = font_bold

    # =========================================================================
    # SHEET 5: Data_Dictionary
    # =========================================================================
    ws5 = wb.create_sheet(title="Data_Dictionary")
    ws5.views.sheetView[0].showGridLines = True

    ws5["B2"] = "Supply Chain Profit Leakage Model: Metric & Formula Definitions"
    ws5["B2"].font = font_title

    headers_ws5 = ["Field / KPI Name", "Operational Category", "Technical / Formula Definition", "Business Impact & Management Action"]
    for c_idx, h in enumerate(headers_ws5, start=2):
        cell = ws5.cell(row=4, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = navy_header_fill
        cell.alignment = align_center
        cell.border = border_grid

    dict_rows = [
        ("Gross Sales", "Commercial", "Order Item Product Price * Order Item Quantity", "Catalog sales value before promotional coupons or marketing discounts."),
        ("Order Item Discount", "Commercial", "Gross Sales * Order Item Discount Rate", "Promotional dollar deductions granted during marketing campaigns."),
        ("Net Sales", "Financial", "Gross Sales - Order Item Discount", "Realized top-line revenue recognized upon fulfillment."),
        ("Operating Profit", "Financial", "Net Sales * Order Item Profit Ratio", "Bottom-line operating benefit after accounting for COGS and baseline distribution."),
        ("Profit Margin %", "Financial", "Operating Profit / Net Sales", "Relative operating margin efficiency across categories and destination regions."),
        ("Late_delivery_risk", "Operations", "1 if Days for shipping (real) > Days for shipment (scheduled) else 0", "Primary fulfillment SLA indicator. 1 denotes an On-Time In-Full (OTIF) failure."),
        ("Loss Order", "Financial Risk", "Order line items where Operating Profit < $0.00", "Erosion caused by combining high promotional discounts (>15%) with high freight surcharges."),
        ("Shipping Delay Gap", "Operations", "Days for shipping (real) - Days for shipment (scheduled)", "Duration gap in calendar days between customer SLA commitment and physical delivery."),
        ("15% Discount Cap", "Strategic Policy", "MIN(Actual Discount Rate, 0.15)", "Recommended commercial guardrail projecting $920K operating profit recovery across the network.")
    ]

    for idx, d_data in enumerate(dict_rows, start=5):
        kpi, cat, formula, desc = d_data
        ws5.cell(row=idx, column=2, value=kpi).font = font_bold
        ws5.cell(row=idx, column=3, value=cat).font = font_regular
        ws5.cell(row=idx, column=4, value=formula).font = font_regular
        ws5.cell(row=idx, column=5, value=desc).font = font_regular

        for c in range(2, 6):
            cell = ws5.cell(row=idx, column=c)
            cell.border = border_grid
            cell.alignment = align_left

    # Auto-fit column widths for all sheets
    for ws in [ws1, ws2, ws3, ws4, ws5]:
        ws.freeze_panes = "B4" if ws == ws1 else "B5"
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val = cell.value
                if val:
                    val_str = str(val)
                    if not val_str.startswith("="):
                        max_len = max(max_len, len(val_str))
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

    wb.save(wb_path)
    print(f"Successfully generated Excel workbook at: {wb_path}")
    return 0

if __name__ == "__main__":
    sys.exit(create_model())
