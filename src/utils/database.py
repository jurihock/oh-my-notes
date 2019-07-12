from pymongo import MongoClient, ASCENDING
from bson.objectid import ObjectId

import re

class database:

  def __init__(self, scope='default'):

    self.scope = scope

  def __enter__(self):

    self.mongo = MongoClient()
    self.db = self.mongo['ohmynotes-' + self.scope]

    return self

  def __exit__(self, type, value, traceback):

    self.db = None

    if self.mongo:
      self.mongo.close()
      self.mongo = None

  def select_folders(self):

    folders = self.db.folders.find().sort('name', ASCENDING)

    for folder in folders:
      folder['id'] = str(folder['_id'])
      del folder['_id']
      yield folder

  def select_folder(self, folder):

    assert folder and isinstance(folder, (str, dict))

    folder = folder['id'] \
      if isinstance(folder, dict) \
      else folder

    try:
      id = {'_id': ObjectId(folder)}
      name = {'name': re.compile('^' + re.escape(folder) + '$', re.IGNORECASE)}
      folder = self.db.folders.find_one({'$or': [id, name]})
    except:
      name = {'name': re.compile('^' + re.escape(folder) + '$', re.IGNORECASE)}
      folder = self.db.folders.find_one(name)

    if folder:
      folder['id'] = str(folder['_id'])
      del folder['_id']
      return folder

    return None

  def create_folder(self, name):

    assert name and isinstance(name, str)

    folder = self.select_folder(name)
    
    if folder:
      return folder

    folder = \
    {
      'name': name
    }

    result = self.db.folders.insert_one(folder)
    folder = self.db.folders.find_one({'_id': result.inserted_id})

    folder['id'] = str(folder['_id'])
    del folder['_id']
    return folder

  def delete_folder(self, folder):

    folder = self.select_folder(folder)
    assert folder

    files = list(self.select_files(folder))

    for file in files:
      self.delete_file(file)

    self.db.folders.delete_one({'_id': ObjectId(folder['id'])})
    return folder

  def select_files(self, folder):

    assert folder and isinstance(folder, (str, dict))

    folder = self.select_folder(folder)

    if not folder:
      return None

    files = self.db.files.find({'folder._id': ObjectId(folder['id'])}).sort('name', ASCENDING)

    for file in files:
      file['id'] = str(file['_id'])
      del file['_id']
      file['folder']['id'] = str(file['folder']['_id'])
      del file['folder']['_id']
      yield file

  def select_file(self, file):

    assert file and isinstance(file, (str, dict))

    file = file['id'] \
      if isinstance(file, dict) \
      else file

    try:
      id = {'_id': ObjectId(file)}
      file = self.db.files.find_one(id)
    except:
      return None

    if file:
      file['id'] = str(file['_id'])
      del file['_id']
      file['folder']['id'] = str(file['folder']['_id'])
      del file['folder']['_id']
      return file

    return None

  def create_file(self, folder, name, type):

    assert folder and isinstance(folder, (str, dict))
    assert name and isinstance(name, str)
    assert type and isinstance(type, str)

    folder = self.select_folder(folder) or self.create_folder(folder)

    file = \
    {
      'folder': {'_id': ObjectId(folder['id'])},
      'name': name,
      'type': type,
      'value': None
    }

    result = self.db.files.insert_one(file)
    file = self.db.files.find_one({'_id': result.inserted_id})

    file['id'] = str(file['_id'])
    del file['_id']
    file['folder']['id'] = str(file['folder']['_id'])
    del file['folder']['_id']
    return file

  def delete_file(self, file):

    file = self.select_file(file)
    assert file

    self.db.files.delete_one({'_id': ObjectId(file['id'])})
    return file
