from app import app

from utils import request
from utils import response
from utils import database

@app.route('/file/names.json')
def suggest_file_name():

  q = request.str('q')

  with database.database(request.username()) as db:

    names = list(db.suggest_file_name(q))

  return response.jsonify(names)

@app.route('/folder/<folder>/file/<file>.json')
def select_file_as_json(folder, file):

  with database.database(request.username()) as db:

    file = db.select_file(file)
    assert file

  return response.jsonify(file)

@app.route('/folder/<folder>/file/<file>')
def select_file(folder, file):

  with database.database(request.username()) as db:

    folder = db.select_folder(folder)
    assert folder

    file = db.select_file(file)
    assert file

    folders = list(db.select_folders())
    files = list(db.select_files(folder))

  selected = \
  {
    'folder': folder,
    'file': file
  }

  return response.template('bootstrap.html', folders=folders, files=files, selected=selected)

@app.route('/file/create')
def create_file():

  if not request.has('folder'):
    return response.error(400)

  if not request.has('name'):
    return response.error(400)

  if not request.has('type'):
    return response.error(400)

  folder = request.str('folder')
  name = request.str('name')
  type = request.str('type')

  with database.database(request.username()) as db:

    file = db.create_file(folder, name, type)

  return response.redirect('select_file', folder=file['folder']['id'], file=file['id'])

@app.route('/file/<file>/delete')
def delete_file(file):

  with database.database(request.username()) as db:

    file = db.delete_file(file)
    folder = file['folder']['id']

  return response.redirect('select_folder', folder=folder)

@app.route('/file/<file>/update')
def update_file(file):

  kwargs = {}

  if request.contains('value'):
    kwargs['value'] = request.str('value', default='').strip()

  with database.database(request.username()) as db:

    file = db.update_file(file, **kwargs)

  return response.redirect('select_file', folder=file['folder']['id'], file=file['id'])
