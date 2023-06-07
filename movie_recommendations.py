import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
import random
import mysql.connector

# Create empty DataFrames
ht="193.204.40.146"
user="gr3"
pwd="group3#20"
db="group3"

mydb = mysql.connector.connect(
    host = ht,
    user = user,
    password = pwd,
    database = db
)

mycursor = mydb.cursor()


sql = "SELECT * FROM Users"
mycursor.execute(sql)
myresult = mycursor.fetchall()

users_df  = pd.read_sql(sql, mydb)
users_df.rename(columns = {'username':'Username', 'name':"First name","last_name": "Last name", "password":'Password'}, inplace = True)

sql = "SELECT * FROM Genres"
mycursor.execute(sql)
myresult = mycursor.fetchall()

genres_df  = pd.read_sql(sql, mydb)
genres_df.rename(columns = {'id':'Id', 'name':"Name"}, inplace = True)
print(genres_df.columns)

sql = "select p.user_id, u.name as first_name, u.last_name, g.name from Preferences p join Users u ON p.user_id=u.username JOIN Genres g ON p.genre_id=g.id;"
mycursor.execute(sql)
myresult = mycursor.fetchall()

preferences_df  = pd.read_sql(sql, mydb)
#names = ["Username","First name","Last name", "Genre"]
preferences_df.rename(columns = {"user_id":"Username","first_name":"First name", "last_name":"Last name", "name":"Genre"}, inplace = True)
print(preferences_df.columns)

sql = "select type , title, director, country, release_year, rating, duration, name from Shows JOIN Genres ON listed_in=id;"
mycursor.execute(sql)
myresult = mycursor.fetchall()

shows_df  = pd.read_sql(sql, mydb)
shows_df.rename(columns = {"type":"Type","title":"Title", "director":"Director", \
                           "country":"Country", "release_year":"Release year", "rating":"Rating", \
                           "duration":"Duration","name":"Genre"}, inplace = True)


    




# Initialize the Dash app
app = dash.Dash(__name__)

# Styling for tables
table_style = {
    'border': '1px solid gray',
    'border-collapse': 'collapse',
    'padding': '8px',
    'margin': 'auto',
    'color': '#780743'
}

# First part: Movie recommendations
first_part = html.Div(
    [
        html.H1('Movie recommendations', style={'text-align': 'center', 'color': '#780743', 'font-size': '40px', 'margin-bottom': '30px', 'font-family':'Century Gothic'}),
        html.H2('Pick a show based on the genre', style={'text-align': 'center', 'background-color': '#ff44a7', 'color': '#fff', 'padding': '10px', 'margin-bottom': '20px', 'font-family':'Century Gothic'}),
        html.Div(
            [
                html.Div(
                    [
                        html.Label('Type:', style={'font-weight': 'bold', 'margin-bottom': '20px', 'color':'#780743', 'font-family':'Century Gothic'}),
                        dcc.Dropdown(
                            id='type-dropdown',
                            options=[{'label': t, 'value': t} for t in shows_df['Type'].unique()],
                            placeholder='Select a type',
                            style={'margin-top': '10px','width': '95%', 'padding': '8px', 'border-radius': '4px', 'border': '2px solid #ff44a7', 'font-family':'Century Gothic'}
                        )
                    ],
                    style={'width': '45%', 'display': 'inline-block', 'margin-bottom': '10px'}
                ),
                html.Div(
                    [
                        html.Label('Genre:', style={'font-weight': 'bold', 'margin-bottom': '20px', 'color':'#780743', 'font-family':'Century Gothic'}),
                        dcc.Dropdown(
                            id='genre-dropdown',
                            options=[{'label': g, 'value': g} for g in genres_df['Name'].unique()],
                            placeholder='Select a genre',
                            style={'margin-top': '10px','width': '95%', 'padding': '8px', 'border-radius': '4px', 'border': '2px solid #ff44a7', 'font-family':'Century Gothic'}
                        )
                    ],
                    style={'width':'45%', 'display': 'inline-block'}
                )
            ],
             style={'text-align': 'center', 'margin-bottom': '20px','font-family':'Century Gothic' }
        ),
        html.Div(id='shows-table', style={'background-color': '#fff', 'padding': '20px', 'border-radius': '4px', 'box-shadow': '0px 2px 6px rgba(0, 0, 0, 0.2)', 'font-family':'Century Gothic'})
    ],
    style={'text-align': 'center', 'background-color': '#ffe6f3', 'padding': '20px'}
)

# Second part: Get recommendations based on preferences
second_part = html.Div(
    [
        html.H2('Get recommendations based on your preferences', style={'text-align': 'center', 'color': '#ff44a7', 'font-family':'Century Gothic'}),
        html.Div(
            [
                html.Label('Username:   ', style={'font-weight': 'bold', 'font-family':'Century Gothic', 'color':'#780743'}),
                dcc.Input(id='username-input', type='text', placeholder='Enter your username', style={'padding': '8px', 'border-radius': '4px', 'border': '1px solid #ff44a7', 'font-family':'Century Gothic'})
            ],
            style={'text-align': 'center', 'margin-bottom': '10px'}
        ),
        html.Div(
            [
                html.Label('Password:   ', style={'font-weight': 'bold', 'font-family':'Century Gothic', 'color':'#780743'}),
                dcc.Input(id='password-input', type='password', placeholder='Enter your password', style={'padding': '8px', 'border-radius': '4px', 'border': '1px solid #ff44a7', 'font-family':'Century Gothic'})
            ],
            style={'text-align': 'center', 'margin-bottom': '20px'}
        ),
        html.Div(id='preferences-table', style={'text-align': 'center', 'font-family':'Century Gothic'})
    ],
    style={'text-align': 'center', 'background-color': '#ffe6f3', 'padding': '20px', 'font-family':'Century Gothic'}
)


# Third part: Insert your preference
third_part = html.Div(
    [
        html.H2('Insert your preference!', style={'text-align': 'center', 'color': '#ff44a7', 'font-family':'Century Gothic'}),
        html.Div(
            [
                html.Label('Username:   ', style={'font-weight': 'bold', 'font-family':'Century Gothic', 'color':'#780743'}),
                dcc.Input(id='new-username-input', type='text', placeholder='Enter your username', style={'padding': '8px', 'border-radius': '4px', 'border': '1px solid #ff44a7', 'font-family':'Century Gothic'})
            ],
            style={'text-align': 'center', 'margin-bottom': '10px', 'font-family':'Century Gothic'}
        ),
        html.Div(
            [
                html.Label('Password:   ', style={'font-weight': 'bold', 'color':'#780743'}),
                dcc.Input(id='new-password-input', type='password', placeholder='Enter your password', style={'padding': '8px', 'border-radius': '4px', 'border': '1px solid #ff44a7', 'font-family':'Century Gothic'})
            ],
            style={'text-align': 'center', 'margin-bottom': '20px', 'font-family':'Century Gothic'}
        ),
        html.Div(
            [
                html.Label('Genre:', style={'font-weight': 'bold', 'font-family':'Century Gothic', 'color':'#780743'}),
                dcc.Dropdown(
                    id='new-genre-dropdown',
                    options=[{'label': g, 'value': g} for g in genres_df['Name'].unique()],
                    placeholder='Select a genre',
                    style={'width': '70%', 'padding': '4px', 'border-radius': '8px', 'border': '2px solid #ff44a7', 'margin': '0 auto' }
                )
            ],
            style={'text-align': 'center', 'margin-bottom': '20px'}
        ),
        html.Button('Add your preference', id='add-preference-btn', n_clicks=0, style={'margin-bottom': '30px', 'text-align': 'center', 'margin': 'auto', 'background-color': '#ff44a7', 'color': '#fff', 'padding': '8px 16px', 'border': 'none', 'border-radius': '4px', 'font-family':'Century Gothic'}),
        html.Div(id='preference-message', style={'text-align': 'center', 'margin-top': '10px'})
    ],
    style={'text-align': 'center', 'background-color': '#ffe6f3', 'padding': '20px', 'font-family':'Century Gothic'}
)

# App layout
app.layout = html.Div([first_part, second_part, third_part])


# Callback for filtering shows_df based on dropdown selections
@app.callback(
    Output('shows-table', 'children'),
    Input('type-dropdown', 'value'),
    Input('genre-dropdown', 'value')
)
def filter_shows_table(type_value, genre_value):
    filtered_shows = shows_df[(shows_df['Type'] == type_value) & (shows_df['Genre'] == genre_value)].head(15)
    if filtered_shows.empty:
        return 'No shows match the selected criteria.'
    return html.Table(
        [
            html.Tr([html.Th(col, style=table_style) for col in filtered_shows.columns]),
            *[
                html.Tr([html.Td(data, style=table_style) for data in row])
                for row in filtered_shows.values
            ]
        ],
        style=table_style
    )



# Callback for retrieving recommendations based on preferences
@app.callback(
    Output('preferences-table', 'children'),
    Input('username-input', 'value'),
    Input('password-input', 'value')
)
def get_preferences(username, password):
    if username and password:
        user_row = users_df[(users_df['Username'] == username) & (users_df['Password'] == password)]
        if not user_row.empty:
            user_genre = preferences_df.loc[preferences_df['Username'] == username, 'Genre'].values
            filtered_shows = shows_df[shows_df['Genre'].isin(user_genre)].sample(15, random_state=1)
            if filtered_shows.empty:
                return 'No recommendations based on your preferences.'
            return html.Table(
                [
                    html.Tr([html.Th(col, style=table_style) for col in filtered_shows.columns]),
                    *[
                        html.Tr([html.Td(data, style=table_style) for data in row])
                        for row in filtered_shows.values
                    ]
                ],
                style=table_style
            )
        return 'Username and/or password don\'t match!'
    return 'Please enter your username and password.'





 
# Callback for adding a new preference
@app.callback(
    Output('preference-message', 'children'),
    Input('add-preference-btn', 'n_clicks'),
    State('new-username-input', 'value'),
    State('new-password-input', 'value'),
    State('new-genre-dropdown', 'value')
)

def add_preference(n_clicks, username, password, genre):
    global preferences_df
    user_id=str(username)
    genre_name = str(genre)
    if n_clicks > 0:
        if username and password and genre:
            if username not in users_df['Username'].values:
                return 'Username does not exist!'
            if (username, password) in zip(users_df['Username'].values, users_df['Password'].values):
                if genre not in preferences_df.loc[preferences_df['Username'] == username, 'Genre'].values:
                    new_row = pd.DataFrame([[username, '', '', genre]], columns=preferences_df.columns)
                    preferences_df = preferences_df.append(new_row, ignore_index=True)
                 
                    return 'Preference successfully added!'
                return 'Preference already exists!'
            return 'Username and/or password don\'t match!'
        return 'Please enter your username, password, and genre.'
    return ''


if __name__ == '__main__':
    app.run_server(debug=True)