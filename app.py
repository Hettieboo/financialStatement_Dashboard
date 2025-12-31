import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Financial Dashboard", page_icon="💰", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
    }
    .main {
        padding: 1rem 2rem;
    }
    [data-testid="stMetricValue"] {
        font-size: 24px;
        font-weight: 600;
        color: white !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 14px;
        color: #e0e0e0 !important;
    }
    [data-testid="stMetricDelta"] {
        color: white !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255,255,255,0.05);
        padding: 8px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        color: #a0a0b0;
        padding: 8px 20px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(255,255,255,0.1);
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    .card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    h1, h2, h3 {
        color: white !important;
    }
    p, span, label, div {
        color: white !important;
    }
    
    /* Selectbox - Main container */
    .stSelectbox {
        color: white !important;
    }
    .stSelectbox label {
        color: white !important;
    }
    
    /* Selectbox - Input field */
    .stSelectbox > div > div {
        background-color: rgba(30, 30, 46, 0.95) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
    
    /* Selectbox - All internal divs */
    .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(30, 30, 46, 0.95) !important;
    }
    
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: rgba(30, 30, 46, 0.95) !important;
        color: white !important;
        border-color: rgba(255,255,255,0.2) !important;
    }
    
    /* Selectbox - Button and text */
    .stSelectbox [role="button"] {
        background-color: rgba(30, 30, 46, 0.95) !important;
        color: white !important;
    }
    
    .stSelectbox [data-baseweb="select"] span {
        color: white !important;
    }
    
    .stSelectbox [data-baseweb="select"] svg {
        fill: white !important;
    }
    
    /* Dropdown menu container */
    div[data-baseweb="popover"] {
        background-color: rgba(30, 30, 46, 0.98) !important;
    }
    
    div[data-baseweb="popover"] > div {
        background-color: rgba(30, 30, 46, 0.98) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
    
    /* Dropdown list */
    ul[role="listbox"] {
        background-color: rgba(30, 30, 46, 0.98) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
    
    /* Dropdown options */
    li[role="option"] {
        color: white !important;
        background-color: rgba(30, 30, 46, 0.98) !important;
    }
    
    li[role="option"]:hover {
        background-color: rgba(102, 126, 234, 0.6) !important;
        color: white !important;
    }
    
    /* Selected option */
    li[role="option"][aria-selected="true"] {
        background-color: rgba(102, 126, 234, 0.4) !important;
        color: white !important;
    }
    
    /* All input elements */
    input, select, textarea {
        background-color: rgba(30, 30, 46, 0.95) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
    
    /* Dataframe */
    [data-testid="stDataFrame"] {
        background-color: rgba(255,255,255,0.05) !important;
    }
    
    .stDataFrame {
        color: white !important;
    }
    
    /* Force all text in selectbox to be white */
    .stSelectbox * {
        color: white !important;
    }
    
    /* Slider */
    .stSlider label {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def generate_company_data():
    np.random.seed(42)
    start_date = datetime.now() - timedelta(days=365)
    dates = [start_date + timedelta(days=x) for x in range(365)]
    transactions = []
    
    for week in range(52):
        week_date = start_date + timedelta(weeks=week)
        for _ in range(np.random.randint(2, 6)):
            revenue_date = week_date + timedelta(days=np.random.randint(0, 7))
            amount = np.random.uniform(5000, 50000)
            transactions.append({
                'Date': revenue_date.strftime('%Y-%m-%d'),
                'Description': 'Revenue',
                'Amount': round(amount, 2),
                'Category': 'Revenue',
                'Subcategory': 'Sales',
                'Type': 'Credit'
            })
    
    for month in range(12):
        month_date = start_date + timedelta(days=month*30)
        for day in [1, 15]:
            payroll_date = month_date.replace(day=day)
            for dept in ['Engineering', 'Sales', 'Operations', 'Management']:
                amounts = {'Engineering': -45000, 'Sales': -35000, 'Operations': -30000, 'Management': -40000}
                transactions.append({
                    'Date': payroll_date.strftime('%Y-%m-%d'),
                    'Description': f'Payroll - {dept}',
                    'Amount': amounts[dept] + np.random.uniform(-5000, 5000),
                    'Category': 'Payroll',
                    'Subcategory': 'Salaries',
                    'Type': 'Debit'
                })
        
        transactions.append({
            'Date': month_date.replace(day=1).strftime('%Y-%m-%d'),
            'Description': 'Office Rent',
            'Amount': -8500.00,
            'Category': 'Operating',
            'Subcategory': 'Office',
            'Type': 'Debit'
        })
        
        for software in ['AWS', 'Microsoft 365', 'Salesforce']:
            transactions.append({
                'Date': month_date.replace(day=10).strftime('%Y-%m-%d'),
                'Description': software,
                'Amount': -np.random.uniform(1000, 4000),
                'Category': 'Operating',
                'Subcategory': 'Software',
                'Type': 'Debit'
            })
    
    for date in dates:
        if np.random.random() > 0.7:
            transactions.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Description': 'Marketing',
                'Amount': -np.random.uniform(1000, 5000),
                'Category': 'Operating',
                'Subcategory': 'Marketing',
                'Type': 'Debit'
            })
    
    df = pd.DataFrame(transactions)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    df['Balance'] = 250000 + df['Amount'].cumsum()
    return df

def predict_runway(df):
    current_balance = df['Balance'].iloc[-1]
    monthly_expenses = df[df['Amount'] < 0].groupby(df[df['Amount'] < 0]['Date'].dt.to_period('M'))['Amount'].sum().abs()
    avg_monthly_burn = monthly_expenses.mean()
    monthly_revenue = df[df['Amount'] > 0].groupby(df[df['Amount'] > 0]['Date'].dt.to_period('M'))['Amount'].sum()
    avg_monthly_revenue = monthly_revenue.mean()
    net_monthly = avg_monthly_revenue - avg_monthly_burn
    runway_months = current_balance / abs(net_monthly) if net_monthly < 0 else float('inf')
    return {
        'current_balance': current_balance,
        'monthly_burn': avg_monthly_burn,
        'monthly_revenue': avg_monthly_revenue,
        'net_monthly': net_monthly,
        'runway_months': runway_months
    }

def main():
    df = generate_company_data()
    
    # Header
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.title("💰 Financial Dashboard")
    with col2:
        period = st.selectbox("Period", ["Last 30 Days", "Last 90 Days", "Last Year", "All Time"], index=2, key="period_select")
    with col3:
        view = st.selectbox("View", ["Overview", "Detailed"], key="view_select")
    
    # Calculate date filter
    if period == "Last 30 Days":
        start_date = df['Date'].max() - timedelta(days=30)
    elif period == "Last 90 Days":
        start_date = df['Date'].max() - timedelta(days=90)
    elif period == "Last Year":
        start_date = df['Date'].max() - timedelta(days=365)
    else:
        start_date = df['Date'].min()
    
    filtered_df = df[df['Date'] >= start_date]
    
    # Key Metrics
    total_revenue = filtered_df[filtered_df['Amount'] > 0]['Amount'].sum()
    total_expenses = filtered_df[filtered_df['Amount'] < 0]['Amount'].sum()
    net_income = total_revenue + total_expenses
    current_balance = filtered_df['Balance'].iloc[-1]
    runway = predict_runway(filtered_df)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Top metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Balance", f"${current_balance:,.0f}", delta=f"${net_income:,.0f}")
    with col2:
        st.metric("Revenue", f"${total_revenue:,.0f}", delta="12.5%")
    with col3:
        st.metric("Expenses", f"${abs(total_expenses):,.0f}", delta="-8.2%", delta_color="inverse")
    with col4:
        profit_margin = (net_income / total_revenue * 100) if total_revenue > 0 else 0
        st.metric("Profit Margin", f"{profit_margin:.1f}%", delta="2.3%")
    with col5:
        if runway['runway_months'] == float('inf'):
            st.metric("Runway", "∞", delta="Positive")
        else:
            st.metric("Runway", f"{runway['runway_months']:.0f}mo", delta="3mo")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Balance trend
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color: white; margin-bottom: 20px;'>Balance Trend</h3>", unsafe_allow_html=True)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=filtered_df['Date'],
            y=filtered_df['Balance'],
            mode='lines',
            name='Balance',
            line=dict(color='#667eea', width=3),
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.1)'
        ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(showgrid=False, color='#a0a0b0'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='#a0a0b0'),
            hovermode='x unified',
            margin=dict(l=0, r=0, t=0, b=0),
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Cash flow
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color: white; margin-bottom: 20px;'>Monthly Cash Flow</h3>", unsafe_allow_html=True)
        
        monthly_data = filtered_df.copy()
        monthly_data['Month'] = monthly_data['Date'].dt.to_period('M')
        monthly_revenue = monthly_data[monthly_data['Amount'] > 0].groupby('Month')['Amount'].sum()
        monthly_expenses = monthly_data[monthly_data['Amount'] < 0].groupby('Month')['Amount'].sum().abs()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Revenue',
            x=monthly_revenue.index.astype(str),
            y=monthly_revenue.values,
            marker_color='#10b981',
            marker_line_color='#10b981',
            marker_line_width=1.5,
            opacity=0.9
        ))
        fig.add_trace(go.Bar(
            name='Expenses',
            x=monthly_expenses.index.astype(str),
            y=monthly_expenses.values,
            marker_color='#ef4444',
            marker_line_color='#ef4444',
            marker_line_width=1.5,
            opacity=0.9
        ))
        
        fig.update_layout(
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(showgrid=False, color='#a0a0b0'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='#a0a0b0'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=30, b=0),
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Expense breakdown
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color: white; margin-bottom: 20px;'>Expense Breakdown</h3>", unsafe_allow_html=True)
        
        expense_by_category = filtered_df[filtered_df['Amount'] < 0].groupby('Category')['Amount'].sum().abs()
        
        colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe']
        
        fig = go.Figure(data=[go.Pie(
            labels=expense_by_category.index,
            values=expense_by_category.values,
            hole=.6,
            marker=dict(colors=colors, line=dict(color='#1e1e2e', width=2)),
            textinfo='percent',
            textfont=dict(size=14, color='white'),
            hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=14),
            showlegend=True,
            legend=dict(
                orientation="v", 
                yanchor="middle", 
                y=0.5, 
                xanchor="left", 
                x=0,
                font=dict(color='white', size=13),
                bgcolor='rgba(0,0,0,0)'
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick stats
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color: white; margin-bottom: 20px;'>Quick Stats</h3>", unsafe_allow_html=True)
        
        payroll_total = filtered_df[filtered_df['Category'] == 'Payroll']['Amount'].sum()
        operating_total = filtered_df[filtered_df['Category'] == 'Operating']['Amount'].sum()
        
        st.metric("💼 Payroll", f"${abs(payroll_total):,.0f}", delta="-5.2%", delta_color="inverse")
        st.metric("⚙️ Operating", f"${abs(operating_total):,.0f}", delta="3.1%", delta_color="inverse")
        
        avg_transaction = filtered_df[filtered_df['Amount'] < 0]['Amount'].mean()
        st.metric("📊 Avg Transaction", f"${abs(avg_transaction):,.0f}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Bottom section - Recent transactions
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: white; margin-bottom: 20px;'>Recent Transactions</h3>", unsafe_allow_html=True)
    
    recent = filtered_df.tail(10).sort_values('Date', ascending=False)
    display_df = recent[['Date', 'Description', 'Category', 'Amount']].copy()
    display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
    display_df['Amount'] = display_df['Amount'].apply(lambda x: f"${x:,.2f}")
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=300
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
