import os
import glob
import shutil
import subprocess

__tmp__ = os.path.join('/', 'tmp', 'ohmynotes')

def auto(type, id, value):

  if type == 'markdown':
    return markdown(id, value)

  if type == 'lilypond':
    return lilypond(id, value)

  return text(id, value)

def text(id, value, geometry='portrait'):

  tmp = os.path.join(__tmp__, 'files', id)
  os.makedirs(tmp, exist_ok=True)

  with open(os.path.join(tmp, 'input.html'), 'w') as file:
    file.write('<html><body><pre>' + os.linesep)
    file.write(value)
    file.write('</pre></body></html>' + os.linesep)

  subprocess.check_call(
  [
    'pandoc',
    'input.html',
    '-r', 'html',
    '-w', 'latex',
    '-o', 'output.pdf',
    '-V', 'geometry:' + geometry,
  ],
  cwd=tmp)

  with open(os.path.join(tmp, 'output.pdf'), 'rb') as file:
    result = file.read()

  if os.path.exists(tmp):
    shutil.rmtree(tmp)

  return result

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

def lilypond(id, value):

  tmp = os.path.join(__tmp__, 'files', id)
  os.makedirs(tmp, exist_ok=True)

  if os.path.exists(os.path.join(tmp, 'output')):
    shutil.rmtree(os.path.join(tmp, 'output'))

  os.makedirs(os.path.join(tmp, 'output'), exist_ok=True)

  with open(os.path.join(tmp, 'input.ly'), 'w') as file:
    file.write(value)

  try:

    subprocess.check_output(
    [
      'lilypond',
      '-o', 'output',
      'input.ly',
    ],
    stderr=subprocess.STDOUT,
    cwd=tmp)

  except subprocess.CalledProcessError as e:

    stdout = e.output.decode(encoding='utf-8', errors='replace')
    stdout = stdout.replace(os.path.join(tmp, ''), '')
    return text(id, stdout, geometry='landscape')

  files = sorted(glob.glob(os.path.join(tmp, 'output', '*.pdf')))
  assert len(files) > 0, 'No compiled files found!'
  assert len(files) < 2, 'Multiple output files ({0}) are currently not supported!'.format(len(files))

  with open(files[0], 'rb') as file:
    result = file.read()

  if os.path.exists(tmp):
    shutil.rmtree(tmp)

  return result
