"""Drawing and export functions for labeled molecules."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D

from chem_gui.chemistry import get_extended_smiles, parse_cxsmiles_av_labels
from chem_gui.labeling import add_labels_as_atom_notes, build_proton_rule_labels


def draw_labeled_mol_svg(mol: Chem.Mol, width: int = 600, height: int = 450, legend: Optional[str] = None) -> str:
    """Draw the molecule with labels as an SVG string."""
    AllChem.Compute2DCoords(mol)
    drawer = rdMolDraw2D.MolDraw2DSVG(width, height)
    options = drawer.drawOptions()
    options.addAtomIndices = False
    options.annotationFontScale = 1.0
    rdMolDraw2D.PrepareMolForDrawing(mol)
    drawer.DrawMolecule(mol, legend=legend if legend else "")
    drawer.FinishDrawing()
    return drawer.GetDrawingText()


def draw_labeled_mol_png(mol: Chem.Mol, file_path: str, width: int = 800, height: int = 600, legend: Optional[str] = None) -> Optional[str]:
    """Draw the molecule with labels and export as a PNG file."""
    try:
        drawer = rdMolDraw2D.MolDraw2DCairo(width, height)
        options = drawer.drawOptions()
        options.addAtomIndices = False
        options.annotationFontScale = 1.0
        AllChem.Compute2DCoords(mol)
        rdMolDraw2D.PrepareMolForDrawing(mol)
        drawer.DrawMolecule(mol, legend=legend if legend else "")
        drawer.FinishDrawing()
        with open(file_path, "wb") as file:
            file.write(drawer.GetDrawingText())
        return file_path
    except Exception as error:  # pylint: disable=broad-except
        print("PNG 导出失败：", error)
        return None


def generate_labeled_images(iupac_name: str, rule: str = 'carbon_only', out_prefix: str = "iupac_labeled") -> Tuple[Chem.Mol, Optional[List[str]], str, Optional[str]]:
    """Generate labeled molecule images and return paths to the created files."""
    cxsmi = get_extended_smiles(iupac_name)
    base_smiles, labels_iupac = parse_cxsmiles_av_labels(cxsmi)

    mol = Chem.MolFromSmiles(base_smiles)
    if mol is None:
        first_line = cxsmi.splitlines()[0].strip()
        mol = Chem.MolFromSmiles(first_line)
    if mol is None:
        mol = Chem.MolFromSmiles(cxsmi)
    if mol is None:
        raise ValueError("SMILES 解析失败")

    if rule == 'proton_rule':
        labels_used = build_proton_rule_labels(mol)
    else:
        labels_used = labels_iupac

    add_labels_as_atom_notes(mol, labels_used, rule)

    svg = draw_labeled_mol_svg(mol, legend="")
    svg = svg.replace("#33CCCC", "#000000").replace("#FF0000", "#000000")

    svg_path = Path(f"{out_prefix}.svg")
    svg_path.write_text(svg, encoding="utf-8")

    png_path = draw_labeled_mol_png(mol, f"{out_prefix}.png", legend="")
    return mol, labels_used, str(svg_path), png_path


def export_mol_v3000(mol: Chem.Mol, path: str) -> str:
    """Export the molecule as an MOL V3000 file."""
    AllChem.Compute2DCoords(mol)
    mol_block = Chem.MolToV3KMolBlock(mol)
    Path(path).write_text(mol_block, encoding="utf-8")
    return path
