# Humanitarian Projects Dashboard 🌍

A comprehensive, interactive dashboard for monitoring humanitarian projects, implementing partner payments, project completion rates, and budget allocations. Built with Streamlit and designed to provide real-time insights for program managers and stakeholders.

![Dashboard Status](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red)

## Overview

This dashboard provides a centralized view of humanitarian project operations, including:
- Project completion tracking across quarters and years
- Implementing partner payment status
- Budget allocation monitoring
- Urgent task management
- Geographic distribution of projects
- Real-time KPI metrics

## Features

### 📊 Core Metrics
- **Completion Rate** - Visual gauge showing overall project completion percentage
- **Total Budget** - Aggregate contract value across all projects
- **Payment Status** - Completed vs. pending payments visualization
- **Urgent Tasks Tracker** - Priority-coded list of overdue activities

### 📈 Interactive Visualizations

1. **Implementing Partner Payment Status**
   - Horizontal stacked bar chart
   - Shows completed and pending payments by partner
   - Real-time financial tracking

2. **Project Completion by Year & Quarter**
   - Dual visualization: quarterly bars + cumulative trend line
   - Historical performance tracking
   - Trend analysis across multiple years

3. **Budget Allocation by Partner and Year**
   - Multi-line chart showing spending patterns
   - Partner-wise budget comparison
   - Year-over-year analysis

### 🎯 Filtering & Controls
- **Country/Region Selector** - Filter projects by geographic location
- **Project Phase Checkboxes** - Filter by project lifecycle stage:
  - 01 Inception
  - 02 Planning
  - 03 Implementation
  - 04 Completed
  - 05 Closed
- **Export Options** - Generate reports in multiple formats
- **Refresh Function** - Update data in real-time

### 🚨 Priority Management
- **Critical** - High-priority overdue tasks (red badge)
- **Warning** - Medium-priority items requiring attention (yellow badge)
- **On Track** - Tasks progressing normally (green badge)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the repository:**
```bash
git clone <repository-url>
cd humanitarian-projects-dashboard
```

2. **Install required dependencies:**
```bash
pip install -r requirements.txt
```

Or install packages individually:
```bash
pip install streamlit pandas plotly numpy
```

3. **Run the dashboard:**
```bash
streamlit run humanitarian_dashboard.py
```

4. **Access the dashboard:**
The application will automatically open in your browser at `http://localhost:8501`

## Project Structure

```
humanitarian-projects-dashboard/
│
├── humanitarian_dashboard.py    # Main application file
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── data/                        # (Optional) Data directory
    └── sample_data.csv          # Sample datasets
```

## Usage Guide

### Navigation

**Sidebar Controls:**
- Select country/region from dropdown
- Filter by project phase using checkboxes
- Export reports or refresh data using action buttons

**Main Dashboard:**
- View key metrics in the top row
- Analyze partner payments in the middle section
- Review completion trends and budget allocations below
- Monitor urgent tasks requiring immediate attention

### Understanding the Metrics

**Completion Rate (80%)**
- Percentage of projects completed vs. total projects
- Visual gauge indicator with color coding:
  - Red (0-50%): Below target
  - Yellow (50-75%): Approaching target
  - Green (75-100%): Meeting/exceeding target

**Payment Status**
- Blue: Completed payments
- Red: Pending payments
- Helps track financial obligations and cash flow

**Urgent Tasks**
- Lists overdue activities with priority levels
- Shows number of days overdue
- Enables proactive project management

## Sample Data

The dashboard uses realistic synthetic data including:

**Countries/Regions:**
- Ethiopia, Yemen, Syria, Afghanistan
- South Sudan, Somalia, Myanmar
- Venezuela, Haiti

**Implementing Partners:**
- Global Relief Foundation
- International Aid Alliance
- Community Development Trust
- Emergency Response Network
- Sustainable Futures Initiative

**Data Ranges:**
- Time period: 2022-2025 (quarterly data)
- Budget range: $15K - $45K per project
- Payment status: ~80% completion rate
- Urgent tasks: 5 active items with varying priorities

## Customization

### Adding Real Data

Replace the `load_data()` function with your data source:

```python
@st.cache_data
def load_data():
    # Option 1: Load from CSV
    partner_payments = pd.read_csv('data/partner_payments.csv')
    
    # Option 2: Connect to database
    import sqlalchemy
    engine = sqlalchemy.create_engine('your_database_url')
    partner_payments = pd.read_sql('SELECT * FROM payments', engine)
    
    # Option 3: API integration
    import requests
    response = requests.get('your_api_endpoint')
    partner_payments = pd.DataFrame(response.json())
    
    return partner_payments, other_data...
```

### Modifying Visualizations

Customize chart colors, layouts, or styles:

```python
# Example: Change color scheme
fig.update_layout(
    colorway=['#your_color1', '#your_color2'],
    template='plotly_white'  # or 'plotly_dark'
)

# Example: Adjust chart height
fig.update_layout(height=500)
```

### Branding

Update the header gradient and colors in the CSS section:

```python
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #your_color1 0%, #your_color2 100%);
    }
</style>
""", unsafe_allow_html=True)
```

## Data Requirements

If connecting to your own data source, ensure the following structure:

**Partner Payments:**
```
Partner | Completed | Pending
--------|-----------|--------
Org A   | 450000    | 85000
```

**Project Completion:**
```
Year | Quarter | Quarterly_Completed | Cumulative_Completed
-----|---------|-------------------|--------------------
2024 | Q1      | 10                | 45
```

**Budget Allocation:**
```
Partner | Year | Cost
--------|------|------
Org A   | 2024 | 25000
```

**Urgent Tasks:**
```
Task              | Overdue_Days | Priority
------------------|--------------|----------
Project Approval  | 12           | Critical
```

## Technical Details

### Performance Optimization
- Data caching with `@st.cache_data` decorator
- Efficient data aggregation using pandas
- Optimized Plotly rendering

### Browser Compatibility
- Chrome (recommended)
- Firefox
- Safari
- Microsoft Edge

### Responsive Design
- Adapts to different screen sizes
- Mobile-friendly layout
- Touch-optimized controls

## Troubleshooting

**Issue: Dashboard won't start**
```bash
# Solution: Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**Issue: Charts not displaying**
```bash
# Solution: Clear Streamlit cache
streamlit cache clear
```

**Issue: Slow performance**
- Reduce data range in filters
- Check data volume in `load_data()` function
- Ensure caching is enabled

## Future Enhancements

Planned features for upcoming versions:
- [ ] Real-time data integration with APIs
- [ ] Advanced filtering (date ranges, budget thresholds)
- [ ] PDF/Excel export functionality
- [ ] Email alerts for urgent tasks
- [ ] Multi-language support
- [ ] Role-based access control
- [ ] Custom report builder
- [ ] Mobile app version

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

For questions, issues, or feature requests:
- Open an issue in the repository
- Email: [your-email@example.com]
- Documentation: [link to docs]

## License

This project is available for demonstration and educational purposes. 

For commercial use, please contact the repository owner.

## Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - Interactive web framework
- [Plotly](https://plotly.com/) - Interactive visualizations
- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [NumPy](https://numpy.org/) - Numerical computing

## Changelog

### Version 1.0.0 (Current)
- Initial release
- Core dashboard functionality
- 5 implementing partners
- 9 countries/regions
- Quarterly completion tracking
- Budget allocation monitoring
- Urgent task management

---

**Dashboard Design Inspired By:** IRFF Diagnostic Reports Dashboard

**Created For:** Humanitarian project monitoring and management

**Last Updated:** December 2024

---

## Screenshots

### Main Dashboard View
*Completion rate gauge, budget metrics, and payment status at a glance*

### Partner Payment Analysis
*Detailed breakdown of completed vs pending payments by implementing partner*

### Completion Trends
*Quarterly and cumulative project completion over multiple years*

### Budget Tracking
*Year-over-year budget allocation trends by partner organization*

---

For more information or to report issues, please visit the project repository.
