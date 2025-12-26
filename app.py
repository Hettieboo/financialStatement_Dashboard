import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Humanitarian Projects Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with modern design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    .hero-header {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
        backdrop-filter: blur(20px);
        padding: 3rem 2rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: #64748b;
        margin: 0.5rem 0 0 0;
        font-weight: 500;
    }
    
    .hero-date {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 1rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .metric-card-premium {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card-premium::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-value {
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0.5rem 0;
        line-height: 1;
    }
    
    .metric-delta {
        font-size: 0.95rem;
        font-weight: 600;
        opacity: 0.95;
    }
    
    .metric-icon {
        position: absolute;
        top: 1.5rem;
        right: 1.5rem;
        font-size: 2.5rem;
        opacity: 0.2;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    }
    
    .success-card {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }
    
    .danger-card {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    }
    
    .info-card {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    }
    
    .task-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        border-left: 4px solid #ef4444;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .task-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }
    
    .task-card.critical {
        border-left-color: #ef4444;
        background: linear-gradient(90deg, #fef2f2 0%, white 100%);
    }
    
    .task-card.warning {
        border-left-color: #f59e0b;
        background: linear-gradient(90deg, #fffbeb 0%, white 100%);
    }
    
    .task-card.ontrack {
        border-left-color: #10b981;
        background: linear-gradient(90deg, #f0fdf4 0%, white 100%);
    }
    
    .badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge-critical {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #991b1b;
    }
    
    .badge-warning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #92400e;
    }
    
    .badge-success {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        color: #065f46;
    }
    
    .chart-container {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
    }
    
    .chart-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .insight-title {
        font-size: 0.85rem;
        font-weight: 700;
        color: #667eea;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .insight-value {
        font-size: 1.5rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 0.3rem;
    }
    
    .insight-text {
        font-size: 0.8rem;
        color: #64748b;
        line-height: 1.4;
    }
    
    .sidebar .stSelectbox, .sidebar .stMultiselect {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.9) 100%);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #1e293b;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Generate enhanced sample data
@st.cache_data
def load_data():
    countries = ['Ethiopia', 'Yemen', 'Syria', 'Afghanistan', 'South Sudan', 
                 'Somalia', 'Myanmar', 'Venezuela', 'Haiti', 'All']
    
    partners = [
        'Global Relief Foundation',
        'International Aid Alliance',
        'Community Development Trust',
        'Emergency Response Network',
        'Sustainable Futures Initiative'
    ]
    
    partner_payments = pd.DataFrame({
        'Partner': partners,
        'Completed': [550000, 420000, 380000, 295000, 245000],
        'Pending': [95000, 75000, 58000, 45000, 38000]
    })
    
    quarters_data = []
    cumulative = 0
    for year in [2022, 2023, 2024, 2025]:
        for q in range(1, 5):
            if year == 2025 and q > 1:
                break
            if year == 2024 and q >= 3:
                quarterly = np.random.randint(18, 25)
            else:
                quarterly = np.random.randint(4, 12)
            cumulative += quarterly
            quarters_data.append({
                'Year': year,
                'Quarter': f'Q{q}',
                'Quarterly_Completed': quarterly,
                'Year_Quarter': f'{year}\nQ{q}',
                'Cumulative_Completed': cumulative
            })
    
    completion_by_quarter = pd.DataFrame(quarters_data)
    
    cost_data = []
    years = [2022, 2023, 2024, 2025]
    for partner in partners[:3]:
        base = np.random.randint(15000, 20000)
        for idx, year in enumerate(years):
            multiplier = [1.0, 1.3, 2.0, 1.5][idx]
            cost_data.append({
                'Partner': partner,
                'Year': year,
                'Cost': base * multiplier + np.random.randint(-2000, 2000)
            })
    
    contractual_costs = pd.DataFrame(cost_data)
    
    urgent_tasks = pd.DataFrame({
        'Task': [
            'Budget Revision Approval',
            'Field Assessment Completion',
            'Beneficiary Registration Update',
            'Quarterly Report Submission',
            'Partner Agreement Renewal'
        ],
        'Overdue_Days': [15, 12, 8, 5, 2],
        'Priority': ['Critical', 'Critical', 'Warning', 'Warning', 'On Track'],
        'Owner': ['Finance Team', 'Field Operations', 'Program Team', 'M&E Unit', 'Partnerships']
    })
    
    return (countries, partner_payments, completion_by_quarter, 
            contractual_costs, urgent_tasks)

(countries, partner_payments, completion_by_quarter, 
 contractual_costs, urgent_tasks) = load_data()

# Calculate metrics
total_contract_value = partner_payments['Completed'].sum() + partner_payments['Pending'].sum()
completion_rate = 82.5
completed_payments = partner_payments['Completed'].sum()
pending_payments = partner_payments['Pending'].sum()
total_projects = int(completion_by_quarter['Cumulative_Completed'].iloc[-1])
active_projects = 38

# Sidebar
with st.sidebar:
    st.markdown("### 🎛️ Dashboard Controls")
    st.markdown("---")
    
    selected_country = st.selectbox(
        "🌍 Select Region",
        options=countries,
        index=len(countries)-1
    )
    
    st.markdown("---")
    st.markdown("### 📊 Project Phases")
    
    phases = {
        "01 Inception": st.checkbox("01 Inception", value=True),
        "02 Planning": st.checkbox("02 Planning", value=True),
        "03 Implementation": st.checkbox("03 Implementation", value=True),
        "04 Completed": st.checkbox("04 Completed", value=True),
        "05 Closed": st.checkbox("05 Closed", value=False)
    }
    
    st.markdown("---")
    st.markdown("### 📅 Date Range")
    date_range = st.date_input(
        "Select Period",
        value=(datetime(2024, 1, 1), datetime.now()),
        max_value=datetime.now()
    )
    
    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")
    
    if st.button("📥 Export Dashboard"):
        st.success("✅ Dashboard exported!")
    
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.success("✅ Data refreshed!")
    
    if st.button("📊 Generate Report"):
        st.success("✅ Report generated!")
    
    st.markdown("---")
    st.markdown("### 📈 Quick Stats")
    st.info(f"**Total Projects:** {total_projects}")
    st.info(f"**Active Projects:** {active_projects}")
    st.info(f"**Completion Rate:** {completion_rate}%")

# Hero Header
st.markdown(f"""
<div class="hero-header">
    <h1 class="hero-title">🌍 Humanitarian Projects Command Center</h1>
    <p class="hero-subtitle">Real-time monitoring and analytics for global humanitarian operations</p>
    <div class="hero-date">📅 Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
</div>
""", unsafe_allow_html=True)

# Top Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card-premium info-card">
        <div class="metric-icon">💰</div>
        <div class="metric-label">Total Budget</div>
        <div class="metric-value">${total_contract_value/1000000:.2f}M</div>
        <div class="metric-delta">↑ 12.5% from last quarter</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card-premium success-card">
        <div class="metric-icon">✅</div>
        <div class="metric-label">Completion Rate</div>
        <div class="metric-value">{completion_rate}%</div>
        <div class="metric-delta">↑ 5.2% improvement</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card-premium warning-card">
        <div class="metric-icon">⏱️</div>
        <div class="metric-label">Active Projects</div>
        <div class="metric-value">{active_projects}</div>
        <div class="metric-delta">8 projects in final phase</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    critical_tasks = len(urgent_tasks[urgent_tasks['Priority'] == 'Critical'])
    st.markdown(f"""
    <div class="metric-card-premium danger-card">
        <div class="metric-icon">🚨</div>
        <div class="metric-label">Urgent Items</div>
        <div class="metric-value">{critical_tasks}</div>
        <div class="metric-delta">Requires immediate action</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Content Grid
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">💼 Implementing Partner Payment Status</div>', unsafe_allow_html=True)
    
    fig_partners = go.Figure()
    
    fig_partners.add_trace(go.Bar(
        name='Completed',
        y=partner_payments['Partner'],
        x=partner_payments['Completed'],
        orientation='h',
        marker=dict(
            color='#667eea',
            line=dict(color='#764ba2', width=2)
        ),
        text=partner_payments['Completed'].apply(lambda x: f'${x/1000:.0f}K'),
        textposition='inside',
        textfont=dict(color='white', size=12, family='Inter'),
        hovertemplate='<b>%{y}</b><br>Completed: $%{x:,.0f}<extra></extra>'
    ))
    
    fig_partners.add_trace(go.Bar(
        name='Pending',
        y=partner_payments['Partner'],
        x=partner_payments['Pending'],
        orientation='h',
        marker=dict(
            color='#ef4444',
            line=dict(color='#dc2626', width=2)
        ),
        text=partner_payments['Pending'].apply(lambda x: f'${x/1000:.0f}K'),
        textposition='inside',
        textfont=dict(color='white', size=12, family='Inter'),
        hovertemplate='<b>%{y}</b><br>Pending: $%{x:,.0f}<extra></extra>'
    ))
    
    fig_partners.update_layout(
        barmode='stack',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=12, color='#1e293b'),
        xaxis=dict(
            title='Payment Amount (USD)',
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            zeroline=False
        ),
        yaxis=dict(
            title='',
            showgrid=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(0,0,0,0.1)',
            borderwidth=1
        ),
        margin=dict(l=20, r=20, t=60, b=60)
    )
    
    st.plotly_chart(fig_partners, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">🚨 Urgent Tasks</div>', unsafe_allow_html=True)
    
    for idx, row in urgent_tasks.iterrows():
        priority_class = row['Priority'].lower().replace(' ', '')
        if row['Priority'] == 'Critical':
            badge_class = 'badge-critical'
            card_class = 'critical'
        elif row['Priority'] == 'Warning':
            badge_class = 'badge-warning'
            card_class = 'warning'
        else:
            badge_class = 'badge-success'
            card_class = 'ontrack'
        
        st.markdown(f"""
        <div class="task-card {card_class}">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
                <strong style="font-size: 0.95rem; color: #1e293b; flex: 1;">{row['Task']}</strong>
                <span class="badge {badge_class}">{row['Priority']}</span>
            </div>
            <div style="color: #64748b; font-size: 0.8rem; margin-bottom: 0.3rem;">
                👤 {row['Owner']}
            </div>
            <div style="color: #ef4444; font-size: 0.85rem; font-weight: 600;">
                ⏰ {row['Overdue_Days']} days overdue
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Second Row Charts
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📈 Project Completion Trend</div>', unsafe_allow_html=True)
    
    fig_completion = go.Figure()
    
    fig_completion.add_trace(go.Bar(
        name='Quarterly',
        x=completion_by_quarter['Year_Quarter'],
        y=completion_by_quarter['Quarterly_Completed'],
        marker=dict(
            color='#667eea',
            line=dict(color='#764ba2', width=1)
        ),
        text=completion_by_quarter['Quarterly_Completed'],
        textposition='outside',
        textfont=dict(size=11, family='Inter'),
        hovertemplate='<b>%{x}</b><br>Completed: %{y}<extra></extra>'
    ))
    
    fig_completion.add_trace(go.Scatter(
        name='Cumulative',
        x=completion_by_quarter['Year_Quarter'],
        y=completion_by_quarter['Cumulative_Completed'],
        mode='lines+markers',
        line=dict(color='#ef4444', width=3),
        marker=dict(size=8, color='#ef4444', line=dict(color='white', width=2)),
        yaxis='y2',
        hovertemplate='<b>%{x}</b><br>Total: %{y}<extra></extra>'
    ))
    
    fig_completion.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=12, color='#1e293b'),
        xaxis=dict(
            title='',
            showgrid=False,
            tickangle=-45
        ),
        yaxis=dict(
            title='Quarterly Projects',
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            zeroline=False
        ),
        yaxis2=dict(
            title='Cumulative Total',
            overlaying='y',
            side='right',
            showgrid=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(0,0,0,0.1)',
            borderwidth=1
        ),
        margin=dict(l=20, r=20, t=60, b=100)
    )
    
    st.plotly_chart(fig_completion, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">💵 Budget Allocation by Partner</div>', unsafe_allow_html=True)
    
    fig_costs = go.Figure()
    
    colors = ['#667eea', '#ef4444', '#10b981']
    for idx, partner in enumerate(contractual_costs['Partner'].unique()):
        partner_data = contractual_costs[contractual_costs['Partner'] == partner]
        fig_costs.add_trace(go.Scatter(
            name=partner,
            x=partner_data['Year'],
            y=partner_data['Cost'],
            mode='lines+markers',
            line=dict(width=3, color=colors[idx % len(colors)]),
            marker=dict(size=10, line=dict(color='white', width=2)),
            hovertemplate='<b>%{fullData.name}</b><br>Year: %{x}<br>Cost: $%{y:,.0f}<extra></extra>'
        ))
    
    fig_costs.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=12, color='#1e293b'),
        xaxis=dict(
            title='Year',
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            dtick=1
        ),
        yaxis=dict(
            title='Budget Allocation (USD)',
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            zeroline=False
        ),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.98,
            xanchor="right",
            x=0.98,
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='rgba(0,0,0,0.1)',
            borderwidth=1
        ),
        margin=dict(l=20, r=20, t=40, b=60),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_costs, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Payment Distribution Pie Chart
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">💰 Payment Distribution Overview</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Completed Payments', 'Pending Payments'],
        values=[completed_payments, pending_payments],
        hole=0.6,
        marker=dict(
            colors=['#667eea', '#ef4444'],
            line=dict(color='white', width=3)
        ),
        textinfo='label+percent',
        textposition='outside',
        textfont=dict(size=13, family='Inter', color='#1e293b'),
        hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>'
    )])
    
    fig_pie.update_layout(
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=12, color='#1e293b'),
        annotations=[dict(
            text=f'${(completed_payments + pending_payments)/1000000:.2f}M',
            x=0.5, y=0.5,
            font_size=28,
            showarrow=False,
            font=dict(family='Inter', weight=700, color='#1e293b')
        )],
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    fig_bar_comparison = go.Figure()
    
    partners_top = partner_payments.nlargest(5, 'Completed')
    
    fig_bar_comparison.add_trace(go.Bar(
        y=partners_top['Partner'],
        x=partners_top['Completed'],
        orientation='h',
