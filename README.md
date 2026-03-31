<div align="center">

<h1>🏗️ Post-Plaxis</h1>

<p>
  <strong>基于远程脚本的 Plaxis 后处理自动化工具</strong>
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3.7-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Plaxis-2D%20%2F%203D-green" alt="Plaxis">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
  <img src="https://img.shields.io/badge/Shanghai%20Model-UDSM-red" alt="Shanghai Model">
</p>

<p>
  <b>中文</b> | <a href="README_EN.md">English</a>
</p>

</div>

---

## 📖 项目简介

本项目主要介绍如何利用远程脚本服务器从 **Plaxis 2D/3D Output Viewer** 中高效、快速地导出计算结果。

项目提供了一个二维基坑开挖的参数敏感性分析算例，使用 Python 自动提取 **地连墙位移** 和 **地表土体沉降** 数据，其中使用了 **上海本构模型 (Shanghai Model)** 进行计算。

### ✨ 主要功能

- 🔌 通过远程脚本服务器自动连接 Plaxis Output
- 📊 自动提取地连墙侧向位移 & 地表土体竖向位移
- 📈 自动绘制各施工工况下的位移曲线
- 💾 结果自动保存为 Excel 文件 + PNG 图片

### 📁 项目结构

```
Post-Plaxis/
├── main.py                # 主程序 — 数据提取 & 绘图
├── requirements.txt       # pip 依赖
├── environment.yaml       # conda 环境配置
├── model/                 # Plaxis 2D 算例模型
├── output/                # 结果输出目录
├── udsm/                  # 本构子程序 DLL
└── image/                 # 文档插图
```

---

## 🔧 本构程序安装

在文件夹 `udsm` 中有本构子程序 `20230801-UnifiedModel64.dll`，将其复制到本地 Plaxis 安装目录下：

```
...\Plaxis\3D\udsm\
```

<details>
<summary>📷 查看安装示意图</summary>

![dll_install](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/dll_install.png)

</details>

---

## 🐍 Python 环境配置

> **前提条件：** 已安装 [Anaconda](https://www.anaconda.com/)

提供两种方式配置环境，任选其一即可：

<details>
<summary><b>方式 A：使用 <code>environment.yaml</code>（推荐）</b></summary>

在项目目录下打开终端，运行：

```bash
conda env create -f environment.yaml
```

</details>

<details>
<summary><b>方式 B：使用 <code>requirements.txt</code></b></summary>

在项目目录下打开终端，依次运行：

```bash
conda create -n plaxis37 python=3.7   # 创建 Python 3.7 环境
conda activate plaxis37                # 激活环境
pip install -r requirements.txt        # 安装依赖
```

> ⚠️ **注意：** 请务必先激活 `plaxis37` 环境再执行 `pip install`，否则将在 `base` 环境安装依赖，可能导致版本冲突甚至环境损坏！

</details>

<br>

完成配置后，`.../Anaconda/envs/` 目录下将生成 `plaxis37` 文件夹：

<details>
<summary>📷 查看目录示意图</summary>

![envir_dir](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/envir_dir.png)

</details>

### 安装 `plxscripting`

`plxscripting` 是 Plaxis 后处理最重要的库，**无法**通过 `pip` 安装，需要通过 Plaxis 软件安装：

1. 打开 `model/2Dmodel.p2dx` 进入 Plaxis 2D
2. 点击 **专业** → **Python** → **配置Python解释器**
3. 选择 `plaxis37` 环境下的 Python 解释器，点击 **安装所需组件**

<details>
<summary>📷 查看配置流程</summary>

![Py_interpreter](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/Py_interpreter.png)

![plxscripting_install](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/plxscripting_install.gif)

</details>

---

## 🚀 程序运行说明

### 算例概况

本算例为均匀地基中的二维基坑开挖平面应变问题，目标是分析本构参数对 **地连墙侧向位移** 与 **地表土体沉降** 的敏感程度。

<details>
<summary>📷 查看模型示意图</summary>

![model_description](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/model_description.png)

</details>

### 参数敏感性分析

| 本构参数 | 符号 | 基准值 | 敏感性分析范围 |
|:--------:|:----:|:------:|:--------------:|
| 初始孔隙比 | e₀ | 0.9 | 0.6 → 0.9 → 1.2 |
| 泊松比 | ν | 0.3 | 0.3 → 0.4 → 0.45 |
| 临界状态线斜率 | M | 1.2 | 0.9 → 1.2 → 1.5 |
| 小应变参数 | γ₀.₇ | 0.0002 | 0.0001 → 0.001 → 1 |
| 压缩指数 | λ | 0.2 | 0.04 → 0.1 → 0.2 |
| 回弹指数 | κ | 0.02 | 0.02 → 0.04 → 0.08 |
| 超固结控制参数 | m | 2.5 | 0.2 → 1.0 → 5.0 |
| 结构性控制参数 | a | 1 | 0.1 → 0.5 → 2.0 |
| 初始超固结参数 | OCR | 5 | 1 → 5 → 10 |
| 初始结构性参数 | R₀* | 0.5 | 0.01 → 0.1 → 1 |

### 运行计算

设置好参数和计算工况后运行求解器，在求解完成后查看结果：

<details>
<summary>📷 查看计算流程</summary>

![run_calculation](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/run_calculation.gif)

</details>

### 配置远程脚本服务器

进入 **Plaxis 2D Output Viewer**，点击 **专业** → **配置远程脚本服务器**：

| 参数 | 推荐值 |
|:----:|:------:|
| 端口 | `10001` |
| 密码 | `user` |

<details>
<summary>📷 查看配置截图</summary>

![set_button](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/set_button.png)

![set_servicer](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/set_servicer.png)

</details>

### 提取结果

打开 `main.py`，确保连接参数与 Plaxis 配置一致：

```python
s_o, g_o = new_server('localhost', '10001', password='user')
```

运行 `main.py`，即可完成结果提取：

<details>
<summary>📷 查看提取流程</summary>

![extract_results](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/extract_results.gif)

</details>

---

<div align="center">
  <sub>如果觉得有帮助，欢迎 ⭐ Star 支持！</sub>
</div>
