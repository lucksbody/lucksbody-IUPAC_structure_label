# IUPAC 到带编号结构图转换器

## 项目结构

```
.
├── main.py                    # 程序入口
├── requirements.txt           # Python依赖
└── chem_gui/                  # 应用程序包
    ├── __init__.py           # 包初始化
    ├── core/                 # 核心功能模块
    │   ├── __init__.py      
    │   ├── chemistry.py      # 化学处理（IUPAC转换、SMILES解析）
    │   ├── labeling.py       # 标注逻辑（原子选择、标签处理）
    │   └── drawing.py        # 绘图导出（SVG/PNG/MOL）
    └── gui/                  # GUI界面模块
        ├── __init__.py
        └── app.py            # Tkinter GUI应用
```

## 模块说明

### core/ - 核心功能模块

#### 1. chemistry.py - 化学处理
- `get_extended_smiles()`: 将IUPAC名称转换为ExtendedSMILES
- `parse_cxsmiles_av_labels()`: 解析CXSMILES中的原子标签

#### 2. labeling.py - 标注逻辑
- `choose_atoms_to_label()`: 根据规则选择需要标注的原子
- `add_labels_as_atom_notes()`: 将标签添加到原子属性
- `build_proton_rule_labels()`: 生成氢谱规则的编号
- `sync_mapnum_from_labels()`: 同步标签到原子映射编号

#### 3. drawing.py - 绘图导出
- `draw_labeled_mol_svg()`: 生成SVG格式的分子结构图
- `draw_labeled_mol_png()`: 生成PNG格式的分子结构图
- `generate_labeled_images()`: 生成带标签的分子图像
- `export_mol_v3000()`: 导出MOL V3000格式文件

### gui/ - GUI界面模块

#### app.py - Tkinter界面
- `ChemistryGUI`: Tkinter GUI应用程序类
- `launch_gui()`: 启动GUI应用的函数

## 安装和使用

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行程序
```bash
python main.py
```

## 功能特性

- **IUPAC规则**: 仅对碳原子进行编号
- **氢谱规则**: 对碳原子和带氢的杂原子进行编号
- **导出格式**: 支持SVG、PNG和MOL V3000格式
