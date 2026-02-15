from typing import Iterable, Tuple
import pandas as pd


def count_tokens_tiktoken(
    messages: Iterable[Tuple[str, str]], encoding_name: str = "o200k_base"
) -> pd.DataFrame:
    """
    messages: iterable de (conversation_id, text)
    Retour: df (conversation_id, tokens)
    """
    import tiktoken  # lazy import

    enc = tiktoken.get_encoding(encoding_name)

    rows = []
    for conv_id, text in messages:
        n = len(enc.encode(text))
        rows.append({"conversation_id": conv_id, "tokens": n})
    return pd.DataFrame(rows)
