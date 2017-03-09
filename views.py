from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader

import requests
import json




def home_page(request):

	if not request.GET.get('code'):
		return HttpResponseRedirect('https://accounts.spotify.com/authorize/?&client_id=0c80f57cc6594ada93bfdbdacb8b5037&response_type=code&scope=playlist-modify-private&redirect_uri=http://127.0.0.1:8000/')

	code = request.GET.get('code')
	# POST https://accounts.spotify.com/api/token
	postData = {
			'grant_type': 'authorization_code',
			'code': code,
			'redirect_uri': 'http://127.0.0.1:8000/',
			'client_id': '0c80f57cc6594ada93bfdbdacb8b5037',
			'client_secret': '746f3b762f1c4cd1a59608f344faa335',

	}

	r = requests.post('https://accounts.spotify.com/api/token', postData)

	access = r.json().get('access_token')


	playlist_header = {
			'Authorization': 'Bearer ' + access,
			'Content-Type': 'application/json'

	}

	get_user = requests.get(
		'https://api.spotify.com/v1/me',
		headers = playlist_header
	)

	user = get_user.json().get('id')

	# print user


	playlist_data = {
			'name': 'Test',
			'public': 'false'

	}

	playlist_data = json.dumps(playlist_data)
	playlist_create = requests.post(
		'https://api.spotify.com/v1/users/' + user + '/playlists',
		data = playlist_data,
		headers = playlist_header
		)

	# print playlist_create.text

	template = loader.get_template('songs/home.html')

	context = {
			'code': code,
			'access': access
			
	}
	return HttpResponse(template.render(context, request))
