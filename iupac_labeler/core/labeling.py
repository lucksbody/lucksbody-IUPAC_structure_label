"""Atom labeling and annotation logic."""

from __future__ import annotations

import re
from typing import List, Optional, Set

from rdkit import Chem


def choose_atoms_to_label(mol: Chem.Mol, rule: str) -> Set[int]:
    """Determine which atoms should be labeled based on the given rule."""
    pick = set()
    for atom in mol.GetAtoms():
        symbol = atom.GetSymbol()
        index = atom.GetIdx()
        if rule == 'carbon_only':
            if symbol == 'C':
                pick.add(index)
        elif rule == 'proton_rule':
            if symbol == 'C':
                pick.add(index)
            else:
                if atom.GetTotalNumHs() > 0 and symbol not in ('C', 'H'):
                    pick.add(index)
        else:
            if symbol == 'C':
                pick.add(index)
    return pick


def add_labels_as_atom_notes(mol: Chem.Mol, labels: Optional[List[str]], rule: str) -> None:
    """Add labels to atoms as atomNote properties."""
    if labels is None:
        return
    num_atoms = mol.GetNumAtoms()
    if len(labels) != num_atoms:
        raise ValueError(f"标签数量({len(labels)})与分子原子数({num_atoms})不一致！")
    picks = choose_atoms_to_label(mol, rule)
    for index, atom in enumerate(mol.GetAtoms()):
        label = labels[index]
        if index in picks and label:
            atom.SetProp("atomNote", label)
        else:
            if atom.HasProp("atomNote"):
                atom.ClearProp("atomNote")


def build_proton_rule_labels(mol: Chem.Mol) -> List[str]:
    """Build labels based on the proton NMR rule."""
    num_atoms = mol.GetNumAtoms()
    labels = [""] * num_atoms
    picks = sorted(list(choose_atoms_to_label(mol, 'proton_rule')))
    num = 1
    for index in picks:
        labels[index] = str(num)
        num += 1
    return labels


def sync_mapnum_from_labels(mol: Chem.Mol, labels: Optional[List[str]], rule: str) -> None:
    """Synchronize atom map numbers from labels."""
    if labels is None:
        return
    picks = choose_atoms_to_label(mol, rule)
    for index, atom in enumerate(mol.GetAtoms()):
        if index in picks:
            label = labels[index]
            if label:
                match = re.search(r"\d+", label)
                atom.SetAtomMapNum(int(match.group(0)) if match else 0)
            else:
                atom.SetAtomMapNum(0)
        else:
            atom.SetAtomMapNum(0)
