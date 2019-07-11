from app import app

from utils import request
from utils import response
from utils import database

@app.route('/folder/names.json')
def list_of_folder_names():

  with database.database(request.username()) as db:

    folders = list(db.select_folders())

  return response.jsonify([folder['name'] for folder in folders])

@app.route('/folder/<folder>')
def select_folder(folder):

  with database.database(request.username()) as db:

    folder = db.select_folder(folder)
    assert folder

    folders = list(db.select_folders())
    files = list(db.select_files(folder))

  selected = \
  {
    'folder': folder,
    'file': files[0] if files else { 'id': None, 'name': None }
  }

  return response.template('bootstrap.html', folders=folders, files=files, selected=selected)

@app.route('/folder/create')
def create_folder():

  if not request.has('name'):
    return response.error(400)

  name = request.str('name')

  with database.database(request.username()) as db:

    folder = db.create_folder(name)

  return response.redirect('select_folder', folder=folder['id'])

@app.route('/folder/<folder>/delete')
def delete_folder(folder):

  with database.database(request.username()) as db:

    db.delete_folder(folder)

  return response.redirect('index')
