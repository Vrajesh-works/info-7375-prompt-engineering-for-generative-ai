# Week 1 explainer evidence: how open tokenizers split the words in the video.
# Reproduce:  pip install tiktoken==0.14.0  &&  python3 tokenize_examples.py
# Writes tokens.json next to this file. These are OpenAI's open tokenizers,
# NOT Claude's (Claude's tokenizer is not public), so exact splits differ.
import json
from pathlib import Path

import tiktoken

ENCODINGS = ["o200k_base", "cl100k_base"]
STRINGS = [
    "strawberry",
    " strawberry",
    "Strawberry",
    "the",
    " the",
    "unbelievable",
    " unbelievable",
    "How many r's are in strawberry?",
    "s t r a w b e r r y",
]


def pieces(enc, ids):
    return [enc.decode_single_token_bytes(i).decode("utf-8", "replace") for i in ids]


def main():
    out = {"tiktoken_version": tiktoken.__version__, "encodings": {}}
    for name in ENCODINGS:
        enc = tiktoken.get_encoding(name)
        rows = []
        for s in STRINGS:
            ids = enc.encode(s)
            rows.append({"text": s, "n_tokens": len(ids), "ids": ids, "pieces": pieces(enc, ids)})
            print(f"{name:12} {s!r:36} {len(ids)} {ids} {pieces(enc, ids)}")
        out["encodings"][name] = {"vocab_size": enc.n_vocab, "examples": rows}
    path = Path(__file__).with_name("tokens.json")
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {path.name}")


if __name__ == "__main__":
    main()
