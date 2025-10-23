import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import base64
from io import BytesIO
from wordcloud import WordCloud, STOPWORDS
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import webbrowser
import threading
import time

# 1. Load your data
DF_PATH = "5_Cluster_Visualization\Cluster_Representative_Summaries.csv"
df = pd.read_csv(DF_PATH)

# 2. Compute TF‑IDF across all session summaries
tfidf = TfidfVectorizer(stop_words='english', max_features=1000)
X = tfidf.fit_transform(df['Representative_Summary'])
feature_names = tfidf.get_feature_names_out()

# 3. Extract per-session keyword scores and count “important” ones
session_keywords = {}
session_counts = []
for i, sid in enumerate(df['Cluster_ID']):
    row = X[i].tocoo()
    scores = {feature_names[j]: v for j, v in zip(row.col, row.data)}
    mean_score = np.mean(list(scores.values())) if scores else 0
    important = {w: s for w, s in scores.items() if s > mean_score}
    session_keywords[sid] = important
    session_counts.append({'session_id': sid, 'n_keywords': len(important)})

# 4. Compute global importance (sum of TF‑IDF over all sessions)
global_sums = np.array(X.sum(axis=0)).flatten()
global_scores = dict(zip(feature_names, global_sums))

# 5. Build the bubble‑chart figure with equidistant x positions
bubble_df = pd.DataFrame(session_counts)
bubble_df['xpos'] = range(len(bubble_df))  # equidistant positions

# Increase size_max to enlarge all circles
fig = px.scatter(
    bubble_df,
    x='xpos',
    y=[0]*len(bubble_df),
    size='n_keywords',
    size_max=50,               # larger maximum bubble size
    hover_name='session_id',
    title='Sessions Overview',
    labels={'xpos':'Session', 'session_id':'Session ID'},
    height=400
)
# Map ticks to session IDs
fig.update_xaxes(
    tickmode='array',
    tickvals=bubble_df['xpos'],
    ticktext=bubble_df['session_id'],
    showgrid=False
)
fig.update_yaxes(visible=False)
fig.update_layout(
    clickmode='event+select',
    margin=dict(l=40, r=40, t=60, b=40)
)

# 6. Dash app setup
app = dash.Dash(__name__)

# 7. App layout with improved styling
app.layout = html.Div(
    style={
        'fontFamily': 'Arial, sans-serif',
        'padding': '20px',
        'maxWidth': '1200px',
        'margin': '0 auto'
    },
    children=[
        html.H1(
            'Session Keyword Explorer',
            style={'textAlign': 'center', 'marginBottom': '30px'}
        ),
        html.Div(
            dcc.Graph(
                id='bubble-chart',
                figure=fig,
                config={'displayModeBar': False}
            ),
            style={'marginBottom': '50px'}
        ),
        html.Div(
            style={'display': 'flex', 'gap': '20px'},
            children=[
                html.Div(
                    style={
                        'flex': 1,
                        'border': '1px solid #ddd',
                        'padding': '15px',
                        'borderRadius': '8px',
                        'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)',
                        'textAlign': 'center'
                    },
                    children=[
                        html.H4('Session‑only Word Cloud'),
                        html.Img(id='wc-session', style={'maxWidth': '100%'})
                    ]
                ),
                html.Div(
                    style={
                        'flex': 1,
                        'border': '1px solid #ddd',
                        'padding': '15px',
                        'borderRadius': '8px',
                        'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)',
                        'textAlign': 'center'
                    },
                    children=[
                        html.H4('Global Word Cloud'),
                        html.Img(id='wc-global', style={'maxWidth': '100%'})
                    ]
                )
            ]
        )
    ]
)

# 8. Helper: generate base64‑encoded PNG for word clouds
def make_wc_image(freqs):
    wc = WordCloud(
        width=400,
        height=300,
        background_color='white',
        stopwords=STOPWORDS,
        collocations=False
    ).generate_from_frequencies(freqs)
    buf = BytesIO()
    wc.to_image().save(buf, format='PNG')
    encoded = base64.b64encode(buf.getvalue()).decode('utf-8')
    return f'data:image/png;base64,{encoded}'

# 9. Callback: update word clouds on bubble click
@app.callback(
    Output('wc-session', 'src'),
    Output('wc-global', 'src'),
    Input('bubble-chart', 'clickData')
)
def update_wordclouds(clickData):
    if not clickData:
        return '', ''
    sid = clickData['points'][0]['hovertext']
    sess_freqs = session_keywords.get(sid, {})
    global_freqs = {w: global_scores[w] for w in sess_freqs}
    return make_wc_image(sess_freqs), make_wc_image(global_freqs)

# 10. Auto-open browser and run server
def open_browser():
    time.sleep(1)
    webbrowser.open('http://127.0.0.1:8050')

if __name__ == '__main__':
    threading.Thread(target=open_browser).start()
    app.run(debug=True, host='127.0.0.1', port=8050)
