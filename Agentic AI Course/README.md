# Project Setup Guide

Follow the steps below to set up and run the project successfully.

## 🚀 Setup Instructions

1. **Create a Virtual Environment**

   ```bash
   python -m venv [ENV_NAME]
   ```

2. **Bypass Script Execution Policy (If Required)**  
   Some systems (especially Windows) block script execution by default.  
   To temporarily bypass this restriction, run:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```

3. **Activate the Virtual Environment**  
   Activate the environment so that all packages install inside it:

   ```bash
   .\[ENV_NAME]\Scripts\activate
   ```

4. **Install Required Packages**  
   Install all dependencies listed in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**

   ```bash
   streamlit run app.py
   ```

---

✅ Your application should now be running successfully!
