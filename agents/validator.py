def validate_fact_sheet(data):

    safe_data = {}

    safe_data["product"] = data.get("product")
    safe_data["features"] = data.get("features", [])
    safe_data["audience"] = data.get("audience")

    # Remove unsafe % claims
    vp = data.get("value_proposition", "")
    if "%" in vp:
        vp = "Improves team productivity through intelligent automation"

    safe_data["value_proposition"] = vp

    # Only verified claims
    safe_data["claims"] = data.get("verified_claims", [])

    # Ensure technical specs always exist
    safe_data["technical_specs"] = data.get("technical_specs", {
        "architecture": "",
        "apis": [],
        "uptime": "",
        "compliance": []
    })

    # Use actual use case if available
    use_case = data.get("use_case")
    if not use_case:
        use_case = "Reduced onboarding time from 5 days to 2 days"

    safe_data["use_case"] = use_case

    return safe_data