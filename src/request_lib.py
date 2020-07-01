
import requests #it is a blocking library by nature !
import asyncio
import urllib
import functools
from src import scrape_elements
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib3.exceptions import NewConnectionError



PROXIES = {
    #not working
    'http': "167.71.165.106",
    'https': "140.82.61.218"
    
}

cookies = {
    "Cookie":"SFSESSIONID=1eb3dddd-5cf9-4318-94eb-5d14ab678aca; hbus_anonymousId=9fbf-34c5-c555-cdc0-d202-1cf0-323b-9e3e; _hjid=002b716a-d1de-4359-80d1-6a4d86ddd113; _fbp=fb.1.1568722947157.1151055043; _ga=GA1.2.645376679.1568722950; cookieconsentanon=false%7C9%2F24%2F2019%2C%203%3A23%3A50%20PM; __zlcmid=ukibn8bzdAIdPW; cookieconsentauth=true; hb_privacy=1; optimizelyEndUserId=oeu1571272979247r0.5020110549755761; hblg=11_1; visid_incap_2112677=Ar+97Xm8RaKWcJsvvvib7UUUxF0AAAAAQUIPAAAAAAAL2PrzHDPPmiqSotBeIE2M; __gads=ID=3b74a071d1117992:T=1573341486:S=ALNI_MauUvPsp9dYuSz5--BVE7phLG5GzA; useinternal=true; wt_fa=lv~1588431081433|1619535081433#cv~5|1619535081433#fv~2019-10|1602376749549#vf~102|1619535081432#; jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBcHBLZXkiOiJBRjdGMkEzNy1DQzRCLTRGMUMtODdGRC1GRjM2NDJGNjdFQ0IiLCJFbWFpbCI6ImJlcmtheS5rb2Nha0Bob3RtYWlsLmNvbSIsIkZpcnN0TmFtZSI6IkJlcmtheSIsIkdlbmRlciI6IjEiLCJJc0F1dGhlbnRpY2F0ZWQiOiJUcnVlIiwiSXNMYXp5UmVnaXN0cmF0aW9uIjoiMCIsIkxhc3ROYW1lIjoiS0_Dh0FLIiwiTWlncmF0aW9uRmxhZyI6IjAiLCJQYXJ0bmVyVHlwZUNvZGUiOiIwIiwiU2hhcmVEYXRhUGVybWlzc2lvbiI6IlRydWUiLCJUaXRsZSI6IkJlcmtheSBLT8OHQUsiLCJUb2tlbklkIjoiM0VBNDYxREMtRjA5QS00RTY0LUI2MjktMzZCMTNBODA3QzZFIiwiVHlwZUNvZGUiOiIxIiwiVXNlcklkIjoiYzdiNDNjOGYtNTQ3ZS00Y2VhLTk0ZjgtYThiNzI4Y2M4Y2FlIiwiU2Vzc2lvbklkIjoiMWViM2RkZGQtNWNmOS00MzE4LTk0ZWItNWQxNGFiNjc4YWNhIiwibmJmIjoxNTg4NDU4Mjg3LCJleHAiOjE1ODg0NjU0ODcsImlhdCI6MTU4ODQ1ODI4N30.HRUwDlgy-6D-VI5Kr-tBmq9p6thXvh_gUNlUDLSJGm8; anon=6D8D394BBAD2F36D08B51B31D5C60FC9AA9992159359791E1E760DDF252372C1405666D3525E2B8B91A2F8D6F1200FD445172DC28215EE75C62AFBE2AAEFD7C0CE9BAB5EC0F553632EFA76C108887D3882F3D2058A377749DC8A3AF290E1932580B4D1221421B87637EDCDA4924EE50B495358E9C68EF5931F83680CD132CFB7DF43A056B554394FB9F925D678BEB6E814BE3C150DB3E87C006D754EDC8D6C489E3699276B416A4428F1A4ECFC0BB154546F4027B54D5E30CD863E5811E3600822E81B786FB5766C3B2F451C24703F870C115C6BD1A2DD0D02A7ABA0C425E15FE72E64F824BD872894AC6EA6755D371B1BF469B1FAC1339D06CA58A35FC7F7DFF63D8F58D3712982F81CBDFB7994AADA27698DB32B763CAE73E5BB93C4EE44E8438DC4BEDEC465669F96247F7E383207D491E5A5D0AE2C6CFEB23AA8AB85ED5AB7EF1A86DBB7FE997C36CE437B2DE4321ABDC59DB6422EC86D6FD7602FC48764FCC62E561AADE95C2D3B284043371F57050DB9116C6ED2790DDB9D25; newhbv1=6D8D394BBAD2F36D08B51B31D5C60FC9AA9992159359791E1E760DDF252372C1405666D3525E2B8B91A2F8D6F1200FD445172DC28215EE75C62AFBE2AAEFD7C0CE9BAB5EC0F553632EFA76C108887D3882F3D2058A377749DC8A3AF290E1932580B4D1221421B87637EDCDA4924EE50B495358E9C68EF5931F83680CD132CFB7DF43A056B554394FB9F925D678BEB6E814BE3C150DB3E87C006D754EDC8D6C489E3699276B416A4428F1A4ECFC0BB154546F4027B54D5E30CD863E5811E3600822E81B786FB5766C3B2F451C24703F870C115C6BD1A2DD0D02A7ABA0C425E15FE72E64F824BD872894AC6EA6755D371B1BF469B1FAC1339D06CA58A35FC7F7DFF63D8F58D3712982F81CBDFB7994AADA27698DB32B763CAE73E5BB93C4EE44E8438DC4BEDEC465669F96247F7E383207D491E5A5D0AE2C6CFEB23AA8AB85ED5AB7EF1A86DBB7FE997C36CE437B2DE4321ABDC59DB6422EC86D6FD7602FC48764FCC62E561AADE95C2D3B284043371F57050DB9116C6ED2790DDB9D25; _gaexp=GAX1.2.Yc0x4ur2RTGCYOuS7WxbzA.18462.x983; _gac_UA-834379-1=1.1589289355.CjwKCAjwkun1BRAIEiwA2mJRWRMa-o_DMFtnLXA7G7VQCwBEc74pHFCsPJbUpmLK6pihZRzBQmglOBoClRUQAvD_BwE; _gid=GA1.2.2131315975.1589538399; ab.storage.deviceId.a19ee87d-6625-49ed-ad8c-f427b0067dec=%7B%22g%22%3A%22be2f4b8a-9fdc-3410-daad-8df6303656ea%22%2C%22c%22%3A1589538400070%2C%22l%22%3A1589538400070%7D; ab.storage.userId.a19ee87d-6625-49ed-ad8c-f427b0067dec=%7B%22g%22%3A%22c7b43c8f-547e-4cea-94f8-a8b728cc8cae%22%2C%22c%22%3A1589538400077%2C%22l%22%3A1589538400077%7D; isFavoritesRequiredToReload=false; isGlobalIp=0; HB_S_MR=1; wt3_sid=%3B289941511384204; _hjShownFeedbackMessage=true; ASP.NET_SessionId=pkgl0w33wxlbujydihdruaxe; wt3_eid=%3B289941511384204%7C2156872294600500228%232158963706800710163%3B692379182816325%7C2157127279100569316%232157127304400775644; ab.storage.sessionId.a19ee87d-6625-49ed-ad8c-f427b0067dec=%7B%22g%22%3A%221d00fe3d-f5d3-da6d-0fe3-dfce0a82b3e1%22%2C%22e%22%3A1589638868991%2C%22c%22%3A1589634610303%2C%22l%22%3A1589637068991%7D; hbus_sessionId=e9c3bf73-1d83-41e3-2f25-36f9e7564abe%7C1589642501304; datadome=ZOIDsGT6WCpNPrN3Q_MAsIqdh18nkO1PK4BSKhLk9J28fVZZNLS7-.lOuKHGeMxDDaC~dwomhNt.2MZ_K9apgktgU1inI_CN.4ekFOqW6l"
}

headers = {
    'User-agent' :  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    "Referer": "https://www.google.com/",
    }

"""
def GET_request (url):
    """ """
    GET request without asynch

    Uses a session to let cookie based tracking
    """ """
    try:
        session = requests.Session()
        session.headers = headers
        retry = Retry(connect=1, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        response = session.get(url,allow_redirects=True)
        contentToReturn = response.content
        session.close()
        return contentToReturn

    except Exception as e:
        print(" @@@@ ERROR IN SIMPLE GET @@@@ : "+ str(e))  
"""

#WARNING - when connection lost, it needs to retry.ATM it just throws exception.
#Also you need to make it a stream!
async def GET_request_async (vendor,url):
    """
    Asyncio used here.

    we create event loops to parallel request process. It simply runs it on another thread and returns to main one.
    """  
   
    #session.proxies = PROXIES
    website = scrape_elements.websites[vendor]
    session = requests.Session()

    session.headers = headers

    retry = Retry(connect=1, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    loop = asyncio.get_event_loop()

    try:
       
        future = loop.run_in_executor(None, functools.partial( session.get, url,timeout=10))
        #response = await asyncio.wait_for(future, timeout=10)
        response = await future
        redirected = response.url != url

        #It looks redirecting because sometimes while trying to find last sub page of a product,
        #website simply redirects from none existing sub page query to main page.
        
        if website['redirect-allowed']: pass
        else:
            if redirected: return None
            else: pass
                
    except requests.exceptions.Timeout as err: 
        print(" @@@@ ERROR IN ASYNCH REQUEST -- TIMEOUT @@@@ \n MESSAGE : "+ str(err))
        session.close()
        return None
    except Exception as e:
        print(" @@@@ ERROR IN ASYNCH REQUEST @@@@ \n MESSAGE : "+ str(e))
        session.close()
        return None
    session.close()
    return  response.content 

#TODO - stream
def GET_request_stream (url):
    print("! UNDER CONSTRUCT !")
    """
    response = requests.get(url, stream=True)
    # if the server sent a Gzip or Deflate compressed response, decompress
    # as we read the raw stream:
    response.raw.decode_content = True

    events = ElementTree.iterparse(response.raw)
    for event, elem in events:
        # do something with `elem`
    """