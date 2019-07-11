from app import app

from utils import request
from utils import response
from utils import database

@app.route('/')
def index():

  with database.database(request.username()) as db:

    folders = list(db.select_folders())
    files = list(db.select_files(folders[0])) if folders else None

  selected = \
  {
    'folder': folders[0] if folders else { 'id': None, 'name': None },
    'file': files[0] if files else { 'id': None, 'name': None }
  }

  return response.template('bootstrap.html', folders=folders, files=files, selected=selected)
