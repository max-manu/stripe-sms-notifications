import requests,json,time,os
from twilio.rest import Client

def get_message(data):
    
    def tell(item,vaccine):
        text=' Hospital: {0}\n Address: {1}\n Vaccine: {2} '.format(item['name'],item['address'],vaccine)
        return text

    available=False
    vaccine=set()
    message=''
    total_vaccine=0
    dic=data
    for item in dic['centers']:
        for i in item['sessions']:
            #print(item)
            if i['min_age_limit']==18:
                if i['available_capacity_dose1']>0 and  item['block_name'] =='Haveli':
                    #tell()
                    available=True
                    text=i['vaccine']+'('+str(i['available_capacity_dose1'])+")"
                    vaccine.add(text)
                    total_vaccine+=1
                    #print(i,item)
        if available:
            message+=tell(item,', '.join(vaccine))+'\n\n'
            available=False
            vaccine=set()
    return message,total_vaccine
def send_telegram(message):
    
    parameter={'chat_id':'1799898826','text':message}
    token=os.environ['TELEGRAM_TOKEN']

    requests.get('https://api.telegram.org/bot{}/sendMessage'.format(token),params=parameter)

def send1(message='hello',heart_beat=1):
    if len(message)==0:
        return 'not send'
    account_sid =os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    
    client = Client(account_sid, auth_token)
    numbers=list(os.environ['numbers'].split())
    if heart_beat==1:
        
        for number in numbers:
            call = client.calls.create(
                                url='http://demo.twilio.com/docs/voice.xml',
                                to = '+91'+number,
                                from_='+12017194978'
                            )
            # message = client.messages.create(
            #                         body=message,
            #                         from_='whatsapp:+14155238886',
            #                         to='whatsapp:+91'+number
            #                     )
            
    else:
        pass
        # message = client.messages.create(
        #                             body="Bot working well",
        #                             from_='whatsapp:+14155238886',
        #                             to='whatsapp:+91'+numbers[0]
        #                         )


def data(date):
    parameters={
    'district_id':'363',
    'date':date
    }
    r=requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict',params=parameters)
    #text=json.dumps(r.json(),indent=4)
    dic=r.json()
    #print(text)
    return dic
#strftime(gmtime())

def run():
    os.environ['TZ'] = 'india-05:30'
    time.tzset()
    send_telegram('app started')
    while True:
        date=time.strftime('%d-%m-%Y')
        H=time.strftime('%H')
        M=time.strftime('%M')
        HM=H+":"+M
        Sec=time.strftime('%S')
        if HM in('07:00','19:00') and int(Sec) in range(5)  :
            send_telegram("BOT beat @ {}:{}:{}".format(H,M,Sec),0)
        else:
            message,total_vaccine=get_message(data(date))
            send_telegram(message)
            if H in range(6,21) and total_vaccine>=2:
                send_call(message)
        time.sleep(5)
if __name__ == "__main__":        
    run()
