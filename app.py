# Create the necessary files for deploying the Python script on Render

from pathlib import Path

# Flask app file
app_py = Path("/mnt/data/app.py")
app_py.write_text('''\
from flask import Flask, request, jsonify
import requests
import hashlib
import json

app = Flask(__name__)

@app.route('/promo', methods=['POST'])
def promo():
    number = request.json.get('phone')
    password = request.json.get('pass')

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

    login = requests.post(url, json=payload, headers=headers).json()
    try:
        user_id = login['SignInUserResult']['UserData']["UserID"]
    except:
        return jsonify({"status": "error", "message": "رقم أو باسورد خطأ"})

    token_res = requests.post("https://services.orange.eg/GetToken.svc/GenerateToken",
                              headers={
                                  "Content-Type": "application/json; charset=UTF-8",
                                  "Host": "services.orange.eg",
                                  "User-Agent": "okhttp/3.14.9"
                              },
                              data=json.dumps({"channel": {"ChannelName": "MobinilAndMe", "Password": "ig3yh*mk5l42@oj7QAR8yF"}}))

    try:
        ctv = token_res.json()['GenerateTokenResult']['Token']
        htv = hashlib.sha256((ctv + ",{.c][o^uecnlkijh*.iomv:QzCFRcd;drof/zx}w;ls.e85T^#ASwa?=(lk").encode()).hexdigest().upper()
    except:
        return jsonify({"status": "error", "message": "خطأ في توليد التوكن"})

    final_headers = {
        "_ctv": ctv,
        "_htv": htv,
        "isEasyLogin": "false",
        "UserId": user_id,
        "Content-Type": "application/json; charset=UTF-8",
        "Host": "services.orange.eg",
        "User-Agent": "okhttpwhitepro/3.12.1"
    }

    final_body = {
        "Language": "ar",
        "OSVersion": "Android7.0",
        "PromoCode": "رمضان كريم",
        "dial": number,
        "password": password,
        "Channelname": "MobinilAndMe",
        "ChannelPassword": "ig3yh*mk5l42@oj7QAR8yF"
    }

    promo_res = requests.post("https://services.orange.eg/APIs/Promotions/api/CAF/Redeem",
                              headers=final_headers,
                              json=final_body)
    try:
        msg = promo_res.json()['ErrorDescription']
        if msg == "Success":
            return jsonify({"status": "success", "message": "✅ تم إرسال 500 ميجا 🎉"})
        elif msg == "User is redeemed before":
            return jsonify({"status": "error", "message": "❌ حصلت على 500 ميجا قبل كده"})
        else:
            return jsonify({"status": "error", "message": msg})
    except:
        return jsonify({"status": "error", "message": "❌ حصل خطأ غير متوقع"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
''')

# Requirements file
req_txt = Path("/mnt/data/requirements.txt")
req_txt.write_text("flask\nrequests")

# Procfile
procfile = Path("/mnt/data/Procfile")
procfile.write_text("web: python app.py")

"/mnt/data"  # Directory where files were saved

