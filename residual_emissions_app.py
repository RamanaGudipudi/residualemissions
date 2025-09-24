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
@st.cache_data
def load_industry_data():
    """Load industry data with caching to improve performance"""
    return {
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

# Load data
residual_industry_data = load_industry_data()

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
    
    # Create static comparison chart - Fixed version
    try:
        industries = list(residual_industry_data.keys())
        static_values = [11] * len(industries)
        
        fig_static = go.Figure(data=[
            go.Bar(
                x=[ind.replace(' & ', '\n& ').replace(' ', '\n') for ind in industries], 
                y=static_values, 
                marker_color='red', 
                name='Static 11% Residual'
            )
        ])
        
        fig_static.update_layout(
            title="SBTi Static Residuals",
            yaxis_title="Residual Emissions (%)",
            height=350,
            showlegend=False,
            margin=dict(l=40, r=40, t=60, b=100)  # Add bottom margin for labels
        )
        
        fig_static.add_annotation(
            x=2, y=15,
            text="Same threshold<br>for all industries!",
            showarrow=True,
            arrowhead=2,
            arrowcolor="red"
        )
        
        st.plotly_chart(fig_static, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error creating static chart: {e}")
        # Fallback to simple metrics
        st.metric("All Industries", "11% Residual", help="SBTi applies the same threshold everywhere")
    
    st.markdown("""
    **Problems with Static Approach:**
    - ❌ Ignores industry-specific constraints
    - ❌ Same threshold despite 67-99% Scope 3 variation
    - ❌ No scientific basis for 11% across all sectors
    - ❌ Enables premature offset reliance
    """)

with col2:
    st.success("**RF2 Dynamic Approach: Industry-Specific Reality**")
    
    # Create dynamic comparison chart - Fixed version
    try:
        industries = list(residual_industry_data.keys())
        conservative_residuals = [100 - data['illustrative_scenarios']['conservative_max_reduction'] 
                                for data in residual_industry_data.values()]
        ambitious_residuals = [100 - data['illustrative_scenarios']['ambitious_max_reduction'] 
                              for data in residual_industry_data.values()]
        
        fig_dynamic = go.Figure()
        
        # Add bars with error bars showing range
        fig_dynamic.add_trace(go.Bar(
            x=[ind.replace(' & ', '\n& ').replace(' ', '\n') for ind in industries],
            y=ambitious_residuals,
            error_y=dict(
                type='data',
                array=[c - a for c, a in zip(conservative_residuals, ambitious_residuals)],
                visible=True
            ),
            marker_color='green',
            name='RF2 Dynamic Range'
        ))
        
        fig_dynamic.update_layout(
            title="RF2 Industry-Specific Residuals",
            yaxis_title="Residual Emissions (%)",
            height=350,
            showlegend=False,
            margin=dict(l=40, r=40, t=60, b=100)
        )
        
        st.plotly_chart(fig_dynamic, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error creating dynamic chart: {e}")
        # Fallback display
        for industry, data in residual_industry_data.items():
            conservative_residual = 100 - data['illustrative_scenarios']['conservative_max_reduction']
            st.metric(industry, f"{conservative_residual}%", help="Industry-specific residual threshold")
    
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
    
    # Simplified complexity visualization - avoid radar chart issues
    try:
        # Create a bar chart instead of radar for better compatibility
        complexity_factors = []
        complexity_scores = []
        
        for key, value in complexity_data.items():
            if key == 'main_challenge':
                continue
            complexity_factors.append(key.replace('_', ' ').title())
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
        
        fig_complexity = go.Figure(data=[
            go.Bar(x=complexity_factors, y=complexity_scores, 
                   marker_color=['red' if s > 7 else 'orange' if s > 5 else 'green' for s in complexity_scores])
        ])
        
        fig_complexity.update_layout(
            title="Industry Complexity Factors (Higher = More Challenging)",
            yaxis_title="Complexity Score",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig_complexity, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error creating complexity chart: {e}")
        # Fallback to simple display
        st.write("**Complexity Factors:**")
        for key, value in complexity_data.items():
            if key != 'main_challenge':
                st.write(f"• **{key.replace('_', ' ').title()}**: {value}")

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
    
    # Create residual comparison - Fixed version
    try:
        scenarios = ['SBTi Static', 'Conservative RF2', 'Ambitious RF2', 'Breakthrough RF2']
        residuals = [static_residual, conservative_residual, ambitious_residual, breakthrough_residual]
        colors = ['red', '#ff7f0e', '#2ca02c', '#1f77b4']
        
        fig_scenarios = go.Figure(data=[
            go.Bar(x=scenarios, y=residuals, marker_color=colors)
        ])
        
        fig_scenarios.update_layout(
            title=f"{selected_industry} Residual Emissions by Scenario",
            yaxis_title="Residual Emissions (%)",
            height=350,
            showlegend=False
        )
        
        # Add annotations showing the range
        fig_scenarios.add_annotation(
            x=1.5, y=max(residuals) + 2,
            text=f"RF2 Range: {breakthrough_residual:.1f}% - {conservative_residual:.1f}%",
            showarrow=False,
            font=dict(size=12, color="green")
        )
        
        st.plotly_chart(fig_scenarios, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error creating scenario chart: {e}")
        # Fallback metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("SBTi Static", f"{static_residual}%")
        with col2:
            st.metric("Conservative RF2", f"{conservative_residual:.1f}%")
        with col3:
            st.metric("Ambitious RF2", f"{ambitious_residual:.1f}%")
        with col4:
            st.metric("Breakthrough RF2", f"{breakthrough_residual:.1f}%")

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
    
    # Create removal comparison - Fixed version
    try:
        removal_data = pd.DataFrame({
            'Scenario': ['SBTi Static', 'Conservative RF2', 'Ambitious RF2', 'Breakthrough RF2'],
            'Removals_Needed': [static_removals, conservative_removals, ambitious_removals, breakthrough_removals]
        })
        
        colors_map = {'SBTi Static': 'red', 'Conservative RF2': '#ff7f0e', 
                     'Ambitious RF2': '#2ca02c', 'Breakthrough RF2': '#1f77b4'}
        
        fig_removals = px.bar(removal_data, x='Scenario', y='Removals_Needed', 
                             color='Scenario', color_discrete_map=colors_map)
        fig_removals.update_layout(title="Required Carbon Removals (tCO2e/year)", showlegend=False, height=350)
        
        st.plotly_chart(fig_removals, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error creating removals chart: {e}")
        # Fallback metrics
        st.metric("SBTi Static Removals", f"{static_removals:,.0f} tCO2e/year")
        st.metric("Conservative RF2 Removals", f"{conservative_removals:,.0f} tCO2e/year")

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

# Create interventions dataframe with better error handling
try:
    intervention_data = pd.DataFrame(selected_data['key_interventions'])
    
    # Extract numeric values from potential ranges
    def extract_numeric_midpoint(range_str):
        """Extract midpoint from ranges like '30-50%'"""
        try:
            if '-' in range_str:
                low, high = range_str.replace('%', '').split('-')
                return (float(low) + float(high)) / 2
            else:
                return float(range_str.replace('%', ''))
        except:
            return 50  # Default value
    
    def extract_timeline_midpoint(timeline_str):
        """Extract midpoint from timelines like '5-10 years'"""
        try:
            if '-' in timeline_str:
                low, high = timeline_str.replace(' years', '').split('-')
                return (float(low) + float(high)) / 2
            else:
                return float(timeline_str.replace(' years', ''))
        except:
            return 10  # Default value
    
    intervention_data['potential_numeric'] = intervention_data['potential'].apply(extract_numeric_midpoint)
    intervention_data['timeline_numeric'] = intervention_data['timeline'].apply(extract_timeline_midpoint)
    
    # Map scalability to numeric values
    scalability_map = {'High': 100, 'Medium': 60, 'Low': 30, 'Variable': 50}
    intervention_data['scalability_numeric'] = intervention_data['scalability'].map(scalability_map)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Intervention potential vs timeline - Fixed version
        try:
            fig_interventions = px.scatter(intervention_data, 
                                          x='timeline_numeric', y='potential_numeric', 
                                          size='scalability_numeric', 
                                          color='scalability',
                                          hover_name='name',
                                          title="Intervention Potential vs Timeline")
            
            fig_interventions.update_xaxes(title="Implementation Timeline (years)")
            fig_interventions.update_yaxes(title="Emission Reduction Potential (%)")
            fig_interventions.update_layout(height=400)
            
            st.plotly_chart(fig_interventions, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error creating interventions chart: {e}")
            # Fallback table
            st.dataframe(intervention_data[['name', 'potential', 'timeline', 'scalability']])
    
    with col2:
        st.markdown("### Available Interventions")
        for intervention in selected_data['key_interventions']:
            with st.expander(f"🔧 {intervention['name']}"):
                st.write(f"**Potential**: {intervention['potential']} emission reduction")
                st.write(f"**Timeline**: {intervention['timeline']} to implement")
                st.write(f"**Scalability**: {intervention['scalability']}")

except Exception as e:
    st.error(f"Error processing intervention data: {e}")
    # Simple fallback display
    st.markdown("### Available Interventions")
    for intervention in selected_data['key_interventions']:
        st.write(f"• **{intervention['name']}**: {intervention['potential']} potential, {intervention['timeline']} timeline")

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
