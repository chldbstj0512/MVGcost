import time, csv, os
import random
from datetime import datetime

from src.pii_mask import mask_pii
from src.moderation import moderate
from src.tokenizer import count_tokens
from src.cost import calc_cost

LOG_PATH = "logs/access_cost_log.csv"

def process_request(
    user_text,
    route="default",
    price_per_1k=0.002,
    cache_hit_rate=0.0
):
    start = time.time()

    # 1. PII masking
    masked_text, pii_hits = mask_pii(user_text)

    # 2. Dummy completion
    completion_len = max(20, len(masked_text) // 5)
    dummy_output = masked_text

    # 3. Moderation
    mod = moderate(dummy_output)
    blocked = mod["blocked"]

    # 4. Token count
    prompt_tok = count_tokens(masked_text)

    if blocked:
        completion_tok = 0
        final_output = mod["output"]
    else:
        completion_tok = count_tokens(dummy_output)
        final_output = dummy_output

    # 5. Raw cost
    request_cost = calc_cost(prompt_tok, completion_tok, price_per_1k)

    # 6. Cache simulation
    cached = random.random() < cache_hit_rate
    effective_cost = 0.0 if cached else request_cost

    latency_ms = int((time.time() - start) * 1000)

    # 7. CSV logging
    os.makedirs("logs", exist_ok=True)
    write_header = not os.path.exists(LOG_PATH)

    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow([
                "ts","route","prompt_tok","completion_tok",
                "price_per_1k","request_cost",
                "cached","latency_ms","pii_hits","blocked"
            ])
        writer.writerow([
            datetime.utcnow().isoformat(),
            route,
            prompt_tok,
            completion_tok,
            price_per_1k,
            round(effective_cost, 6),
            cached,
            latency_ms,
            pii_hits,
            blocked
        ])

    return {
        "response": final_output,
        "cost": effective_cost,
        "blocked": blocked,
        "cached": cached,
        "latency_ms": latency_ms
    }
