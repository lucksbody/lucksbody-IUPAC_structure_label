"""Tkinter-based GUI interface for the IUPAC to labeled structure converter."""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox
from typing import List, Optional

from rdkit import Chem

from iupac_labeler.core.drawing import export_mol_v3000, generate_labeled_images
from iupac_labeler.core.labeling import sync_mapnum_from_labels


class ChemistryGUI:
    """Main GUI application for IUPAC to labeled structure conversion."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("IUPAC 到带编号结构图")

        self.current_mol: Optional[Chem.Mol] = None
        self.current_labels: Optional[List[str]] = None
        self.current_rule: str = 'carbon_only'
        self.current_name: Optional[str] = None

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the user interface components."""
        tk.Label(self.root, text="输入 IUPAC 名:").pack(pady=(10, 2))
        self.entry = tk.Entry(self.root, width=80)
        self.entry.pack(pady=5)

        rule_frame = tk.LabelFrame(self.root, text="编号规则", padx=8, pady=6)
        rule_frame.pack(fill='x', padx=10, pady=6)
        self.rule_var = tk.StringVar(value='carbon_only')
        tk.Radiobutton(rule_frame, text="IUPAC 规则（仅碳）", variable=self.rule_var, value='carbon_only').pack(side='left', padx=8)
        tk.Radiobutton(rule_frame, text="氢谱规则（碳+带H杂原子）", variable=self.rule_var, value='proton_rule').pack(side='left', padx=8)

        tk.Button(self.root, text="生成结构图", command=self.on_generate).pack(pady=10)

        export_frame = tk.LabelFrame(self.root, text="导出", padx=8, pady=6)
        export_frame.pack(fill='x', padx=10, pady=6)
        self.export_var = tk.StringVar(value='mol')
        tk.Radiobutton(export_frame, text="导出 MOL (V3000)", variable=self.export_var, value='mol').pack(side='left', padx=8)
        tk.Button(export_frame, text="导出结构", command=self.on_export).pack(side='left', padx=16)

    def on_generate(self) -> None:
        """Handle the generate button click event."""
        iupac_name = self.entry.get().strip()
        if not iupac_name:
            messagebox.showerror("错误", "请输入 IUPAC 名")
            return
        rule = self.rule_var.get()
        try:
            mol, labels, svg_fn, png_fn = generate_labeled_images(
                iupac_name, rule=rule, out_prefix="output_iupac_labeled"
            )
            self.current_mol = mol
            self.current_labels = labels
            self.current_rule = rule
            self.current_name = iupac_name
            msg = f"已生成文件：\nSVG: {svg_fn}\nPNG: {png_fn if png_fn else '未生成'}"
            if rule == 'carbon_only' and labels is None:
                msg += "\n\n注意：未在 CXSMILES 中找到 $_AV:(...)$，因此图中不会显示编号。"
            messagebox.showinfo("成功", msg)
        except Exception as error:  # pylint: disable=broad-except
            messagebox.showerror("错误", f"生成失败：{str(error)}")

    def on_export(self) -> None:
        """Handle the export button click event."""
        if self.current_mol is None:
            messagebox.showwarning("提示", "请先生成结构图，再导出。")
            return
        fmt = self.export_var.get()
        default_name = (self.current_name or "structure").replace(" ", "_")

        if fmt == 'mol':
            file_path = filedialog.asksaveasfilename(
                defaultextension=".mol",
                filetypes=[("Molfile V3000", "*.mol"), ("All files", "*.*")],
                initialfile=f"{default_name}.mol",
                title="导出 MOL (V3000)"
            )
            if not file_path:
                return
            try:
                mol_copy = Chem.Mol(self.current_mol)
                sync_mapnum_from_labels(mol_copy, self.current_labels, self.current_rule)
                export_mol_v3000(mol_copy, file_path)
                messagebox.showinfo("成功", f"已导出 MOL：\n{file_path}")
            except Exception as error:  # pylint: disable=broad-except
                messagebox.showerror("错误", f"MOL 导出失败：{str(error)}")

    def run(self) -> None:
        """Start the GUI event loop."""
        self.root.mainloop()


def launch_gui() -> None:
    """Create and launch the GUI application."""
    root = tk.Tk()
    app = ChemistryGUI(root)
    app.run()


if __name__ == "__main__":  # pragma: no cover
    launch_gui()
