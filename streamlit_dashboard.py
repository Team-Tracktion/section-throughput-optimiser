"""
Streamlit Dashboard for Railway Section Throughput Optimizer
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from main import RailwayOptimizer

# Page configuration
st.set_page_config(
    page_title="Railway Throughput Optimizer",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme color palette
COLORS = {
    'primary': '#ffffff',
    'secondary': '#e0e0e0',
    'accent': '#4a9eff',
    'success': '#4caf50',
    'warning': '#ff9800',
    'danger': '#f44336',
    'text': '#ffffff',
    'text_light': '#b0b0b0',
    'bg': '#0a0a0a',
    'bg_light': '#1a1a1a',
    'bg_dark': '#000000',
    'border': '#2a2a2a',
    'card_bg': '#1a1a1a'
}

# Custom CSS for dark theme styling
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}
    
    .stApp {{
        background-color: {COLORS['bg_dark']};
    }}
    
    .main .block-container {{
        background-color: {COLORS['bg_dark']};
        padding-top: 2rem;
    }}
    
    .main-header {{
        font-size: 2.5rem;
        font-weight: 600;
        color: {COLORS['text']};
        text-align: left;
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
        border-bottom: 2px solid {COLORS['border']};
        padding-bottom: 1rem;
    }}
    
    .section-header {{
        font-size: 1.5rem;
        font-weight: 600;
        color: {COLORS['text']};
        margin-top: 2rem;
        margin-bottom: 1rem;
    }}
    
    .sub-header {{
        font-size: 1.1rem;
        font-weight: 500;
        color: {COLORS['text']};
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }}
    
    .metric-container {{
        background-color: {COLORS['card_bg']};
        padding: 1.25rem;
        border-radius: 8px;
        border: 1px solid {COLORS['border']};
        margin-bottom: 1rem;
    }}
    
    .stMetric {{
        background-color: {COLORS['card_bg']};
        color: {COLORS['text']};
    }}
    
    .stMetric label {{
        color: {COLORS['text_light']} !important;
    }}
    
    .stMetric [data-testid="stMetricValue"] {{
        color: {COLORS['text']} !important;
    }}
    
    .stProgress > div > div > div {{
        background-color: {COLORS['accent']};
    }}
    
    .stDataFrame {{
        font-size: 0.9rem;
        background-color: {COLORS['card_bg']};
        color: {COLORS['text']};
    }}
    
    .stDataFrame table {{
        background-color: {COLORS['card_bg']} !important;
        color: {COLORS['text']} !important;
    }}
    
    .stDataFrame th {{
        background-color: {COLORS['bg_light']} !important;
        color: {COLORS['text']} !important;
    }}
    
    .stDataFrame td {{
        background-color: {COLORS['card_bg']} !important;
        color: {COLORS['text']} !important;
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: {COLORS['bg_light']};
        border-bottom: 1px solid {COLORS['border']};
    }}
    
    .stTabs [data-baseweb="tab"] {{
        padding: 12px 24px;
        font-weight: 500;
        color: {COLORS['text_light']} !important;
        background-color: {COLORS['bg_light']};
    }}
    
    .stTabs [aria-selected="true"] {{
        color: {COLORS['text']} !important;
        border-bottom: 2px solid {COLORS['accent']};
    }}
    
    .stSidebar {{
        background-color: {COLORS['bg_dark']} !important;
    }}
    
    .stSidebar [data-baseweb="base-input"] {{
        background-color: {COLORS['card_bg']} !important;
        color: {COLORS['text']} !important;
    }}
    
    .stSidebar label {{
        color: {COLORS['text']} !important;
    }}
    
    .stSidebar h1, .stSidebar h2, .stSidebar h3 {{
        color: {COLORS['text']} !important;
    }}
    
    .stMarkdown {{
        color: {COLORS['text']};
    }}
    
    .stHeader {{
        background-color: {COLORS['bg_dark']};
    }}
    
    .stHeader h1, .stHeader h2, .stHeader h3 {{
        color: {COLORS['text']} !important;
    }}
    
    .info-box {{
        background-color: {COLORS['card_bg']};
        padding: 1rem;
        border-left: 4px solid {COLORS['accent']};
        border-radius: 4px;
        margin: 1rem 0;
    }}
    
    div[data-baseweb="select"] > div {{
        background-color: {COLORS['card_bg']} !important;
        color: {COLORS['text']} !important;
    }}
    
    .stRadio label {{
        color: {COLORS['text']} !important;
    }}
    
    .stCheckbox label {{
        color: {COLORS['text']} !important;
    }}
    
    .stFileUploader {{
        background-color: {COLORS['card_bg']} !important;
    }}
    
    .stButton > button {{
        background-color: {COLORS['accent']} !important;
        color: {COLORS['text']} !important;
        border: none;
    }}
    
    .stButton > button:hover {{
        background-color: {COLORS['accent']} !important;
        opacity: 0.9;
    }}
    
    .stDownloadButton > button {{
        background-color: {COLORS['accent']} !important;
        color: {COLORS['text']} !important;
    }}
    
    .stSpinner {{
        color: {COLORS['accent']} !important;
    }}
    
    .stAlert {{
        background-color: {COLORS['card_bg']} !important;
        border: 1px solid {COLORS['border']} !important;
    }}
    
    .stAlert [data-testid="stMarkdownContainer"] {{
        color: {COLORS['text']} !important;
    }}
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def load_and_optimize(csv_path):
    """Load data and run optimization"""
    optimizer = RailwayOptimizer()
    df_input = optimizer.load_simulation_data(csv_path)
    df_optimized = optimizer.optimize_schedule()
    report = optimizer.generate_optimization_report()
    return df_input, df_optimized, report

def main():
    st.markdown('<h1 class="main-header">Railway Section Throughput Optimizer</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: {COLORS["text_light"]}; margin-bottom: 2rem;">Analytics and Optimization Dashboard for Mumbai Suburban Region</p>', unsafe_allow_html=True)
    
    # Sidebar for file upload
    with st.sidebar:
        st.header("Data Upload")
        uploaded_file = st.file_uploader(
            "Upload CSV file",
            type=['csv'],
            help="Upload train simulation data in CSV format"
        )
        
        # Or use default file
        use_default = st.checkbox("Use default sample data", value=True)
        
        if use_default:
            default_file = "train_simulation_output_before.csv"
            if Path(default_file).exists():
                csv_path = default_file
            else:
                st.error(f"Default file not found: {default_file}")
                st.stop()
        elif uploaded_file:
            # Save uploaded file temporarily
            with open("temp_upload.csv", "wb") as f:
                f.write(uploaded_file.getbuffer())
            csv_path = "temp_upload.csv"
        else:
            st.info("Please upload a CSV file or use default data")
            st.stop()
        
        st.divider()
        st.header("Settings")
        auto_refresh = st.checkbox("Auto-refresh on data change", value=True)
    
    # Main content
    if csv_path:
        try:
            with st.spinner("Loading and optimizing data..."):
                df_input, df_optimized, report = load_and_optimize(csv_path)
            
            # Key Metrics Row
            st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric(
                    "Total Trains",
                    report['total_trains'],
                    delta=None
                )
            
            with col2:
                efficiency_color = "normal"
                if report['efficiency_score'] >= 80:
                    efficiency_color = "normal"
                elif report['efficiency_score'] >= 60:
                    efficiency_color = "off"
                else:
                    efficiency_color = "inverse"
                
                st.metric(
                    "Efficiency Score",
                    f"{report['efficiency_score']:.1f}%",
                    delta=None
                )
                st.progress(report['efficiency_score'] / 100)
            
            with col3:
                st.metric(
                    "On-Time Rate",
                    f"{report['on_time_percentage']:.1f}%",
                    delta=f"{report['on_time_trains']} trains"
                )
            
            with col4:
                st.metric(
                    "Avg Delay",
                    f"{report['average_delay_minutes']:.2f} min",
                    delta=f"Max: {report['max_delay_minutes']:.1f} min"
                )
            
            with col5:
                st.metric(
                    "Avg Speed",
                    f"{report['average_speed_kmph']:.1f} km/h",
                    delta=None
                )
            
            st.divider()
            
            # Tabs for different views
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "Overview", "Train Types", "Stations", 
                "Lines", "Speed Analysis", "Raw Data"
            ])
            
            with tab1:
                st.markdown('<div class="section-header">System Overview</div>', unsafe_allow_html=True)
                
                # Row 1: Delay Analysis
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('<div class="sub-header">Delay Distribution Analysis</div>', unsafe_allow_html=True)
                    if 'delay_minutes' in df_optimized.columns and len(df_optimized) > 0:
                        delay_ranges = df_optimized['delay_minutes'].apply(
                            lambda x: 'On-Time (≤5min)' if x <= 5 else 
                                     ('Minor (5-10min)' if x <= 10 else 
                                     ('Moderate (10-20min)' if x <= 20 else 'Severe (>20min)'))
                        )
                        delay_counts = delay_ranges.value_counts()
                        
                        # Create more informative chart
                        delay_df = pd.DataFrame({
                            'Category': delay_counts.index,
                            'Count': delay_counts.values,
                            'Percentage': (delay_counts.values / len(df_optimized) * 100).round(1) # type: ignore
                        })
                        
                        fig_delay = px.bar(
                            delay_df,
                            x='Category',
                            y='Count',
                            text='Percentage',
                            color='Category',
                            color_discrete_map={
                                'On-Time (≤5min)': COLORS['success'],
                                'Minor (5-10min)': COLORS['warning'],
                                'Moderate (10-20min)': COLORS['accent'],
                                'Severe (>20min)': COLORS['danger']
                            }
                        )
                        fig_delay.update_traces(
                            texttemplate='%{text}%',
                            textposition='outside',
                            marker_line_color='rgba(255,255,255,0.2)',
                            marker_line_width=1
                        )
                        fig_delay.update_layout(
                            xaxis_title="Delay Category",
                            yaxis_title="Number of Records",
                            showlegend=False,
                            plot_bgcolor=COLORS['card_bg'],
                            paper_bgcolor=COLORS['bg_dark'],
                            font=dict(family='Inter', size=11, color=COLORS['text']),
                            height=400
                        )
                        fig_delay.update_xaxes(
                            gridcolor=COLORS['border'],
                            tickfont=dict(color=COLORS['text']),
                            title=dict(font=dict(color=COLORS['text']))
                        )
                        fig_delay.update_yaxes(
                            gridcolor=COLORS['border'],
                            tickfont=dict(color=COLORS['text']),
                            title=dict(font=dict(color=COLORS['text']))
                        )
                        st.plotly_chart(fig_delay, use_container_width=True)
                    else:
                        st.warning("No delay data available")
                    
                    # Delay statistics table
                    if 'delay_minutes' in df_optimized.columns and len(df_optimized) > 0:
                        st.markdown('<div class="sub-header">Delay Statistics</div>', unsafe_allow_html=True)
                        delay_stats = pd.DataFrame({
                            'Metric': ['Average', 'Median', 'Minimum', 'Maximum', 'Standard Deviation'],
                            'Value (minutes)': [
                                f"{df_optimized['delay_minutes'].mean():.2f}",
                                f"{df_optimized['delay_minutes'].median():.2f}",
                                f"{df_optimized['delay_minutes'].min():.2f}",
                                f"{df_optimized['delay_minutes'].max():.2f}",
                                f"{df_optimized['delay_minutes'].std():.2f}"
                            ]
                        })
                        st.dataframe(delay_stats, use_container_width=True, hide_index=True)
                
                with col2:
                    st.markdown('<div class="sub-header">Train Event Status Distribution</div>', unsafe_allow_html=True)
                    if 'event' in df_optimized.columns and len(df_optimized) > 0:
                        event_counts = df_optimized['event'].value_counts()
                        event_df = pd.DataFrame({
                            'Event': event_counts.index,
                            'Count': event_counts.values,
                            'Percentage': (event_counts.values / len(df_optimized) * 100).round(1) # type: ignore
                        })
                        
                        fig_event = px.bar(
                            event_df,
                            x='Event',
                            y='Count',
                            text='Percentage',
                            color='Count',
                            color_continuous_scale=['#e8f4f8', COLORS['accent']]
                        )
                        fig_event.update_traces(
                            texttemplate='%{text}%',
                            textposition='outside',
                            marker_line_color='rgba(255,255,255,0.2)',
                            marker_line_width=1
                        )
                        fig_event.update_layout(
                            xaxis_title="Event Type",
                            yaxis_title="Number of Records",
                            showlegend=False,
                            plot_bgcolor=COLORS['card_bg'],
                            paper_bgcolor=COLORS['bg_dark'],
                            font=dict(family='Inter', size=11, color=COLORS['text']),
                            height=400
                        )
                        fig_event.update_xaxes(
                            gridcolor=COLORS['border'],
                            tickfont=dict(color=COLORS['text']),
                            title=dict(font=dict(color=COLORS['text']))
                        )
                        fig_event.update_yaxes(
                            gridcolor=COLORS['border'],
                            tickfont=dict(color=COLORS['text']),
                            title=dict(font=dict(color=COLORS['text']))
                        )
                        st.plotly_chart(fig_event, use_container_width=True)
                        
                        # Event breakdown
                        st.markdown('<div class="sub-header">Event Breakdown</div>', unsafe_allow_html=True)
                        st.dataframe(event_df, use_container_width=True, hide_index=True)
                    else:
                        st.warning("No event data available")
                
                # Row 2: Performance metrics and conflicts
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('<div class="sub-header">Performance Metrics Summary</div>', unsafe_allow_html=True)
                    metrics_data = {
                        'Category': ['Delayed Trains (>5min)', 'Halted Trains', 'Rerouted Trains', 'On-Time Trains (≤5min)'],
                        'Count': [
                            report['delayed_trains'],
                            report['halted_trains'],
                            report['rerouted_trains'],
                            report['on_time_trains']
                        ],
                        'Percentage': [
                            f"{report['delayed_percentage']:.1f}%",
                            f"{report['halted_percentage']:.1f}%",
                            f"{report['rerouted_percentage']:.1f}%",
                            f"{report['on_time_percentage']:.1f}%"
                        ]
                    }
                    metrics_df = pd.DataFrame(metrics_data)
                    
                    # Create visual comparison
                    fig_metrics = px.bar(
                        metrics_df,
                        x='Category',
                        y='Count',
                        text='Percentage',
                        color='Count',
                        color_continuous_scale=['#ffcccc', COLORS['success']]
                    )
                    fig_metrics.update_traces(
                        texttemplate='%{text}',
                        textposition='outside',
                        marker_line_color='rgba(255,255,255,0.2)',
                        marker_line_width=1
                    )
                    fig_metrics.update_layout(
                        xaxis_title="",
                        yaxis_title="Number of Trains",
                        showlegend=False,
                        plot_bgcolor=COLORS['card_bg'],
                        paper_bgcolor=COLORS['bg_dark'],
                        font=dict(family='Inter', size=11, color=COLORS['text']),
                        height=350
                    )
                    fig_metrics.update_xaxes(
                        gridcolor=COLORS['border'],
                        tickangle=-45,
                        tickfont=dict(color=COLORS['text']),
                        title=dict(font=dict(color=COLORS['text']))
                    )
                    fig_metrics.update_yaxes(
                        gridcolor=COLORS['border'],
                        tickfont=dict(color=COLORS['text']),
                        title=dict(font=dict(color=COLORS['text']))
                    )
                    st.plotly_chart(fig_metrics, use_container_width=True)
                
                with col2:
                    st.markdown('<div class="sub-header">Conflict Detection and Resolution</div>', unsafe_allow_html=True)
                    conflict_data = {
                        'Type': list(report['conflict_types'].keys()),
                        'Count': list(report['conflict_types'].values())
                    }
                    if conflict_data['Type']:
                        conflict_df = pd.DataFrame(conflict_data)
                        conflict_df['Percentage'] = (conflict_df['Count'] / conflict_df['Count'].sum() * 100).round(1)
                        
                        fig_conflict = px.bar(
                            conflict_df,
                            x='Type',
                            y='Count',
                            text='Count',
                            color='Count',
                            color_continuous_scale=['#ffe5e5', COLORS['danger']]
                        )
                        fig_conflict.update_traces(
                            texttemplate='%{text}',
                            textposition='outside',
                            marker_line_color='rgba(255,255,255,0.2)',
                            marker_line_width=1
                        )
                        fig_conflict.update_layout(
                            xaxis_title="Conflict Type",
                            yaxis_title="Number of Conflicts",
                            showlegend=False,
                            plot_bgcolor=COLORS['card_bg'],
                            paper_bgcolor=COLORS['bg_dark'],
                            font=dict(family='Inter', size=11, color=COLORS['text']),
                            height=350
                        )
                        fig_conflict.update_xaxes(
                            gridcolor=COLORS['border'],
                            tickfont=dict(color=COLORS['text']),
                            title=dict(font=dict(color=COLORS['text']))
                        )
                        fig_conflict.update_yaxes(
                            gridcolor=COLORS['border'],
                            tickfont=dict(color=COLORS['text']),
                            title=dict(font=dict(color=COLORS['text']))
                        )
                        st.plotly_chart(fig_conflict, use_container_width=True)
                        
                        st.dataframe(conflict_df[['Type', 'Count', 'Percentage']], use_container_width=True, hide_index=True)
                    else:
                        st.info("No conflicts detected in the optimized schedule")
            
            with tab2:
                st.markdown('<div class="section-header">Train Type Performance Analysis</div>', unsafe_allow_html=True)
                
                # Train type statistics
                train_type_df = pd.DataFrame(report['train_type_performance']).T
                train_type_df = train_type_df.reset_index()
                train_type_df.columns = ['Train Type', 'Count', 'Avg Delay (min)', 'Avg Speed (km/h)', 
                                        'Delayed %', 'On-Time %']
                train_type_df = train_type_df.sort_values('Avg Delay (min)', ascending=True)
                
                # Summary metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    best_type = train_type_df.loc[train_type_df['On-Time %'].idxmax()]
                    st.metric(
                        "Best On-Time Performance",
                        f"{best_type['Train Type']}",
                        f"{best_type['On-Time %']:.1f}%"
                    )
                with col2:
                    worst_delay = train_type_df.loc[train_type_df['Avg Delay (min)'].idxmax()]
                    st.metric(
                        "Highest Average Delay",
                        f"{worst_delay['Train Type']}",
                        f"{worst_delay['Avg Delay (min)']:.2f} min"
                    )
                with col3:
                    fastest = train_type_df.loc[train_type_df['Avg Speed (km/h)'].idxmax()]
                    st.metric(
                        "Fastest Average Speed",
                        f"{fastest['Train Type']}",
                        f"{fastest['Avg Speed (km/h)']:.1f} km/h"
                    )
                
                st.divider()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('<div class="sub-header">Average Delay by Train Type</div>', unsafe_allow_html=True)
                    fig_delay_type = px.bar(
                        train_type_df,
                        x='Train Type',
                        y='Avg Delay (min)',
                        text='Avg Delay (min)',
                        color='Avg Delay (min)',
                        color_continuous_scale=['#cfe2ff', COLORS['danger']]
                    )
                    fig_delay_type.update_traces(
                        texttemplate='%{text:.2f} min',
                        textposition='outside',
                        marker_line_color='rgba(255,255,255,0.2)',
                        marker_line_width=1
                    )
                    fig_delay_type.update_layout(
                        xaxis_title="Train Type",
                        yaxis_title="Average Delay (minutes)",
                        showlegend=False,
                        plot_bgcolor=COLORS['card_bg'],
                        paper_bgcolor=COLORS['bg_dark'],
                        font=dict(family='Inter', size=11, color=COLORS['text']),
                        height=400
                    )
                    fig_delay_type.update_xaxes(
                        gridcolor=COLORS['border'],
                        tickfont=dict(color=COLORS['text']),
                        title=dict(font=dict(color=COLORS['text']))
                    )
                    fig_delay_type.update_yaxes(
                        gridcolor=COLORS['border'],
                        tickfont=dict(color=COLORS['text']),
                        title=dict(font=dict(color=COLORS['text']))
                    )
                    st.plotly_chart(fig_delay_type, use_container_width=True)
                
                with col2:
                    st.markdown('<div class="sub-header">Average Speed by Train Type</div>', unsafe_allow_html=True)
                    fig_speed_type = px.bar(
                        train_type_df,
                        x='Train Type',
                        y='Avg Speed (km/h)',
                        text='Avg Speed (km/h)',
                        color='Avg Speed (km/h)',
                        color_continuous_scale=['#e8f4f8', COLORS['accent']]
                    )
                    fig_speed_type.update_traces(
                        texttemplate='%{text:.1f} km/h',
                        textposition='outside',
                        marker_line_color='rgba(255,255,255,0.2)',
                        marker_line_width=1
                    )
                    fig_speed_type.update_layout(
                        xaxis_title="Train Type",
                        yaxis_title="Average Speed (km/h)",
                        showlegend=False,
                        plot_bgcolor=COLORS['card_bg'],
                        paper_bgcolor=COLORS['bg_dark'],
                        font=dict(family='Inter', size=11, color=COLORS['text']),
                        height=400
                    )
                    fig_speed_type.update_xaxes(
                        gridcolor=COLORS['border'],
                        tickfont=dict(color=COLORS['text']),
                        title=dict(font=dict(color=COLORS['text']))
                    )
                    fig_speed_type.update_yaxes(
                        gridcolor=COLORS['border'],
                        tickfont=dict(color=COLORS['text']),
                        title=dict(font=dict(color=COLORS['text']))
                    )
                    st.plotly_chart(fig_speed_type, use_container_width=True)
                
                # Combined comparison chart
                st.markdown('<div class="sub-header">Performance Comparison: Delay vs On-Time Rate</div>', unsafe_allow_html=True)
                fig_comparison = go.Figure()
                fig_comparison.add_trace(go.Scatter(
                    x=train_type_df['Avg Delay (min)'],
                    y=train_type_df['On-Time %'],
                    mode='markers+text',
                    text=train_type_df['Train Type'],
                    textposition="top center",
                    marker=dict(
                        size=train_type_df['Count'] * 2,
                        color=train_type_df['Count'],
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="Train Count")
                    ),
                    name='Train Types'
                ))
                fig_comparison.update_layout(
                    xaxis_title="Average Delay (minutes)",
                    yaxis_title="On-Time Rate (%)",
                    plot_bgcolor=COLORS['card_bg'],
                    paper_bgcolor=COLORS['bg_dark'],
                    font=dict(family='Inter', size=11, color=COLORS['text']),
                    height=450,
                    legend=dict(font=dict(color=COLORS['text']))
                )
                fig_comparison.update_xaxes(
                    gridcolor=COLORS['border'],
                    tickfont=dict(color=COLORS['text']),
                    title=dict(font=dict(color=COLORS['text']))
                )
                fig_comparison.update_yaxes(
                    gridcolor=COLORS['border'],
                    tickfont=dict(color=COLORS['text']),
                    title=dict(font=dict(color=COLORS['text']))
                )
                st.plotly_chart(fig_comparison, use_container_width=True)
                
                # Detailed table
                st.markdown('<div class="sub-header">Detailed Performance Metrics</div>', unsafe_allow_html=True)
                display_df = train_type_df.copy()
                display_df['Avg Delay (min)'] = display_df['Avg Delay (min)'].round(2)
                display_df['Avg Speed (km/h)'] = display_df['Avg Speed (km/h)'].round(1)
                display_df['Delayed %'] = display_df['Delayed %'].round(1)
                display_df['On-Time %'] = display_df['On-Time %'].round(1)
                st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            with tab3:
                st.markdown('<div class="section-header">Station Performance Analysis</div>', unsafe_allow_html=True)
                
                station_df = pd.DataFrame(report['station_stats']).T
                station_df = station_df.reset_index()
                station_df.columns = ['Station', 'Platforms', 'Occupancy', 'Utilization %', 
                                     'Trains', 'Avg Delay', 'Max Delay', 'Min Delay']
                station_df = station_df.sort_values('Avg Delay', ascending=False)
                
                # Key station metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    busiest_station = station_df.loc[station_df['Trains'].idxmax()]
                    st.metric(
                        "Busiest Station",
                        busiest_station['Station'], # type: ignore
                        f"{busiest_station['Trains']} trains"
                    )
                with col2:
                    highest_util = station_df.loc[station_df['Utilization %'].idxmax()]
                    st.metric(
                        "Highest Utilization",
                        highest_util['Station'], # type: ignore
                        f"{highest_util['Utilization %']:.1f}%"
                    )
                with col3:
                    worst_delay_station = station_df.loc[station_df['Avg Delay'].idxmax()]
                    st.metric(
                        "Highest Average Delay",
                        worst_delay_station['Station'], # type: ignore
                        f"{worst_delay_station['Avg Delay']:.2f} min"
                    )
                
                st.divider()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('<div class="sub-header">Platform Utilization by Station</div>', unsafe_allow_html=True)
                    fig_util = px.bar(
                        station_df,
                        x='Station',
                        y='Utilization %',
                        text='Utilization %',
                        color='Utilization %',
                        color_continuous_scale=['#fff3cd', COLORS['warning']]
                    )
                    fig_util.update_traces(
                        texttemplate='%{text:.1f}%',
                        textposition='outside',
                        marker_line_color='rgba(255,255,255,0.2)',
                        marker_line_width=1
                    )
                    fig_util.update_layout(
                        xaxis_title="Station",
                        yaxis_title="Platform Utilization (%)",
                        showlegend=False,
                        plot_bgcolor=COLORS['card_bg'],
                        paper_bgcolor=COLORS['bg_dark'],
                        font=dict(family='Inter', size=11, color=COLORS['text']),
                        height=400
                    )
                    fig_util.update_xaxes(
                        gridcolor=COLORS['border'],
                        tickangle=-45,
                        tickfont=dict(color=COLORS['text']),
                        title=dict(font=dict(color=COLORS['text']))
                    )
                    fig_util.update_yaxes(
                        gridcolor=COLORS['border'],
                        range=[0, 100],
                        tickfont=dict(color=COLORS['text']),
                        title=dict(font=dict(color=COLORS['text']))
                    )
                    st.plotly_chart(fig_util, use_container_width=True)
                    
                    # Platform capacity info
                    st.markdown('<div class="sub-header">Platform Capacity Overview</div>', unsafe_allow_html=True)
                    capacity_df = station_df[['Station', 'Platforms', 'Occupancy', 'Utilization %']].copy()
                    capacity_df['Available'] = capacity_df['Platforms'] - capacity_df['Occupancy']
                    st.dataframe(capacity_df, use_container_width=True, hide_index=True)
                
                with col2:
                    st.markdown('<div class="sub-header">Delay Performance by Station</div>', unsafe_allow_html=True)
                    fig_station_delay = go.Figure()
                    fig_station_delay.add_trace(go.Bar(
                        name='Average Delay',
                        x=station_df['Station'],
                        y=station_df['Avg Delay'],
                        marker_color=COLORS['danger'],
                        text=station_df['Avg Delay'].round(2),
                        textposition='outside'
                    ))
                    fig_station_delay.add_trace(go.Bar(
                        name='Max Delay',
                        x=station_df['Station'],
                        y=station_df['Max Delay'],
                        marker_color=COLORS['warning'],
                        text=station_df['Max Delay'].round(2),
                        textposition='outside'
                    ))
                    fig_station_delay.update_layout(
                        xaxis_title="Station",
                        yaxis_title="Delay (minutes)",
                        barmode='group',
                        plot_bgcolor=COLORS['card_bg'],
                        paper_bgcolor=COLORS['bg_dark'],
                        font=dict(family='Inter', size=11, color=COLORS['text']),
                        height=400,
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=COLORS['text']))
                    )
                    fig_station_delay.update_xaxes(
                        gridcolor=COLORS['border'],
                        tickangle=-45,
                        tickfont=dict(color=COLORS['text']),
                        title=dict(font=dict(color=COLORS['text']))
                    )
                    fig_station_delay.update_yaxes(
                        gridcolor=COLORS['border'],
                        tickfont=dict(color=COLORS['text']),
                        title=dict(font=dict(color=COLORS['text']))
                    )
                    st.plotly_chart(fig_station_delay, use_container_width=True)
                    
                    # Station delay statistics
                    st.markdown('<div class="sub-header">Station Delay Statistics</div>', unsafe_allow_html=True)
                    delay_stats_df = station_df[['Station', 'Avg Delay', 'Max Delay', 'Min Delay', 'Trains']].copy()
                    delay_stats_df = delay_stats_df.round(2)
                    st.dataframe(delay_stats_df, use_container_width=True, hide_index=True)
                
                # Comprehensive station table
                st.markdown('<div class="sub-header">Complete Station Performance Metrics</div>', unsafe_allow_html=True)
                display_station_df = station_df.copy()
                display_station_df = display_station_df.round(2)
                st.dataframe(display_station_df, use_container_width=True, hide_index=True)
            
            with tab4:
                st.markdown('<div class="section-header">Line Efficiency Analysis</div>', unsafe_allow_html=True)
                
                line_df = pd.DataFrame(report['line_efficiency']).T
                line_df = line_df.reset_index()
                line_df.columns = ['Line', 'Train Count', 'Avg Delay', 'Avg Speed', 'On-Time Rate']
                line_df = line_df.sort_values('On-Time Rate', ascending=False)
                
                # Key line metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    best_line = line_df.loc[line_df['On-Time Rate'].idxmax()]
                    st.metric(
                        "Best On-Time Performance",
                        best_line['Line'], # type: ignore
                        f"{best_line['On-Time Rate']:.1f}%"
                    )
                with col2:
                    most_used = line_df.loc[line_df['Train Count'].idxmax()]
                    st.metric(
                        "Most Utilized Line",
                        most_used['Line'], # type: ignore
                        f"{most_used['Train Count']} trains"
                    )
                with col3:
                    fastest_line = line_df.loc[line_df['Avg Speed'].idxmax()]
                    st.metric(
                        "Fastest Average Speed",
                        fastest_line['Line'], # type: ignore
                        f"{fastest_line['Avg Speed']:.1f} km/h"
                    )
                
                st.divider()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('<div class="sub-header">Train Distribution by Line</div>', unsafe_allow_html=True)
                    fig_line_dist = px.bar(
                        line_df,
                        x='Line',
                        y='Train Count',
                        text='Train Count',
                        color='Train Count',
                        color_continuous_scale=['#e8f4f8', COLORS['accent']]
                    )
                    fig_line_dist.update_traces(
                        texttemplate='%{text}',
                        textposition='outside',
                        marker_line_color='rgba(255,255,255,0.2)',
                        marker_line_width=1
                    )
                    fig_line_dist.update_layout(
                        xaxis_title="Railway Line",
                        yaxis_title="Number of Trains",
                        showlegend=False,
                        plot_bgcolor=COLORS['card_bg'],
                        paper_bgcolor=COLORS['bg_dark'],
                        font=dict(family='Inter', size=11, color=COLORS['text']),
                        height=400
                    )
                    fig_line_dist.update_xaxes(
                        gridcolor=COLORS['border'],
                        tickfont=dict(color=COLORS['text']),
                        title=dict(font=dict(color=COLORS['text']))
                    )
                    fig_line_dist.update_yaxes(
                        gridcolor=COLORS['border'],
                        tickfont=dict(color=COLORS['text']),
                        title=dict(font=dict(color=COLORS['text']))
                    )
                    st.plotly_chart(fig_line_dist, use_container_width=True)
                    
                    # Distribution percentages
                    line_df_pct = line_df.copy()
                    line_df_pct['Distribution %'] = (line_df_pct['Train Count'] / line_df_pct['Train Count'].sum() * 100).round(1)
                    st.dataframe(line_df_pct[['Line', 'Train Count', 'Distribution %']], use_container_width=True, hide_index=True)
                
                with col2:
                    st.markdown('<div class="sub-header">On-Time Performance by Line</div>', unsafe_allow_html=True)
                    fig_line_on_time = px.bar(
                        line_df,
                        x='Line',
                        y='On-Time Rate',
                        text='On-Time Rate',
                        color='On-Time Rate',
                        color_continuous_scale=['#d4edda', COLORS['success']]
                    )
                    fig_line_on_time.update_traces(
                        texttemplate='%{text:.1f}%',
                        textposition='outside',
                        marker_line_color='rgba(255,255,255,0.2)',
                        marker_line_width=1
                    )
                    fig_line_on_time.update_layout(
                        xaxis_title="Railway Line",
                        yaxis_title="On-Time Rate (%)",
                        showlegend=False,
                        plot_bgcolor=COLORS['card_bg'],
                        paper_bgcolor=COLORS['bg_dark'],
                        font=dict(family='Inter', size=11, color=COLORS['text']),
                        height=400
                    )
                    fig_line_on_time.update_xaxes(
                        gridcolor=COLORS['border'],
                        tickfont=dict(color=COLORS['text']),
                        title=dict(font=dict(color=COLORS['text']))
                    )
                    fig_line_on_time.update_yaxes(
                        gridcolor=COLORS['border'],
                        range=[0, 100],
                        tickfont=dict(color=COLORS['text']),
                        title=dict(font=dict(color=COLORS['text']))
                    )
                    st.plotly_chart(fig_line_on_time, use_container_width=True)
                    
                    # Line efficiency summary
                    efficiency_df = line_df[['Line', 'On-Time Rate', 'Avg Delay', 'Avg Speed']].copy()
                    efficiency_df = efficiency_df.round(2)
                    st.dataframe(efficiency_df, use_container_width=True, hide_index=True)
                
                # Comprehensive line comparison
                st.markdown('<div class="sub-header">Line Performance Comparison</div>', unsafe_allow_html=True)
                fig_line_comparison = go.Figure()
                fig_line_comparison.add_trace(go.Bar(
                    name='Average Delay (min)',
                    x=line_df['Line'],
                    y=line_df['Avg Delay'],
                    marker_color=COLORS['danger'],
                    text=line_df['Avg Delay'].round(2),
                    textposition='outside'
                ))
                fig_line_comparison.add_trace(go.Bar(
                    name='Average Speed (km/h)',
                    x=line_df['Line'],
                    y=line_df['Avg Speed'],
                    marker_color=COLORS['accent'],
                    text=line_df['Avg Speed'].round(1),
                    textposition='outside'
                ))
                fig_line_comparison.update_layout(
                    xaxis_title="Railway Line",
                    yaxis_title="Value",
                    barmode='group',
                    plot_bgcolor=COLORS['card_bg'],
                    paper_bgcolor=COLORS['bg_dark'],
                    font=dict(family='Inter', size=11, color=COLORS['text']),
                    height=450,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=COLORS['text']))
                )
                fig_line_comparison.update_xaxes(
                    gridcolor=COLORS['border'],
                    tickfont=dict(color=COLORS['text']),
                    title=dict(font=dict(color=COLORS['text']))
                )
                fig_line_comparison.update_yaxes(
                    gridcolor=COLORS['border'],
                    tickfont=dict(color=COLORS['text']),
                    title=dict(font=dict(color=COLORS['text']))
                )
                st.plotly_chart(fig_line_comparison, use_container_width=True)
                
                # Complete line details
                st.markdown('<div class="sub-header">Complete Line Performance Metrics</div>', unsafe_allow_html=True)
                display_line_df = line_df.copy()
                display_line_df = display_line_df.round(2)
                st.dataframe(display_line_df, use_container_width=True, hide_index=True)
            
            with tab5:
                st.markdown('<div class="section-header">Speed Analysis</div>', unsafe_allow_html=True)
                
                speed_stats = report['speed_stats']
                
                # Speed statistics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Average Speed", f"{speed_stats['avg']:.1f} km/h", help="Mean speed across all trains")
                with col2:
                    st.metric("Maximum Speed", f"{speed_stats['max']:.1f} km/h", help="Highest recorded speed")
                with col3:
                    st.metric("Minimum Speed", f"{speed_stats['min']:.1f} km/h", help="Lowest recorded speed")
                with col4:
                    st.metric("Median Speed", f"{speed_stats['median']:.1f} km/h", help="Median speed value")
                
                st.divider()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('<div class="sub-header">Speed Distribution Histogram</div>', unsafe_allow_html=True)
                    speeds = df_optimized[df_optimized['speed_kmph'] > 0]['speed_kmph']
                    
                    fig_speed_dist = px.histogram(
                        speeds,
                        nbins=25,
                        labels={'value': 'Speed (km/h)', 'count': 'Frequency'},
                        color_discrete_sequence=[COLORS['accent']]
                    )
                    fig_speed_dist.update_traces(
                        marker_line_color='rgba(255,255,255,0.2)',
                        marker_line_width=1
                    )
                    fig_speed_dist.update_layout(
                        xaxis_title="Speed (km/h)",
                        yaxis_title="Frequency",
                        plot_bgcolor=COLORS['card_bg'],
                        paper_bgcolor=COLORS['bg_dark'],
                        font=dict(family='Inter', size=11, color=COLORS['text']),
                        height=400,
                        showlegend=False
                    )
                    fig_speed_dist.update_xaxes(
                        gridcolor=COLORS['border'],
                        tickfont=dict(color=COLORS['text']),
                        title=dict(font=dict(color=COLORS['text']))
                    )
                    fig_speed_dist.update_yaxes(
                        gridcolor=COLORS['border'],
                        tickfont=dict(color=COLORS['text']),
                        title=dict(font=dict(color=COLORS['text']))
                    )
                    st.plotly_chart(fig_speed_dist, use_container_width=True)
                    
                    # Speed statistics table
                    speed_summary = pd.DataFrame({
                        'Statistic': ['Mean', 'Median', 'Std Dev', 'Min', 'Max', '25th Percentile', '75th Percentile'],
                        'Speed (km/h)': [
                            f"{speeds.mean():.1f}",
                            f"{speeds.median():.1f}",
                            f"{speeds.std():.1f}",
                            f"{speeds.min():.1f}",
                            f"{speeds.max():.1f}",
                            f"{speeds.quantile(0.25):.1f}",
                            f"{speeds.quantile(0.75):.1f}"
                        ]
                    })
                    st.dataframe(speed_summary, use_container_width=True, hide_index=True)
                
                with col2:
                    st.markdown('<div class="sub-header">Average Speed by Train Type</div>', unsafe_allow_html=True)
                    speed_by_type = df_optimized[df_optimized['speed_kmph'] > 0].groupby('train_type')['speed_kmph'].agg(['mean', 'std', 'count']).reset_index()
                    speed_by_type.columns = ['Train Type', 'Avg Speed', 'Std Dev', 'Count']
                    speed_by_type = speed_by_type.sort_values('Avg Speed', ascending=False)
                    
                    fig_speed_type = px.bar(
                        speed_by_type,
                        x='Train Type',
                        y='Avg Speed',
                        text='Avg Speed',
                        error_y='Std Dev',
                        color='Avg Speed',
                        color_continuous_scale=['#1a3a5c', COLORS['accent']]
                    )
                    fig_speed_type.update_traces(
                        texttemplate='%{text:.1f} km/h',
                        textposition='outside',
                        marker_line_color='rgba(255,255,255,0.2)',
                        marker_line_width=1
                    )
                    fig_speed_type.update_layout(
                        xaxis_title="Train Type",
                        yaxis_title="Average Speed (km/h)",
                        showlegend=False,
                        plot_bgcolor=COLORS['card_bg'],
                        paper_bgcolor=COLORS['bg_dark'],
                        font=dict(family='Inter', size=11, color=COLORS['text']),
                        height=400
                    )
                    fig_speed_type.update_xaxes(
                        gridcolor=COLORS['border'],
                        tickfont=dict(color=COLORS['text']),
                        title=dict(font=dict(color=COLORS['text']))
                    )
                    fig_speed_type.update_yaxes(
                        gridcolor=COLORS['border'],
                        tickfont=dict(color=COLORS['text']),
                        title=dict(font=dict(color=COLORS['text']))
                    )
                    st.plotly_chart(fig_speed_type, use_container_width=True)
                    
                    # Speed by type table
                    speed_by_type_display = speed_by_type.copy()
                    speed_by_type_display['Avg Speed'] = speed_by_type_display['Avg Speed'].round(1)
                    speed_by_type_display['Std Dev'] = speed_by_type_display['Std Dev'].round(1)
                    st.dataframe(speed_by_type_display, use_container_width=True, hide_index=True)
                
                # Speed vs Delay Analysis
                st.markdown('<div class="sub-header">Speed vs Delay Correlation Analysis</div>', unsafe_allow_html=True)
                speed_delay_df = df_optimized[df_optimized['speed_kmph'] > 0].copy()
                fig_speed_delay = px.scatter(
                    speed_delay_df,
                    x='speed_kmph',
                    y='delay_minutes',
                    color='train_type',
                    size='speed_kmph',
                    hover_data=['train_id'],
                    labels={'speed_kmph': 'Speed (km/h)', 'delay_minutes': 'Delay (minutes)'}
                )
                fig_speed_delay.update_layout(
                    xaxis_title="Speed (km/h)",
                    yaxis_title="Delay (minutes)",
                    plot_bgcolor=COLORS['card_bg'],
                    paper_bgcolor=COLORS['bg_dark'],
                    font=dict(family='Inter', size=11, color=COLORS['text']),
                    height=450,
                    legend=dict(font=dict(color=COLORS['text']))
                )
                fig_speed_delay.update_xaxes(
                    gridcolor=COLORS['border'],
                    tickfont=dict(color=COLORS['text']),
                    title=dict(font=dict(color=COLORS['text']))
                )
                fig_speed_delay.update_yaxes(
                    gridcolor=COLORS['border'],
                    tickfont=dict(color=COLORS['text']),
                    title=dict(font=dict(color=COLORS['text']))
                )
                st.plotly_chart(fig_speed_delay, use_container_width=True)
            
            with tab6:
                st.markdown('<div class="section-header">Raw Data View</div>', unsafe_allow_html=True)
                
                data_view = st.radio("Select data view", ["Optimized Data", "Input Data"], horizontal=True)
                
                if data_view == "Optimized Data":
                    st.markdown('<div class="sub-header">Optimized Train Schedule</div>', unsafe_allow_html=True)
                    
                    # Data summary
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Records", len(df_optimized))
                    with col2:
                        st.metric("Unique Trains", df_optimized['train_id'].nunique())
                    with col3:
                        st.metric("Date Range", f"{df_optimized['timestamp'].min()[:10]} to {df_optimized['timestamp'].max()[:10]}")
                    
                    # Dataframe with filters
                    st.dataframe(df_optimized, use_container_width=True, height=400)
                    
                    # Download button
                    csv = df_optimized.to_csv(index=False)
                    st.download_button(
                        label="Download Optimized Data (CSV)",
                        data=csv,
                        file_name="optimized_schedule.csv",
                        mime="text/csv"
                    )
                else:
                    st.markdown('<div class="sub-header">Input Train Schedule</div>', unsafe_allow_html=True)
                    
                    # Data summary
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Records", len(df_input))
                    with col2:
                        st.metric("Unique Trains", df_input['train_id'].nunique())
                    with col3:
                        st.metric("Date Range", f"{df_input['timestamp'].min()[:10]} to {df_input['timestamp'].max()[:10]}")
                    
                    st.dataframe(df_input, use_container_width=True, height=400)
            
            # Footer
            st.divider()
            st.markdown(f"""
            <div style='text-align: center; color: {COLORS['text_light']}; padding: 20px; font-family: Inter, sans-serif;'>
                <p style='margin: 0; font-weight: 500;'>Railway Section Throughput Optimizer Dashboard</p>
                <p style='margin: 5px 0 0 0; font-size: 0.9rem;'>Optimized for Mumbai Central to Thane route</p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error processing data: {str(e)}")
            st.exception(e)

if __name__ == "__main__":
    main()
