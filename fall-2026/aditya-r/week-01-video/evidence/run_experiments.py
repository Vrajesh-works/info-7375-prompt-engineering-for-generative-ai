"""run_experiments.py — every recorded number in "A Chatbot Is a Loop." comes from this file.

Runs a small open chat model (SmolLM2-135M-Instruct, pinned revision) locally on CPU and
writes one JSON per experiment into evidence/runs/, plus runs/manifest.json with a SHA-256
of each file and the environment that produced it.

  france        greedy answer to "What is the capital of France?", top-10 candidates per pass
  middlemarch   greedy answer to "Who wrote the novel Middlemarch?", top-10 per pass
  no_stop       the France question with the end-of-turn tokens banned: the loop cannot stop
  force_george  the Middlemarch question with " George" forced at the name pass
  paths         the model's own probability for the Richardson answer and the Eliot answer
  sample        the Middlemarch question sampled 200 times (seeds 0-199, temperature 1.0,
                no top-k/top-p truncation), each answer stored verbatim

Greedy = always append the single most likely token (argmax). Deterministic on a given
torch build; see verify.py for the check.

Usage (from evidence/):  python run_experiments.py [--out runs]
"""
import argparse, hashlib, json, math, platform, re, sys
from pathlib import Path

import torch
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = "HuggingFaceTB/SmolLM2-135M-Instruct"
REVISION = "12fd25f77366fa6b3b4b768ec3050bf629380bac"
TOPK = 10
N_SAMPLES = 200
SAMPLE_MAX_NEW = 48
ELIOT = re.compile(r"\bGeorge Eliot\b|\bMary Ann Evans\b")


def load():
    tok = AutoTokenizer.from_pretrained(MODEL, revision=REVISION)
    model = AutoModelForCausalLM.from_pretrained(MODEL, revision=REVISION, dtype=torch.float32)
    return tok, model.eval()


def chat_ids(tok, question):
    text = tok.apply_chat_template([{"role": "user", "content": question}], tokenize=False,
                                   add_generation_prompt=True)
    return text, tok(text, return_tensors="pt").input_ids


def trace(model, tok, ids, max_steps, stop_ids, banned=(), forced=None):
    """Run the loop one token at a time. Probabilities are the model's own softmax BEFORE any
    ban or force is applied, so every number is what the model predicted."""
    steps = []
    with torch.no_grad():
        for s in range(max_steps):
            logits = model(ids).logits[0, -1]
            probs = torch.softmax(logits, dim=-1)
            top = torch.topk(probs, TOPK)
            if forced and s in forced:
                nxt = forced[s]
            else:
                masked = logits.clone()
                for b in banned:
                    masked[b] = float("-inf")
                nxt = int(torch.argmax(masked))
            steps.append({
                "pass": s + 1,
                "tokens_in": int(ids.shape[1]),
                "top": [{"token": tok.decode([int(i)]), "id": int(i), "p": round(float(p), 4)}
                        for p, i in zip(top.values, top.indices)],
                "chosen": tok.decode([nxt]), "chosen_id": nxt,
                "p_chosen": round(float(probs[nxt]), 6),
                "rank_chosen": int((probs > probs[nxt]).sum()) + 1,
                "p_stop": round(float(sum(probs[i] for i in stop_ids)), 4),
                "forced": bool(forced and s in forced),
            })
            ids = torch.cat([ids, torch.tensor([[nxt]])], dim=1)
            if not banned and nxt in stop_ids:
                break
    return ids, steps


def answer_text(tok, ids, n_prompt):
    return tok.decode(ids[0, n_prompt:], skip_special_tokens=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="runs")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    torch.manual_seed(0)
    tok, model = load()
    stop_ids = sorted({tok.eos_token_id, tok.convert_tokens_to_ids("<|im_end|>")})
    common = {"model": MODEL, "revision": REVISION, "decoding": "greedy (argmax)"}
    results = {}

    for key, q in (("france", "What is the capital of France?"),
                   ("middlemarch", "Who wrote the novel Middlemarch?")):
        text, ids0 = chat_ids(tok, q)
        ids, steps = trace(model, tok, ids0, 40, set(stop_ids))
        results[key] = {**common, "question": q, "chat_template_text": text,
                        "prompt_tokens": int(ids0.shape[1]), "vocab_size": model.config.vocab_size,
                        "answer": answer_text(tok, ids, ids0.shape[1]),
                        "passes": len(steps), "stopped": steps[-1]["chosen_id"] in stop_ids,
                        "steps": steps}

    # the loop with its stop tokens banned
    q = "What is the capital of France?"
    _, ids0 = chat_ids(tok, q)
    ids, steps = trace(model, tok, ids0, 60, set(stop_ids), banned=stop_ids)
    results["no_stop"] = {**common, "question": q, "intervention": "end-of-turn tokens banned",
                          "banned": [tok.decode([i]) for i in stop_ids], "max_passes": 60,
                          "continuation": answer_text(tok, ids, ids0.shape[1]), "steps": steps}

    # force " George" at the pass where the greedy answer chose " Samuel"
    q = "Who wrote the novel Middlemarch?"
    _, ids0 = chat_ids(tok, q)
    base = results["middlemarch"]["steps"]
    name_idx = [s["chosen"] for s in base].index(" Samuel")
    george = tok.encode(" George", add_special_tokens=False)
    assert len(george) == 1, george
    ids, steps = trace(model, tok, ids0, 40, set(stop_ids), forced={name_idx: george[0]})
    results["force_george"] = {**common, "question": q,
                               "intervention": f"' George' forced at pass {name_idx + 1}",
                               "name_pass": name_idx + 1, "answer": answer_text(tok, ids, ids0.shape[1]),
                               "steps": steps}

    # the model's own probability for each whole answer = product of its passes (chain rule)
    def path(steps):
        logp = sum(math.log(s["p_chosen"]) for s in steps)
        return {"passes": len(steps), "log_p": logp, "p": math.exp(logp),
                "factors": [s["p_chosen"] for s in steps]}
    results["paths"] = {**common,
                        "richardson": {"answer": results["middlemarch"]["answer"], **path(base)},
                        "eliot": {"answer": results["force_george"]["answer"],
                                  **path(results["force_george"]["steps"])},
                        "paris": {"answer": results["france"]["answer"],
                                  **path(results["france"]["steps"])}}

    # sampling: one seed per run, the model's full distribution at temperature 1.0
    _, ids0 = chat_ids(tok, q)
    runs = []
    for seed in range(N_SAMPLES):
        torch.manual_seed(seed)
        with torch.no_grad():
            g = model.generate(ids0, do_sample=True, temperature=1.0, top_k=0, top_p=1.0,
                               max_new_tokens=SAMPLE_MAX_NEW, pad_token_id=tok.eos_token_id)
        t = answer_text(tok, g, ids0.shape[1]).strip()
        runs.append({"seed": seed, "names_george_eliot": bool(ELIOT.search(t)), "answer": t})
    results["sample"] = {"model": MODEL, "revision": REVISION, "question": q,
                         "decoding": "sampling, temperature 1.0, top_k=0, top_p=1.0",
                         "seeds": f"0-{N_SAMPLES - 1}", "max_new_tokens": SAMPLE_MAX_NEW,
                         "classifier": "names_george_eliot = regex " + ELIOT.pattern,
                         "n": N_SAMPLES,
                         "george_eliot_runs": sum(r["names_george_eliot"] for r in runs),
                         "runs": runs}

    env = {"python": sys.version.split()[0], "torch": torch.__version__,
           "transformers": transformers.__version__, "platform": platform.platform()}
    manifest = {"env": env, "files": {}}
    for key, body in results.items():
        p = out / f"{key}.json"
        p.write_text(json.dumps(body, indent=2, ensure_ascii=False) + "\n")
        manifest["files"][p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    f, m, fg = results["france"], results["middlemarch"], results["force_george"]
    print(f"france       : {f['answer']!r}  ({f['passes']} passes)")
    print(f"middlemarch  : {m['answer']!r}  ({m['passes']} passes)")
    print(f"no_stop      : {results['no_stop']['continuation']!r}")
    g = next(c for c in m["steps"][name_idx]["top"] if c["token"] == " George")
    print(f"force_george : {fg['answer']!r}  (' George' at pass {name_idx + 1}: p={g['p']}, "
          f"rank {[c['token'] for c in m['steps'][name_idx]['top']].index(' George') + 1})")
    for k in ("paris", "richardson", "eliot"):
        print(f"path {k:10}: p={results['paths'][k]['p']:.6g} over {results['paths'][k]['passes']} passes")
    print(f"sample       : {results['sample']['george_eliot_runs']}/{N_SAMPLES} name George Eliot")
    print(f"env          : {env}")


if __name__ == "__main__":
    main()
