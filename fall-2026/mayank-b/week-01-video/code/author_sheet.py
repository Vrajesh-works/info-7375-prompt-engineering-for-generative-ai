"""Authors beat_sheet.json (narration + show blocks). Run once; build_props.py
later adds measured timings and computed props. Numbers here are copied from
code/temperature_results.json (printed by run_temperature.py)."""
import json

TITLE = "Temperature Is Not a Fact Checker."
SLUG = "temperature-concentration"
V = {"voice": "am_onyx", "engine": "kokoro"}

def beat(bid, act, narration, pattern, props, show, lane="BODY", **extra):
    b = {"beat_id": bid, "act": act, "lane": lane, "narration_text": narration, **V,
         "shot": {"type": "REMOTION", "source": "own", "motion": "illustrate",
                  "show": show, "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b

CODE = '''def probabilities(logits, temperature=1.0):
    if not logits or not math.isfinite(temperature) or temperature <= 0:
        raise ValueError("Need logits and a positive finite temperature")
    if not all(math.isfinite(x) for x in logits):
        raise ValueError("Logits must be finite")
    peak = max(logits)
    weights = [math.exp((x - peak) / temperature) for x in logits]
    total = sum(weights)
    return [weight / total for weight in weights]'''

beats = [
  beat("B00", "cold open — the ask",
       "Hola, this is Liam. Turn a model's temperature down and its answers sound more certain. "
       "Does that make them more correct? We ran the chapter's own code to find out.",
       "ClaudeComposerAsk",
       {"greeting": "Hola, Liam", "topic": "CHAPTER 1 · TEMPERATURE", "segment": TITLE.rstrip('.'),
        "command": "Does turning the temperature down of the model make an answer more accurate?",
        "runningText": "running the chapter's code offline, no model call…",
        "output": ["$ python3 run_temperature.py",
                   "T = 0.5   top outcome  0.8668",
                   "T = 2.0   top outcome  0.5065",
                   "ranking at every T:  2 > 1 > 0"],
        "folderLabel": "@Mayank"},
       [{"at": "Hola", "event": "greeting + composer; the question types in"},
        {"at": "We ran", "event": "running indicator, then four stdout lines from run_temperature.py (real output, not a Claude reply)"}],
       lane="BOOKEND"),
  beat("B01", "BLUF — hesitant writer",
       "Temperature sets how concentrated the choices are. It reshapes the odds on answers already on the table. "
       "It never checks which answer is true — so confident is not the same as correct.",
       "BrutalistHesitantWriter",
       {"text": "Temperature sets how creative the model is.\nIt reshapes the odds on answers already there.\nIt never checks which answer is true.",
        "triggerWords": "how creative the model is",
        "replacementWords": "how concentrated the choices are",
        "seed": "temperature-concentration-b01", "fontSize": 76, "align": "center"},
       [{"at": 0.0, "event": "writer types 'Temperature sets how creative the model is.'"},
        {"at": "concentrated", "event": "'how creative the model is' highlighted, deleted, retyped as 'how concentrated the choices are'"},
        {"at": "never checks", "event": "remaining two lines type in"}],
       lane="BOOKEND", lead_silence_s=0.8),
  beat("B01A", "setup — how a chatbot picks the next word",
       "First, what a chatbot does. It writes one token, roughly one word, at a time. "
       "At each step it scores every possible next token: Paris high, Lyon lower. "
       "Scores aren't chances yet. A formula called softmax turns them into chances that add up to one. "
       "Then the model draws.",
       "TcNextWord",
       {"sparkLine": "One word at a time.", "prompt": "The capital of France is",
        "candidates": ["Paris", "Lyon", "beautiful", "a"],
        "barLengths": [1.0, 0.62, 0.38, 0.22],
        "stampText": "ILLUSTRATIVE SCORES · NOT FROM A REAL MODEL"},
       [{"at": "writes", "event": "sentence 'The capital of France is ___' appears, blank pulsing"},
        {"at": "scores every", "event": "four candidate tokens slide in; unnumbered score bars grow (illustrative ordering only)"},
        {"at": "Scores aren't", "event": "a 'chance?' column appears beside the bars with a question mark"},
        {"at": "softmax", "event": "label 'softmax: scores → chances that add up to 100%' draws in under the bars"},
        {"at": "draws", "event": "'Paris' lifts out of the list into the blank (terracotta)"}]),
  beat("B02", "framework — softmax, the formula, and e",
       "Let's take three sample values as scores: one, two, three. These are constructed toy scores, not from a real model. "
       "Softmax is the formula that turns scores into chances: each option's weight, e to its score, divided by the total weight. "
       "Here, e is a fixed number, about two point seven one eight. Raising e to any score gives a positive number, "
       "and bigger scores grow much faster. Any base above one would keep the order; e is the standard choice because it keeps the math simple.",
       "TcSoftmaxIntro", {"sparkLine": "Softmax: scores into chances."},
       [{"at": "three sample values", "event": "three score chips z = 1, 2, 3; CONSTRUCTED TOY SCORES stamp"},
        {"at": "Softmax is the formula", "event": "the softmax equation, typeset, large"},
        {"at": "divided by the total", "event": "labels: top = your weight · bottom = everyone's total"},
        {"at": "Here, e", "event": "card: e ≈ 2.71828"},
        {"at": "positive number", "event": "row e^-1 … e^3 = 0.37, 1, 2.72, 7.39, 20.09 with bars: always positive, grows fast"},
        {"at": "Any base", "event": "note: any base above 1 keeps the order; e is the standard choice"}]),
  beat("B02B", "worked example — softmax in three moves",
       "Now the example. One: raise e to each score. Two point seven, seven point four, twenty point one. "
       "Two: add them up. Thirty point two. Three: divide each weight by the total. "
       "Nine, twenty-four point five, and sixty-six point five percent.",
       "TcScoresToOdds", {"sparkLine": "Softmax in three moves."},
       [{"at": "Now the example", "event": "table: option 0/1/2 with score z = 1, 2, 3"},
        {"at": "raise e", "event": "MOVE 1: weight column fills, 2.72 / 7.39 / 20.09"},
        {"at": "add them up", "event": "MOVE 2: total row 2.72 + 7.39 + 20.09 = 30.19"},
        {"at": "divide each", "event": "MOVE 3: chance column 'weight ÷ 30.19' fills; bars grow to 9.0% / 24.5% / 66.5%"},
        {"at": "Nine", "event": "formula labels: top = your weight · bottom = everyone's total"}]),
  beat("B03", "worked example — temperature divides first",
       "Temperature adds one step first: divide every score by T. At T point five, the scores double to two, four, six. "
       "The gaps grow, and the top option takes eighty-six point seven percent. At T two, they halve. "
       "The gaps shrink, and it falls to fifty point six. Temperature zooms in or out on the gaps. "
       "But the ranking never moves.",
       "TcTemperatureDial", {"sparkLine": "Temperature zooms the gaps."},
       [{"at": "divide every score", "event": "a 'z ÷ T' column appears between score and weight; T readout 1.00"},
        {"at": "point five", "event": "T slides 1 → 0.5: z÷T 2, 4, 6; weights 7.39 / 54.60 / 403.43; chances 1.6 / 11.7 / 86.7% (live softmax)"},
        {"at": "At T two", "event": "T slides 0.5 → 2: z÷T 0.5, 1, 1.5; weights 1.65 / 2.72 / 4.48; chances 18.6 / 30.7 / 50.6%"},
        {"at": "zooms", "event": "dashed T = 1 ghost bars stay for comparison"},
        {"at": "ranking", "event": "rank badges 1st/2nd/3rd pulse — unchanged at every T"}]),
  beat("B04", "mechanism — the ratio",
       "Here's why. Divide one probability by another and the denominator cancels, leaving e to the score gap over T. "
       "Outcomes two and zero sit two points apart. At T point five, that ratio is fifty-four point six. "
       "At T two, two point seven two. Temperature stretches a gap; it never creates one.",
       "TcRatio", {"sparkLine": "It stretches the gap."},
       [{"at": "Divide", "event": "ratio equation p_i/p_k = exp((z_i − z_k)/T) reveals"},
        {"at": "two points apart", "event": "gap z₂ − z₀ = 2 marked"},
        {"at": "point five", "event": "row T = 0.5 → ratio counter runs to 54.60"},
        {"at": "At T two", "event": "rows T = 1 (7.39) and T = 2 (2.72) land; all three ratios > 1"}]),
  beat("B05", "the code — one place temperature enters",
       "That's the chapter's actual function. Temperature enters the arithmetic in one place: it divides the score differences. "
       "No question goes in, no answer key, no evidence. And zero is rejected outright — "
       "low temperature here isn't a secret 'pick the best' mode.",
       "TcCode", {"sparkLine": "One division. No evidence.", "code": CODE, "title": "main.py · probabilities()"},
       [{"at": 0.0, "event": "real function source (verbatim from chapter) appears"},
        {"at": "divides", "event": "line `(x - peak) / temperature` highlighted"},
        {"at": "No question", "event": "input list shown beside the signature: logits, temperature — nothing else"},
        {"at": "zero is rejected", "event": "the `temperature <= 0` guard line highlighted"}]),
  beat("B06", "evidence — a thousand draws",
       "Probabilities aren't outcomes, so draw a thousand times with seed seven. "
       "At temperature point five, outcome two comes up eight hundred forty-nine times. "
       "At temperature two, four hundred sixty-nine. Same scores, same seed. Only the concentration changed.",
       "TcSampleCounts", {"sparkLine": "Concentration, counted."},
       [{"at": "draw a thousand", "event": "two 40×25 dot grids fill in draw order (real seed-7 sequences)"},
        {"at": "eight hundred", "event": "left grid (T = 0.5) counter lands 18 / 133 / 849"},
        {"at": "four hundred", "event": "right grid (T = 2) counter lands 202 / 329 / 469"},
        {"at": "Only the concentration", "event": "grids held side by side"}]),
  beat("B07", "falsifiability — the constructed counterexample",
       "Now a constructed hypothetical — not a real Claude error. Say an answer key marks outcome zero as correct. "
       "Lower the temperature from one to point five: the correct answer drops from nine percent to one point six, "
       "and the wrong favourite climbs to eighty-seven. The formula worked perfectly. It never saw the key.",
       "TcWrongAnswer", {"sparkLine": "It never saw the key."},
       [{"at": 0.0, "event": "stamp: CONSTRUCTED HYPOTHETICAL — not an observed Claude error"},
        {"at": "answer key", "event": "answer key card marks outcome 0 ✓ correct"},
        {"at": "Lower the temperature", "event": "T slides 1.0 → 0.5; correct bar shrinks 9.0% → 1.6%, wrong bar grows 66.5% → 86.7%"},
        {"at": "never saw", "event": "arrow from answer key to formula struck out: 'not an input'"}]),
  beat("B08", "boundary — what this does not establish",
       "What this doesn't show: how any Claude product sets or exposes temperature. This is a three-outcome toy, run offline. "
       "And it can't tell you whether the scores themselves were any good — that's a separate question, needing separate evidence.",
       "TcBoundary", {"sparkLine": "Where the proof stops."},
       [{"at": 0.0, "event": "claims sort into two columns: SHOWN / NOT SHOWN"},
        {"at": "Claude product", "event": "'How a Claude product sets or exposes temperature' lands in NOT SHOWN, terracotta"},
        {"at": "three-outcome toy", "event": "SHOWN column: three constructed scores, offline, Python 3.11"},
        {"at": "scores themselves", "event": "'Whether the scores were any good' joins NOT SHOWN"}]),
  beat("BVDT", "verdict page",
       "Nothing broke; the recipe did exactly its job. Lowering temperature just made the model more confidently wrong. "
       "So \"turn the temperature down to get more accurate answers\" is a misunderstanding. "
       "Low temperature gives you more consistent answers, not more correct ones. "
       "Being correct depends on the scores, meaning what the model actually learned and the evidence it has.",
       "ClaudeVerdictArtifact",
       {"artifactTitle": TITLE, "artifactHeading": "The verdict",
        "brandLabel": "Recap written by the author, not a Claude response",
        "artifactLines": ["Nothing broke: the recipe did exactly its job",
                          "Lower T made the model more confidently wrong (constructed case: 9.0% → 1.6%)",
                          "Myth: \"turn the temperature down for more accurate answers\"",
                          "Low T gives more consistent answers, not more correct ones",
                          "Correctness depends on the scores: what the model learned, and its evidence"]},
       [{"at": "Nothing broke", "event": "verdict artifact page; five lines reveal in narration order"}],
       lane="BOOKEND"),
  beat("BOUT", "outro — title restate",
       "Temperature Is Not a Fact Checker. At Muh-yunk.",  # spelled for Kokoro; on screen: @Mayank
       "TcTitleOutro", {"title": TITLE, "slug": SLUG, "handle": "@Mayank"},
       [{"at": 0.0, "event": "title card, terracotta period, @Mayank handle"}],
       lane="BOOKEND"),
]

sheet = {"metadata": {
    "title": TITLE, "slug": SLUG, "topic": "CHAPTER 1 · TEMPERATURE",
    "concept": "Temperature controls how concentrated the choices are; it doesn't check facts",
    "source": "01-randomness-and-first-prompts.md §'Temperature is a concentration control, not a fact checker'",
    "register": "Teardown", "audience": "Claude", "brand": "claude-liam", "persona": "Liam",
    "in_for_bear": False, "voice": "am_onyx", "engine": "kokoro", "voice_kokoro": "am_onyx",
    "palette": "claude", "style_preset": "claude", "ground": "#FAF9F5",
    "typography": {"serif": "Tiempos/EB Garamond", "ui": "system sans", "mono": "SF Mono"},
    "greeting": "Hola, Liam", "greeting_note": "hello lexicon: Spanish. Wagwan is Bear's only; Liam never takes it.",
    "folderLabel": "@Mayank", "aspect_ratio": "16:9", "target_runtime_s": [120, 180],
    "derived_from": "beat_sheet.json",
    "evidence": "code/run_temperature.py -> code/temperature_results.json (every on-screen number)",
  }, "beats": beats}
json.dump(sheet, open("beat_sheet.json", "w"), indent=2, ensure_ascii=False)
print(len(beats), "beats;", sum(len(b["narration_text"].split()) for b in beats), "words")
