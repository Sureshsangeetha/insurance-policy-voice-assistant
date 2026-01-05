import json
import os

POLICY_FILE_PATH = os.path.join("policies", "HealthSecure_v3.json")


def fetch_policy_content(intent: str) -> dict:
    """
    Fetches policy information strictly from approved policy documents.
    NO hallucination. NO inference.
    """

    with open(POLICY_FILE_PATH, "r", encoding="utf-8") as file:
        policy_data = json.load(file)

    intent_section_map = {
        "policy_coverage": "2.1",
        "policy_benefits": "2.1",
        "policy_exclusions": "2.4",
        "claim_process_info": "4.1",
        "renewal_date": "5.1",
        "policy_validity": "5.2"
    }

    section_id = intent_section_map.get(intent)

    if not section_id:
        return {
            "answer": "This request requires assistance from a human agent.",
            "reference": []
        }

    section = policy_data["sections"].get(section_id)

    if not section:
        return {
            "answer": "Requested policy information is unavailable.",
            "reference": []
        }

    return {
        "answer": section["content"],
        "reference": [f"HealthSecure_v3_Section_{section_id}"]
    }
