#!/usr/bin/env python3
"""Apply mattbucci patch 060: fix gemma4_unified config alias for transformers >= 5.12.

The upstream SGLang v0.5.16 image registers _Gemma4UnifiedConfigAlias(Gemma4Config)
unconditionally, which shadows the native Gemma4UnifiedConfig on tx >= 5.12.
This causes audio_config to load as Gemma4AudioConfig (output_proj_dims=1536)
instead of Gemma4UnifiedAudioConfig (output_proj_dims=audio_embed_dim=640),
leading to a weight shape mismatch crash at boot.

Fix: only register the alias when Gemma4UnifiedConfig is absent.
"""
import pathlib
import sys

p = pathlib.Path("python/sglang/srt/utils/hf_transformers/common.py")
text = p.read_text()

old = '''try:
    from transformers import Gemma4Config as _HFGemma4Config

    class _Gemma4UnifiedConfigAlias(_HFGemma4Config):
        model_type = "gemma4_unified"

    _CONFIG_REGISTRY["gemma4_unified"] = _Gemma4UnifiedConfigAlias
except ImportError:
    pass'''

new = '''try:
    import transformers as _hf_transformers_gemma4u

    # Only alias gemma4_unified -> plain Gemma4Config when transformers
    # lacks the native family (tx < 5.12). On tx >= 5.12 the alias is strictly
    # harmful: config.py registry-first reload re-parses the checkpoint through
    # plain Gemma4Config, whose sub-configs lack properties that the unified
    # model reads at construction -> crash at boot.
    # Mirrors upstream Mellum fallback pattern. (mattbucci patch 060)
    if getattr(_hf_transformers_gemma4u, "Gemma4UnifiedConfig", None) is None:
        from transformers import Gemma4Config as _HFGemma4Config

        class _Gemma4UnifiedConfigAlias(_HFGemma4Config):
            model_type = "gemma4_unified"

        _CONFIG_REGISTRY["gemma4_unified"] = _Gemma4UnifiedConfigAlias
except ImportError:
    pass'''

if old not in text:
    print("ERROR: Expected code block not found in common.py", file=sys.stderr)
    print("The file may have already been patched or the code structure changed.", file=sys.stderr)
    sys.exit(1)

if new in text:
    print("Patch 060 already applied, skipping.")
    sys.exit(0)

p.write_text(text.replace(old, new))
print("Patch 060 applied successfully.")
