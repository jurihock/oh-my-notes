from app import app

@app.template_filter('shorten')
def shorten(values, value, limit):

  limit = int(limit)
  halflimit = int(limit/2)

  try:

    if len(values) <= limit:
      return (None, None)

    index = values.index(value)

    if index <= halflimit:
      return (values[:limit], +1)

    if (len(values) - index - 1) <= halflimit:
      return (values[-limit:], -1)

    offset = index - halflimit
    values = list(values[offset:] + values[:offset])

    return (values[:limit], 0)

  except:

    return (None, None)
