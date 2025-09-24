import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Set page config
st.set_page_config(
    page_title="Dynamic Residual Emissions: Why Static 11% Thresholds Fail",
    page_icon="🎯",
    layout="wide"
)

# Configure Altair
alt.data_transformers.disable_max_rows()

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
            'supply_chain_tiers': 4,
            'control_level': 'Limited - depends on thousands of farmers',
            'main_challenge': 'Farm-level methane emissions have biological floors that exceed 11% assumption'
        },
        'illustrative_scenarios': {
            'conservative_max_reduction': 75,  # 25% residual
            'ambitious_max_reduction': 85,    # 15% residual
            'breakthrough_max_reduction': 88,  # 12% residual
            'static_sbt_assumption': 89        # 11% residual
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
            'supply_chain_tiers': 3,
            'control_level': 'Very Limited - depends on customer behavior',
            'main_challenge': 'Cannot control decades of customer equipment use across multiple end-use sectors'
        },
        'illustrative_scenarios': {
            'conservative_max_reduction': 92,  # 8% residual
            'ambitious_max_reduction': 95,    # 5% residual
            'breakthrough_max_reduction': 97,  # 3% residual
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
            'supply_chain_tiers': 5,
            'control_level': 'Limited - depends on global supply chains',
            'main_challenge': 'Depends on consumer behavior and global supply chain transformation'
        },
        'illustrative_scenarios': {
            'conservative_max_reduction': 78,  # 22% residual
            'ambitious_max_reduction': 82,    # 18% residual
            'breakthrough_max_reduction': 85,  # 15% residual
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
            'supply_chain_tiers': 0,  # Different model
            'control_level': 'Indirect - through capital allocation',
            'main_challenge': 'Residual emissions depend entirely on portfolio company sector mix and their maximum potentials'
        },
        'illustrative_scenarios': {
            'conservative_max_reduction': 70,  # 30% residual
            'ambitious_max_reduction': 80,    # 20% residual
            'breakthrough_max_reduction': 85,  # 15% residual
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
            'supply_chain_tiers': 4,
            'control_level': 'Limited - depends on supplier capabilities',
            'main_challenge': 'Success depends on supplier decarbonization and customer behavior change'
        },
        'illustrative_scenarios': {
            'conservative_max_reduction': 80,  # 20% residual
            'ambitious_max_reduction': 85,    # 15% residual
            'breakthrough_max_reduction': 88,  # 12% residual
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

# Sidebar for industry selection
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
    static_data = pd.DataFrame({
        'Industry': [ind.replace(' ', '\n') for ind in industries],
        'Residual_Emissions': [11] * len(industries),
        'Type': ['Static 11%'] * len(industries)
    })
    
    static_chart = alt.Chart(static_data).mark_bar(color='red').encode(
        x=alt.X('Industry:N', title='Industry'),
        y=alt.Y('Residual_Emissions:Q', title='Residual Emissions (%)', scale=alt.Scale(domain=[0, 30])),
        tooltip=['Industry', 'Residual_Emissions']
    ).properties(
        title='SBTi Static Residuals',
        width=300,
        height=250
    )
    
    st.altair_chart(static_chart, use_container_width=True)
    
    st.markdown("""
    **Problems with Static Approach:**
    - ❌ Ignores industry-specific constraints
    - ❌ Same threshold despite 67-99% Scope 3 variation
    - ❌ No scientific basis for 11% across all sectors
    - ❌ Enables premature offset reliance
    """)

with col2:
    st.success("**RF2 Dynamic Approach: Industry-Specific Reality**")
    
    # Create dynamic comparison chart
    dynamic_data = []
    for ind, data in residual_industry_data.items():
        conservative_residual = 100 - data['illustrative_scenarios']['conservative_max_reduction']
        ambitious_residual = 100 - data['illustrative_scenarios']['ambitious_max_reduction']
        
        dynamic_data.extend([
            {'Industry': ind.replace(' ', '\n'), 'Residual_Emissions': conservative_residual, 'Scenario': 'Conservative'},
            {'Industry': ind.replace(' ', '\n'), 'Residual_Emissions': ambitious_residual, 'Scenario': 'Ambitious'}
        ])
    
    dynamic_df = pd.DataFrame(dynamic_data)
    
    dynamic_chart = alt.Chart(dynamic_df).mark_point(size=100).encode(
        x=alt.X('Industry:N', title='Industry'),
        y=alt.Y('Residual_Emissions:Q', title='Residual Emissions (%)', scale=alt.Scale(domain=[0, 30])),
        color=alt.Color('Scenario:N', scale=alt.Scale(range=['orange', 'green'])),
        tooltip=['Industry', 'Scenario', 'Residual_Emissions']
    ).properties(
        title='RF2 Industry-Specific Residuals',
        width=300,
        height=250
    )
    
    st.altair_chart(dynamic_chart, use_container_width=True)
    
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
    
    # Create complexity overview chart
    complexity_data = selected_data['rf2_complexity']
    
    # Create a simple bar chart showing key metrics
    complexity_metrics = [
        {'Factor': 'Supply Chain Tiers', 'Score': complexity_data.get('supply_chain_tiers', 3)},
        {'Factor': 'Scope 3 Dominance', 'Score': selected_data['scope3_percentage'] / 10},
        {'Factor': 'Control Level', 'Score': 2 if 'Limited' in complexity_data['control_level'] else 5}
    ]
    
    complexity_df = pd.DataFrame(complexity_metrics)
    
    complexity_chart = alt.Chart(complexity_df).mark_bar().encode(
        x=alt.X('Score:Q', title='Complexity Score'),
        y=alt.Y('Factor:N', title=''),
        color=alt.value('steelblue'),
        tooltip=['Factor', 'Score']
    ).properties(
        title='Industry Complexity Metrics',
        width=400,
        height=200
    )
    
    st.altair_chart(complexity_chart, use_container_width=True)

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
    
    # Create residual comparison chart
    scenario_data = pd.DataFrame({
        'Scenario': ['SBTi Static', 'Conservative RF2', 'Ambitious RF2', 'Breakthrough RF2'],
        'Residual': [static_residual, conservative_residual, ambitious_residual, breakthrough_residual],
        'Color': ['red', 'orange', 'green', 'blue']
    })
    
    scenario_chart = alt.Chart(scenario_data).mark_bar().encode(
        x=alt.X('Scenario:N', title=''),
        y=alt.Y('Residual:Q', title='Residual Emissions (%)'),
        color=alt.Color('Color:N', scale=None, legend=None),
        tooltip=['Scenario', 'Residual']
    ).properties(
        title=f"{selected_industry} Residual Emissions by Scenario",
        width=400,
        height=250
    )
    
    st.altair_chart(scenario_chart, use_container_width=True)

# Impact analysis
st.subheader("📊 The Impact of Dynamic vs. Static Residuals")

impact_col1, impact_col2 = st.columns(2)

with impact_col1:
    st.markdown("### Carbon Removal Requirements")
    
    company_emissions = st.number_input("Hypothetical Company Baseline Emissions (tCO2e/year)", 
                                       min_value=1000, max_value=10000000, value=100000, step=10000)
    
    static_removals = company_emissions * (static_residual / 100)
    conservative_removals = company_emissions * (conservative_residual / 100)
    ambitious_removals = company_emissions * (ambitious_residual / 100)
    breakthrough_removals = company_emissions * (breakthrough_residual / 100)
    
    removal_data = pd.DataFrame({
        'Scenario': ['SBTi Static', 'Conservative RF2', 'Ambitious RF2', 'Breakthrough RF2'],
        'Removals_Needed': [static_removals, conservative_removals, ambitious_removals, breakthrough_removals]
    })
    
    removal_chart = alt.Chart(removal_data).mark_bar().encode(
        x=alt.X('Scenario:N', title=''),
        y=alt.Y('Removals_Needed:Q', title='Required Removals (tCO2e/year)'),
        color=alt.Color('Scenario:N', scale=alt.Scale(range=['red', 'orange', 'green', 'blue'])),
        tooltip=['Scenario', 'Removals_Needed']
    ).properties(
        title='Required Carbon Removals',
        width=400,
        height=250
    )
    
    st.altair_chart(removal_chart, use_container_width=True)

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

intervention_df = pd.DataFrame(selected_data['key_interventions'])

col1, col2 = st.columns(2)

with col1:
    # Convert timeline to numeric for chart
    intervention_df['timeline_mid'] = intervention_df['timeline'].apply(
        lambda x: np.mean([int(i.split('-')[0]) for i in x.split() if i.split('-')[0].isdigit()])
    )
    
    # Convert potential to numeric (take average)
    intervention_df['potential_mid'] = intervention_df['potential'].apply(
        lambda x: np.mean([int(i) for i in x.replace('%', '').split('-')])
    )
    
    intervention_chart = alt.Chart(intervention_df).mark_circle(size=100).encode(
        x=alt.X('timeline_mid:Q', title='Implementation Timeline (years)'),
        y=alt.Y('potential_mid:Q', title='Emission Reduction Potential (%)'),
        color=alt.Color('scalability:N'),
        size=alt.condition(alt.datum.scalability == 'High', alt.value(150), alt.value(100)),
        tooltip=['name', 'potential', 'timeline', 'scalability']
    ).properties(
        title='Intervention Potential vs Timeline',
        width=400,
        height=250
    )
    
    st.altair_chart(intervention_chart, use_container_width=True)

with col2:
    st.markdown("### Available Interventions")
    for intervention in selected_data['key_interventions']:
        with st.expander(f"🔧 {intervention['name']}"):
            st.write(f"**Potential**: {intervention['potential']} emission reduction")
            st.write(f"**Timeline**: {intervention['timeline']} to implement")
            st.write(f"**Scalability**: {intervention['scalability']}")

# Timeline visualization
st.subheader("🕒 Evolution Timeline: From Static to Dynamic Residuals")

timeline_years = list(range(2025, 2051))
selected_scenarios = selected_data['illustrative_scenarios']

def sigmoid_residual(year, max_reduction, inflection_year=2035, steepness=0.3):
    """Create sigmoid curve showing residual emissions evolution"""
    t = year - 2025
    inflection_t = inflection_year - 2025
    base_residual = 100 - max_reduction
    current_residual = base_residual + (25 - base_residual) * np.exp(-steepness * (t - 5))
    return max(base_residual, min(25, current_residual))

# Create timeline data
timeline_data = []
for year in timeline_years:
    timeline_data.extend([
        {'Year': year, 'Residual': 11, 'Scenario': 'SBTi Static'},
        {'Year': year, 'Residual': sigmoid_residual(year, selected_scenarios['conservative_max_reduction']), 'Scenario': 'Conservative RF2'},
        {'Year': year, 'Residual': sigmoid_residual(year, selected_scenarios['ambitious_max_reduction']), 'Scenario': 'Ambitious RF2'},
        {'Year': year, 'Residual': sigmoid_residual(year, selected_scenarios['breakthrough_max_reduction']), 'Scenario': 'Breakthrough RF2'}
    ])

timeline_df = pd.DataFrame(timeline_data)

timeline_chart = alt.Chart(timeline_df).mark_line(strokeWidth=3).encode(
    x=alt.X('Year:O', title='Year'),
    y=alt.Y('Residual:Q', title='Residual Emissions (%)'),
    color=alt.Color('Scenario:N', scale=alt.Scale(range=['red', 'orange', 'green', 'blue'])),
    strokeDash=alt.condition(alt.datum.Scenario == 'SBTi Static', alt.value([5, 5]), alt.value([1])),
    tooltip=['Year', 'Scenario', 'Residual:Q']
).properties(
    title=f"{selected_industry}: Static vs Dynamic Residual Emissions (2025-2050)",
    width=700,
    height=400
)

st.altair_chart(timeline_chart, use_container_width=True)

# Research urgency analysis
st.subheader("🎯 Research Priority: Why This Matters Now")

urgency_col1, urgency_col2 = st.columns([2, 1])

with urgency_col1:
    # Create urgency matrix data
    urgency_data = []
    for ind, data in residual_industry_data.items():
        scope3_percentage = data['scope3_percentage']
        guidance_gap = (100 - data['illustrative_scenarios']['conservative_max_reduction']) - 11
        urgency_data.append({
            'Industry': ind,
            'Scope3_Dominance': scope3_percentage,
            'Guidance_Gap': guidance_gap
        })
    
    urgency_df = pd.DataFrame(urgency_data)
    
    urgency_chart = alt.Chart(urgency_df).mark_circle(size=200).encode(
        x=alt.X('Scope3_Dominance:Q', title='Scope 3 Dominance (%)'),
        y=alt.Y('Guidance_Gap:Q', title='Static Threshold Gap (percentage points)'),
        color=alt.condition(
            alt.expr('datum.Scope3_Dominance > 80 && datum.Guidance_Gap > 0'),
            alt.value('red'),
            alt.value('steelblue')
        ),
        tooltip=['Industry', 'Scope3_Dominance', 'Guidance_Gap']
    ).properties(
        title='Research Urgency Matrix',
        width=400,
        height=300
    )
    
    # Add reference lines
    ref_lines = alt.Chart(pd.DataFrame({'x': [80], 'y': [0]})).mark_rule(strokeDash=[5, 5], color='gray').encode(
        x='x:Q'
    ) + alt.Chart(pd.DataFrame({'x': [0], 'y': [0]})).mark_rule(strokeDash=[5, 5], color='gray').encode(
        y='y:Q'
    )
    
    st.altair_chart(urgency_chart + ref_lines, use_container_width=True)

with urgency_col2:
    st.markdown("### Research Impact")
    
    current_gap = abs(conservative_residual - static_residual)
    
    st.metric("Static Threshold Error", f"{current_gap:.1f}%", 
             help="Difference between industry reality and SBTi assumption")
    
    removal_cost_default = 400
    static_cost_default = company_emissions * (static_residual / 100) * removal_cost_default
    conservative_cost_default = company_emissions * (conservative_residual / 100) * removal_cost_default
    
    st.markdown(f"""
    **Business Impact:**
    - **Planning uncertainty**: ${abs(conservative_cost_default - static_cost_default):,.0f}/year
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

# Expected outcomes
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
