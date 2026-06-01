#!/usr/bin/env python3
"""Copia y optimiza la foto para images/portrait.jpg.

Uso:
  python3 scripts/install-portrait.py ruta/a/tu-foto.jpg
  python3 scripts/install-portrait.py   # usa images/portrait-incoming.jpg si existe
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Instala Pillow: pip install pillow")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "images" / "portrait.jpg"
INCOMING = ROOT / "images" / "portrait-incoming.jpg"
MAX_WIDTH = 1200


def optimize(src: Path, dest: Path) -> None:
    im = Image.open(src).convert("RGB")
    if im.width > MAX_WIDTH:
        h = int(im.height * MAX_WIDTH / im.width)
        im = im.resize((MAX_WIDTH, h), Image.Resampling.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, format="JPEG", quality=92, optimize=True)
    print(f"Guardado: {dest} ({im.width}x{im.height})")


def main() -> None:
    if len(sys.argv) > 1:
        src = Path(sys.argv[1]).expanduser().resolve()
    elif INCOMING.is_file():
        src = INCOMING
    else:
        print(__doc__)
        sys.exit(1)

    if not src.is_file():
        print(f"No existe: {src}")
        sys.exit(1)

    optimize(src, DEST)


if __name__ == "__main__":
    main()
