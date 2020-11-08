
"""Plotly Dash HTML layout override."""

html_layout = '''
<!DOCTYPE html>
    <html>
        <head>

        </head>
        <body class="dash-template">
            
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
'''
