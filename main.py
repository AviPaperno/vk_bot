from data_conv import create_doc,create_nice_date
from config import *
from requests import *
import vk

session = vk.Session(access_token = VK_API_ACCESS_TOKEN)
api = vk.API(session, v = VK_API_VERSION)

longPoll = api.groups.getLongPollServer(group_id = GROUP_ID)
server, key, ts = longPoll['server'], longPoll['key'], longPoll['ts']

Users = {}

def upload_file(file_name):
    upload_url = api.docs.getWallUploadServer(group_id=GROUP_ID)['upload_url']
    request = post(upload_url, files={'file': open(file_name, "rb")})
    file_rez = api.docs.save(file = request.json()['file'],title = file_name)[0]
    print(file_rez)
    return 'doc'+str(file_rez['owner_id'])+'_'+str(file_rez['id'])

def encode_to_correct_answer(inp_data):
    return inp_data['first_name'], inp_data['last_name']

while True:
    # Последующие запросы: меняется только ts
    longPoll = post('%s'%server, data = {'act': 'a_check',
                                         'key': key,
                                         'ts': ts,
                                         'wait': 25}).json()

    if longPoll['updates'] and len(longPoll['updates']) != 0:
        for update in longPoll['updates']:
            if update['type'] == 'message_new':
                info = api.users.get(user_id = update['object']['user_id'])[0]
                ans_0 = encode_to_correct_answer(info)
                try:
                    tmp = update['object']['body'].split()
                    bday = [int(i) for i in tmp[0].split('.')]
                    try:
                        if tmp[1].lower() == 'после':
                            bday[0]+=1
                    except:
                        pass
                    name = ans_0[0]+" "+ans_0[1]
                    fname = str(update['object']['user_id'])+'.pdf'
                    create_doc(update['object']['user_id'],name,*bday)
                    file_d = upload_file(fname)
                    api.messages.send(peer_id=update['object']['user_id'],message = "Ваш сертификат готов!", attachment = file_d)
                except Exception as e:
                    api.messages.send(peer_id=update['object']['user_id'], message="Я не могу распознать дату рождения. Попробуй ещё раз, формат : ДД.ММ.ГГГГ до/после, например 12.04.1994 до"+str(e))

    ts = longPoll['ts']
