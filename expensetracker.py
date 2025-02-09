import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random

# Initialize the expense dataframe
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Index', 'Date', 'Category', 'Amount', 'Description'])

# List of quotes
quotes = [
    "A budget is telling your money where to go instead of wondering where it went.",
    "Do not save what is left after spending, but spend what is left after saving.",
    "Wealth consists not in having great possessions, but in having few wants.",
    "A penny saved is a penny earned.",
    "The more you save, the more freedom you have.",
    "The habit of saving is itself an education.",
    "Beware of little expenses; a small leak will sink a great ship.",
    "Rich people stay rich by living like they’re broke.",
    "Saving money today secures your future tomorrow.",
    "Every Rupee saved is a step toward financial independence."
]

# Functions to manage expenses
def add_expense(date, category, amount, description):
    new_index = len(st.session_state.expenses) + 1
    new_expense = pd.DataFrame([[new_index, date, category, amount, description]], 
                               columns=st.session_state.expenses.columns)
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)

def delete_expense(index):
    st.session_state.expenses = st.session_state.expenses[st.session_state.expenses['Index'] != index].reset_index(drop=True)
    st.session_state.expenses['Index'] = range(1, len(st.session_state.expenses) + 1)

def visualize_expenses():
    if not st.session_state.expenses.empty:
        fig, ax = plt.subplots(figsize=(3, 3))  # Reduce the pie chart size further
        category_totals = st.session_state.expenses.groupby('Category')['Amount'].sum()
        ax.pie(category_totals, labels=category_totals.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
        ax.axis('equal')
        st.pyplot(fig)
    else:
        st.warning("No expenses to visualize!")

# UI Enhancements
st.set_page_config(page_title='Expense Tracker', page_icon='💰', layout='wide', initial_sidebar_state='expanded')
st.markdown("""
    <style>
        .big-font {font-size: 24px !important; font-weight: bold;}
        .highlight {color: #4CAF50; font-size: 20px; font-weight: bold;}
        .total-expense {text-align: center; font-size: 24px; font-weight: bold; color: #4CAF50; margin-top: 20px;}
    </style>
""", unsafe_allow_html=True)

st.title('💰 Expense Tracker')
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1170/1170576.png", width=100)
menu = st.sidebar.radio("📌 Navigation", ["🏠 Home", "➕ Add Expense", "📊 View Expenses", "📈 Visualization"], key='menu')

if menu == "🏠 Home":
    st.header("Welcome to Expense Tracker! 🎯")
    if not st.session_state.expenses.empty:
        total_expense = st.session_state.expenses["Amount"].sum()
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"<p class='big-font'>Total Expenses: <span class='highlight'>₹{total_expense}</span></p>", unsafe_allow_html=True)
            st.dataframe(st.session_state.expenses.set_index('Index'))
        with col2:
            visualize_expenses()
    else:
        st.info(random.choice(quotes))

elif menu == "➕ Add Expense":
    st.header('📝 Add a New Expense')
    date = st.date_input('📅 Date')
    category = st.selectbox('📂 Category', ['Food', 'Transport', 'Entertainment', 'Utilities', 'Other'])
    amount = st.number_input('💵 Amount', min_value=0.0, format="%.2f")
    description = st.text_input('📝 Description')
    if st.button('✅ Add Expense'):
        add_expense(date, category, amount, description)
        st.success('Expense added successfully! 🎉')

elif menu == "📊 View Expenses":
    st.header('📜 Expense Records')
    if not st.session_state.expenses.empty:
        edited_expenses = st.data_editor(
            st.session_state.expenses.set_index('Index'),
            num_rows="fixed"
        )
        if not edited_expenses.equals(st.session_state.expenses.set_index('Index')):
            if st.button("Save Changes"):
                st.session_state.expenses = edited_expenses.reset_index()
                st.success("Changes saved successfully!")
        
        total_expense = st.session_state.expenses["Amount"].sum()
        st.markdown(f"<p class='total-expense'>Total Expenses: ₹{total_expense}</p>", unsafe_allow_html=True)
    else:
        st.warning("No expenses to display!")
    
    index_to_delete = st.number_input("Enter index to delete", min_value=1, max_value=len(st.session_state.expenses) if not st.session_state.expenses.empty else 1, step=1, key='delete_index')
    if st.button("Delete", key='delete_btn'):
        delete_expense(index_to_delete)
        st.success("Expense deleted successfully!")
        st.rerun()

elif menu == "📈 Visualization":
    st.header('📊 Expense Visualization')
    visualize_expenses()
