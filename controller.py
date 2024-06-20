import requests
import datetime
import json

chave= '1bebbc645d7db8fbf9319e8735fe94d1'
api_link = 'http://api.openweathermap.org/data/2.5/forecast?id=524901&appid={}'.format(chave)

#fazendo chamada da API usando request
