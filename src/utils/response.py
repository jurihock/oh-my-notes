import flask
import flask.json

from flask import Response

def error(code):

    return flask.abort(code)

def redirect(endpoint, suffix='', **kwargs):

    return flask.redirect(flask.url_for(endpoint, **kwargs) + suffix)

def template(name, **kwargs):

    return flask.render_template(name, **kwargs)

def file(data, filename=None, mimetype=None):

    response = flask.make_response(data)

    if filename:
      response.headers.set('Content-Disposition', 'attachment', filename=filename)

    if mimetype:
      response.headers.set('Content-Type', mimetype)

    return response

def jsonify(*args, **kwargs):

  return flask.json.jsonify(*args, **kwargs)

def json(data, filename=None, callback=None):

    if callback:

        data = str(callback) + '(' + flask.json.dumps(data) + ')'

    return file(flask.json.dumps(data), filename=filename, mimetype='application/javascript')

def pdf(data, filename=None):

    return file(data, filename=filename, mimetype='application/pdf')

def tex(data, filename=None):

    return file(data, filename=filename, mimetype='application/x-tex')

def txt(data, filename=None):

    return file(data, filename=filename, mimetype='text/plain')

def csv(data, filename=None):

    return file(data, filename=filename, mimetype='text/csv')

def ics(data, filename=None):

    return file(data, filename=filename, mimetype='text/calendar')

def vcf(data, filename=None):

    return file(data, filename=filename, mimetype='text/vcard')
