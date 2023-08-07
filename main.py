from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os, sqlite3

db = sqlite3.connect('album.db')
db.execute("CREATE TABLE IF NOT EXISTS photos(photo TEXT); ")
db.commit()
db.close()

app = Flask(__name__)


@app.route('/', methods = ['GET','POST'])
def home():
  if request.method == 'POST' and \
  request.files and 'photo' in request.files:
    # get file
    photo = request.files['photo']
    # protect 
    filename = secure_filename(photo.filename)
    # form and save file
    path = os.path.join('uploads', filename)
    photo.save(path)
    # add filename to database
    db = sqlite3.connect('album.db')
    db.execute("INSERT INTO photos(photo) VALUES(?)", (filename,))
    db.commit()
    db.close()
  return render_template('index.html')

@app.route('/view')
def view():
  db = sqlite3.connect('album.db')
  recs = db.execute('SELECT * FROM photos;')
  pics = []
  for rec in recs:
    pics.append(rec[0])
  db.close()
  return render_template('view.html',pics = pics)

@app.route('/photos/<filename>')
def get_file(filename):
  return send_from_directory('uploads', filename)
  

app.run(host='0.0.0.0', port=81)
