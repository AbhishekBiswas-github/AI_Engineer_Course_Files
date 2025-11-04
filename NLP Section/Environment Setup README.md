# 🧠 NLP Environment Setup Guide

This guide walks you through setting up a dedicated Python virtual environment for Natural Language Processing (NLP) projects with all essential libraries installed.

---

## 🪜 Step 1: Create the Virtual Environment

A virtual environment allows you to manage project-specific dependencies without affecting the global Python installation.
`python -m venv nlp_course_env python=3.11`

- `python -m venv`: Creates a new virtual environment.  
- `nlp_course_env`: Name of your environment (you can choose another name if desired).  
- `python=3.11`: Specifies the Python version (ensure Python 3.11 is installed).


---

## ⚙️ Step 2: Activate the Environment

Activate the environment so all packages install inside it.
`.\nlp_course_env\Scripts\activate`

You’ll know it’s activated when `(nlp_course_env)` appears at the start of your command line.

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
`pip install "numpy<2.0" nltk==3.9.1 pandas==2.2.3 matplotlib==3.10.0 spacy==3.8.3 textblob==0.18.0.post0 vaderSentiment==3.3.2 transformers==4.47.1 scikit-learn==1.6.0 gensim==4.3.3 seaborn==0.13.2 torch==2.5.1 ipywidgets==8.1.5 chardet ipykernel`


### 📘 Description of Key Libraries

| Library | Purpose |
|----------|----------|
| `numpy`, `pandas` | Data manipulation and numerical operations |
| `matplotlib`, `seaborn` | Data visualization |
| `nltk`, `spacy`, `textblob` | Core NLP processing and linguistic analysis |
| `vaderSentiment` | Sentiment analysis |
| `transformers` | Hugging Face models for advanced NLP tasks |
| `scikit-learn` | Machine learning algorithms and utilities |
| `gensim` | Topic modeling and word embeddings |
| `torch` | Deep learning framework used by transformers |
| `ipywidgets` | Interactive controls in Jupyter Notebooks |
| `ipykernel` | Enables the environment to appear as a kernel in Jupyter Notebook |

---

## 🧠 Step 5: Add the Environment to Jupyter Notebook

To use this environment within Jupyter:
`python -m ipykernel install --user --name=nlp_course_env --display-name "Python (nlp_course_env)"`

- `--name`: Internal name for the kernel  
- `--display-name`: Name that appears in the Jupyter Notebook interface

Then, open **Jupyter Notebook** or **JupyterLab** and select:
`Kernel → Change Kernel → Python (nlp_course_env)`

---

## ✅ Final Verification

Test the setup by running:
`import nltk, spacy, torch, transformers, pandas
print("NLP environment is successfully set up!")`


If no errors occur, your environment is ready for NLP experimentation! 🎉

---

### 🧾 Notes

- Always activate your environment before running Python scripts.  
- To deactivate, simply type:
`deactivate`

- You can recreate this setup anytime using the same commands.

---

**Author:** *Abhishek Biswas*  
**Project:** NLP Course / Lab Setup
