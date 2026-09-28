# INFO 7375 Week 1 video evidence: why preference tuning can prefer a
# confident wrong answer (Chapter 1, Part 1, "Where the numbers come from").
#
# CONSTRUCTED TOY. Every name, reply, and rater rule below was chosen by us to
# illustrate one mechanism. No model, no real raters, and no Claude output are
# involved. Python standard library only; offline; seeded; prints JSON.
#
# Usage: python3 preference_toy.py            (from this folder or anywhere)
import importlib.util
import inspect
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
try:  # inside the course repo: fall-2026/shubham-b/week-01-video/evidence
    REPO = HERE.parents[3]
except IndexError:  # copied somewhere shallow (e.g. unzipped from Canvas)
    REPO = HERE
COURSE_MAIN = REPO / "lessons/01-randomness-and-first-prompts/code/main.py"
COPY_MAIN = HERE / "course_main_copy.py"  # verbatim copy, for use outside the repo


def _load_course_main():
    path = COURSE_MAIN if COURSE_MAIN.exists() else COPY_MAIN
    spec = importlib.util.spec_from_file_location("course_main", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, path


course, COURSE_PATH = _load_course_main()
probabilities = course.probabilities  # the chapter's own scores -> chances step
sample = course.sample                # the chapter's own seeded sampler

QUESTION = "What is the capital of Australia?"
REPLIES = [
    "I think it's Canberra, though Sydney is the biggest city.",  # 0: hedged
    "The capital of Australia is Sydney.",                        # 1: confident
]
# Used ONLY to label the report. nudge() never receives it.
ANSWER_KEY = 0

VOTES = 1000
LEARNING_RATE = 0.02
SEED = 7
CHECKPOINTS = [0, 10, 50, 100, 200, 500, 1000]
SHARES_WHO_CAN_CHECK = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]


def rater_pick(can_check):
    """Constructed rater rule.

    A rater who can check picks the correct reply. A rater who cannot check
    picks the reply that sounds surer. The rule is an assumption we chose,
    not a measurement of real people.
    """
    return 0 if can_check else 1


def nudge(scores, picked, learning_rate):
    """One preference-tuning step on two reply scores.

    Raise the picked reply's score and lower the other one, by an amount that
    is larger when the picked reply was less likely. This is the gradient of
    log(probability of the picked reply), which for two replies is the same
    pairwise (Bradley-Terry) loss used to train reward models from comparisons.
    Note the arguments: scores, the rater's pick, a step size. No answer key.
    """
    chances = probabilities(scores)
    step = learning_rate * (1 - chances[picked])
    new = list(scores)
    new[picked] += step
    new[1 - picked] -= step
    return new


def train(share_who_can_check, votes=VOTES, learning_rate=LEARNING_RATE, seed=SEED):
    """Collect `votes` constructed votes and apply one nudge per vote."""
    rng = random.Random(seed)
    scores = [0.0, 0.0]
    votes_for = [0, 0]
    trajectory = {0: probabilities(scores)[0]}
    tallies = {0: [0, 0]}
    for i in range(1, votes + 1):
        can_check = rng.random() < share_who_can_check
        picked = rater_pick(can_check)
        votes_for[picked] += 1
        scores = nudge(scores, picked, learning_rate)
        if i in CHECKPOINTS:
            trajectory[i] = probabilities(scores)[0]
            tallies[i] = list(votes_for)
    return {"scores": scores, "votes_for": votes_for, "trajectory": trajectory,
            "tallies": tallies}


def main():
    headline = train(0.3)
    hl_scores = headline["scores"]
    # Ask the tuned toy 1,000 times with the chapter's own sampler (seed 7).
    asked = sample(hl_scores, count=1000, seed=SEED)
    sweep = []
    for share in SHARES_WHO_CAN_CHECK:
        run = train(share)
        sweep.append({
            "share_who_can_check": share,
            "votes_for_correct": run["votes_for"][0],
            "final_chance_correct": round(probabilities(run["scores"])[0], 4),
            "favourite": "correct (Canberra)" if run["scores"][0] > run["scores"][1]
                         else "wrong (Sydney)",
        })
    result = {
        "mode": "CONSTRUCTED toy; offline; seeded; no model or Claude output",
        "course_function_source": str(COURSE_PATH.relative_to(REPO))
        if COURSE_PATH == COURSE_MAIN else COURSE_PATH.name,
        "question": QUESTION,
        "replies": REPLIES,
        "answer_key_used_only_for_labels": ANSWER_KEY,
        "nudge_arguments": list(inspect.signature(nudge).parameters),
        "settings": {"votes": VOTES, "learning_rate": LEARNING_RATE, "seed": SEED},
        "start_chances": [round(p, 4) for p in probabilities([0.0, 0.0])],
        "headline_share_who_can_check": 0.3,
        "headline_votes_for": headline["votes_for"],
        "headline_trajectory_chance_correct": {
            str(k): round(v, 4) for k, v in headline["trajectory"].items()},
        "headline_tallies_at_checkpoints": {
            str(k): v for k, v in headline["tallies"].items()},
        "headline_final_scores": [round(s, 4) for s in hl_scores],
        "headline_final_chances": [round(p, 4) for p in probabilities(hl_scores)],
        "headline_asked_1000_times": {
            "correct (Canberra)": asked.get(0, 0), "wrong (Sydney)": asked.get(1, 0)},
        "sweep": sweep,
    }
    return result


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
