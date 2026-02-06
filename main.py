# Medical Laboratory Reference Checker

reference_ranges = {
    "hb": {"low": 13.0, "high": 17.0, "unit": "g/dL"},
    "wbc": {"low": 4.0, "high": 11.0, "unit": "x10^9/L"},
    "platelets": {"low": 150, "high": 450, "unit": "x10^9/L"}
}

test = input("Enter test name (Hb, WBC, Platelets): ").lower()
value = float(input("Enter result value: "))

if test in reference_ranges:
    ref = reference_ranges[test]
    if value < ref["low"]:
        print("Result: LOW")
    elif value > ref["high"]:
        print("Result: HIGH")
    else:
        print("Result: NORMAL")
    print(f"Reference Range: {ref['low']}–{ref['high']} {ref['unit']}")
else:
    print("Test not found.")
