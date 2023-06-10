from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
from bs4 import BeautifulSoup


app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request, response: Response):
    api_endpoint = "https://api.cricapi.com/v1/currentMatches?apikey=aada59e6-fdfa-49eb-b67a-52c74fe6a80c&offset=0"
    response = requests.get(api_endpoint)
    received = response.json()
    extracted_data = []
    for match in received.get('data', []):
        name = match.get('name')
        type = match.get('matchType').upper()
        status = match.get('status')
        venue = match.get('venue')
        teams = match.get('teams')
        score = match.get('score')
        id = match.get('id')

        extracted_fields = {
            'name': name,
            'type': type,
            'status': status,
            'venue': venue,
            'teams': teams,
            'id': id,
        }

        innings = []
        for runs in score:
            inning = runs.get('inning')
            team = inning.split(' Inning ')[0].upper()
            run = runs.get('r')
            wicket = runs.get('w')
            over = runs.get('o')

            innings.append({'team': team, 'inning': inning, 'run': run, 'wicket': wicket, 'over': over})

        extracted_fields['innings'] = innings
        extracted_data.append(extracted_fields)

    return templates.TemplateResponse('index.html', {'request': request, 'data': extracted_data})

