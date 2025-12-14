import re

PHONE = re.compile(r"\b(01[016789])[-.\s]?(\d{3,4})[-.\s]?(\d{4})\b")
EMAIL = re.compile(r"([A-Za-z0-9._%+-])[^@]*(@[^@\s]+)")
RRN   = re.compile(r"\b(\d{6})[-]?\d{7}\b")

def mask_pii(text: str):
    hits = 0

    def _phone(m):
        nonlocal hits
        hits += 1
        return f"{m.group(1)}-****-{m.group(3)}"

    def _email(m):
        nonlocal hits
        hits += 1
        return f"{m.group(1)}***{m.group(2)}"

    def _rrn(m):
        nonlocal hits
        hits += 1
        return f"{m.group(1)}-*******"

    text = PHONE.sub(_phone, text)
    text = EMAIL.sub(_email, text)
    text = RRN.sub(_rrn, text)

    return text, hits
