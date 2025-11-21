# 🧠 NLP Environment Setup Guide

This guide walks you through setting up a dedicated Python virtual environment for Natural Language Processing (NLP) projects with all essential libraries installed.

---

## 🪜 Step 1: Create the Virtual Environment

A virtual environment allows you to manage project-specific dependencies without affecting the global Python installation.
`python -m venv llms_course_env`

- `python -m venv`: Creates a new virtual environment.  
- `llms_course_env`: Name of your environment (you can choose another name).


---

## ⚙️ Step 2: Activate the Environment

Activate the environment so all packages install inside it.
`.\llms_course_env\Scripts\activate`

You’ll know it’s activated when `(llms_course_env)` appears at the start of your command line.

### 🔒 If System Restricts Activation

Some systems block script execution by default. To bypass temporarily:
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

### ✅ Check Current Execution Policy:
`Get-ExecutionPolicy`

*Tip:* This setting is temporary and resets after you close the terminal.


---

## 🧩 Step 3: Upgrade pip

Ensure your pip is up to date before installing libraries.
`python.exe -m pip install --upgrade pip`


---

## 📦 Step 4: Install Required Libraries

Install essential NLP and data analysis libraries:
`pip install openai==0.28
pip install configparser==5.3.0
pip install langchain==0.0.297
pip install pydantic==1.10.9
pip install tiktoken
pip install faiss-cpu
pip install transformers
pip install torch
pip install datasets
pip install evaluate
pip install accelerate
pip install ipywidgets
pip install matplotlib
pip install seaborn
pip install clean-text
pip install sentencepiece
`


### 📘 Description of Key Libraries

| **Library**       | **Purpose**                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| openai            | Access OpenAI API for LLM-based applications                               |
| configparser      | Manage configuration files in Python                                       |
| langchain         | Build applications using LLMs with chaining and orchestration             |
| pydantic          | Data validation and settings management using Python type hints           |
| tiktoken          | Tokenization for OpenAI models                                            |
| faiss-cpu         | Efficient similarity search and clustering for embeddings                 |
| transformers       | Hugging Face library for NLP and LLM models                               |
| torch             | Deep learning framework for model training and inference                  |
| datasets          | Load and process datasets for ML and NLP tasks                            |
| evaluate          | Metrics and evaluation utilities for ML models                            |
| accelerate        | Optimize and accelerate training on multiple devices                      |
| ipywidgets        | Interactive widgets for Jupyter notebooks                                 |
| matplotlib        | Data visualization library                                                |
| seaborn           | Statistical data visualization                                            |
| clean-text        | Text cleaning and preprocessing utilities                                  |
| sentencepiece     | Tokenizer for NLP models (used in transformers)                           |
| pandas            | Data manipulation and analysis                                            |
| scikit-learn      | Machine learning algorithms and utilities                                 |

---

## 🧠 Step 5: Add the Environment to Jupyter Notebook

To use this environment within Jupyter:
`python -m ipykernel install --user --name=llms_course_env --display-name "Python (llms_course_env)" `

- `--name`: Internal name for the kernel  
- `--display-name`: Name that appears in the Jupyter Notebook interface

Then, open **Jupyter Notebook** or **JupyterLab** and select:
`Kernel → Change Kernel → Python (llms_course_env)`

---

## ✅ Final Verification

Test the setup by running:
`import openai, langchain, torch, transformers, pandas
print("LLM environment is successfully set up!") `


If no errors occur, your environment is ready for NLP experimentation! 🎉

---

### 🧾 Notes

- Always activate your environment before running Python scripts.  
- To deactivate, simply type:
`deactivate`

- You can recreate this setup anytime using the same commands.

---

**Author:** *Abhishek Biswas*  
**Project**: LLM Course / Lab Setup
