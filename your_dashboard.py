import pandas as pd
import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import calendar

# ================================
# Load dataset
# ================================
df = pd.read_csv(r"C:\Users\Sejal Rane\Downloads\climate_dvp.csv")
df['Day'] = pd.to_datetime(df['Day'], errors='coerce')
df['Month'] = df['Day'].dt.month  # Month column for monthly histogram

# Aggregate annual data
annual_df = df.groupby(['Entity', 'Year']).agg({
    'Annual average surface temp': 'first',
    'Annual precipitation': 'first',
    'Annual CO₂ emissions growth (abs)': 'first'
}).reset_index()

countries = df['Entity'].unique()

# ================================
# App Initialization
# ================================
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Global Climatic Change Dashboard"

# ================================
# Layout
# ================================
app.layout = html.Div([
    # Toggle button
    html.Button("☰ Filters", id="toggle-sidebar",
                style={"position": "fixed", "top": "10px", "left": "10px",
                       "zIndex": "3", "padding": "8px", "backgroundColor": "#1f77b4",
                       "color": "white", "border": "none", "borderRadius": "5px",
                       "cursor": "pointer"}),

    # Sidebar
    html.Div(id="sidebar", children=[
        html.H2("Filters", style={'textAlign': 'center', "color": "#1f77b4"}),

        # Theme toggle
        html.Label("Theme:", style={"fontWeight": "bold", "fontSize": "18px"}),
        dcc.RadioItems(
            id='theme-toggle',
            options=[{"label": "Light", "value": "light"},
                     {"label": "Dark", "value": "dark"}],
            value="light",
            labelStyle={"display": "inline-block", "marginRight": "10px", "fontSize": "16px"},
            style={"marginBottom": "20px"}
        ),

        # Country Dropdown
        html.Label("Country:", style={"fontWeight": "bold", "fontSize": "18px"}),
        dcc.Dropdown(
            id='entity-dropdown',
            options=[{'label': i, 'value': i} for i in countries],
            value=[countries[0]],
            multi=True,
            style={"marginBottom": "15px"}
        ),

        # Year Range Slider
        html.Label("Select Year Range:", style={"fontWeight": "bold", "fontSize": "18px"}),
        dcc.RangeSlider(
            id='year-slider',
            min=df['Year'].min(),
            max=df['Year'].max(),
            value=[df['Year'].min(), df['Year'].max()],
            marks={int(i): str(int(i)) for i in range(df['Year'].min(), df['Year'].max() + 1, 5)},
            step=1,
            tooltip={"placement": "bottom", "always_visible": False}
        )
    ], style={"width": "0"}),  # start collapsed

    # Main content
      html.Div(id="main-content", children=[
        # Dashboard Header Card - UPDATED LAYOUT
        html.Div([
            # Centered Title and Description
            html.Div([
                html.H1("🌍 Global Climatic Change Dashboard",
                    style={"margin": "0", "fontSize": "36px", "fontWeight": "bold", "color": "white", "textAlign": "center", "width": "100%"}),
                html.P("An interactive platform to visualize climate trends across countries and years",
                    style={"margin": "28px 0 0", "fontSize": "18px", "color": "rgba(255,255,255,0.9)", "textAlign": "center", "width": "100%"}),
                html.P("Explore temperature variations, precipitation patterns, and CO₂ emissions growth with advanced visualizations",
                    style={"margin": "5px 0 20px", "fontSize": "18px", "color": "rgba(255,255,255,0.8)", "textAlign": "center", "width": "100%"})
            ], style={"width": "100%", "padding": "20px"}),
            
            # Metrics Row - Centered
            html.Div([
                html.Div([
                    html.Div("🌡️", style={"fontSize": "30px", "marginRight": "10px"}),
                    html.Div([
                        html.H4("Global Temp", style={"margin": "0", "fontSize": "16px", "color": "white", "textAlign": "center"}),
                        html.H3(id="global-temp-value", style={"margin": "0", "fontSize": "24px", "color": "white", "textAlign": "center"})
                    ])
                ], style={"display": "flex", "flexDirection": "column", "alignItems": "center", "justifyContent": "center", "margin": "0 20px"}),
                
                html.Div([
                    html.Div("💧", style={"fontSize": "30px", "marginRight": "10px"}),
                    html.Div([
                        html.H4("Avg Rainfall", style={"margin": "0", "fontSize": "16px", "color": "white", "textAlign": "center"}),
                        html.H3(id="global-rain-value", style={"margin": "0", "fontSize": "24px", "color": "white", "textAlign": "center"})
                    ])
                ], style={"display": "flex", "flexDirection": "column", "alignItems": "center", "justifyContent": "center", "margin": "0 20px"}),
                
                html.Div([
                    html.Div("🏭", style={"fontSize": "30px", "marginRight": "10px"}),
                    html.Div([
                        html.H4("CO₂ Growth", style={"margin": "0", "fontSize": "16px", "color": "white", "textAlign": "center"}),
                        html.H3(id="global-co2-value", style={"margin": "0", "fontSize": "24px", "color": "white", "textAlign": "center"})
                    ])
                ], style={"display": "flex", "flexDirection": "column", "alignItems": "center", "justifyContent": "center", "margin": "0 20px"})
            ], style={"display": "flex", "justifyContent": "center", "width": "100%", "padding": "0 0 20px 0"})
        ], style={
            "display": "flex", 
            "flexDirection": "column",
            "alignItems": "center",
            "backgroundColor": "#1f77b4", 
            "borderRadius": "12px", 
            "marginBottom": "25px",
            "boxShadow": "0 4px 20px rgba(0,0,0,0.15)"
        }),


        # Row 1: Donut charts
        html.Div([
            html.Div([
                html.Div([
                    html.H4("🌡️ Temperature Distribution", style={"marginBottom": "10px", "color": "#1f77b4", "textAlign": "center"}),
                    dcc.Graph(id='temp-donut', style={'height': '350px'}),
                    html.P("Proportional distribution of average annual temperature across selected countries", 
                           style={"fontSize": "20px", "color": "#555", "textAlign": "center", "padding": "0 10px", "marginTop": "10px"})
                ], style={
                    "backgroundColor": "white",
                    "padding": "15px",
                    "borderRadius": "8px",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
                    "height": "100%"
                })
            ], style={'flex': '1', 'padding': '10px'}),
            
            html.Div([
                html.Div([
                    html.H4("💧 Rainfall Distribution", style={"marginBottom": "10px", "color": "#1f77b4", "textAlign": "center"}),
                    dcc.Graph(id='precip-donut', style={'height': '350px'}),
                    html.P("Proportional distribution of total annual rainfall across selected countries", 
                           style={"fontSize": "20px", "color": "#555", "textAlign": "center", "padding": "0 10px", "marginTop": "10px"})
                ], style={
                    "backgroundColor": "white",
                    "padding": "15px",
                    "borderRadius": "8px",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
                    "height": "100%"
                })
            ], style={'flex': '1', 'padding': '10px'}),
            
            html.Div([
                html.Div([
                    html.H4("🏭 CO₂ Emissions Distribution", style={"marginBottom": "10px", "color": "#1f77b4", "textAlign": "center"}),
                    dcc.Graph(id='co2-donut', style={'height': '350px'}),
                    html.P("Proportional distribution of CO₂ emissions growth across selected countries", 
                           style={"fontSize": "20px", "color": "#555", "textAlign": "center", "padding": "0 10px", "marginTop": "10px"})
                ], style={
                    "backgroundColor": "white",
                    "padding": "15px",
                    "borderRadius": "8px",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
                    "height": "100%"
                })
            ], style={'flex': '1', 'padding': '10px'})
        ], style={'display': 'flex', 'width': '100%', 'marginBottom': '20px'}),

        # Insight Cards (moved below donut charts)
        html.Div([
            html.Div([
                html.Div([
                    html.H4("🌡️ Temperature Insights", style={"marginBottom": "15px", "color": "#1f77b4", "display": "flex", "alignItems": "center", "justifyContent": "center"}),
                    html.Div([
                        html.Div([
                            dcc.Graph(id='temp-trend-mini', config={'displayModeBar': False}, 
                                     style={'height': '80px', 'width': '100%'})
                        ], style={'width': '40%', 'paddingRight': '10px'}),
                        html.Div([
                            html.P(id="temp-insight", children="", style={"fontSize": "14px", "color": "#333", "margin": "5px 0"})
                        ], style={'width': '60%'})
                    ], style={"display": "flex"})
                ], style={
                    "backgroundColor": "#f9f9f9",
                    "padding": "15px",
                    "borderRadius": "8px",
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                    "marginTop": "10px"
                })
            ], style={'flex': '1', 'padding': '10px'}),
            
            html.Div([
                html.Div([
                    html.H4("💧 Rainfall Insights", style={"marginBottom": "15px", "color": "#1f77b4", "display": "flex", "alignItems": "center", "justifyContent": "center"}),
                    html.Div([
                        html.Div([
                            dcc.Graph(id='precip-trend-mini', config={'displayModeBar': False}, 
                                     style={'height': '80px', 'width': '100%'})
                        ], style={'width': '40%', 'paddingRight': '10px'}),
                        html.Div([
                            html.P(id="precip-insight", children="", style={"fontSize": "14px", "color": "#333", "margin": "5px 0"})
                        ], style={'width': '60%'})
                    ], style={"display": "flex"})
                ], style={
                    "backgroundColor": "#f9f9f9",
                    "padding": "15px",
                    "borderRadius": "8px",
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                    "marginTop": "10px"
                })
            ], style={'flex': '1', 'padding': '10px'}),
            
            html.Div([
                html.Div([
                    html.H4("🏭 CO₂ Emissions Insights", style={"marginBottom": "15px", "color": "#1f77b4", "display": "flex", "alignItems": "center", "justifyContent": "center"}),
                    html.Div([
                        html.Div([
                            dcc.Graph(id='co2-trend-mini', config={'displayModeBar': False}, 
                                     style={'height': '80px', 'width': "100%"})
                        ], style={'width': '40%', 'paddingRight': '10px'}),
                        html.Div([
                            html.P(id="co2-insight", children="", style={"fontSize": "14px", "color": "#333", "margin": "5px 0"})
                        ], style={'width': '60%'})
                    ], style={"display": "flex"})
                ], style={
                    "backgroundColor": "#f9f9f9",
                    "padding": "15px",
                    "borderRadius": "8px",
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                    "marginTop": "10px"
                })
            ], style={'flex': '1', 'padding': '10px'})
        ], style={'display': 'flex', 'width': '100%', 'marginBottom': '20px'}),

        # Row 2: World Map + Correlation Heatmap
        html.Div([
            html.Div([
                html.Div([
                    html.H4("🌎 Global Temperature Map", style={"marginBottom": "10px", "color": "#1f77b4", "textAlign": "center"}),
                    dcc.Graph(id='world-map', style={'height': '500px'}),
                    html.P("Choropleth map showing average annual surface temperature changes across countries", 
                           style={"fontSize": "20px", "color": "#555", "textAlign": "center", "padding": "0 10px", "marginTop": "10px"})
                ], style={
                    "backgroundColor": "white",
                    "padding": "15px",
                    "borderRadius": "8px",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
                    "height": "100%"
                })
            ], style={'flex': '1', 'padding': '10px'}),
            
            html.Div([
                html.Div([
                    html.H4("📊 Climate Indicators Correlation", style={"marginBottom": "10px", "color": "#1f77b4", "textAlign": "center"}),
                    dcc.Graph(id='precipitation-hist', style={'height': '500px'}),
                    html.P("Heatmap showing correlation between temperature, precipitation, and CO₂ emissions", 
                           style={"fontSize": "20px", "color": "#555", "textAlign": "center", "padding": "0 10px", "marginTop": "10px"})
                ], style={
                    "backgroundColor": "white",
                    "padding": "15px",
                    "borderRadius": "8px",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
                    "height": "100%"
                })
            ], style={'flex': '1', 'padding': '10px'})
        ], style={'display': 'flex', 'width': '100%', 'marginBottom': '20px'}),

        # Row 3: Four charts
        html.Div([
            html.Div([
                html.Div([
                    html.H4("📈 CO₂ Emissions Trend", style={"marginBottom": "10px", "color": "#1f77b4", "textAlign": "center"}),
                    dcc.Graph(id='co2-growth', style={'height': '300px'}),
                    html.P("Annual CO₂ emissions growth trend for selected countries over time", 
                           style={"fontSize": "20px", "color": "#555", "textAlign": "center", "padding": "0 10px", "marginTop": "10px"})
                ], style={
                    "backgroundColor": "white",
                    "padding": "15px",
                    "borderRadius": "8px",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
                    "height": "100%"
                })
            ], style={'flex': '1', 'padding': '10px'}),
            
            html.Div([
                html.Div([
                    html.H4("📊 Temperature Distribution", style={"marginBottom": "10px", "color": "#1f77b4", "textAlign": "center"}),
                    dcc.Graph(id='avg-temp-hist', style={'height': '300px'}),
                    html.P("Distribution of average annual temperatures across selected countries and years", 
                           style={"fontSize": "20px", "color": "#555", "textAlign": "center", "padding": "0 10px", "marginTop": "10px"})
                ], style={
                    "backgroundColor": "white",
                    "padding": "15px",
                    "borderRadius": "8px",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
                    "height": "100%"
                })
            ], style={'flex': '1', 'padding': '10px'}),
            
            html.Div([
                html.Div([
                    html.H4("💧 Annual Rainfall", style={"marginBottom": "10px", "color": "#1f77b4", "textAlign": "center"}),
                    dcc.Graph(id='annual-precipitation', style={'height': '300px'}),
                    html.P("Annual rainfall patterns for selected countries across the selected time period", 
                           style={"fontSize": "20px", "color": "#555", "textAlign": "center", "padding": "0 10px", "marginTop": "10px"})
                ], style={
                    "backgroundColor": "white",
                    "padding": "15px",
                    "borderRadius": "8px",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
                    "height": "100%"
                })
            ], style={'flex': '1', "padding": "10px"}),
            
            html.Div([
                html.Div([
                    html.H4("📅 Monthly Temperature", style={"marginBottom": "10px", "color": "#1f77b4", "textAlign": "center"}),
                    dcc.Graph(id='co2-line', style={'height': '300px'}),
                    html.P("Monthly temperature patterns by year for each selected country", 
                           style={"fontSize": "20px", "color": "#555", "textAlign": "center", "padding": "0 10px", "marginTop": "10px"})
                ], style={
                    "backgroundColor": "white",
                    "padding": "15px",
                    "borderRadius": "8px",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
                    "height": "100%"
                })
            ], style={'flex': '1', 'padding': '10px'})
        ], style={'display': 'flex', 'width': '100%', 'marginBottom': '20px'}),

        # Row 4: Scatter + Bubble
        html.Div([
            html.Div([
                html.Div([
                    html.H4("🔍 Temperature vs CO₂ Emissions", style={"marginBottom": "10px", "color": "#1f77b4", "textAlign": "center"}),
                    dcc.Graph(id='temp-vs-co2', style={'height': '450px'}),
                    html.P("Relationship between average temperature and CO₂ emissions (bubble size represents precipitation)", 
                           style={"fontSize": "20px", "color": "#555", "textAlign": "center", "padding": "0 10px", "marginTop": "10px"})
                ], style={
                    "backgroundColor": "white",
                    "padding": "15px",
                    "borderRadius": "8px",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
                    "height": "100%"
                })
            ], style={'flex': '1', 'padding': '10px'}),
            
            html.Div([
                html.Div([
                    html.H4("🔄 Climate Change Over Time", style={"marginBottom": "10px", "color": "#1f77b4", "textAlign": "center"}),
                    dcc.Graph(id='bubble-chart', style={'height': '450px'}),
                    html.P("Animated visualization showing temperature, CO₂, and rainfall trends evolving over years", 
                           style={"fontSize": "20px", "color": "#555", "textAlign": "center", "padding": "0 10px", "marginTop": "10px"})
                ], style={
                    "backgroundColor": "white",
                    "padding": "15px",
                    "borderRadius": "8px",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
                    "height": "100%"
                })
            ], style={'flex': '1', 'padding': '10px'})
        ], style={'display': 'flex', 'width': '100%', 'marginBottom': '20px'}),

        # ========================
        # Climatic Summary + Table
        # ========================
        html.Div([
            html.Div([
                html.H3("Climate Data Summary", style={"textAlign": "center", "color": "#1f77b4", "marginBottom": "15px"}),
                dcc.RadioItems(
                    id='table-view-toggle',
                    options=[
                        {'label': 'Aggregated View', 'value': 'agg' },
                        {'label': 'Year-wise View', 'value': 'year'}
                    ],
                    value='agg',
                    inline=True,
                    labelStyle={
                        "marginRight": "20px",
                        "fontSize": "16px",
                        "padding": "8px 16px",
                        "border": "1px solid #1f77b4",
                        "borderRadius": "5px",
                        "cursor": "pointer",
                        "transition": "0.2s"
                    },
                    inputStyle={"marginRight": "8px"}
                )
            ], style={"textAlign": "center", "marginBottom": "20px"}),

            html.Div([
                dash_table.DataTable(
                    id='country-table',
                    style_cell={
                        'textAlign': 'center',
                        'fontSize': 16,
                        'fontFamily': 'Arial, sans-serif',
                        'padding': '10px',
                        'border': '1px solid #ccc',
                        'backgroundColor': '#ffffff'
                    },
                    style_header={
                        'backgroundColor': '#1f77b4',
                        'color': 'white',
                        'fontWeight': 'bold',
                        'fontSize': 18,
                        'border': '1px solid #1f77b4'
                    },
                    style_data_conditional=[
                        {'if': {'row_index': 'odd'}, 'backgroundColor': '#f9f9f9'},
                        {'if': {'row_index': 'even'}, 'backgroundColor': '#ffffff'},
                        {'if': {'state': 'active'}, 'backgroundColor': '#e6f2ff', 'border': '1px solid #1f77b4'},
                        {'if': {'state': 'selected'}, 'backgroundColor': '#cce0ff', 'border': "1px solid #1f77b4"},
                        {
                            'if': {'column_id': 'Temp %'},
                            'padding': '0',
                            'textAlign': 'left',
                            'fontSize': 14,
                            'color': '#1f77b4'
                        }
                    ],
                    style_table={
                        'overflowX': 'auto',
                        'border': '1px solid #1f77b4',
                        'borderRadius': '8px',
                        'boxShadow': '0 4px 12px rgba(0,0,0,0.15)',
                        'margin': '0 auto',
                        'width': '95%'
                    },
                    page_size=10
                )
            ], style={'marginBottom': '30px'})
        ], style={
            "backgroundColor": "white",
            "padding": "20px",
            "borderRadius": "8px",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"
        })
    ], style={"marginLeft": "0", "transition": "0.3s", "padding": "10px", "width": "100%"})
])

# ================================
# Sidebar Open/Close
# ================================
@app.callback(
    Output("sidebar", "style"),
    Output("main-content", "style"),
    Input("toggle-sidebar", "n_clicks")
)
def toggle_sidebar(n):
    if not n:
        raise dash.exceptions.PreventUpdate
    if n % 2 == 1:  # Sidebar open
        sidebar_style = {"width": "25%", "overflow": "hidden", "backgroundColor": "#f9f9f9",
                         "height": "100vh", "transition": "0.3s", "position": "fixed",
                         "zIndex": "2", "padding": "20px", "boxShadow": "2px 0 5px rgba(0,0,0,0.1)"}
        main_style = {"marginLeft": "25%", "transition": "0.3s", "padding": "10px", "width": "75%"}
    else:
        sidebar_style = {"width": "0", "overflow": "hidden", "backgroundColor": "#f9f9f9",
                         "height": "100vh", "transition": "0.3s", "position": "fixed",
                         "zIndex": "2", "padding": "0px"}
        main_style = {"marginLeft": "0", "transition": "0.3s", "padding": "10px", "width": "100%"}
    return sidebar_style, main_style

# ================================
# Header Stats Callback
# ================================
@app.callback(
    [Output('global-temp-value', 'children'),
     Output('global-rain-value', 'children'),
     Output('global-co2-value', 'children')],
    [Input('entity-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_header_stats(selected_countries, year_range):
    # Use the entire dataset for global averages, filtered by year range only
    dff_global = annual_df[(annual_df['Year'] >= year_range[0]) &
                           (annual_df['Year'] <= year_range[1])]
    
    if len(dff_global) > 0:
        # Calculate global averages across all countries in the dataset
        avg_temp = dff_global['Annual average surface temp'].mean()
        avg_rain = dff_global['Annual precipitation'].mean()
        avg_co2 = dff_global['Annual CO₂ emissions growth (abs)'].mean()
        
        return f"{avg_temp:.2f}°C", f"{avg_rain:.0f}mm", f"{avg_co2:.0f}kt"
    else:
        return "N/A", "N/A", "N/A"
# ================================
# Insight Text Callback
# ================================
@app.callback(
    [Output('temp-insight', 'children'),
     Output('precip-insight', 'children'),
     Output('co2-insight', 'children'),
     Output('temp-trend-mini', 'figure'),
     Output('precip-trend-mini', 'figure'),
     Output('co2-trend-mini', 'figure')],
    [Input('entity-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_insights(selected_countries, year_range):
    dff_annual = annual_df[(annual_df['Entity'].isin(selected_countries)) &
                           (annual_df['Year'] >= year_range[0]) &
                           (annual_df['Year'] <= year_range[1])]
    
    # Temperature insights
    temp_data = dff_annual.groupby('Entity')['Annual average surface temp'].mean()
    if len(temp_data) > 0:
        # Create a list of all countries with their temperatures
        temp_insight_list = []
        for country, temp in temp_data.items():
            temp_insight_list.append(html.Div([
                html.Span(f"🌡️ {country}: {temp:.2f}°C", 
                         style={"fontSize": "14px", "color": "#333", "display": "block", "marginBottom": "5px"})
            ]))
        
        temp_insight = html.Div(temp_insight_list)
        
        # Mini temperature trend chart
        temp_trend = dff_annual.groupby('Year')['Annual average surface temp'].mean().reset_index()
        temp_mini_fig = go.Figure(go.Scatter(x=temp_trend['Year'], y=temp_trend['Annual average surface temp'], 
                                            mode='lines+markers', line=dict(color='#ef553b', width=2),
                                            marker=dict(size=4)))
        temp_mini_fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), plot_bgcolor='rgba(0,0,0,0)', 
                                   paper_bgcolor='rgba(0,0,0,0)', height=80, xaxis_showticklabels=False,
                                   yaxis_showticklabels=False)
    else:
        temp_insight = "No temperature data available for selected filters"
        temp_mini_fig = go.Figure()
        temp_mini_fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), plot_bgcolor='rgba(0,0,0,0)', 
                                   paper_bgcolor='rgba(0,0,0,0)', height=80, xaxis_showticklabels=False,
                                   yaxis_showticklabels=False)
        temp_mini_fig.add_annotation(text="No data", x=0.5, y=0.5, showarrow=False)
    
    # Precipitation insights
    precip_data = dff_annual.groupby('Entity')['Annual precipitation'].sum()
    if len(precip_data) > 0:
        # Create a list of all countries with their precipitation
        precip_insight_list = []
        for country, precip in precip_data.items():
            precip_insight_list.append(html.Div([
                html.Span(f"💧 {country}: {precip:.0f}mm", 
                         style={"fontSize": "14px", "color": "#333", "display": "block", "marginBottom": "5px"})
            ]))
        
        precip_insight = html.Div(precip_insight_list)
        
        # Mini precipitation trend chart
        precip_trend = dff_annual.groupby('Year')['Annual precipitation'].mean().reset_index()
        precip_mini_fig = go.Figure(go.Scatter(x=precip_trend['Year'], y=precip_trend['Annual precipitation'], 
                                              mode='lines+markers', line=dict(color='#00cc96', width=2),
                                              marker=dict(size=4)))
        precip_mini_fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), plot_bgcolor='rgba(0,0,0,0)', 
                                     paper_bgcolor='rgba(0,0,0,0)', height=80, xaxis_showticklabels=False,
                                     yaxis_showticklabels=False)
    else:
        precip_insight = "No precipitation data available for selected filters"
        precip_mini_fig = go.Figure()
        precip_mini_fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), plot_bgcolor='rgba(0,0,0,0)', 
                                     paper_bgcolor='rgba(0,0,0,0)', height=80, xaxis_showticklabels=False,
                                     yaxis_showticklabels=False)
        precip_mini_fig.add_annotation(text="No data", x=0.5, y=0.5, showarrow=False)
    
    # CO2 insights
    co2_data = dff_annual.groupby('Entity')['Annual CO₂ emissions growth (abs)'].sum()
    if len(co2_data) > 0:
        # Create a list of all countries with their CO2 emissions
        co2_insight_list = []
        for country, co2 in co2_data.items():
            co2_insight_list.append(html.Div([
                html.Span(f"🏭 {country}: {co2:.0f}kt", 
                         style={"fontSize": "14px", "color": "#333", "display": "block", "marginBottom": "5px"})
            ]))
        
        co2_insight = html.Div(co2_insight_list)
        
        # Mini CO2 trend chart
        co2_trend = dff_annual.groupby('Year')['Annual CO₂ emissions growth (abs)'].mean().reset_index()
        co2_mini_fig = go.Figure(go.Scatter(x=co2_trend['Year'], y=co2_trend['Annual CO₂ emissions growth (abs)'], 
                                           mode='lines+markers', line=dict(color='#636efa', width=2),
                                           marker=dict(size=4)))
        co2_mini_fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), plot_bgcolor='rgba(0,0,0,0)', 
                                  paper_bgcolor='rgba(0,0,0,0)', height=80, xaxis_showticklabels=False,
                                  yaxis_showticklabels=False)
    else:
        co2_insight = "No CO₂ emissions data available for selected filters"
        co2_mini_fig = go.Figure()
        co2_mini_fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), plot_bgcolor='rgba(0,0,0,0)', 
                                  paper_bgcolor='rgba(0,0,0,0)', height=80, xaxis_showticklabels=False,
                                  yaxis_showticklabels=False)
        co2_mini_fig.add_annotation(text="No data", x=0.5, y=0.5, showarrow=False)
    
    return temp_insight, precip_insight, co2_insight, temp_mini_fig, precip_mini_fig, co2_mini_fig

# ================================
# Graph & Table Updates
# ================================
@app.callback(
    [
        Output('temp-donut', 'figure'),
        Output('precip-donut', 'figure'),
        Output('co2-donut', 'figure'),
        Output('world-map', 'figure'),
        Output('annual-precipitation', 'figure'),
        Output('co2-growth', 'figure'),
        Output('avg-temp-hist', 'figure'),
        Output('precipitation-hist', 'figure'),
        Output('co2-line', 'figure'),
        Output('temp-vs-co2', 'figure'),
        Output('bubble-chart', 'figure'),
        Output('country-table', 'data')
    ],
    [Input('entity-dropdown', 'value'),
     Input('year-slider', 'value'),
     Input('theme-toggle', 'value'),
     Input('table-view-toggle', 'value')]
)
def update_graphs(selected_countries, year_range, theme, table_view):
    dff_annual = annual_df[(annual_df['Entity'].isin(selected_countries)) &
                           (annual_df['Year'] >= year_range[0]) &
                           (annual_df['Year'] <= year_range[1])]

    # Theme styles
    bg_color = "#1e1e1e" if theme == "dark" else "white"
    font_color = "white" if theme == "dark" else "black"


    def apply_theme(fig):
        fig.update_layout(plot_bgcolor=bg_color, paper_bgcolor=bg_color, font=dict(color=font_color),
                          xaxis=dict(showgrid=False, zeroline=False, showline=True, linecolor=font_color, linewidth=1.5),
                          yaxis=dict(showgrid=False, zeroline=False, showline=True, linecolor=font_color, linewidth=1.5),
                          margin=dict(l=10, r=10, t=40, b=10))
        return fig

    # Donut charts
    temp_donut = px.pie(dff_annual.groupby('Entity')['Annual average surface temp'].mean().reset_index(),
                        names='Entity', values='Annual average surface temp',
                        title='', hole=0.4)
    precip_donut = px.pie(dff_annual.groupby('Entity')['Annual precipitation'].sum().reset_index(),
                          names='Entity', values='Annual precipitation',
                          title='', hole=0.4)
    co2_donut = px.pie(dff_annual.groupby('Entity')['Annual CO₂ emissions growth (abs)'].sum().reset_index(),
                       names='Entity', values='Annual CO₂ emissions growth (abs)',
                       title='', hole=0.4)

    # World map
    world_df = dff_annual.groupby('Entity')['Annual average surface temp'].mean().reset_index()
    world_map = px.choropleth(world_df, locations='Entity', locationmode='country names',
                              color='Annual average surface temp', color_continuous_scale='RdYlBu_r',
                              title='')

    # Annual rainfall bar
    fig_annual_precip = px.bar(dff_annual, x='Year', y='Annual precipitation', color='Entity', barmode='group',
                               title='')

    # CO2 growth line
    fig_co2_growth = px.line(dff_annual, x='Year', y='Annual CO₂ emissions growth (abs)', color='Entity',
                             title='')

    # Avg temp histogram
    fig_avg_temp_hist = px.histogram(dff_annual, x='Annual average surface temp', nbins=30, color='Entity',
                                     title='')

    # Correlation heatmap
    corr_df = dff_annual[['Annual average surface temp', 'Annual precipitation', 'Annual CO₂ emissions growth (abs)']]
    corr_matrix = corr_df.corr()
    fig_corr_heatmap = px.imshow(corr_matrix, text_auto=True, color_continuous_scale='RdYlBu_r',
                                 title='')

    # Monthly temperature heatmap
    dff_monthly = df[(df['Entity'].isin(selected_countries)) &
                     (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    monthly_avg = dff_monthly.groupby(['Entity', 'Year', 'Month'])['Average surface temperature'].mean().reset_index()
    monthly_avg['Month'] = monthly_avg['Month'].apply(lambda x: calendar.month_abbr[x])
    fig_monthly_bar = px.bar(monthly_avg, x='Year', y='Average surface temperature', color='Month',
                             barmode='stack', facet_col='Entity', title='',
                             labels={'Average surface temperature':'Avg Temp', 'Year':'Year'})
    fig_monthly_bar.update_layout(xaxis_title='Year', yaxis_title='Average Temperature',
                                  legend_title='Month', margin=dict(l=40, r=20, t=50, b=50))

    # Temp vs CO2 scatter
    fig_temp_vs_co2 = px.scatter(dff_annual, x='Annual average surface temp', y='Annual CO₂ emissions growth (abs)',
                                 color='Entity', size='Annual precipitation', hover_data=['Year'],
                                 title='')

    # Animated bubble
    fig_bubble = px.scatter(dff_annual, x="Annual average surface temp", y="Annual CO₂ emissions growth (abs)",
                            animation_frame="Year", animation_group="Entity", size="Annual precipitation",
                            color="Entity", hover_name="Entity", title="",
                            size_max=60)

    # ========================
    # Table data
    # ========================
    if table_view == 'agg':
        table_df = dff_annual.groupby('Entity').agg({
            'Annual average surface temp': 'mean',
            'Annual precipitation': 'mean',
            'Annual CO₂ emissions growth (abs)': 'mean'
        }).reset_index()
        table_df.rename(columns={'Entity': 'Country',
                                 'Annual average surface temp': 'Avg Temp',
                                 'Annual precipitation': 'Annual Precipitation',
                                 'Annual CO₂ emissions growth (abs)': 'CO2 Emissions'}, inplace=True)
    else:  # Year-wise
        table_df = dff_annual.copy()
        table_df.rename(columns={'Entity': 'Country',
                                 'Annual average surface temp': 'Avg Temp',
                                 'Annual precipitation': 'Annual Precipitation',
                                 'Annual CO₂ emissions growth (abs)': 'CO2 Emissions'}, inplace=True)
        table_df = table_df[['Country', 'Year', 'Avg Temp', 'Annual Precipitation', 'CO2 Emissions']]

    # Temp % column with smaller bars
    max_temp = table_df['Avg Temp'].max()
    table_df['Temp Comparison % '] = table_df['Avg Temp'] / max_temp * 100
    table_df['Temp Comparison % '] = table_df['Temp Comparison % '].apply(lambda x: f"{int(x/5)*'▓'} {round(x,1)}%")  # smaller bars
    table_df['Avg Temp'] = table_df['Avg Temp'].round(3).astype(str) + " °C"
    table_df['Annual Precipitation'] = table_df['Annual Precipitation'].round(3).astype(str) + " mm"
    table_df['CO2 Emissions'] = table_df['CO2 Emissions'].round(3).astype(str) + " kt"

    table_data = table_df.to_dict('records')

    figs = [temp_donut, precip_donut, co2_donut, world_map, fig_annual_precip,
            fig_co2_growth, fig_avg_temp_hist, fig_corr_heatmap, fig_monthly_bar,
            fig_temp_vs_co2, fig_bubble]

    figs = [apply_theme(fig) for fig in figs]

    return *figs, table_data

# ================================
# Run App
# ================================
if __name__ == "__main__":
    app.run(debug=True)