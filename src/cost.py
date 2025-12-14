def calc_cost(prompt_tok, completion_tok, price_per_1k):
    return ((prompt_tok + completion_tok) / 1000) * price_per_1k
