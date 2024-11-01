from instagrapi import Client
from credentials import USERNAME, PASSWORD
cl = Client()
cl.login(USERNAME, PASSWORD)

user_id = cl.user_id_from_username('basangdataid')
medias = cl.user_medias(user_id, count=10)