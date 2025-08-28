import streamlit as st
import pandas as pd
import ollama

# Tag cleaning function
def clean_tag(tag):
    if pd.isna(tag):
        return 'Uncategorized'
    t = str(tag).lower().strip()
    if 'food' in t or '🥘' in t:
        return 'Food'
    elif 'groceries' in t or '🛒' in t:
        return 'Groceries'
    elif 'services' in t or '🏦' in t:
        return 'Services'
    elif 'fuel' in t or '⛽️' in t:
        return 'Fuel'
    elif 'bill payment' in t or '🧾' in t:
        return 'Bills'
    elif 'travel' in t or '✈️' in t:
        return 'Travel'
    elif 'entertainment' in t or '🎈' in t:
        return 'Entertainment'
    elif 'medical' in t or '🏥' in t:
        return 'Medical'
    elif 'cash withdrawal' in t or 'atm' in t:
        return 'Cash Withdrawal'
    elif 'transfer' in t or '💵' in t:
        return 'Transfers'
    else:
        return 'Miscellaneous'

def get_finance_advice_with_ollama(total_income, total_received, total_spent, category_spending, model_name="llama3.1:8b"):
    category_spending_text = "\n".join([f"- {cat}: ₹{amt:,.2f}" for cat, amt in category_spending.items()])
    prompt = f"""
    You are an expert personal finance coach. Here is the user’s financial summary:

    - Total Income: ₹{total_income:,.2f}
    - Total Money Received: ₹{total_received:,.2f}
    - Total Money Spent: ₹{abs(total_spent):,.2f}

    Spending by category:
    {category_spending_text}

    Using common budgeting guidelines such as the 50/30/20 rule and category-specific percentage limits, identify:

    1. Which categories are exceeding recommended spending thresholds based on the user’s income.
    2. Provide clear, friendly, and actionable advice on how to reduce expenses or improve financial health in these categories.
    3. Suggest areas where the user is doing well.
    4. Mention any other financial habits to watch out for, like too many transfers or irregular spending.
    5. Summarize the overall financial health based on income versus total expenditure.
    
    Also just do an in depth analysis of the user's financial health and provide suggestions for improvement. 
    You don't need to stick to the 50/30/20 rule but just serve as a financial coach and analyze the user specific spending habits and applt whatever rule relevant.

    Remember to give an in depth analysis and act like a financial coach who analyzes separate category's expenditure in depth. 
    
    Present this advice in an encouraging tone that motivates positive change.
    Also remember to not ask any question in the end at all. This is a one time advice and not a conversation. So don't ask any question
    """
    try:
        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content']
    except Exception as e:
        return f"Error communicating with Ollama: {e}"

# Streamlit app
st.title("SafeSpend - Personal Finance Risk & Literacy Coach")

uploaded_file = st.file_uploader("Upload your 1 Month Paytm UPI transaction Excel file", type=['xlsx', 'xls'])

user_income = st.number_input("Enter your monthly Total Income (₹)", min_value=0.0, value=0.0, step=1000.0)

if uploaded_file is not None and user_income > 0:
    # Read all sheets
    all_sheets = pd.read_excel(uploaded_file, sheet_name=None)
    
    # Remove Summary sheet if exists
    all_sheets.pop('Summary', None)
    
    # Get Passbook Payment History sheet
    df = all_sheets['Passbook Payment History']
    
    # Keep necessary columns
    df = df[['Date', 'Time', 'Amount', 'Tags']]
    
    # Clean tags
    df['Cleaned Category'] = df['Tags'].apply(clean_tag)

    # Drop original Tags column
    df = df.drop('Tags', axis=1)
    
    # Convert Amount to numeric
    df['Amount'] = df['Amount'].astype(str).str.replace(',', '').astype(float)
    
    st.subheader("Transactions Data (First 10 rows)")
    st.dataframe(df.head(10))
    
    # Calculate spending metrics
    total_spent = df[df['Amount'] < 0]['Amount'].sum()
    total_received = df[df['Amount'] > 0]['Amount'].sum()
    category_spending = df[df['Amount'] < 0].groupby('Cleaned Category')['Amount'].sum().abs().to_dict()
    
    st.subheader("Spending Summary")
    st.write(f"Monthly Income: ₹{user_income:,.2f}")
    st.write(f"Total spent: ₹{abs(total_spent):,.2f}")
    st.write(f"Total money received: ₹{total_received:,.2f}")
    st.write("Spending by category:")
    st.write(category_spending)
    
    # Get AI generated advice
    with st.spinner("Generating financial advice..."):
        advice = get_finance_advice_with_ollama(user_income, total_received, total_spent, category_spending)
    
    st.subheader("Financial Advice")
    st.write(advice)

else:

    st.info("Please upload a transaction Excel file and enter your monthly income.")
