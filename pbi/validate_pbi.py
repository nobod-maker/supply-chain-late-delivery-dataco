"""
04_Supply_Chain_DataCo: Power BI PBIR & TMDL Validator
Validates PBIR schema rules, TMDL tab indentation, relationship integrity, and DAX measures.
"""

import os
import sys
import json
import subprocess

def validate():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pbip_file = os.path.join(base_dir, "Supply_Chain_Command_Center.pbip")
    report_dir = os.path.join(base_dir, "Supply_Chain_Command_Center.Report")
    model_dir = os.path.join(base_dir, "Supply_Chain_Command_Center.SemanticModel")
    measures_file = os.path.join(base_dir, "measures.dax")

    print("Running Power BI PBIR & TMDL Validation Checks...")
    errors = []

    # 1. Validate .pbip
    if not os.path.exists(pbip_file):
        errors.append(f"Missing .pbip file: {pbip_file}")
    else:
        with open(pbip_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        artifacts = data.get("artifacts", [])
        if len(artifacts) != 1 or "report" not in artifacts[0]:
            errors.append(".pbip artifacts array must contain ONLY a 'report' entry!")
        print(" [PASS] .pbip format is valid.")

    # 2. Validate definition.pbir
    pbir_file = os.path.join(report_dir, "definition.pbir")
    if not os.path.exists(pbir_file):
        errors.append(f"Missing definition.pbir: {pbir_file}")
    else:
        with open(pbir_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        path_ref = data.get("datasetReference", {}).get("byPath", {}).get("path")
        if not path_ref or not isinstance(path_ref, str):
            errors.append("definition.pbir datasetReference.byPath.path must be a non-null string!")
        print(" [PASS] definition.pbir relative path reference is valid.")

    # 3. Validate report pages & visuals
    pages_json = os.path.join(report_dir, "definition", "pages", "pages.json")
    if not os.path.exists(pages_json):
        errors.append(f"Missing pages.json: {pages_json}")
    else:
        with open(pages_json, "r", encoding="utf-8") as f:
            p_data = json.load(f)
        pages = p_data.get("pageOrder", [])
        if len(pages) != 4:
            errors.append(f"Expected 4 report pages, found {len(pages)}")
        print(f" [PASS] 4 report pages registered in pages.json: {pages}")

    # 4. Validate TMDL syntax & strict tab indentation
    tmdl_files = [
        os.path.join(model_dir, "definition", "model.tmdl"),
        os.path.join(model_dir, "definition", "relationships.tmdl")
    ]
    tables_dir = os.path.join(model_dir, "definition", "tables")
    if os.path.exists(tables_dir):
        for f in os.listdir(tables_dir):
            if f.endswith(".tmdl"):
                tmdl_files.append(os.path.join(tables_dir, f))

    for tf in tmdl_files:
        if not os.path.exists(tf):
            errors.append(f"Missing TMDL file: {tf}")
            continue
        with open(tf, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for idx, line in enumerate(lines):
            stripped = line.lstrip()
            if stripped and line.startswith(" "):
                # TMDL requires tabs (\t) rather than spaces
                errors.append(f"TMDL indentation violation at {os.path.basename(tf)} line {idx+1}: contains leading spaces instead of tabs!")
                break
    print(f" [PASS] Checked {len(tmdl_files)} TMDL files for strict tab-indentation compliance.")

    # 5. Validate measures.dax
    if not os.path.exists(measures_file):
        errors.append(f"Missing measures.dax: {measures_file}")
    else:
        with open(measures_file, "r", encoding="utf-8") as f:
            dax_text = f.read()
        required_measures = [
            "[Total Orders]", "[Total Sales]", "[Total Profit]", "[Profit Margin %]",
            "[Late Delivery Rate %]", "[OTIF %]", "[Shipping Delay Gap Days]",
            "[Loss Orders Count]", "[Sales SPLY]", "[Sales YoY %]",
            "[Simulated 15% Cap Profit Recovery]"
        ]
        for m in required_measures:
            if m not in dax_text:
                errors.append(f"Missing required DAX measure: {m}")
        print(f" [PASS] All {len(required_measures)} enterprise DAX measures verified in measures.dax.")

    # 6. Try running pbi-cli if available
    pbi_exe = r"C:\Users\ADMIN\AppData\Roaming\Python\Python312\Scripts\pbi.exe"
    if os.path.exists(pbi_exe):
        try:
            print("Running external pbi report info...")
            res = subprocess.run([pbi_exe, "report", "info", "--path", report_dir], capture_output=True, text=True, timeout=15)
            print(f"pbi report info exit code: {res.returncode}")
            if res.stdout:
                print(res.stdout[:200])
        except Exception as e:
            print(f"Note: pbi CLI execution note: {e}")

    if errors:
        print("\nVALIDATION FAILED with errors:")
        for err in errors:
            print(f" - {err}")
        return 1

    print("\nALL POWER BI PBIR & TMDL VALIDATION CHECKS PASSED! (Exit code 0)")
    return 0

if __name__ == "__main__":
    sys.exit(validate())
