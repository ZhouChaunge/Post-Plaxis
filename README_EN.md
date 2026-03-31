<div align="center">

<h1>🏗️ Post-Plaxis</h1>

<p>
  <strong>Automated Plaxis Post-Processing via Remote Scripting</strong>
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3.7-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Plaxis-2D%20%2F%203D-green" alt="Plaxis">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
  <img src="https://img.shields.io/badge/Shanghai%20Model-UDSM-red" alt="Shanghai Model">
</p>

<p>
  <a href="README.md">中文文档</a> | <b>English</b>
</p>

</div>

---

## 📖 Overview

This project demonstrates how to efficiently export results from **Plaxis 2D/3D Output Viewer** using the remote scripting server. It provides a 2D excavation parametric sensitivity analysis example, extracting **diaphragm wall displacement** and **ground surface settlement** using Python with the **Shanghai Model (UDSM)**.

### ✨ Key Features

- 🔌 Auto-connect to Plaxis Output via remote scripting server
- 📊 Extract diaphragm wall lateral displacement & surface soil settlement
- 📈 Auto-generate displacement curves for each construction phase
- 💾 Save results as Excel files + PNG figures

### 📁 Project Structure

```
Post-Plaxis/
├── main.py                # Main script — data extraction & plotting
├── requirements.txt       # pip dependencies
├── environment.yaml       # conda environment config
├── model/                 # Plaxis 2D example model
├── output/                # Result output directory
├── udsm/                  # Constitutive model DLL
└── image/                 # Documentation images
```

---

## 🔧 Constitutive Model Installation

The user-defined soil model DLL (`20230801-UnifiedModel64.dll`) is in the `udsm` folder. Copy it to your local Plaxis installation directory:

```
...\Plaxis\3D\udsm\
```

<details>
<summary>📷 View installation screenshot</summary>

![dll_install](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/dll_install.png)

</details>

---

## 🐍 Python Environment Setup

> **Prerequisite:** [Anaconda](https://www.anaconda.com/) must be installed.

Two configuration methods are available. Choose one:

<details>
<summary><b>Option A: Using <code>environment.yaml</code> (Recommended)</b></summary>

Open a terminal in the project directory and run:

```bash
conda env create -f environment.yaml
```

</details>

<details>
<summary><b>Option B: Using <code>requirements.txt</code></b></summary>

Open a terminal in the project directory and run:

```bash
conda create -n plaxis37 python=3.7   # Create a Python 3.7 environment
conda activate plaxis37                # Activate the environment
pip install -r requirements.txt        # Install dependencies
```

> ⚠️ **Warning:** Make sure `plaxis37` is activated before running `pip install`. Otherwise, packages will be installed into your `base` environment, which may cause conflicts or corruption!

</details>

<br>

After setup, a `plaxis37` folder will appear under `.../Anaconda/envs/`:

<details>
<summary>📷 View directory screenshot</summary>

![envir_dir](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/envir_dir.png)

</details>

### Installing `plxscripting`

The `plxscripting` library is essential for Plaxis post-processing. It **cannot** be installed via `pip` and must be installed through Plaxis:

1. Open `model/2Dmodel.p2dx` in Plaxis 2D
2. Click **Expert** → **Python** → **Configure Python Interpreter**
3. Select the Python interpreter from the `plaxis37` environment, then click **Install required components**

<details>
<summary>📷 View configuration process</summary>

![Py_interpreter](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/Py_interpreter.png)

![plxscripting_install](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/plxscripting_install.gif)

</details>

---

## 🚀 Running the Program

### Example Model

The example is a 2D plane-strain excavation in a uniform foundation, designed to analyze the sensitivity of constitutive parameters on **diaphragm wall lateral displacement** and **ground surface settlement**.

<details>
<summary>📷 View model diagram</summary>

![model_description](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/model_description.png)

</details>

### Sensitivity Analysis Parameters

| Parameter | Symbol | Baseline | Sensitivity Range |
|:---------:|:------:|:--------:|:-----------------:|
| Initial void ratio | e₀ | 0.9 | 0.6 → 0.9 → 1.2 |
| Poisson's ratio | ν | 0.3 | 0.3 → 0.4 → 0.45 |
| Critical state line slope | M | 1.2 | 0.9 → 1.2 → 1.5 |
| Small strain parameter | γ₀.₇ | 0.0002 | 0.0001 → 0.001 → 1 |
| Compression index | λ | 0.2 | 0.04 → 0.1 → 0.2 |
| Swelling index | κ | 0.02 | 0.02 → 0.04 → 0.08 |
| OCR control parameter | m | 2.5 | 0.2 → 1.0 → 5.0 |
| Structure control parameter | a | 1 | 0.1 → 0.5 → 2.0 |
| Initial OCR | OCR | 5 | 1 → 5 → 10 |
| Initial structure parameter | R₀* | 0.5 | 0.01 → 0.1 → 1 |

### Running the Solver

After configuring parameters and construction phases, run the solver and view results:

<details>
<summary>📷 View calculation process</summary>

![run_calculation](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/run_calculation.gif)

</details>

### Configuring the Remote Scripting Server

Open **Plaxis 2D Output Viewer**, then click **Expert** → **Configure remote scripting server**:

| Setting | Recommended Value |
|:-------:|:-----------------:|
| Port | `10001` |
| Password | `user` |

<details>
<summary>📷 View configuration screenshots</summary>

![set_button](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/set_button.png)

![set_servicer](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/set_servicer.png)

</details>

### Extracting Results

Open `main.py` and ensure the connection settings match your Plaxis configuration:

```python
s_o, g_o = new_server('localhost', '10001', password='user')
```

Run `main.py` to extract the results:

<details>
<summary>📷 View extraction process</summary>

![extract_results](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/extract_results.gif)

</details>

---

<div align="center">
  <sub>If you find this helpful, please consider giving it a ⭐ Star!</sub>
</div>
