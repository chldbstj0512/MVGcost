TOXIC_WORDS = ["kill", "hate", "stupid", "idiot", "die"]

def moderate(text: str, threshold=0.5):
    hits = sum(word in text.lower() for word in TOXIC_WORDS)
    score = hits / max(len(TOXIC_WORDS), 1)

    if score >= threshold:
        return {
            "blocked": True,
            "score": score,
            "output": "This response was blocked due to safety policy."
        }

    return {
        "blocked": False,
        "score": score,
        "output": text
    }
