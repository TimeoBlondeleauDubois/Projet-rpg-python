import flask 
import sqlite3

app = flask.Flask(__name__, template_folder='views')

@app.route('/')

def home():
   connection = sqlite3.connect('Rpg.db')
   cursor = connection.cursor()
   cursor.execute('SELECT * FROM player_data')
   players = cursor.fetchall()
   connection.close()

   list_players = []

   for player in players:
      list_players.append({
         "id": player[0],
         "name": player[1],
         "class": player[2]
      })

   return flask.render_template('index.html', players=list_players)