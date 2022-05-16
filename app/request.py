import requests,json





def get_qoute():
    
    result=requests.get('http://quotes.stormconsultancy.co.uk/random.json')
    if result.status_code==200:
        qoute=result.json()
        
    return qoute