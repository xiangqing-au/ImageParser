"""Route (pickup / drop-off) list loading."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import pandas as pd

Route = Dict[str, object]


def routes_file(work_base: Path, name: str) -> Path:
    """Path of ``<work_base>/routes/<name>.csv``."""
    return Path(work_base) / "routes" / f"{name}.csv"


def read_routes(work_base: Path, name: str) -> List[Route]:
    """Load route rows from a CSV with ``id,src,dst`` columns."""
    return pd.read_csv(routes_file(work_base, name)).to_dict("records")
