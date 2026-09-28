# How much do the video's seed-7 results depend on seed 7?
# Re-runs the SAME constructed toy (preference_toy.train) for seeds 0..499 at each
# share of reviewers who can check, and reports the spread. Offline; prints JSON.
# Added after an independent review pointed out that the "near the vote share"
# test was only checked on seed 7 (see FRICTIONAL.md entry 3).
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("toy", HERE / "preference_toy.py")
toy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(toy)

SEEDS = range(500)


def pct(values, q):
    values = sorted(values)
    return values[min(len(values) - 1, int(q * len(values)))]


def main():
    rows = []
    for share in toy.SHARES_WHO_CAN_CHECK:
        gaps, learned, sydney_fav, fav_matches_votes = [], [], 0, 0
        for seed in SEEDS:
            run = toy.train(share, seed=seed)
            p = toy.probabilities(run["scores"])[0]
            v = run["votes_for"][0] / toy.VOTES
            gaps.append(abs(p - v))
            learned.append(p)
            sydney_fav += p < 0.5
            fav_matches_votes += (p > 0.5) == (run["votes_for"][0] > run["votes_for"][1])
        n = len(SEEDS)
        rows.append({
            "share_who_can_check": share,
            "seeds": n,
            "learned_chance_correct_median": round(pct(learned, 0.5), 4),
            "learned_chance_correct_5th_95th": [round(pct(learned, 0.05), 4), round(pct(learned, 0.95), 4)],
            "abs_gap_to_vote_share_median": round(pct(gaps, 0.5), 4),
            "abs_gap_to_vote_share_95th": round(pct(gaps, 0.95), 4),
            "abs_gap_to_vote_share_max": round(max(gaps), 4),
            "share_of_seeds_wrong_reply_favoured": round(sydney_fav / n, 4),
            "share_of_seeds_favourite_is_reply_with_more_votes": round(fav_matches_votes / n, 4),
        })
    return {"mode": "CONSTRUCTED toy, seeds 0-499, same settings as preference_toy.py",
            "settings": {"votes": toy.VOTES, "learning_rate": toy.LEARNING_RATE},
            "by_share": rows}


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
