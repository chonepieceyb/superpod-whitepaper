from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_FILE = ROOT / "scripts" / "generate_spi_registry.py"


def _load_generate():
    spec = importlib.util.spec_from_file_location("spi_generate_spi_registry", SCRIPT_FILE)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load SPI generator from {SCRIPT_FILE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.generate


def on_pre_build(config, **kwargs):
    generate = _load_generate()

    output_file = ROOT / "src" / "07-spi-registry.md"
    output_file.write_text(generate(), encoding="utf-8")
    print(f"[SPI] Generated {output_file.relative_to(ROOT)}")
