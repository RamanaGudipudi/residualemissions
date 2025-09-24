import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots

# Set page config with dark theme
st.set_page_config(
    page_title="Dynamic Residual Emissions: Why Static 11% Thresholds Fail",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    /* Dark theme styling */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    .main .block-container {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #262730;
    }
    
    /* Metric styling */
    [data-testid="metric-container"] {
        background-color: #262730;
        border: 1px solid #464457;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #262730;
        color: #FAFAFA;
    }
    
    /* Success/Error/Warning boxes */
    .stAlert > div {
        background-color: #262730;
        border-left: 4px solid #00D4AA;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #FAFAFA;
    }
    
    /* Text */
    p, li, span {
        color: #FAFAFA;
    }
    
    /* DataFrame */
    .dataframe {
        background-color: #262730;
        color: #FAFAFA;
    }
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.title("🎯 Industry-Specific Residual Emissions: Why 11% Static Thresholds Fail")
st.markdown("""
**Demonstrating Research Frontier 4: Dynamic residual emissions based on RF2 industry pathways**

The previous RF2 analysis showed that industries face vastly different decarbonization challenges across 
sectors with costs ranging from $0-200/tCO2e. So how can all industries have the same 11% residual threshold?

*This analysis demonstrates why SBTi's static approach ignores the RF2 realities that determine 
actual maximum decarbonization potential, using real CDP data and climate science.*
""")

# Enhanced industry data focusing on Scope 3 heavy industries
residual_industry_data = {
    'Food, Beverage & Tobacco': {
        'scope3_percentage': 67,
        'cdp_sample_size': 162,
        'scope3_categories': ['C1: Agricultural inputs (40%)', 'C1: Packaging (20%)', 'C4+C9: Transport (15%)', 'C2: Processing (15%)', 'C13: Retail (10%)'],
        'rf2_complexity': {
            'agricultural_constraints': 'Methane from ruminants has biological floors',
            'seasonal_variation': 'Weather-dependent crop yields',
            'geographic_spread': 'Global supply chains across climate zones',
            'main_challenge': 'Farm-level methane emissions have biological floors that exceed 11% assumption'
        },
        'illustrative_scenarios': {
            'conservative_max_reduction': 75,  # 25% residual - biological constraints
            'ambitious_max_reduction': 85,    # 15% residual - with regenerative agriculture
            'breakthrough_max_reduction': 88,  # 12% residual - major technology breakthroughs
            'static_sbt_assumption': 89        # 11% residual - one size fits all
        },
        'why_static_fails': 'Agricultural biology creates higher residual floors than 11% - ruminant methane, soil N2O, and land use constraints',
        'key_interventions': [
            {'name': 'Regenerative agriculture', 'potential': '30-50%', 'timeline': '5-10 years', 'scalability': 'High'},
            {'name': 'Alternative proteins', 'potential': '60-80%', 'timeline': '10-15 years', 'scalability': 'Medium'},
            {'name': 'Precision fermentation', 'potential': '70-90%', 'timeline': '15-25 years', 'scalability': 'Low'},
            {'name': 'Packaging optimization', 'potential': '40-60%', 'timeline': '2-5 years', 'scalability': 'High'}
        ],
        'residual_drivers': ['Biological methane limits', 'Seasonal agricultural cycles', 'Land use constraints', 'Global supply chain logistics']
    },
    
    'Capital Goods': {
        'scope3_percentage': 90,
        'cdp_sample_size': 166,
        'scope3_categories': ['C11: Equipment use-phase (91%)', 'C1: Manufacturing (6%)', 'C2: Facilities (3%)'],
        'rf2_complexity': {
            'use_phase_duration': '20-30 years',
            'customer_behavior_control': 'None - equipment sold to independent operators',
            'technology_evolution': 'Varies by end-use sector (buildings vs transport vs industry)',
            'main_challenge': 'Cannot control decades of customer equipment use across multiple end-use sectors'
        },
        'illustrative_scenarios': {
            'conservative_max_reduction': 92,  # 8% residual - efficiency improvements
            'ambitious_max_reduction': 95,    # 5% residual - breakthrough efficiency + electrification
            'breakthrough_max_reduction': 97,  # 3% residual - full sector transformation
            'static_sbt_assumption': 89        # 11% residual
        },
        'why_static_fails': 'Use-phase optimization potential varies dramatically by end-use sector - buildings can electrify, heavy industry cannot',
        'key_interventions': [
            {'name': 'Equipment efficiency', 'potential': '20-40%', 'timeline': '2-5 years', 'scalability': 'High'},
            {'name': 'Smart controls/IoT', 'potential': '15-30%', 'timeline': '3-7 years', 'scalability': 'High'},
            {'name': 'Electrification-ready design', 'potential': '50-80%', 'timeline': '5-15 years', 'scalability': 'Medium'},
            {'name': 'Circular design', 'potential': '30-50%', 'timeline': '10-20 years', 'scalability': 'Medium'}
        ],
        'residual_drivers': ['Heavy industrial process heat requirements', 'Long equipment lifespans', 'Customer behavior variability', 'End-use sector constraints']
    },
    
    'Consumer Goods': {
        'scope3_percentage': 85,
        'cdp_sample_size': 120,
        'scope3_categories': ['C1: Raw materials (45%)', 'C1: Packaging (25%)', 'C11: Consumer use (15%)', 'C4+C9: Transport (10%)', 'C12: End-of-life (5%)'],
        'rf2_complexity': {
            'supply_chain_complexity': 'Global sourcing across multiple material categories',
            'consumer_behavior': 'Unpredictable use patterns and disposal habits',
            'packaging_constraints': 'Food safety and shelf-life requirements limit alternatives',
            'main_challenge': 'Depends on consumer behavior and global supply chain transformation'
        },
        'illustrative_scenarios': {
            'conservative_max_reduction': 78,  # 22% residual - incremental improvements
            'ambitious_max_reduction': 82,    # 18% residual - circular economy adoption
            'breakthrough_max_reduction': 85,  # 15% residual - full system transformation
            'static_sbt_assumption': 89        # 11% residual
        },
        'why_static_fails': 'Consumer behavior and packaging requirements create constraints that vary by product category',
        'key_interventions': [
            {'name': 'Sustainable packaging', 'potential': '40-60%', 'timeline': '3-8 years', 'scalability': 'High'},
            {'name': 'Circular business models', 'potential': '50-70%', 'timeline': '5-15 years', 'scalability': 'Medium'},
            {'name': 'Alternative materials', 'potential': '30-80%', 'timeline': '10-20 years', 'scalability': 'Variable'},
            {'name': 'Consumer education', 'potential': '20-40%', 'timeline': '5-10 years', 'scalability': 'Medium'}
        ],
        'residual_drivers': ['Food safety packaging requirements', 'Consumer behavior patterns', 'Material availability constraints', 'Regional waste infrastructure']
    },
    
    'Financial Services': {
        'scope3_percentage': 99.98,
        'cdp_sample_size': 377,
        'scope3_categories': ['C15: Financed emissions (99%)', 'C13: Real estate (0.8%)', 'Other (0.2%)'],
        'rf2_complexity': {
            'portfolio_diversity': 'Investments span ALL sectors with different decarbonization potentials',
            'indirect_control': 'Influence through capital allocation, not direct operational control',
            'sectoral_variation': 'Steel can reach 5% residuals, agriculture may need 25%',
            'main_challenge': 'Residual emissions depend entirely on portfolio company sector mix and their maximum potentials'
        },
        'illustrative_scenarios': {
            'conservative_max_reduction': 70,  # 30% residual - current portfolio mix
            'ambitious_max_reduction': 80,    # 20% residual - shift to lower-carbon sectors
            'breakthrough_max_reduction': 85,  # 15% residual - full portfolio optimization
            'static_sbt_assumption': 89        # 11% residual
        },
        'why_static_fails': 'Portfolio emissions reflect weighted average of ALL sectors - static 11% ignores sectoral variation',
        'key_interventions': [
            {'name': 'Portfolio decarbonization', 'potential': '40-70%', 'timeline': '5-15 years', 'scalability': 'High'},
            {'name': 'Green finance products', 'potential': '20-50%', 'timeline': '2-8 years', 'scalability': 'High'},
            {'name': 'Engagement programs', 'potential': '30-60%', 'timeline': '3-10 years', 'scalability': 'Medium'},
            {'name': 'Sector-specific strategies', 'potential': '50-80%', 'timeline': '10-25 years', 'scalability': 'Medium'}
        ],
        'residual_drivers': ['Sectoral portfolio composition', 'Client decarbonization rates', 'Regulatory constraints', 'Market transformation speeds']
    },
    
    'Retail': {
        'scope3_percentage': 95,
        'cdp_sample_size': 80,
        'scope3_categories': ['C1: Purchased goods (70%)', 'C11: Customer use (15%)', 'C4+C9: Transport (10%)', 'C13: Leased stores (3%)', 'Other (2%)'],
        'rf2_complexity': {
            'product_diversity': 'Thousands of SKUs across multiple product categories',
            'supplier_control': 'Limited direct control over manufacturing processes',
            'customer_influence': 'Can guide but not control customer choices',
            'main_challenge': 'Success depends on supplier decarbonization and customer behavior change'
        },
        'illustrative_scenarios': {
            'conservative_max_reduction': 80,  # 20% residual - supplier engagement only
            'ambitious_max_reduction': 85,    # 15% residual - comprehensive supplier programs
            'breakthrough_max_reduction': 88,  # 12% residual - full value chain transformation
            'static_sbt_assumption': 89        # 11% residual
        },
        'why_static_fails': 'Retailer residuals depend on weighted average of all supplier industries - each with different maximum potentials',
        'key_interventions': [
            {'name': 'Supplier engagement', 'potential': '40-60%', 'timeline': '3-10 years', 'scalability': 'High'},
            {'name': 'Private label optimization', 'potential': '50-70%', 'timeline': '2-7 years', 'scalability': 'High'},
            {'name': 'Customer education', 'potential': '20-40%', 'timeline': '5-15 years', 'scalability': 'Medium'},
            {'name': 'Circular retail models', 'potential': '30-50%', 'timeline': '10-20 years', 'scalability': 'Low'}
        ],
        'residual_drivers': ['Supplier industry mix', 'Customer demand patterns', 'Product category constraints', 'Geographic market differences']
    }
}

# Sidebar for industry selection with enhanced information
st.sidebar.header("🏭 Select Industry for Analysis")
st.sidebar.markdown("*Based on CDP disclosure data and SBTi guidance analysis*")

selected_industry = st.sidebar.selectbox(
    "Choose a Scope 3-heavy industry:",
    list(residual_industry_data.keys()),
    help="These industries have 65%+ of emissions in Scope 3, making residual emissions particularly critical"
)

# Display industry overview
selected_data = residual_industry_data[selected_industry]
st.sidebar.markdown(f"""
**{selected_industry} Overview:**
- **Scope 3 dominance**: {selected_data['scope3_percentage']}%
- **CDP sample**: {selected_data['cdp_sample_size']} companies
- **Main challenge**: {selected_data['rf2_complexity']['main_challenge'][:60]}...
""")

# Main problem demonstration
st.subheader("🚨 The Fundamental Problem: Static Thresholds vs. Industry Reality")

col1, col2 = st.columns(2)

with col1:
    st.error("**Current SBTi Approach: One-Size-Fits-All**")
    
    # Create static comparison chart with dark theme
    industries = list(residual_industry_data.keys())
    static_values = [11] * len(industries)
    
    fig_static = go.Figure(data=[
        go.Bar(x=[ind.replace(' ', '\n') for ind in industries], y=static_values, 
               marker_color='#FF4B4B', name='Static 11% Residual')
    ])
    
    fig_static.update_layout(
        title="SBTi Static Residuals",
        yaxis_title="Residual Emissions (%)",
        height=300,
        showlegend=False,
        paper_bgcolor='#0E1117',
        plot_bgcolor='#0E1117',
        font=dict(color='#FAFAFA')
    )
    
    fig_static.add_annotation(
        x=2, y=15,
        text="Same threshold<br>for all industries!",
        showarrow=True,
        arrowhead=2,
        arrowcolor="#FF4B4B",
        font=dict(color='#FAFAFA')
    )
    
    st.plotly_chart(fig_static, use_container_width=True)
    
    st.markdown("""
    **Problems with Static Approach:**
    - ❌ Ignores industry-specific constraints
    - ❌ Same threshold despite 67-99% Scope 3 variation
    - ❌ No scientific basis for 11% across all sectors
    - ❌ Enables premature offset reliance
    """)

with col2:
    st.success("**RF2 Dynamic Approach: Industry-Specific Reality**")
    
    # Create dynamic comparison chart showing illustrative ranges with dark theme
    industries = list(residual_industry_data.keys())
    conservative_residuals = [100 - data['illustrative_scenarios']['conservative_max_reduction'] 
                            for data in residual_industry_data.values()]
    ambitious_residuals = [100 - data['illustrative_scenarios']['ambitious_max_reduction'] 
                          for data in residual_industry_data.values()]
    
    fig_dynamic = go.Figure()
    
    # Add error bars showing range
    fig_dynamic.add_trace(go.Scatter(
        x=[ind.replace(' ', '\n') for ind in industries],
        y=conservative_residuals,
        error_y=dict(
            type='data',
            symmetric=False,
            array=[c - a for c, a in zip(conservative_residuals, ambitious_residuals)],
            arrayminus=[0] * len(industries),
            color='#00D4AA'
        ),
        mode='markers',
        marker=dict(size=10, color='#00D4AA'),
        name='RF2 Dynamic Range'
    ))
    
    fig_dynamic.update_layout(
        title="RF2 Industry-Specific Residuals",
        yaxis_title="Residual Emissions (%)",
        height=300,
        showlegend=False,
        paper_bgcolor='#0E1117',
        plot_bgcolor='#0E1117',
        font=dict(color='#FAFAFA')
    )
    
    st.plotly_chart(fig_dynamic, use_container_width=True)
    
    st.markdown("""
    **Benefits of Dynamic Approach:**
    - ✅ Reflects actual industry constraints  
    - ✅ Based on technical feasibility analysis
    - ✅ Prevents gaming and premature offsets
    - ✅ Enables authentic climate planning
    """)

# NEW: Dynamic Emissions Decomposition Visualization (from Figure 4)
st.subheader("📊 Dynamic Emissions Decomposition: The Heart of RF4")
st.markdown("""
**This visualization shows how genuine decarbonization differs from accounting artifacts - 
the core insight that RF4 research framework enables.**
""")

# Create the stacked bar chart similar to Figure 4
def create_emissions_decomposition():
    years = [2030, 2035, 2040, 2045, 2050]
    company_baseline = 1000  # MtCO2e baseline
    growth_rate = 0.04  # 4% annual growth
    decarbonization_efficiency = 0.5  # 50% of growth emissions are reduced through genuine decarbonization
    
    data = []
    cumulative_growth = 1.0
    
    for i, year in enumerate(years):
        year_growth = cumulative_growth * (1 + growth_rate) ** (5 * i) if i > 0 else 1.0
        
        # Unabated growth emissions (light blue/grey)
        unabated_growth = company_baseline * (year_growth - 1) * (1 - decarbonization_efficiency)
        
        # Genuine decarbonization (dark green) - negative values
        genuine_decarb = -company_baseline * (year_growth - 1) * decarbonization_efficiency
        
        # Dynamic residual emissions (orange) - increasing over time
        base_residual = company_baseline * 0.11  # Static baseline
        dynamic_multiplier = 1 + 0.6 * (i / 4)  # Increasing residual needs
        dynamic_residual = base_residual * dynamic_multiplier
        
        # Carbon removals (light green) to balance residuals
        carbon_removals = dynamic_residual
        
        # Growth limits alert (red) - showing unsustainability
        growth_limits = -company_baseline * 0.15 * (i / 2) if i > 2 else 0
        
        data.append({
            'year': year,
            'unabated_growth': unabated_growth,
            'genuine_decarb': genuine_decarb,
            'dynamic_residual': dynamic_residual,
            'carbon_removals': carbon_removals,
            'growth_limits': growth_limits
        })
        
        cumulative_growth = year_growth
    
    return pd.DataFrame(data)

decomp_data = create_emissions_decomposition()

# Create stacked bar chart
fig_decomp = go.Figure()

# Add traces for each component
fig_decomp.add_trace(go.Bar(
    x=decomp_data['year'],
    y=decomp_data['unabated_growth'],
    name='Unabated Growth Emissions<br>(4% annual increase)',
    marker_color='#808080',
    hovertemplate='<b>Unabated Growth</b><br>Year: %{x}<br>Emissions: %{y:.0f} MtCO₂e<extra></extra>'
))

fig_decomp.add_trace(go.Bar(
    x=decomp_data['year'],
    y=decomp_data['genuine_decarb'],
    name='Genuine Decarbonization<br>(capped at 50% of growth)',
    marker_color='#2E7D32',
    hovertemplate='<b>Genuine Decarbonization</b><br>Year: %{x}<br>Reduction: %{y:.0f} MtCO₂e<extra></extra>'
))

fig_decomp.add_trace(go.Bar(
    x=decomp_data['year'],
    y=decomp_data['dynamic_residual'],
    name='Dynamic Residual Emissions<br>(reflecting global net-zero progress)',
    marker_color='#FF8C00',
    hovertemplate='<b>Dynamic Residuals</b><br>Year: %{x}<br>Residuals: %{y:.0f} MtCO₂e<extra></extra>'
))

fig_decomp.add_trace(go.Bar(
    x=decomp_data['year'],
    y=decomp_data['carbon_removals'],
    name='Carbon Removals<br>(balancing residuals)',
    marker_color='#81C784',
    hovertemplate='<b>Carbon Removals</b><br>Year: %{x}<br>Removals: %{y:.0f} MtCO₂e<extra></extra>'
))

fig_decomp.add_trace(go.Bar(
    x=decomp_data['year'],
    y=decomp_data['growth_limits'],
    name='Growth Limits Alert<br>(mirrors unabated growth)',
    marker_color='#D32F2F',
    hovertemplate='<b>Growth Limits Alert</b><br>Year: %{x}<br>Alert: %{y:.0f} MtCO₂e<extra></extra>'
))

# Add industry-specific benchmark line
benchmark_values = [400, 450, 500, 550, 600]  # Dynamic benchmark evolution
fig_decomp.add_trace(go.Scatter(
    x=decomp_data['year'],
    y=benchmark_values,
    mode='lines',
    name='Evolution of Industry-Specific Benchmark',
    line=dict(color='#FAFAFA', width=3, dash='dash'),
    hovertemplate='<b>Industry Benchmark</b><br>Year: %{x}<br>Threshold: %{y:.0f} MtCO₂e<extra></extra>'
))

fig_decomp.update_layout(
    title=f"Industry-specific Net-Zero Transition Pathway with Dynamic Benchmarks (2030-2050)<br><sub>{selected_industry} company emissions decomposition with scenario-dependent removal requirements</sub>",
    xaxis_title="Year",
    yaxis_title="MtCO₂e (Positive = Emissions, Negative = Removals)",
    height=600,
    barmode='relative',
    paper_bgcolor='#0E1117',
    plot_bgcolor='#0E1117',
    font=dict(color='#FAFAFA'),
    legend=dict(
        orientation="v",
        yanchor="top",
        y=1,
        xanchor="left",
        x=1.05,
        bgcolor='rgba(38, 39, 48, 0.8)',
        bordercolor='#464457',
        borderwidth=1
    )
)

# Add annotations
fig_decomp.add_annotation(
    x=2042, y=800,
    text="Planetary boundaries<br>Technology evolution &<br>Limits of growth",
    showarrow=True,
    arrowhead=2,
    arrowcolor="#FAFAFA",
    font=dict(color='#FAFAFA', size=10),
    bgcolor='rgba(38, 39, 48, 0.8)',
    bordercolor='#464457',
    borderwidth=1
)

st.plotly_chart(fig_decomp, use_container_width=True)

st.info("""
**Key Insight from Dynamic Decomposition:**
This chart demonstrates why static 11% residual thresholds fail - as global decarbonization efforts intensify, 
constraints tighten and residual emissions naturally increase. The RF4 framework captures this reality through 
dynamic, science-based thresholds that evolve with technological progress and planetary boundaries.
""")

# Continue with rest of the app (industry complexity overview)
st.subheader(f"🔬 Deep Dive: {selected_industry} Residual Emissions Analysis")

# Industry complexity overview with fixed DataFrame handling
complexity_col1, complexity_col2 = st.columns([2, 1])

with complexity_col1:
    st.markdown("### RF2 Complexity Factors")
    
    complexity_data = selected_data['rf2_complexity']
    
    # Create a complexity radar chart with proper data handling
    categories = [key.replace('_', ' ').title() for key in complexity_data.keys() if key != 'main_challenge']
    
    # Convert complexity descriptions to scores for visualization
    complexity_scores = []
    for key, value in complexity_data.items():
        if key == 'main_challenge':
            continue
        # Simple scoring based on text complexity indicators
        value_str = str(value).lower()
        if any(word in value_str for word in ['none', 'limited', 'impossible', 'cannot']):
            score = 8  # High complexity
        elif any(word in value_str for word in ['medium', 'some', 'partial', 'varies']):
            score = 5  # Medium complexity
        elif any(word in value_str for word in ['high', 'full', 'direct', 'easy']):
            score = 2  # Low complexity (good for decarbonization)
        else:
            score = 6  # Default medium-high
        complexity_scores.append(score)
    
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=complexity_scores,
        theta=categories,
        fill='toself',
        name=f'{selected_industry} Complexity',
        line_color='#00D4AA'
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                color='#FAFAFA'
            ),
            angularaxis=dict(color='#FAFAFA')
        ),
        title="Industry Complexity Factors (Higher = More Challenging)",
        height=400,
        paper_bgcolor='#0E1117',
        plot_bgcolor='#0E1117',
        font=dict(color='#FAFAFA')
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)

with complexity_col2:
    st.markdown("### Key Challenge")
    st.info(f"**{complexity_data['main_challenge']}**")
    
    st.markdown("### Scope 3 Categories")
    for category in selected_data['scope3_categories']:
        st.write(f"• {category}")
    
    st.markdown("### Residual Drivers")
    for driver in selected_data['residual_drivers']:
        st.write(f"🔸 {driver}")

# Interactive scenario builder with fixed DataFrame handling
st.subheader("🎮 Interactive Scenario Builder: What IF We Had RF2 Data?")

st.markdown(f"""
**Current State**: {selected_industry} companies must use SBTi's blanket 11% residual threshold.

**What RF2 Research Would Enable**: Industry-specific maximum decarbonization potential based on:
- Technical feasibility across value chains
- Economic constraints and investment requirements  
- Technology readiness and deployment timelines
- Cross-sectoral dependencies and limitations
""")

# Scenario sliders
scenario_col1, scenario_col2 = st.columns(2)

with scenario_col1:
    st.markdown("#### Adjust RF2 Assumptions:")
    
    conservative_reduction = st.slider(
        "Conservative Scenario - Maximum Decarbonization (%)", 
        60, 98, 
        selected_data['illustrative_scenarios']['conservative_max_reduction'],
        help="Current technology constraints and proven interventions only"
    )
    
    ambitious_reduction = st.slider(
        "Ambitious Scenario - Maximum Decarbonization (%)",
        conservative_reduction, 98,
        selected_data['illustrative_scenarios']['ambitious_max_reduction'],
        help="Assumes successful scaling of emerging technologies"
    )
    
    breakthrough_reduction = st.slider(
        "Breakthrough Scenario - Maximum Decarbonization (%)",
        ambitious_reduction, 98,
        selected_data['illustrative_scenarios']['breakthrough_max_reduction'],
        help="Assumes major technological breakthroughs and optimal conditions"
    )

with scenario_col2:
    st.markdown("#### Resulting Residual Emissions:")
    
    conservative_residual = 100 - conservative_reduction
    ambitious_residual = 100 - ambitious_reduction
    breakthrough_residual = 100 - breakthrough_reduction
    static_residual = 11
    
    # Create residual comparison with dark theme
    scenarios = ['SBTi Static', 'Conservative RF2', 'Ambitious RF2', 'Breakthrough RF2']
    residuals = [static_residual, conservative_residual, ambitious_residual, breakthrough_residual]
    colors = ['#FF4B4B', '#FF8C00', '#00D4AA', '#1f77b4']
    
    fig_scenarios = go.Figure(data=[
        go.Bar(x=scenarios, y=residuals, marker_color=colors)
    ])
    
    fig_scenarios.update_layout(
        title=f"{selected_industry} Residual Emissions by Scenario",
        yaxis_title="Residual Emissions (%)",
        height=300,
        paper_bgcolor='#0E1117',
        plot_bgcolor='#0E1117',
        font=dict(color='#FAFAFA')
    )
    
    # Add annotations showing the range
    fig_scenarios.add_annotation(
        x=1.5, y=max(residuals) + 2,
        text=f"RF2 Range: {breakthrough_residual:.1f}% - {conservative_residual:.1f}%",
        showarrow=False,
        font=dict(size=12, color="#00D4AA")
    )
    
    st.plotly_chart(fig_scenarios, use_container_width=True)

# Impact analysis with dark theme
st.subheader("📊 The Impact of Dynamic vs. Static Residuals")

impact_col1, impact_col2 = st.columns(2)

with impact_col1:
    st.markdown("### Carbon Removal Requirements")
    
    # Assume a hypothetical company size for calculation
    company_emissions = st.number_input("Hypothetical Company Baseline Emissions (tCO2e/year)", 
                                       min_value=1000, max_value=10000000, value=100000, step=10000)
    
    static_removals = company_emissions * (static_residual / 100)
    conservative_removals = company_emissions * (conservative_residual / 100)
    ambitious_removals = company_emissions * (ambitious_residual / 100)
    breakthrough_removals = company_emissions * (breakthrough_residual / 100)
    
    removal_scenarios = ['SBTi Static', 'Conservative RF2', 'Ambitious RF2', 'Breakthrough RF2']
    removal_values = [static_removals, conservative_removals, ambitious_removals, breakthrough_removals]
    removal_colors = ['#FF4B4B', '#FF8C00', '#00D4AA', '#1f77b4']
    
    fig_removals = go.Figure(data=[
        go.Bar(x=removal_scenarios, y=removal_values, marker_color=removal_colors)
    ])
    
    fig_removals.update_layout(
        title="Required Carbon Removals (tCO2e/year)", 
        showlegend=False,
        paper_bgcolor='#0E1117',
        plot_bgcolor='#0E1117',
        font=dict(color='#FAFAFA')
    )
    
    st.plotly_chart(fig_removals, use_container_width=True)

with impact_col2:
    st.markdown("### Financial Impact Analysis")
    
    removal_cost = st.slider("Carbon Removal Cost ($/tCO2)", 100, 1000, 400, step=50,
                            help="Current engineered removal costs range $400-600/tCO2")
    
    static_cost = static_removals * removal_cost
    conservative_cost = conservative_removals * removal_cost
    ambitious_cost = ambitious_removals * removal_cost
    breakthrough_cost = breakthrough_removals * removal_cost
    
    st.metric("SBTi Static Annual Cost", f"${static_cost:,.0f}")
    st.metric("Conservative RF2 Cost", f"${conservative_cost:,.0f}", 
             delta=f"{conservative_cost - static_cost:,.0f}")
    st.metric("Ambitious RF2 Cost", f"${ambitious_cost:,.0f}", 
             delta=f"{ambitious_cost - static_cost:,.0f}")
    st.metric("Breakthrough RF2 Cost", f"${breakthrough_cost:,.0f}", 
             delta=f"{breakthrough_cost - static_cost:,.0f}")

# Key interventions analysis with fixed DataFrame handling
st.subheader("🛠️ Decarbonization Intervention Analysis")

# Create DataFrame with proper structure for plotly
intervention_list = selected_data['key_interventions']
intervention_df = pd.DataFrame(intervention_list)

# Extract numeric values from potential ranges
def extract_mid_value(range_str):
    """Extract middle value from range like '30-50%' -> 40"""
    if '-' in range_str:
        parts = range_str.replace('%', '').split('-')
        return (int(parts[0]) + int(parts[1])) / 2
    return 40  # default

intervention_df['potential_numeric'] = intervention_df['potential'].apply(extract_mid_value)

# Extract timeline years
def extract_timeline_years(timeline_str):
    """Extract average years from timeline like '5-10 years' -> 7.5"""
    if '-' in timeline_str:
        parts = timeline_str.replace(' years', '').split('-')
        return (int(parts[0]) + int(parts[1])) / 2
    return 5  # default

intervention_df['timeline_numeric'] = intervention_df['timeline'].apply(extract_timeline_years)

# Map scalability to sizes
scalability_sizes = {'High': 20, 'Medium': 15, 'Low': 10, 'Variable': 12}
intervention_df['size'] = intervention_df['scalability'].map(scalability_sizes)

col1, col2 = st.columns(2)

with col1:
    # Intervention potential vs timeline with fixed DataFrame
    fig_interventions = go.Figure()
    
    colors = {'High': '#00D4AA', 'Medium': '#FF8C00', 'Low': '#FF4B4B', 'Variable': '#1f77b4'}
    
    for scalability in intervention_df['scalability'].unique():
        df_subset = intervention_df[intervention_df['scalability'] == scalability]
        fig_interventions.add_trace(go.Scatter(
            x=df_subset['timeline_numeric'],
            y=df_subset['potential_numeric'],
            mode='markers',
            marker=dict(
                size=df_subset['size'],
                color=colors.get(scalability, '#FAFAFA'),
                opacity=0.7
            ),
            text=df_subset['name'],
            name=f'{scalability} Scalability',
            hovertemplate='<b>%{text}</b><br>Timeline: %{x:.1f} years<br>Potential: %{y:.0f}%<br>Scalability: ' + scalability + '<extra></extra>'
        ))
    
    fig_interventions.update_layout(
        title="Intervention Potential vs Timeline",
        xaxis_title="Implementation Timeline (years)",
        yaxis_title="Emission Reduction Potential (%)",
        paper_bgcolor='#0E1117',
        plot_bgcolor='#0E1117',
        font=dict(color='#FAFAFA')
    )
    
    st.plotly_chart(fig_interventions, use_container_width=True)

with col2:
    st.markdown("### Available Interventions")
    for intervention in selected_data['key_interventions']:
        with st.expander(f"🔧 {intervention['name']}"):
            st.write(f"**Potential**: {intervention['potential']} emission reduction")
            st.write(f"**Timeline**: {intervention['timeline']} to implement")
            st.write(f"**Scalability**: {intervention['scalability']}")

# Research urgency matrix with fixed scatter plot
st.subheader("🎯 Research Priority: Why This Matters Now")

urgency_col1, urgency_col2 = st.columns([2, 1])

with urgency_col1:
    # Create urgency matrix with proper data handling
    industries_list = list(residual_industry_data.keys())
    scope3_percentages = [data['scope3_percentage'] for data in residual_industry_data.values()]
    guidance_gaps = [100 - data['illustrative_scenarios']['conservative_max_reduction'] - 11 
                    for data in residual_industry_data.values()]
    
    fig_urgency = go.Figure()
    
    fig_urgency.add_trace(go.Scatter(
        x=scope3_percentages,
        y=guidance_gaps,
        mode='markers+text',
        text=[ind.replace(' ', '<br>') for ind in industries_list],
        textposition="top center",
        marker=dict(size=15, color='#00D4AA', opacity=0.7),
        hovertemplate='<b>%{text}</b><br>Scope 3: %{x}%<br>Threshold Gap: %{y:.1f}pp<extra></extra>'
    ))
    
    fig_urgency.update_layout(
        title="Research Urgency Matrix",
        xaxis_title="Scope 3 Dominance (%)",
        yaxis_title="Static Threshold Gap (percentage points)",
        height=400,
        paper_bgcolor='#0E1117',
        plot_bgcolor='#0E1117',
        font=dict(color='#FAFAFA')
    )
    
    # Add quadrant annotations
    fig_urgency.add_hline(y=0, line_dash="dash", line_color="#464457")
    fig_urgency.add_vline(x=80, line_dash="dash", line_color="#464457")
    
    fig_urgency.add_annotation(
        x=95, y=15, 
        text="HIGH PRIORITY:<br>High Scope 3 + Large Gap", 
        bgcolor="rgba(211, 47, 47, 0.8)", 
        bordercolor="#FF4B4B", 
        borderwidth=1,
        font=dict(color='#FAFAFA')
    )
    
    st.plotly_chart(fig_urgency, use_container_width=True)

with urgency_col2:
    st.markdown("### Research Impact")
    
    current_gap = abs(conservative_residual - static_residual)
    
    st.metric("Static Threshold Error", f"{current_gap:.1f}%", 
             help="Difference between industry reality and SBTi assumption")
    
    st.markdown(f"""
    **Business Impact:**
    - **Planning uncertainty**: ${abs(conservative_cost - static_cost):,.0f}/year
    - **Investment misallocation**: Decarbonization vs. removals
    - **Climate integrity risk**: Premature offset reliance
    - **Competitive disadvantage**: Suboptimal resource allocation
    """)
    
    st.success(f"""
    **RF2 Solution Value:**
    - Science-based residual thresholds
    - Dynamic technology adjustment  
    - Industry-specific investment optimization
    - Authentic climate accountability
    """)

# Dynamic timeline visualization with dark theme
st.subheader("🕒 Evolution Timeline: From Static to Dynamic Residuals")

timeline_years = list(range(2025, 2051))
selected_scenarios = selected_data['illustrative_scenarios']

# Create dynamic timeline showing residual evolution
fig_timeline = go.Figure()

# Static line (SBTi approach)
static_line = [11] * len(timeline_years)
fig_timeline.add_trace(go.Scatter(
    x=timeline_years, y=static_line,
    mode='lines',
    name='SBTi Static 11%',
    line=dict(color='#FF4B4B', dash='dash', width=3),
    hovertemplate='<b>SBTi Static Approach</b><br>Year: %{x}<br>Residual: %{y}%<extra></extra>'
))

# Dynamic sigmoid curves for different scenarios
def sigmoid_residual(year, max_reduction, inflection_year=2035, steepness=0.3):
    """Create sigmoid curve showing residual emissions evolution"""
    t = year - 2025  # Start from 2025
    inflection_t = inflection_year - 2025
    base_residual = 100 - max_reduction
    
    # Start higher and approach the limit asymptotically
    current_residual = base_residual + (25 - base_residual) * np.exp(-steepness * (t - 5))
    return max(base_residual, min(25, current_residual))

# Conservative scenario
conservative_residuals = [sigmoid_residual(year, selected_scenarios['conservative_max_reduction']) 
                         for year in timeline_years]
fig_timeline.add_trace(go.Scatter(
    x=timeline_years, y=conservative_residuals,
    mode='lines',
    name='Conservative RF2',
    line=dict(color='#FF8C00', width=2),
    hovertemplate='<b>Conservative RF2</b><br>Year: %{x}<br>Residual: %{y:.1f}%<extra></extra>'
))

# Ambitious scenario  
ambitious_residuals = [sigmoid_residual(year, selected_scenarios['ambitious_max_reduction']) 
                      for year in timeline_years]
fig_timeline.add_trace(go.Scatter(
    x=timeline_years, y=ambitious_residuals,
    mode='lines',
    name='Ambitious RF2',
    line=dict(color='#00D4AA', width=2),
    hovertemplate='<b>Ambitious RF2</b><br>Year: %{x}<br>Residual: %{y:.1f}%<extra></extra>'
))

# Breakthrough scenario
breakthrough_residuals = [sigmoid_residual(year, selected_scenarios['breakthrough_max_reduction']) 
                         for year in timeline_years]
fig_timeline.add_trace(go.Scatter(
    x=timeline_years, y=breakthrough_residuals,
    mode='lines',
    name='Breakthrough RF2',
    line=dict(color='#1f77b4', width=2),
    hovertemplate='<b>Breakthrough RF2</b><br>Year: %{x}<br>Residual: %{y:.1f}%<extra></extra>'
))

fig_timeline.update_layout(
    title=f"{selected_industry}: Static vs Dynamic Residual Emissions (2025-2050)",
    xaxis_title="Year",
    yaxis_title="Residual Emissions (%)",
    height=500,
    hovermode='x unified',
    paper_bgcolor='#0E1117',
    plot_bgcolor='#0E1117',
    font=dict(color='#FAFAFA')
)

# Add key milestone annotations
fig_timeline.add_annotation(
    x=2030, y=20,
    text="2030: Technology<br>deployment accelerates",
    showarrow=True,
    arrowhead=2,
    font=dict(color='#FAFAFA')
)

fig_timeline.add_annotation(
    x=2040, y=8,
    text="2040: Maximum potential<br>constraints emerge",
    showarrow=True,
    arrowhead=2,
    font=dict(color='#FAFAFA')
)

st.plotly_chart(fig_timeline, use_container_width=True)

# Key insights and conclusions
st.subheader("🔑 Why Static 11% Residuals Don't Make Scientific Sense")

insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:
    st.markdown("""
    ### 🎯 Industry Reality Gap
    
    **Scope 3-heavy industries face:**
    - **67-99%** emissions beyond direct control
    - **Complex value chains** spanning multiple sectors
    - **Variable constraints** from biological to technological
    - **Different maximum potentials** based on physics
    """)

with insight_col2:
    st.markdown("""
    ### 📊 Static Approach Failures
    
    **SBTi's 11% uniform threshold:**
    - **Ignores industry-specific limits**
    - **Misses biological/physical constraints** 
    - **Creates perverse incentives** for offset gaming
    - **Undermines authentic decarbonization**
    """)

with insight_col3:
    st.markdown("""
    ### 🚀 The RF2 Solution
    
    **Dynamic, science-based residuals:**
    - ✅ Industry-specific maximum potential
    - ✅ Technology evolution tracking
    - ✅ Cross-sectoral dependency mapping
    - ✅ Authentic climate accountability
    """)

# Call to action
st.subheader("🎯 The Research Frontier 4 Case")

st.success("""
### This Analysis Demonstrates:

1. **Problem Scale**: Scope 3-heavy industries (67-99% indirect emissions) cannot use uniform residual thresholds
2. **Scientific Inadequacy**: Static 11% ignores fundamental differences in industry constraints and potentials  
3. **Business Impact**: Misallocation between decarbonization investment vs. carbon removal preparation
4. **Climate Integrity**: Premature offset reliance undermines authentic corporate climate action

### The Solution: Dynamic, Industry-Specific Residual Emissions

**RF4 research framework** delivers science-based residual thresholds through:
- **RF2 Integration**: Maximum decarbonization potential mapping
- **Technology Evolution**: Dynamic adjustment as capabilities advance  
- **Cross-Sectoral Analysis**: Value chain constraint identification
- **Verification Support**: Authentic vs. accounting-driven progress

**Next Steps**: This complexity isn't a limitation—it's the research opportunity that RF4 addresses.
Systematic development of industry-specific residual thresholds can transform corporate net-zero 
from arbitrary compliance to scientifically-grounded climate action aligned with planetary realities.
""")

# Footer with methodology and citations
st.markdown("---")
st.markdown("""
### 📚 Methodology and Data Sources

**This analysis demonstrates the critical need for RF4 research using:**

**Real Corporate Data:**
- CDP Technical Note: Relevance of Scope 3 Categories by Sector (2022)
- Science Based Targets initiative corporate database (7,000+ companies)
- Net-Zero Data Public Utility (NZDPU) comprehensive emissions database

**Scientific Foundations:**
- IPCC AR6 Working Group III: Mitigation of Climate Change (2022)
- IEA Net Zero by 2050 Roadmap (2021, updated 2023)
- Academic literature on industrial decarbonization pathways

**Limitations and Disclaimers:**
- Industry-specific residual percentages are **illustrative scenarios** based on literature review
- Actual RF4 research would require systematic technical analysis and corporate collaboration
- This tool demonstrates **problem complexity** rather than providing definitive residual thresholds
- Investment calculations use simplified assumptions for demonstration purposes

**Research Citation:**
This analysis supports the research framework proposed in "Operationalizing corporate climate action 
through five research frontiers" (submitted to Nature Sustainability, 2024), specifically Research 
Frontier 4: Industry-specific residual emissions quantification.
""")

# About the research team
with st.expander("👥 About the Research Team"):
    st.markdown("""
    **Foundation for Planetary Action** develops science-based frameworks for corporate climate action 
    through systematic research that bridges climate science with business implementation.
    
    **Our Approach:**
    - Rigorous scientific methodology grounded in IPCC assessments
    - Real corporate data analysis using CDP and SBTi databases  
    - Collaborative development with industry partners
    - Open-source tools and transparent methodologies
    
    **Research Frontiers:**
    - RF1: Industry-specific emission accounting 
    - RF2: Science-aligned target setting (demonstrated in companion tool)
    - RF3: Progress verification and tracking
    - RF4: Residual emissions quantification (this tool)
    - RF5: Climate risk and cost of inaction assessment
    
    **Mission:** Transform corporate climate action from fragmented voluntary initiatives 
    to systematic, science-backed strategies that demonstrably contribute to global net-zero transitions.
    """)

st.markdown("---")
st.markdown("*Developed by Foundation for Planetary Action | © 2024 | Open source research tools for climate action*")
