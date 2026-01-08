# 🧠 Vector Database Environment Setup Guide

This guide walks you through setting up a dedicated Python virtual environment for Natural Language Processing (NLP) projects with all essential libraries installed.

---

## 🪜 Step 1: Create the Virtual Environment

A virtual environment allows you to manage project-specific dependencies without affecting the global Python installation.
`python -m venv vector_db_env`

- `python -m venv`: Creates a new virtual environment.  
- `vector_db_env`: Name of your environment (you can choose another name if desired).


---

## ⚙️ Step 2: Activate the Environment

Activate the environment so all packages install inside it.
`.\vector_db_env\Scripts\activate`

You’ll know it’s activated when `(vector_db_env)` appears at the start of your command line.

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
- `pip install langchain`
- `pip install langgraph`
- `pip install langchain_openai`
- `pip install langgraph-checkpoint-sqlite`
- `pip install python-dotenv`
- `pip install grandalf`
- `pip install ipykernel`
- `pip install mypy_ipython`
- `pip install pinecone`

---

## 🧠 Step 5: Add the Environment to Jupyter Notebook

To use this environment within Jupyter:
`python -m ipykernel install --user --name=vector_db_env --display-name "Python (vector_db_env)"`

- `--name`: Internal name for the kernel  
- `--display-name`: Name that appears in the Jupyter Notebook interface

Then, open **Jupyter Notebook** or **JupyterLab** and select:
`Kernel → Change Kernel → Python (vector_db_env)`

---


If no errors occur, your environment is ready for Langchain experimentation! 🎉

---

### 🧾 Notes

- Always activate your environment before running Python scripts.  
- To deactivate, simply type:
`deactivate`

- You can recreate this setup anytime using the same commands.

---

**Author:** *Abhishek Biswas*  
**Project:** Vector Database Course / Lab Setup

