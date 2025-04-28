from flask import Flask, render_template, request
import requests
import base64
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    message = ''
    if request.method == 'POST':
        number = request.form['number']
        password = request.form['password']
        email = request.form['email']

        if "011" in number:
            num = number[+1:]
        else:
            num = number
        
        code = email + ":" + password
        ccode = code.encode("ascii")
        base64_bytes = base64.b64encode(ccode)
        auth = base64_bytes.decode("ascii")
        xauth = "Basic" + " " + auth

        urllog = "https://mab.etisalat.com.eg:11003/Saytar/rest/authentication/loginWithPlan"

        headerslog = {
            "applicationVersion": "2",
            "applicationName": "MAB",
            "Accept": "text/xml",
            "Authorization": xauth,
            "APP-BuildNumber": "964",
            "APP-Version": "27.0.0",
            "OS-Type": "Android",
            "OS-Version": "12",
            "APP-STORE": "GOOGLE",
            "Is-Corporate": "false",
            "Content-Type": "text/xml; charset=UTF-8",
            "Host": "mab.etisalat.com.eg:11003",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/5.0.0-alpha.11",
            "ADRUM_1": "isMobile:true",
            "ADRUM": "isAjax:true"
        }

        datalog = "<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><loginRequest><deviceId></deviceId><firstLoginAttempt>true</firstLoginAttempt><modelType></modelType><osVersion></osVersion><platform>Android</platform><udid></udid></loginRequest>"
        log = requests.post(urllog, headers=headerslog, data=datalog)

        if "true" in log.text:
            st = log.headers["Set-Cookie"]
            ck = st.split(";")[0]
            br = log.headers["auth"]

            url22 = 'https://mab.etisalat.com.eg:11003/Saytar/rest/servicemanagement/submitOrderV2'

            headers22 = {
                'applicationVersion': '2',
                'applicationName': 'MAB',
                'Accept': 'text/xml',
                'Cookie': ck,
                'Language': 'ar',
                'APP-BuildNumber': '10493',
                'APP-Version': '30.1.0',
                'OS-Type': 'Android',
                'OS-Version': '7.1.2',
                'APP-STORE': 'GOOGLE',
                'auth': "Bearer " + br,
                'Is-Corporate': 'false',
                'Content-Type': 'text/xml; charset=UTF-8',
                'Host': 'mab.etisalat.com.eg:11003',
                'Connection': 'Keep-Alive',
                'Accept-Encoding': 'gzip',
                'User-Agent': 'okhttp/5.0.0-alpha.11',
                'ADRUM_1': 'isMobile:true',
                'ADRUM': 'isAjax:true'
            }

            data22 = "<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><submitOrderRequest><mabOperation></mabOperation><msisdn>%s</msisdn><operation>REDEEM</operation><productName>DOWNLOAD_GIFT_1_SOCIAL_UNITS</productName></submitOrderRequest>"%(num)

            response = requests.post(url22, headers=headers22, data=data22).text

            if "true" in response:
                message = "تم إضافة 500 ميجا بنجاح!"
            else:
                message = "حدث خطأ أثناء تنفيذ الطلب."
        else:
            message = "فشل تسجيل الدخول. تأكد من البيانات."

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
