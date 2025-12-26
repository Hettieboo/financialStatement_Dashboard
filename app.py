import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# ----------------------
# Page configuration
# ----------------------
st.set_page_config(
    page_title="Humanitarian Projects Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------
# Custom CSS
# ----------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
.glass-card { background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); border-radius: 20px; padding: 2rem; box-shadow: 0 8px 32px rgba(0,0,0,0.1); border: 1px solid rgba(255,255,255,0.18); margin-bottom: 1.5rem; }
.glass-card:hover { transform: translateY(-2px); box-shadow: 0 12px 40px rgba(0,0,0,0.15); }
.hero-header { background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%); backdrop-filter: blur(20px); padding: 3rem 2rem; border-radius: 24px; margin-bottom: 2rem; box-shadow: 0 20px 60px rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,0.3); }
.hero-title { font-size: 3rem; font-weight: 800; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; letter-spacing: -1px; }
.hero-subtitle { font-size: 1.2rem; color: #64748b; margin: 0.5rem 0 0 0; font-weight: 500; }
.hero-date { display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 0.5rem 1.5rem; border-radius: 50px; font-size: 0.9rem; font-weight: 600; margin-top: 1rem; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); }
.metric-card-premium { padding: 2rem; border-radius: 20px; color: white; height: 100%; position: relative; overflow: hidden; margin-bottom: 1rem; }
.metric-label { font-size: 0.9rem; opacity: 0.9; font-weight: 500; text-transform: uppercase; letter-spacing: 1px; }
.metric-value { font-size: 2.8rem; font-weight: 800; margin: 0.5rem 0; line-height: 1; }
.metric-delta { font-size: 0.95rem; font-weight: 600; opacity: 0.95; }
.metric-icon { position: absolute; top: 1.5rem; right: 1.5rem; font-size: 2.5rem; opacity: 0.2; }
.task-card { background: white; border-radius: 12px; padding: 1rem; margin-bottom: 0.8rem; border-left: 4px solid #ef4444; box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: all 0.3s ease; }
.task-card:hover { transform: translateX(5px); box-shadow: 0 4px 12px rgba(0,0,0,0.12); }
.task-card.critical { border-left-color: #ef4444; background: linear-gradient(90deg, #fef2f2 0%, white 100%); }
.task-card.warning { border-left-color: #f59e0b; background: linear-gradient(90deg, #fffbeb 0%, white 100%); }
.task-card.ontrack { border-left-color: #10b981; background: linear-gradient(90deg, #f0fdf4 0%, white 100%); }
.badge { display: inline-block; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
.badge-critical { background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); color: #991b1b; }
.badge-warning { background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); color: #92400e; }
.badge-success { background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); color: #065f46; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ----------------------
# Sample Data
# ----------------------
@st.cache_data
def load_data():
    countries = ['Ethiopia','Yemen','Syria','Afghanistan','South Sudan','Somalia','Myanmar','Venezuela','Haiti','All']
    partners = ['Global Relief Foundation','International Aid Alliance','Community Development Trust','Emergency Response Network','Sustainable Futures Initiative']
    
    partner_payments = pd.DataFrame({'Partner': partners,
                                     'Completed':[550000,420000,380000,295000,245000],
                                     'Pending':[95000,75000,58000,45000,38000]})
    
    quarters_data=[]
    cumulative=0
    for year in [2022,2023,2024,2025]:
        for q in range(1,5):
            if year==2025 and q>1: break
            quarterly=np.random.randint(4,25)
            cumulative+=quarterly
            quarters_data.append({'Year':year,'Quarter':f'Q{q}','Quarterly_Completed':quarterly,
                                  'Year_Quarter':f'{year}\nQ{q}','Cumulative_Completed':cumulative})
    completion_by_quarter=pd.DataFrame(quarters_data)
    
    cost_data=[]
    years=[2022,2023,2024,2025]
    for partner in partners[:3]:
        base=np.random.randint(15000,20000)
        for idx,year in enumerate(years):
            multiplier=[1.0,1.3,2.0,1.5][idx]
            cost_data.append({'Partner':partner,'Year':year,'Cost':base*multiplier+np.random.randint(-2000,2000)})
    contractual_costs=pd.DataFrame(cost_data)
    
    urgent_tasks=pd.DataFrame({'Task':['Budget Revision Approval','Field Assessment Completion','Beneficiary Registration Update','Quarterly Report Submission','Partner Agreement Renewal'],
                               'Overdue_Days':[15,12,8,5,2],
                               'Priority':['Critical','Critical','Warning','Warning','On Track'],
                               'Owner':['Finance Team','Field Operations','Program Team','M&E Unit','Partnerships']})
    
    return countries, partner_payments, completion_by_quarter, contractual_costs, urgent_tasks

(countries, partner_payments, completion_by_quarter, contractual_costs, urgent_tasks)=load_data()

# Map Data
map_data=pd.DataFrame({'Country':['Ethiopia','Yemen','Syria','Afghanistan','South Sudan','Somalia','Myanmar','Venezuela','Haiti'],
                       'Completed_Payments':np.random.randint(200000,600000,9),
                       'Pending_Payments':np.random.randint(50000,150000,9)})
map_data['Total_Payments']=map_data['Completed_Payments']+map_data['Pending_Payments']

# Metrics
total_contract_value=partner_payments['Completed'].sum()+partner_payments['Pending'].sum()
completion_rate=82.5
completed_payments=partner_payments['Completed'].sum()
pending_payments=partner_payments['Pending'].sum()
total_projects=int(completion_by_quarter['Cumulative_Completed'].iloc[-1])
active_projects=38
critical_tasks=len(urgent_tasks[urgent_tasks['Priority']=='Critical'])

# ----------------------
# Sidebar
# ----------------------
with st.sidebar:
    st.markdown("### 🎛️ Dashboard Controls")
    selected_country=st.selectbox("🌍 Select Region", options=countries, index=len(countries)-1)
    st.markdown("### 📊 Project Phases")
    phases={f"{i:02} {phase}": st.checkbox(f"{i:02} {phase}",value=True) for i,phase in enumerate(["Inception","Planning","Implementation","Completed","Closed"],1)}
    date_range=st.date_input("📅 Date Range", value=(datetime(2024,1,1),datetime.now()), max_value=datetime.now())
    st.markdown("### ⚡ Quick Actions")
    if st.button("📥 Export Dashboard"): st.success("✅ Dashboard exported!")
    if st.button("🔄 Refresh Data"): st.cache_data.clear(); st.success("✅ Data refreshed!")
    if st.button("📊 Generate Report"): st.success("✅ Report generated!")
    st.markdown("### 📈 Quick Stats")
    st.info(f"**Total Projects:** {total_projects}")
    st.info(f"**Active Projects:** {active_projects}")
    st.info(f"**Completion Rate:** {completion_rate}%")

# ----------------------
# Hero Header
# ----------------------
st.markdown(f"""
<div class="hero-header">
    <h1 class="hero-title">🌍 Humanitarian Projects Command Center</h1>
    <p class="hero-subtitle">Real-time monitoring and analytics for global humanitarian operations</p>
    <div class="hero-date">📅 Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
</div>
""", unsafe_allow_html=True)

# ----------------------
# Top Metrics
# ----------------------
cols = st.columns(4)
metrics = [
    ("💰 Total Budget", f"${total_contract_value/1000000:.2f}M", "↑ 12.5% from last quarter", "background:linear-gradient(135deg,#667eea 0%,#764ba2 100%)"),
    ("✅ Completion Rate", f"{completion_rate}%", "↑ 5.2% improvement", "background:linear-gradient(135deg,#10b981 0%,#059669 100%)"),
    ("⏱️ Active Projects", f"{active_projects}", "8 projects in final phase", "background:linear-gradient(135deg,#f59e0b 0%,#d97706 100%)"),
    ("🚨 Urgent Items", f"{critical_tasks}", "Requires immediate action", "background:linear-gradient(135deg,#ef4444 0%,#dc2626 100%)")
]
for col,(label,value,delta,style) in zip(cols,metrics):
    col.markdown(f"""
    <div class="metric-card-premium" style="{style}">
        <div class="metric-icon">{label.split()[0]}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-delta">{delta}</div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------
# Map
# ----------------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">🌍 Humanitarian Activity Map</div>', unsafe_allow_html=True)
fig_map = px.choropleth(
    map_data,
    locations="Country",
    locationmode="country names",
    color="Total_Payments",
    hover_name="Country",
    hover_data={"Completed_Payments":True,"Pending_Payments":True,"Total_Payments":True},
    color_continuous_scale="Blues"
)
fig_map.update_layout(margin=dict(l=10,r=10,t=50,b=10), height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      coloraxis_colorbar=dict(title="Total Payments (USD)"))
st.plotly_chart(fig_map,use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ----------------------
# Main Grid: Partner Payments & Urgent Tasks
# ----------------------
col1,col2 = st.columns([2,1])

# Partner Payments
with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">💼 Implementing Partner Payment Status</div>', unsafe_allow_html=True)
    fig_partners=go.Figure()
    fig_partners.add_trace(go.Bar(y=partner_payments['Partner'], x=partner_payments['Completed'], orientation='h',
                                  name='Completed', marker=dict(color='#667eea'), text=partner_payments['Completed'].apply(lambda x:f"${x/1000:.0f}K"), textposition='inside'))
    fig_partners.add_trace(go.Bar(y=partner_payments['Partner'], x=partner_payments['Pending'], orientation='h',
                                  name='Pending', marker=dict(color='#ef4444'), text=partner_payments['Pending'].apply(lambda x:f"${x/1000:.0f}K"), textposition='inside'))
    fig_partners.update_layout(barmode='stack', height=400)
    st.plotly_chart(fig_partners,use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Urgent Tasks
with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">🚨 Urgent Tasks</div>', unsafe_allow_html=True)
    for idx,row in urgent_tasks.iterrows():
        if row['Priority']=='Critical': cls='critical'; badge='badge-critical'
        elif row['Priority']=='Warning': cls='warning'; badge='badge-warning'
        else: cls='ontrack'; badge='badge-success'
        st.markdown(f"""
        <div class="task-card {cls}">
            <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:0.5rem;">
                <strong style="font-size:0.95rem;flex:1;">{row['Task']}</strong>
                <span class="badge {badge}">{row['Priority']}</span>
            </div>
            <div style="color:#64748b;font-size:0.8rem;margin-bottom:0.3rem;">👤 {row['Owner']}</div>
            <div style="color:#ef4444;font-size:0.85rem;font-weight:600;">⏰ {row['Overdue_Days']} days overdue</div>
        </div>
        """,unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------
# Completion Trend & Budget Allocation
# ----------------------
col1,col2 = st.columns(2)

# Completion Trend
with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📈 Project Completion Trend</div>', unsafe_allow_html=True)
    fig_completion=go.Figure()
    fig_completion.add_trace(go.Bar(x=completion_by_quarter['Year_Quarter'], y=completion_by_quarter['Quarterly_Completed'],
                                    name='Quarterly', marker=dict(color='#667eea')))
    fig_completion.add_trace(go.Scatter(x=completion_by_quarter['Year_Quarter'], y=completion_by_quarter['Cumulative_Completed'],
                                        name='Cumulative', mode='lines+markers', line=dict(color='#ef4444', width=3)))
    fig_completion.update_layout(height=400)
    st.plotly_chart(fig_completion,use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Budget Allocation
with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">💵 Budget Allocation by Partner</div>', unsafe_allow_html=True)
    fig_costs=go.Figure()
    colors=['#667eea','#ef4444','#10b981']
    for idx,partner in enumerate(contractual_costs['Partner'].unique()):
        partner_data=contractual_costs[contractual_costs['Partner']==partner]
        fig_costs.add_trace(go.Scatter(x=partner_data['Year'],y=partner_data['Cost'],mode='lines+markers',
                                       name=partner,line=dict(width=3,color=colors[idx%len(colors)])))
    fig_costs.update_layout(height=400)
    st.plotly_chart(fig_costs,use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------
# Payment Distribution Pie
# ----------------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">💰 Payment Distribution Overview</div>', unsafe_allow_html=True)
fig_pie=go.Figure(data=[go.Pie(labels=['Completed','Pending'],values=[completed_payments,pending_payments],hole=0.6)])
fig_pie.update_layout(height=350)
st.plotly_chart(fig_pie,use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
