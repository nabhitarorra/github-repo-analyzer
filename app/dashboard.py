import os
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from .analyzer import RepoAnalyzer

# Initialize the analyzer with the token from environment variables
analyzer = RepoAnalyzer(github_token=os.environ.get("GITHUB_API_TOKEN"))

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], suppress_callback_exceptions=True)
app.title = "GitHub Repo Analyzer"

# Define the layout of the app
app.layout = dbc.Container([
    # Header
    dbc.Row(
        dbc.Col(html.H1("GitHub Repository Analyzer 📈", className="text-center text-primary my-4"), width=12)
    ),

    # Input section
    dbc.Row([
        dbc.Col(
            dbc.Input(id='repo-url-input', type='text',
                      placeholder='Enter a public GitHub repo URL (e.g., https://github.com/facebook/react)'),
            width=9
        ),
        dbc.Col(
            dbc.Button('Analyze', id='analyze-button', color='primary', n_clicks=0),
            width=3
        )
    ], className="mb-4"),

    # Output section (initially hidden)
    html.Div(id='output-div', children=[], style={'display': 'none'})

], fluid=True)


# Callback to run analysis and update the output
@app.callback(
    [Output('output-div', 'children'),
     Output('output-div', 'style')],
    [Input('analyze-button', 'n_clicks')],
    [State('repo-url-input', 'value')]
)
def update_output(n_clicks, repo_url):
    if n_clicks == 0 or not repo_url:
        return [], {'display': 'none'}

    # Show a loading spinner while analyzing
    loading_spinner = dbc.Spinner(color="primary")

    analysis = analyzer.analyze(repo_url)

    if analysis.get("error"):
        error_alert = dbc.Alert(analysis["error"], color="danger")
        return [error_alert], {'display': 'block', 'marginTop': '20px'}

    # --- Build UI components from analysis results ---
    stats = analysis['stats']
    commit_freq = analysis['commit_frequency']
    tags = analysis['readme_tags']

    # 1. Stat cards
    stat_cards = dbc.Row([
        dbc.Col(dbc.Card([dbc.CardHeader("Language"), dbc.CardBody(stats['language'] or 'N/A')], color="secondary")),
        dbc.Col(dbc.Card([dbc.CardHeader("Stars ★"), dbc.CardBody(f"{stats['stars']:,}")], color="secondary")),
        dbc.Col(dbc.Card([dbc.CardHeader("Forks 🍴"), dbc.CardBody(f"{stats['forks']:,}")], color="secondary")),
        dbc.Col(
            dbc.Card([dbc.CardHeader("Open Issues !"), dbc.CardBody(f"{stats['open_issues']:,}")], color="secondary")),
    ], className="mb-4")

    # 2. NLP-derived tags
    tag_badges = [dbc.Badge(tag, color="info", className="me-1 mb-1") for tag in tags]
    tags_card = dbc.Card([
        dbc.CardHeader("Project Tags (from README)"),
        dbc.CardBody(tag_badges if tag_badges else "No tags found.")
    ], className="mb-4")

    # 3. Commit frequency graph
    df_commits = pd.DataFrame(list(commit_freq.items()), columns=['Week', 'Commits']).sort_values('Week')
    fig_commits = px.bar(df_commits, x='Week', y='Commits', title='Commit Frequency (Last Year)',
                         template='plotly_dark')
    fig_commits.update_layout(xaxis_title="Week of the Year", yaxis_title="Number of Commits")
    commit_graph = dcc.Graph(figure=fig_commits)

    # Combine all components
    output_content = [
        stat_cards,
        tags_card,
        commit_graph
    ]

    return output_content, {'display': 'block', 'marginTop': '20px'}