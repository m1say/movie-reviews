from django.conf import settings
import requests


def get_movie_reviews(query='', offset=0):
  url = getattr(settings, 'MOVIE_REVIEW_BASE_URL', '')
  api_key = getattr(settings, 'NY_TIMES_API_KEY', '')

  payload = { 'api-key': api_key, 'query': query, 'offset': offset }
  response = requests.get(url, params=payload)

  if response.status_code == requests.codes.ok:
    data = response.json()
    has_more = data['has_more']
    num_results = data['num_results']
    results = data['results']

    if isinstance(results, list):
      results = results[:10]
    else:
      results = []

    has_next = has_more or num_results > 10
    has_prev = offset != 0
    return has_prev, results, has_next

  raise Exception('Internal Server Error')
