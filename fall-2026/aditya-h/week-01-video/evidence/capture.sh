#!/usr/bin/env bash
# capture.sh — run seeded_sampler.py twice as separate processes and keep the
# evidence (command, stdout+stderr, exit code, environment, script hash).
# Beat 2's scene reads run1.txt / run2.txt at render time.
cd "$(dirname "$0")"
PY="${PY:-python3}"
{
  echo "captured_at : $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "python      : $($PY --version 2>&1) ($(command -v $PY))"
  echo "platform    : $(uname -srm)"
  echo "script_sha256: $(shasum -a 256 seeded_sampler.py | cut -d' ' -f1)"
} > ENV.txt
for n in 1 2; do
  { echo "\$ $PY seeded_sampler.py"; $PY seeded_sampler.py 2>&1; echo "[exit $?]"; } > run$n.txt
  cat run$n.txt; echo
done
if diff -q run1.txt run2.txt >/dev/null; then echo "RESULT: run1.txt and run2.txt are byte-identical"; else echo "RESULT: runs DIFFER"; diff run1.txt run2.txt; fi
cat ENV.txt
