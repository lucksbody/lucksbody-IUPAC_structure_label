"""Chemistry-related utilities for IUPAC and SMILES processing."""

from __future__ import annotations

import re
from typing import List, Optional, Tuple

from py2opsin import py2opsin


def get_extended_smiles(iupac_name: str) -> str:
    """Convert an IUPAC name to an Extended SMILES string using OPSIN."""
    extended_smiles = py2opsin(chemical_name=iupac_name, output_format="ExtendedSMILES")
    return extended_smiles


def parse_cxsmiles_av_labels(cxsmi: str) -> Tuple[str, Optional[List[str]]]:
    """Parse CXSMILES annotations to extract atom labels."""
    labels = None
    match = re.search(r"\$_AV:\((.*?)\)\$", cxsmi, flags=re.S)
    if not match:
        match = re.search(r"\|[^|]*_AV:([^|]*)\|", cxsmi)
    if match:
        raw = match.group(1).strip()
        labels = [item.strip() for item in raw.split(";")] if raw else None
    first_line = cxsmi.splitlines()[0].strip()
    base_smiles = re.split(r"\s*(?:\||\$)", first_line)[0].strip() or first_line
    return base_smiles, labels
