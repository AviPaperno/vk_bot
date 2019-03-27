import requests
import vk
import config

def upload_file(file_name,user_id):
    upload_url = api.docs.getMessagesUploadServer(peer_id=user_id,v = '5.74')['upload_url']
    request = requests.post(upload_url, files={'file': open(file_name, "rb")})
    return request.json()['file']
