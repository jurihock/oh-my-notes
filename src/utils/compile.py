import os
import shutil
import subprocess

__tmp__ = os.path.join('/', 'tmp', 'ohmynotes')

def markdown(id, value):

  tmp = os.path.join(__tmp__, 'files', id)
  os.makedirs(tmp, exist_ok=True)

  with open(os.path.join(tmp, 'input.md'), 'w') as file:
    file.write(value)

  subprocess.check_call(
  [
    'pandoc',
    'input.md',
    '-r', 'markdown',
    '-w', 'latex',
    '-o', 'output.pdf',
  ],
  cwd=tmp)

  with open(os.path.join(tmp, 'output.pdf'), 'rb') as file:
    result = file.read()

  if os.path.exists(tmp):
    shutil.rmtree(tmp)

  return result
