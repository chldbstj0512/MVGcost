def count_tokens(text: str):
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except Exception:
        # fallback: 문자수/4
        return max(1, len(text) // 4)
