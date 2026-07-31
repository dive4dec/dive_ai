from lmsysorg/sglang:v0.5.16-cu129

user root

# Apply patch 060: fix gemma4_unified config alias for transformers >= 5.12
# See apply_patch.py for details.
copy apply_patch.py /tmp/apply_patch.py
workdir /sgl-workspace/sglang
run python3 /tmp/apply_patch.py && rm /tmp/apply_patch.py

# Rebuild the sglang package (editable install picks up the patched source)
run cd /sgl-workspace/sglang/python && pip install --no-deps -e .

workdir /sgl-workspace
