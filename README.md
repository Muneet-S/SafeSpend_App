# SafeSpend - Personal Finance Risk & Literacy AI Coach

A Streamlit app that analyzes your UPI transaction data to detect risky spending patterns and provides personalized financial advice using local AI models.

## Features

- Upload your Paytm UPI transaction Excel file for analysis
- Cleans and categorizes transactions automatically
- Calculates total income, spending summary, and category-wise expenses
- Uses a local LLM (llama3.1:8b via Ollama) to provide friendly, actionable financial coaching
- Helps promote financial literacy and healthy money habits

## How to Use

1. Clone this repository
2. Install dependencies with:

pip install -r requirements.txt

text

3. Run the app locally:

streamlit run streamlit_app.py
Or
python -m streamlit run "YOUR_PATH/safespend_app.py"


text

4. Upload your transaction Excel file and enter your monthly income in the app interface
5. Get your spending summary and AI-powered financial advice instantly

## Dependencies

- Python 3.8+
- [Streamlit](https://streamlit.io)
- [Pandas](https://pandas.pydata.org)
- [Ollama Python client](https://github.com/ollama/ollama-python)
- Local Ollama LLM runtime with model `llama3.1:8b`

## Deployment

This app can be deployed on [Streamlit Cloud](https://streamlit.io/cloud) by pushing this repository to GitHub and linking it to your Streamlit Cloud account.

---

Created by Muneet Singh

For any questions or issues, please open an issue in this repository.
