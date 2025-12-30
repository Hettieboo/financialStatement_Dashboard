import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Bank Statement AI Analyzer",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Generate comprehensive sample data
@st.cache_data
def generate_sample_data():
    np.random.seed(42)
    
    # Date range: 6 months of data
    start_date = datetime.now() - timedelta(days=180)
    dates = [start_date + timedelta(days=x) for x in range(180)]
    
    transactions = []
    
    # Categories and merchants
    categories = {
        'Groceries': ['Whole Foods', 'Trader Joes', 'Safeway', 'Walmart', 'Target'],
        'Dining': ['Chipotle', 'Starbucks', 'McDonalds', 'Olive Garden', 'Subway', 'Pizza Hut'],
        'Entertainment': ['Netflix', 'Spotify', 'AMC Theaters', 'Steam', 'PlayStation'],
        'Utilities': ['PG&E Electric', 'Comcast Internet', 'AT&T Mobile', 'Water Company'],
        'Transport': ['Uber', 'Lyft', 'Shell Gas', 'Chevron', 'BART Transit'],
        'Shopping': ['Amazon', 'Macys', 'Best Buy', 'Nike', 'Apple Store', 'Zara'],
        'Healthcare': ['CVS Pharmacy', 'Kaiser Permanente', 'Walgreens', 'Dentist'],
        'Subscriptions': ['Netflix', 'Spotify Premium', 'Adobe Creative', 'NYT Digital', 'Amazon Prime'],
        'Fitness': ['Planet Fitness', 'ClassPass', 'Yoga Studio', 'Nike Running'],
        'Bills': ['Rent Payment', 'Insurance Premium', 'Credit Card Payment']
    }
    
    # Monthly salary
    for month in range(6):
        salary_date = start_date + timedelta(days=month*30 + 15)
        transactions.append({
            'Date': salary_date.strftime('%Y-%m-%d'),
            'Description': 'Salary Deposit - Direct Deposit',
            'Amount': 5500.00,
            'Category': 'Income',
            'Type': 'Credit'
        })
    
    # Regular transactions with realistic patterns
    for date in dates:
        day_of_week = date.weekday()
        
        # Rent (1st of each month)
        if date.day == 1:
            transactions.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Description': 'Rent Payment - Landlord',
                'Amount': -1800.00,
                'Category': 'Bills',
                'Type': 'Debit'
            })
        
        # Monthly subscriptions
        if date.day == 5:
            for sub in ['Netflix', 'Spotify Premium', 'Adobe Creative']:
                amount = {'Netflix': -15.99, 'Spotify Premium': -10.99, 'Adobe Creative': -52.99}[sub]
                transactions.append({
                    'Date': date.strftime('%Y-%m-%d'),
                    'Description': sub,
                    'Amount': amount,
                    'Category': 'Subscriptions',
                    'Type': 'Debit'
                })
        
        # Utilities (around 10th)
        if date.day == 10:
            for util in ['PG&E Electric', 'Comcast Internet']:
                amount = np.random.uniform(80, 150)
                transactions.append({
                    'Date': date.strftime('%Y-%m-%d'),
                    'Description': util,
                    'Amount': -round(amount, 2),
                    'Category': 'Utilities',
                    'Type': 'Debit'
                })
        
        # Daily transactions (more on weekends)
        num_transactions = np.random.randint(2, 8) if day_of_week >= 5 else np.random.randint(1, 5)
        
        for _ in range(num_transactions):
            category = np.random.choice(list(categories.keys()), p=[0.25, 0.20, 0.10, 0.05, 0.10, 0.15, 0.05, 0.02, 0.03, 0.05])
            merchant = np.random.choice(categories[category])
            
            # Amount based on category
            if category == 'Groceries':
                amount = -np.random.uniform(20, 150)
            elif category == 'Dining':
                amount = -np.random.uniform(10, 80)
            elif category == 'Entertainment':
                amount = -np.random.uniform(15, 60)
            elif category == 'Transport':
                amount = -np.random.uniform(10, 60)
            elif category == 'Shopping':
                amount = -np.random.uniform(30, 300)
            elif category == 'Healthcare':
                amount = -np.random.uniform(20, 200)
            elif category == 'Fitness':
                amount = -np.random.uniform(15, 50)
            else:
                amount = -np.random.uniform(10, 100)
            
            transactions.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Description': merchant,
                'Amount': round(amount, 2),
                'Category': category,
                'Type': 'Debit'
            })
    
    df = pd.DataFrame(transactions)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    
    # Calculate running balance
    starting_balance = 3000
    df['Balance'] = starting_balance + df['Amount'].cumsum()
    
    return df

# Predictive models
def predict_future_spending(df, days=30):
    """Predict future daily spending using linear regression"""
    df_expenses = df[df['Amount'] < 0].copy()
    daily_spending = df_expenses.groupby(df_expenses['Date'].dt.date)['Amount'].sum().abs()
    
    X = np.arange(len(daily_spending)).reshape(-1, 1)
    y = daily_spending.values
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict next 30 days
    future_X = np.arange(len(daily_spending), len(daily_spending) + days).reshape(-1, 1)
    predictions = model.predict(future_X)
    
    last_date = df['Date'].max()
    future_dates = [last_date + timedelta(days=i+1) for i in range(days)]
    
    return pd.DataFrame({
        'Date': future_dates,
        'Predicted_Spending': predictions
    })

def predict_balance(df, days=30):
    """Predict future account balance"""
    current_balance = df['Balance'].iloc[-1]
    
    # Calculate average daily change
    daily_changes = df.groupby(df['Date'].dt.date)['Amount'].sum()
    avg_daily_change = daily_changes.mean()
    
    # Account for expected monthly income
    monthly_income = df[df['Category'] == 'Income']['Amount'].mean()
    
    future_balances = []
    balance = current_balance
    last_date = df['Date'].max()
    
    for i in range(days):
        future_date = last_date + timedelta(days=i+1)
        
        # Add monthly income around 15th
        if future_date.day == 15:
            balance += monthly_income
        
        balance += avg_daily_change
        future_balances.append(balance)
    
    future_dates = [last_date + timedelta(days=i+1) for i in range(days)]
    
    return pd.DataFrame({
        'Date': future_dates,
        'Predicted_Balance': future_balances
    })

def predict_category_spending(df):
    """Predict next month spending by category"""
    last_30_days = df[df['Date'] >= df['Date'].max() - timedelta(days=30)]
    category_spending = last_30_days[last_30_days['Amount'] < 0].groupby('Category')['Amount'].sum().abs()
    
    # Add 5% growth trend
    predicted = category_spending * 1.05
    
    return pd.DataFrame({
        'Category': category_spending.index,
        'Last_Month': category_spending.values,
        'Predicted_Next_Month': predicted.values
    }).sort_values('Predicted_Next_Month', ascending=False)

def detect_anomalies(df):
    """Detect unusual spending patterns"""
    expenses = df[df['Amount'] < 0]['Amount'].abs()
    mean = expenses.mean()
    std = expenses.std()
    threshold = mean + 2 * std
    
    anomalies = df[(df['Amount'] < 0) & (df['Amount'].abs() > threshold)].copy()
    anomalies['Amount'] = anomalies['Amount'].abs()
    
    return anomalies.sort_values('Amount', ascending=False).head(10)

def find_recurring_transactions(df):
    """Identify recurring transactions (potential subscriptions)"""
    merchant_freq = df[df['Amount'] < 0].groupby('Description').agg({
        'Amount': ['count', 'mean'],
        'Category': 'first'
    }).reset_index()
    
    merchant_freq.columns = ['Merchant', 'Count', 'Avg_Amount', 'Category']
    merchant_freq['Avg_Amount'] = merchant_freq['Avg_Amount'].abs()
    
    recurring = merchant_freq[merchant_freq['Count'] >= 3].sort_values('Count', ascending=False)
    
    return recurring.head(10)

# Main app
def main():
    st.title("💰 AI-Powered Bank Statement Analyzer")
    st.markdown("### Discover insights, patterns, and predict your financial future")
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Data Source")
        data_source = st.radio(
            "Choose data source:",
            ["Use Sample Data", "Upload Your CSV"]
        )
        
        if data_source == "Upload Your CSV":
            uploaded_file = st.file_uploader("Upload bank statement CSV", type=['csv'])
            st.info("Expected columns: Date, Description, Amount, Category")
            
            if uploaded_file:
                df = pd.read_csv(uploaded_file)
                df['Date'] = pd.to_datetime(df['Date'])
                if 'Balance' not in df.columns:
                    df['Balance'] = 3000 + df['Amount'].cumsum()
            else:
                df = generate_sample_data()
        else:
            df = generate_sample_data()
        
        st.markdown("---")
        st.header("⚙️ Settings")
        prediction_days = st.slider("Prediction horizon (days)", 15, 90, 30)
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "🔮 Predictions", "🔍 Insights", "📊 Detailed Analysis"])
    
    with tab1:
        st.header("Financial Overview")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_income = df[df['Amount'] > 0]['Amount'].sum()
        total_expenses = df[df['Amount'] < 0]['Amount'].sum()
        net_cash_flow = total_income + total_expenses
        savings_rate = (net_cash_flow / total_income * 100) if total_income > 0 else 0
        
        with col1:
            st.metric("💰 Total Income", f"${total_income:,.2f}")
        with col2:
            st.metric("💸 Total Expenses", f"${abs(total_expenses):,.2f}")
        with col3:
            st.metric("📊 Net Cash Flow", f"${net_cash_flow:,.2f}", 
                     delta=f"{savings_rate:.1f}% savings rate")
        with col4:
            current_balance = df['Balance'].iloc[-1]
            st.metric("🏦 Current Balance", f"${current_balance:,.2f}")
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Spending by Category")
            category_spending = df[df['Amount'] < 0].groupby('Category')['Amount'].sum().abs().sort_values(ascending=False)
            fig = px.pie(values=category_spending.values, names=category_spending.index, 
                        hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Balance Over Time")
            fig = px.line(df, x='Date', y='Balance', title='Account Balance Trend')
            fig.update_traces(line_color='#1f77b4', line_width=2)
            fig.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.5)
            st.plotly_chart(fig, use_container_width=True)
        
        # Monthly spending trend
        st.subheader("Monthly Spending Trend")
        monthly = df[df['Amount'] < 0].copy()
        monthly['Month'] = monthly['Date'].dt.to_period('M')
        monthly_spending = monthly.groupby('Month')['Amount'].sum().abs()
        
        fig = px.bar(x=monthly_spending.index.astype(str), y=monthly_spending.values,
                    labels={'x': 'Month', 'y': 'Spending ($)'})
        fig.update_traces(marker_color='#ff7f0e')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.header("🔮 Predictive Analytics")
        
        # Balance prediction
        st.subheader(f"Balance Forecast (Next {prediction_days} Days)")
        balance_pred = predict_balance(df, prediction_days)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Balance'], 
                                mode='lines', name='Historical Balance',
                                line=dict(color='blue', width=2)))
        fig.add_trace(go.Scatter(x=balance_pred['Date'], y=balance_pred['Predicted_Balance'],
                                mode='lines', name='Predicted Balance',
                                line=dict(color='red', width=2, dash='dash')))
        fig.update_layout(title='Balance Prediction', xaxis_title='Date', yaxis_title='Balance ($)')
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            end_balance = balance_pred['Predicted_Balance'].iloc[-1]
            st.metric("Predicted End Balance", f"${end_balance:,.2f}")
        with col2:
            min_balance = balance_pred['Predicted_Balance'].min()
            risk = "🔴 HIGH" if min_balance < 500 else "🟡 MEDIUM" if min_balance < 1000 else "🟢 LOW"
            st.metric("Overdraft Risk", risk)
        with col3:
            trend = "📈 Increasing" if balance_pred['Predicted_Balance'].iloc[-1] > balance_pred['Predicted_Balance'].iloc[0] else "📉 Decreasing"
            st.metric("Balance Trend", trend)
        
        st.markdown("---")
        
        # Spending prediction
        st.subheader("Daily Spending Forecast")
        spending_pred = predict_future_spending(df, prediction_days)
        
        fig = px.line(spending_pred, x='Date', y='Predicted_Spending',
                     title=f'Predicted Daily Spending (Next {prediction_days} Days)')
        fig.update_traces(line_color='purple', line_width=2)
        st.plotly_chart(fig, use_container_width=True)
        
        total_predicted = spending_pred['Predicted_Spending'].sum()
        st.info(f"💡 **Predicted total spending for next {prediction_days} days:** ${total_predicted:,.2f}")
        
        # Category predictions
        st.subheader("Category Spending Forecast")
        category_pred = predict_category_spending(df)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Last Month', x=category_pred['Category'], 
                            y=category_pred['Last_Month'], marker_color='lightblue'))
        fig.add_trace(go.Bar(name='Predicted Next Month', x=category_pred['Category'], 
                            y=category_pred['Predicted_Next_Month'], marker_color='darkblue'))
        fig.update_layout(barmode='group', title='Category Spending: Last vs Next Month')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.header("🔍 Hidden Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💳 Recurring Transactions")
            recurring = find_recurring_transactions(df)
            
            if not recurring.empty:
                for idx, row in recurring.iterrows():
                    with st.expander(f"**{row['Merchant']}** - {row['Category']}"):
                        st.write(f"**Frequency:** {row['Count']} times")
                        st.write(f"**Average Amount:** ${row['Avg_Amount']:.2f}")
                        st.write(f"**Estimated Monthly Cost:** ${row['Avg_Amount'] * (row['Count']/6):.2f}")
                
                total_recurring = recurring['Avg_Amount'].sum()
                st.success(f"💡 Total recurring monthly costs: **${total_recurring:.2f}**")
            else:
                st.info("No recurring transactions found")
        
        with col2:
            st.subheader("⚠️ Unusual Transactions")
            anomalies = detect_anomalies(df)
            
            if not anomalies.empty:
                for idx, row in anomalies.iterrows():
                    st.warning(f"**{row['Description']}** - ${row['Amount']:.2f} on {row['Date'].strftime('%Y-%m-%d')}")
            else:
                st.info("No unusual transactions detected")
        
        st.markdown("---")
        
        # Spending patterns
        st.subheader("📅 Spending Patterns")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**By Day of Week**")
            df_temp = df[df['Amount'] < 0].copy()
            df_temp['DayOfWeek'] = df_temp['Date'].dt.day_name()
            day_spending = df_temp.groupby('DayOfWeek')['Amount'].sum().abs()
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_spending = day_spending.reindex(day_order)
            
            fig = px.bar(x=day_spending.index, y=day_spending.values,
                        labels={'x': 'Day', 'y': 'Spending ($)'})
            fig.update_traces(marker_color='teal')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**By Time of Day**")
            if 'Time' in df.columns:
                df_temp = df[df['Amount'] < 0].copy()
                df_temp['Hour'] = pd.to_datetime(df_temp['Time']).dt.hour
                hour_spending = df_temp.groupby('Hour')['Amount'].sum().abs()
                
                fig = px.line(x=hour_spending.index, y=hour_spending.values,
                            labels={'x': 'Hour of Day', 'y': 'Spending ($)'})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Time data not available")
        
        # Top merchants
        st.subheader("🏪 Top Merchants")
        top_merchants = df[df['Amount'] < 0].groupby('Description')['Amount'].agg(['sum', 'count']).reset_index()
        top_merchants['sum'] = top_merchants['sum'].abs()
        top_merchants = top_merchants.sort_values('sum', ascending=False).head(10)
        
        fig = px.bar(top_merchants, x='Description', y='sum', 
                    labels={'sum': 'Total Spent ($)', 'Description': 'Merchant'},
                    title='Top 10 Merchants by Total Spending')
        fig.update_traces(marker_color='orange')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.header("📊 Detailed Transaction Analysis")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            categories = ['All'] + sorted(df['Category'].unique().tolist())
            selected_category = st.selectbox("Filter by Category", categories)
        
        with col2:
            transaction_type = st.selectbox("Transaction Type", ['All', 'Debit', 'Credit'])
        
        with col3:
            date_range = st.date_input("Date Range", 
                                      value=(df['Date'].min(), df['Date'].max()),
                                      min_value=df['Date'].min(),
                                      max_value=df['Date'].max())
        
        # Apply filters
        filtered_df = df.copy()
        
        if selected_category != 'All':
            filtered_df = filtered_df[filtered_df['Category'] == selected_category]
        
        if transaction_type != 'All':
            if transaction_type == 'Debit':
                filtered_df = filtered_df[filtered_df['Amount'] < 0]
            else:
                filtered_df = filtered_df[filtered_df['Amount'] > 0]
        
        if len(date_range) == 2:
            filtered_df = filtered_df[
                (filtered_df['Date'].dt.date >= date_range[0]) & 
                (filtered_df['Date'].dt.date <= date_range[1])
            ]
        
        # Display statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Transactions", len(filtered_df))
        with col2:
            st.metric("Total Amount", f"${filtered_df['Amount'].sum():,.2f}")
        with col3:
            st.metric("Average Transaction", f"${filtered_df['Amount'].mean():,.2f}")
        with col4:
            st.metric("Largest Transaction", f"${filtered_df['Amount'].abs().max():,.2f}")
        
        # Transaction table
        st.subheader("Transaction Details")
        display_df = filtered_df[['Date', 'Description', 'Category', 'Amount', 'Balance']].copy()
        display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
        display_df['Amount'] = display_df['Amount'].apply(lambda x: f"${x:,.2f}")
        display_df['Balance'] = display_df['Balance'].apply(lambda x: f"${x:,.2f}")
        
        st.dataframe(display_df, use_container_width=True, height=400)
        
        # Download button
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data",
            data=csv,
            file_name="filtered_transactions.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
