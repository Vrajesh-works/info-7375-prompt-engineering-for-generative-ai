# PROMPTS — A Chatbot Is a Loop.

No pantry or generation prompts: every beat is rendered from recorded data by the pipeline.

Prompts that appear on screen:
- B00 (the ask to Claude Code): Run a small open chatbot on this Mac and record every step as it answers “What is the capital of France?”
- B13 (Aditya, in a fresh claude.ai chat): Who wrote Middlemarch? Then tell me which word in your answer you were least sure of.
- BHTF (for the viewer): Name the author of Middlemarch. Then list three authors you might have said instead.

Questions sent to the local model (evidence/run_experiments.py):
- "What is the capital of France?"  (greedy; and greedy with <|im_end|> banned)
- "Who wrote the novel Middlemarch?"  (greedy; greedy with " George" forced at pass 9; 200 samples at temperature 1.0)
