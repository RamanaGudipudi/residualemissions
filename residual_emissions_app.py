import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots

# Set page config
st.set_page_config(
    page_title="Dynamic Residual Emissions: Why Static 11% Thresholds Fail",
    page_icon="🎯",
    layout="wide"
)

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
            'agricultural_constraints': {'biological_limits': 'Methane from ruminants has biological floors', 'seasonal_variation': 'Weather-dependent crop yields', 'geographic_spread': 'Global supply chains across climate zones'},
            'supply_chain_tiers': 4,
            'control_level': 'Limited - depends on thousands of farmers',
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
        'cdp_sample_size': 120,  # Estimated from various consumer goods sectors
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
        'cdp_sample_size': 80,  # Estimated from retail sector reporting
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
    
    # Create static comparison chart
    industries = list(residual_industry_data.keys())
    static_values = [11] * len(industries)
    
    fig_static = go.Figure(data=[
        go.Bar(x=[ind.replace(' ', '\n') for ind in industries], y=static_values, 
               marker_color='red', name='Static 11% Residual')
    ])
    
    fig_static.update_layout(
        title="SBTi Static Residuals",
        yaxis_title="Residual Emissions (%)",
        height=300,
        showlegend=False
    )
    
    fig_static.add_annotation(
        x=2, y=15,
        text="Same threshold\nfor all industries!",
        showarrow=True,
        arrowhead=2,
        arrowcolor="red"
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
    
    # Create dynamic comparison chart showing illustrative ranges
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
            arrayminus=[0] * len(industries)
        ),
        mode='markers',
        marker=dict(size=10, color='green'),
        name='RF2 Dynamic Range'
    ))
    
    fig_dynamic.update_layout(
        title="RF2 Industry-Specific Residuals",
        yaxis_title="Residual Emissions (%)",
        height=300,
        showlegend=False
    )
    
    st.plotly_chart(fig_dynamic, use_container_width=True)
    
    st.markdown("""
    **Benefits of Dynamic Approach:**
    - ✅ Reflects actual industry constraints  
    - ✅ Based on technical feasibility analysis
    - ✅ Prevents gaming and premature offsets
    - ✅ Enables authentic climate planning
    """)

# Detailed industry analysis
st.subheader(f"🔬 Deep Dive: {selected_industry} Residual Emissions Analysis")

# Industry complexity overview
complexity_col1, complexity_col2 = st.columns([2, 1])

with complexity_col1:
    st.markdown("### RF2 Complexity Factors")
    
    complexity_data = selected_data['rf2_complexity']
    
    # Create a complexity radar chart
    categories = list(complexity_data.keys())
    
    # Convert complexity descriptions to scores for visualization
    complexity_scores = []
    for key, value in complexity_data.items():
        if key == 'main_challenge':
            continue
        # Simple scoring based on text complexity indicators
        if any(word in str(value).lower() for word in ['none', 'limited', 'impossible']):
            score = 8  # High complexity
        elif any(word in str(value).lower() for word in ['medium', 'some', 'partial']):
            score = 5  # Medium complexity
        elif any(word in str(value).lower() for word in ['high', 'full', 'direct']):
            score = 2  # Low complexity (good for decarbonization)
        else:
            score = 6  # Default medium-high
        complexity_scores.append(score)
    
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=complexity_scores,
        theta=[cat.replace('_', ' ').title() for cat in categories[:-1]],  # Exclude main_challenge
        fill='toself',
        name=f'{selected_industry} Complexity'
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        title="Industry Complexity Factors (Higher = More Challenging)",
        height=400
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

# Interactive scenario builder
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
    
    # Create residual comparison
    scenarios = ['SBTi Static', 'Conservative RF2', 'Ambitious RF2', 'Breakthrough RF2']
    residuals = [static_residual, conservative_residual, ambitious_residual, breakthrough_residual]
    colors = ['red', '#ff7f0e', '#2ca02c', '#1f77b4']
    
    fig_scenarios = go.Figure(data=[
        go.Bar(x=scenarios, y=residuals, marker_color=colors)
    ])
    
    fig_scenarios.update_layout(
        title=f"{selected_industry} Residual Emissions by Scenario",
        yaxis_title="Residual Emissions (%)",
        height=300
    )
    
    # Add annotations showing the range
    fig_scenarios.add_annotation(
        x=1.5, y=max(residuals) + 2,
        text=f"RF2 Range: {breakthrough_residual:.1f}% - {conservative_residual:.1f}%",
        showarrow=False,
        font=dict(size=12, color="green")
    )
    
    st.plotly_chart(fig_scenarios, use_container_width=True)

# Impact analysis
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
    
    removal_data = pd.DataFrame({
        'Scenario': ['SBTi Static', 'Conservative RF2', 'Ambitious RF2', 'Breakthrough RF2'],
        'Removals_Needed': [static_removals, conservative_removals, ambitious_removals, breakthrough_removals],
        'Colors': ['red', '#ff7f0e', '#2ca02c', '#1f77b4']
    })
    
    fig_removals = px.bar(removal_data, x='Scenario', y='Removals_Needed', 
                         color='Scenario', color_discrete_map=dict(zip(removal_data['Scenario'], removal_data['Colors'])))
    fig_removals.update_layout(title="Required Carbon Removals (tCO2e/year)", showlegend=False)
    
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

# Key interventions analysis
st.subheader("🛠️ Decarbonization Intervention Analysis")

intervention_data = pd.DataFrame(selected_data['key_interventions'])

col1, col2 = st.columns(2)

with col1:
    # Intervention potential vs timeline
    fig_interventions = px.scatter(intervention_data, 
                                  x='timeline', y='potential', 
                                  size='scalability', 
                                  color='scalability',
                                  hover_name='name',
                                  title="Intervention Potential vs Timeline")
    
    fig_interventions.update_xaxes(title="Implementation Timeline")
    fig_interventions.update_yaxes(title="Emission Reduction Potential")
    
    st.plotly_chart(fig_interventions, use_container_width=True)

with col2:
    st.markdown("### Available Interventions")
    for intervention in selected_data['key_interventions']:
        with st.expander(f"🔧 {intervention['name']}"):
            st.write(f"**Potential**: {intervention['potential']} emission reduction")
            st.write(f"**Timeline**: {intervention['timeline']} to implement")
            st.write(f"**Scalability**: {intervention['scalability']}")

# The missing science section
st.subheader("🧬 What RF2 Research Would Actually Determine")

st.markdown(f"""
**For {selected_industry} Industry, RF2 research would systematically analyze:**
""")

rf2_col1, rf2_col2, rf2_col3 = st.columns(3)

with rf2_col1:
    st.markdown("""
    ### 🔬 Technical Constraints
    - **Process emission limits**: Physical/chemical boundaries
    - **Technology maturity**: Scale-up timelines and costs  
    - **Energy system integration**: Renewable energy potential
    - **Material substitution**: Alternative input availability
    """)

with rf2_col2:
    st.markdown("""
    ### 🔗 Value Chain Dependencies  
    - **Upstream sector limits**: Supplier decarbonization capacity
    - **Cross-sectoral coordination**: Multi-industry requirements
    - **Geographic variations**: Regional constraint differences
    - **Supply chain transformation**: Systemic change requirements
    """)

with rf2_col3:
    st.markdown("""
    ### 📈 Dynamic Evolution Modeling
    - **Technology breakthrough points**: When limits shift
    - **Policy impact scenarios**: Regulatory acceleration effects
    - **Learning curve projections**: Cost reduction timelines
    - **Global constraint tightening**: Competition for solutions
    """)

# Research urgency matrix
st.subheader("🎯 Research Priority: Why This Matters Now")

urgency_col1, urgency_col2 = st.columns([2, 1])

with urgency_col1:
    # Create urgency matrix
    industries = list(residual_industry_data.keys())
    scope3_percentages = [data['scope3_percentage'] for data in residual_industry_data.values()]
    guidance_gaps = [100 - data['illustrative_scenarios']['conservative_max_reduction'] - 11 
                    for data in residual_industry_data.values()]  # Difference from static assumption
    
    fig_urgency = px.scatter(x=scope3_percentages, y=guidance_gaps, 
                           text=industries, 
                           size=[100]*len(industries),
                           title="Research Urgency Matrix")
    
    fig_urgency.update_traces(textposition="top center")
    fig_urgency.update_xaxes(title="Scope 3 Dominance (%)")
    fig_urgency.update_yaxes(title="Static Threshold Gap (percentage points)")
    fig_urgency.update_layout(height=400)
    
    # Add quadrant annotations
    fig_urgency.add_hline(y=0, line_dash="dash", line_color="gray")
    fig_urgency.add_vline(x=80, line_dash="dash", line_color="gray")
    
    fig_urgency.add_annotation(x=95, y=15, text="HIGH PRIORITY:<br>High Scope 3 + Large Gap", 
                              bgcolor="red", bordercolor="black", borderwidth=1)
    
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

# Dynamic timeline visualization - showing evolution from static to dynamic
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
    line=dict(color='red', dash='dash', width=3),
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
    line=dict(color='orange', width=2),
    hovertemplate='<b>Conservative RF2</b><br>Year: %{x}<br>Residual: %{y:.1f}%<extra></extra>'
))

# Ambitious scenario  
ambitious_residuals = [sigmoid_residual(year, selected_scenarios['ambitious_max_reduction']) 
                      for year in timeline_years]
fig_timeline.add_trace(go.Scatter(
    x=timeline_years, y=ambitious_residuals,
    mode='lines',
    name='Ambitious RF2',
    line=dict(color='green', width=2),
    hovertemplate='<b>Ambitious RF2</b><br>Year: %{x}<br>Residual: %{y:.1f}%<extra></extra>'
))

# Breakthrough scenario
breakthrough_residuals = [sigmoid_residual(year, selected_scenarios['breakthrough_max_reduction']) 
                         for year in timeline_years]
fig_timeline.add_trace(go.Scatter(
    x=timeline_years, y=breakthrough_residuals,
    mode='lines',
    name='Breakthrough RF2',
    line=dict(color='blue', width=2),
    hovertemplate='<b>Breakthrough RF2</b><br>Year: %{x}<br>Residual: %{y:.1f}%<extra></extra>'
))

fig_timeline.update_layout(
    title=f"{selected_industry}: Static vs Dynamic Residual Emissions (2025-2050)",
    xaxis_title="Year",
    yaxis_title="Residual Emissions (%)",
    height=500,
    hovermode='x unified'
)

# Add key milestone annotations
fig_timeline.add_annotation(
    x=2030, y=20,
    text="2030: Technology<br>deployment accelerates",
    showarrow=True,
    arrowhead=2
)

fig_timeline.add_annotation(
    x=2040, y=8,
    text="2040: Maximum potential<br>constraints emerge",
    showarrow=True,
    arrowhead=2
)

st.plotly_chart(fig_timeline, use_container_width=True)

# Research methodology section
st.subheader("🔬 Research Methodology: How RF4 Would Actually Work")

method_col1, method_col2 = st.columns(2)

with method_col1:
    st.markdown("""
    ### Phase 1: Industry Materiality Mapping
    
    **Objectives:**
    - Map Scope 3 emission sources across value chains
    - Identify cross-sectoral dependencies (building on RF2)
    - Quantify control vs. influence boundaries
    - Assess technology readiness by intervention type
    
    **Methods:**
    - Corporate disclosure analysis (CDP, SBTi database)
    - Value chain lifecycle assessment
    - Technology maturity assessment  
    - Stakeholder engagement workshops
    """)
    
    st.markdown("""
    ### Phase 2: Maximum Potential Modeling
    
    **Objectives:**  
    - Define theoretical maximum decarbonization
    - Account for physical/biological constraints
    - Model technology breakthrough scenarios
    - Assess economic feasibility boundaries
    
    **Methods:**
    - Bottom-up technical potential analysis
    - Economic optimization modeling
    - Monte Carlo uncertainty analysis
    - Expert elicitation for breakthrough timing
    """)

with method_col2:
    st.markdown("""
    ### Phase 3: Dynamic Threshold Development
    
    **Objectives:**
    - Create time-dependent residual curves
    - Link to global decarbonization trajectories  
    - Account for technology learning curves
    - Enable policy scenario integration
    
    **Methods:**
    - System dynamics modeling
    - Technology diffusion curves
    - Policy impact assessment
    - Validation with industry experts
    """)
    
    st.markdown("""
    ### Phase 4: Verification Framework
    
    **Objectives:**
    - Distinguish genuine vs. accounting reductions
    - Prevent premature offset reliance
    - Enable transparent progress tracking
    - Support investment decision-making
    
    **Methods:**
    - Automated anomaly detection systems
    - Peer benchmarking protocols
    - Supply chain transparency requirements
    - Third-party validation standards
    """)

# Data requirements and availability
st.subheader("📋 Data Requirements and Current Availability")

data_col1, data_col2, data_col3 = st.columns(3)

with data_col1:
    st.markdown("""
    ### ✅ Available Data Sources
    
    **Corporate Disclosures:**
    - CDP (1,300+ Scope 3 reporters)
    - SBTi database (7,000+ targets)
    - NZDPU (comprehensive database)
    - SEC climate filings (emerging)
    
    **Technical Data:**
    - IPCC AR6 mitigation assessments
    - IEA sectoral roadmaps
    - Academic LCA databases
    - Technology learning curves
    """)

with data_col2:
    st.markdown("""
    ### ⚠️ Data Gaps Requiring Research
    
    **Industry-Specific:**
    - Cross-sectoral interaction effects
    - Technology breakthrough probabilities
    - Regional constraint variations
    - Supply chain transformation rates
    
    **Economic Models:**
    - Dynamic cost curves by intervention
    - Policy impact quantification
    - Investment decision frameworks
    - Risk-adjusted feasibility bounds
    """)

with data_col3:
    st.markdown("""
    ### 🔄 Continuous Data Needs
    
    **Real-time Updates:**
    - Technology maturity progression
    - Policy landscape changes
    - Market transformation indicators
    - Corporate implementation results
    
    **Validation Requirements:**
    - Independent verification protocols
    - Peer review processes
    - Stakeholder feedback loops
    - Scientific advisory oversight
    """)

# Implementation roadmap
st.subheader("🗺️ Implementation Roadmap: From Research to Practice")

roadmap_data = pd.DataFrame([
    {"Phase": "Phase 1", "Timeline": "Year 1-2", "Activity": "Industry Materiality Mapping", 
     "Deliverable": "Cross-sectoral dependency database", "Stakeholders": "Corporates, Researchers"},
    {"Phase": "Phase 2", "Timeline": "Year 2-3", "Activity": "Maximum Potential Modeling", 
     "Deliverable": "Industry-specific constraint models", "Stakeholders": "Technical experts, SBTi"},
    {"Phase": "Phase 3", "Timeline": "Year 3-4", "Activity": "Dynamic Threshold Development", 
     "Deliverable": "Time-dependent residual frameworks", "Stakeholders": "Standards bodies, Policy makers"},
    {"Phase": "Phase 4", "Timeline": "Year 4-5", "Activity": "Verification Framework Design", 
     "Deliverable": "Automated verification systems", "Stakeholders": "Auditors, Technology providers"},
    {"Phase": "Phase 5", "Timeline": "Year 5+", "Activity": "Continuous Improvement", 
     "Deliverable": "Dynamic updating mechanisms", "Stakeholders": "All stakeholders"}
])

st.dataframe(roadmap_data, use_container_width=True, hide_index=True)

# Stakeholder engagement section
st.subheader("🤝 Stakeholder Engagement Strategy")

stakeholder_col1, stakeholder_col2 = st.columns(2)

with stakeholder_col1:
    st.markdown("""
    ### Key Stakeholder Groups
    
    **Corporate Partners:**
    - Leading companies in each target industry
    - Sustainability teams and C-suite executives
    - Supply chain and procurement managers
    - Investment and strategy decision-makers
    
    **Standards Organizations:**
    - Science Based Targets initiative (SBTi)
    - Greenhouse Gas Protocol (GHG Protocol)
    - International Organization for Standardization (ISO)
    - Task Force on Climate-related Disclosures (TCFD)
    """)

with stakeholder_col2:
    st.markdown("""
    ### Engagement Mechanisms
    
    **Research Collaboration:**
    - Industry-specific working groups
    - Technical advisory committees
    - Pilot implementation programs
    - Data sharing partnerships
    
    **Validation Processes:**
    - Expert peer review panels
    - Corporate feedback sessions
    - Academic publication process
    - Public consultation periods
    """)

# Expected outcomes and impact
st.subheader("🎯 Expected Outcomes and Impact")

impact_metrics = pd.DataFrame({
    'Metric': [
        'Industries with RF4 residual thresholds',
        'Companies using dynamic frameworks',
        'Reduction in offset gaming incidents',
        'Improvement in decarbonization investment efficiency',
        'Enhanced climate integrity scores'
    ],
    'Current State': ['0', '0', 'High (estimated 60%)', 'Low (estimated 30%)', 'Mixed credibility'],
    'Target (5 years)': ['6+ major industries', '1,000+ companies', '<10% gaming rate', '>80% efficiency', 'High credibility'],
    'Impact Mechanism': [
        'Systematic RF2→RF4 research program',
        'Standards adoption and corporate uptake', 
        'Science-based threshold enforcement',
        'Optimized investment frameworks',
        'Transparent verification systems'
    ]
})

st.dataframe(impact_metrics, use_container_width=True, hide_index=True)

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

**Contact:**
For research collaboration opportunities or technical questions about RF4 methodology, 
please contact the research team through the institutional channels.
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