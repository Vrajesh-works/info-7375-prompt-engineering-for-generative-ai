"""Deterministic tests for the constructed preference-tuning toy.

Each test checks one property. None of them checks that real raters or real
models behave this way; they check what this program computes.
Run: python3 -m unittest test_preference_toy -v   (from this folder)
"""
import filecmp
import importlib.util
import inspect
import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("toy", HERE / "preference_toy.py")
toy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(toy)


class PreferenceToyTests(unittest.TestCase):
    def test_starts_even(self):
        # Equal scores -> equal chances, via the chapter's own function.
        self.assertEqual(toy.probabilities([0.0, 0.0]), [0.5, 0.5])

    def test_nudge_raises_the_picked_reply(self):
        for picked in (0, 1):
            before = toy.probabilities([0.0, 0.0])[picked]
            after = toy.probabilities(toy.nudge([0.0, 0.0], picked, 0.02))[picked]
            self.assertGreater(after, before)

    def test_nudge_never_receives_an_answer_key(self):
        # The mechanism claim in the video: the update's inputs are the scores,
        # the rater's pick, and a step size. Nothing names the correct reply.
        self.assertEqual(list(inspect.signature(toy.nudge).parameters),
                         ["scores", "picked", "learning_rate"])

    def test_same_seed_repeats_exactly(self):
        # Repeatability, not correctness.
        self.assertEqual(toy.train(0.3), toy.train(0.3))

    def test_learned_chance_lands_near_vote_share_not_truth(self):
        # For these seeded runs the trained chance of the correct reply ends
        # NEAR the share of votes it received, and the favourite is the reply
        # with more votes. SEED 7 ONLY: across 500 seeds the gap reaches ~0.10
        # and at share 0.5 the favourite matches the vote majority in only 63%
        # of seeds (seed_spread_output.json). "Near", not "equal": with a fixed step size
        # the last few votes move the final number. The first version of this
        # test used delta=0.03 and failed at share 0.6 (0.6632 vs 0.633); see
        # preference_toy_tests_output_FIRST_RUN_FAILED.txt and FRICTIONAL.md.
        for share in toy.SHARES_WHO_CAN_CHECK:
            run = toy.train(share)
            vote_share = run["votes_for"][0] / toy.VOTES
            learned = toy.probabilities(run["scores"])[0]
            self.assertAlmostEqual(learned, vote_share, delta=0.05)
            self.assertEqual(learned > 0.5, run["votes_for"][0] > run["votes_for"][1])

    def test_wrong_reply_wins_when_most_raters_cannot_check(self):
        run = toy.train(0.3)
        self.assertGreater(run["scores"][1], run["scores"][0])
        run = toy.train(0.7)
        self.assertGreater(run["scores"][0], run["scores"][1])

    def test_result_is_not_special_to_seed_7(self):
        # Added after review: the video's headline (wrong reply favoured when
        # 3 in 10 can check) holds for every one of seeds 0-99, and flips for
        # 7 in 10. The full 500-seed spread is in seed_spread_output.json.
        for seed in range(100):
            low = toy.train(0.3, seed=seed)["scores"]
            high = toy.train(0.7, seed=seed)["scores"]
            self.assertGreater(low[1], low[0])
            self.assertGreater(high[0], high[1])

    def test_recorded_output_matches_a_fresh_run(self):
        # The numbers shown in the video come from this saved file.
        # Only the provenance field may differ: outside the repo (e.g. unzipped
        # from Canvas) the course function comes from course_main_copy.py.
        saved = json.loads((HERE / "preference_toy_output.json").read_text())
        fresh = json.loads(json.dumps(toy.main()))
        saved.pop("course_function_source"); fresh.pop("course_function_source")
        self.assertEqual(saved, fresh)

    def test_course_copy_matches_repo_when_present(self):
        if toy.COURSE_MAIN.exists():
            self.assertTrue(filecmp.cmp(toy.COURSE_MAIN, toy.COPY_MAIN, shallow=False))


if __name__ == "__main__":
    unittest.main()
