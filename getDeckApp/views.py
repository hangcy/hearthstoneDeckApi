from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

import json
import requests
import random

from getDeckApp.models import Card


def index(request):
	response = json.dumps([{}])
	return HttpResponse(response, content_type = 'text/json')

def get_deck(request, card_player_class):
	if request.method == 'GET':
		try:
			dbData = Card.objects.all()
			# Get cards data from API if database has no data.
			if not dbData:
				url = "https://omgvamp-hearthstone-v1.p.rapidapi.com/cards/sets/Rastakhan%27s%20Rumble"

				headers = {
					'x-rapidapi-host': "omgvamp-hearthstone-v1.p.rapidapi.com",
					'x-rapidapi-key': "ZTMJtzbYvXmshPTFEZI4ztIy3I68p1nPwgHjsnIGukKZeJxGcs"
				}

				response = requests.get(url,headers=headers)
				objects = json.loads(response.text)

				# Loop until all cards data are inserted into database.
				for counter in range(0, len(objects)):
					obj = objects[counter]
					# Data massage for cards wih no playerClass key.
					if 'playerClass' in obj:
						playerClazz = obj['playerClass']
					else:
						playerClazz = 'N/A'

					card = Card(dbf_id = obj['dbfId'], name = obj['name'], player_class = playerClazz)
					card.save()

			cards = Card.objects.filter(player_class = card_player_class) | Card.objects.filter(player_class = 'Neutral')
			deck = []
			# Randomly insert 30 cards into deck with duplication checking.
			while len(deck) < 30:
				selectedCard = random.choice(cards)

				if deck.count(selectedCard) < 2:
					deck.append(selectedCard)

			response  = serializers.serialize('json', deck)
		except Exception as e:
			print('Failed to get_deck:' + str(e))
			response = json.dumps([{'Error': 'Could not retrieved'}])

	return HttpResponse(response,content_type = 'text/json')