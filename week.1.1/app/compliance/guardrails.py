import re

class apply_guardrails:
    # Very simple demo masking (expand as needed)
    @staticmethod
    def mask_pii(text: str) -> str:
        # Mask 10-digit phone numbers
        text = re.sub(r"\b\d{10}\b", "XXXXXXXXXX", text)
        # Mask email
        text = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[EMAIL]", text)
        return text

    @staticmethod
    def enforce_no_advice(answer: str) -> str:
        # Block personalized advice phrases
        banned = ["you should", "i recommend", "best plan", "choose", "take this policy"]
        lower = answer.lower()
        if any(b in lower for b in banned):
            return (
                "I can share policy information, but I can’t provide personalized recommendations. "
                "Please refer to the policy document or speak to a licensed agent."
            )
        return answer
