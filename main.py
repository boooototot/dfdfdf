import os
try:
    import requests
except:
    os.system('pip install requests')
import hashlib
import json

f = input
ff = print

number = f('Enter Your number : ')
password = f('Enter Your pasaword : ')

url = "https://services.orange.eg/SignIn.svc/SignInUser"
payload = {
  "appVersion": "9.0.0",
  "channel": {
    "ChannelName": "MobinilAndMe",
    "Password": "ig3yh*mk5l42@oj7QAR8yF"
  },
  "dialNumber": number,
  "isAndroid": True,
  "lang": "ar",
  "password": password,
}

headers = {
  'User-Agent': "okhttp/4.10.0",
  'Connection': "Keep-Alive",
  'Accept-Encoding': "gzip",
  'Content-Type': "application/json; charset=UTF-8"
}

response = requests.post(url, data=json.dumps(payload), headers=headers)

try:
    fox = response.json()['SignInUserResult']['UserData']["UserID"]
except:
    ff('error number or password')
    exit()

url1 = "https://services.orange.eg/GetToken.svc/GenerateToken"
headers1 = {
    "Content-Type": "application/json; charset=UTF-8",
    "Host": "services.orange.eg",
    "User-Agent": "okhttp/3.14.9"
}
data1 = '{"channel":{"ChannelName":"MobinilAndMe","Password":"ig3yh*mk5l42@oj7QAR8yF"}}'
response = requests.post(url1, headers=headers1, data=data1)

try:
    ctv = response.json()['GenerateTokenResult']['Token']
    h = hashlib.sha256((ctv + ",{.c][o^uecnlkijh*.iomv:QzCFRcd;drof/zx}w;ls.e85T^#ASwa?=(lk").encode()).hexdigest()
    htv = h.upper()
except:
    print('Error : حدث خطاء في تخطي ctv و htv')
    exit()

url4 = "https://services.orange.eg/APIs/Promotions/api/CAF/Redeem"
headers4 = {
    "_ctv": ctv,
    "_htv": htv,
    "isEasyLogin": "false",
    "UserId": fox,
    "Content-Type": "application/json; charset=UTF-8",
    "Host": "services.orange.eg",
    "User-Agent": "okhttpwhitepro/3.12.1"
}
json4 = {
    "Language": "ar",
    "OSVersion": "Android7.0",
    "PromoCode": "رمضان كريم",
    "dial": number,
    "password": password,
    "Channelname": "MobinilAndMe",
    "ChannelPassword": "ig3yh*mk5l42@oj7QAR8yF"
}
response4 = requests.post(url4, headers=headers4, json=json4)
print(response4.text)
try:
    ErrorDescription = response4.json()['ErrorDescription']
    if ErrorDescription == "Success":
        ff('𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹 : DONE SEND 500 MG 🎉')
    elif ErrorDescription == "User is redeemed before":
        ff('𝐄𝐑𝐎𝐑𝐑🔴 : You take 500MG before')
    else:
        ff(f'𝐄𝐑𝐎𝐑𝐑🔴 : {ErrorDescription}')
except:
    ff('𝐄𝐑𝐎𝐑𝐑🔴 : try agien')
    exit()
