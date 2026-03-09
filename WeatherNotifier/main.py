import requests
import datetime as dt
import smtplib
import os
from email.message import EmailMessage
from email.mime.text import MIMEText
import pandas

rainfall_alert_time=[]
time_check_period=[7,11,1,3,5]
location=[1,2]

MY_LAT_BANG="12.971599"
MY_LONG_BANG="77.594566"

MY_LAT_MUM="19.075983"
MY_LONG_MUM="72.877655"



my_api_full_day_forecast_bang="https://api.weatherapi.com/v1/forecast.json?key=3c0de8c0228d4cbdbf8172702260703&q=12.97,77.59&days=1"
my_api_full_day_forecast_mum="https://api.weatherapi.com/v1/forecast.json?key=3c0de8c0228d4cbdbf8172702260703&q=12.97,77.59&days=1"

username = "brucewayne78602@gmail.com"
password = os.getenv("EMAIL_PASS")

def get_current_weather(api_url):
    response=requests.get(api_url)
    if response.status_code == 200 and response.text:
            try:
                data = response.json()
            except Exception as e:
                print("Error occurred : ",e)
            else:
                cur_time=dt.datetime.now()
                cur_hour=cur_time.hour
                # print(cur_hour)
                cur_hour_forecast=data['forecast']['forecastday'][0]['hour'][cur_hour]
                today_max_min_temp=data['forecast']['forecastday'][0]['day']
                max_temp=today_max_min_temp['maxtemp_c']
                min_temp =today_max_min_temp['mintemp_c']
                # print((max_temp,min_temp))
                cur_temp=cur_hour_forecast['temp_c']
                cur_condition=cur_hour_forecast['condition']['text']
                rain_percentage=cur_hour_forecast['chance_of_rain']
                possibility_of_rain="Yes" if cur_hour_forecast['will_it_rain'] else "No"
                return cur_temp,cur_condition,rain_percentage,possibility_of_rain,max_temp,min_temp
    else:
        print("Error occurred : ",response.status_code)
        return 0

data=pandas.read_csv("./Info/userdata.csv")
data_dict=data.to_dict(orient="records")
bang_user=[value['email'] for value in data_dict if value['Location']=="BANG"]
mum_user=[value['email'] for value in data_dict if value['Location']=="MUM"]

with open("./Info/Weather_email_template.txt","r") as f:
    email_content=f.read()



for val in location:
    if val==1:
        result=get_current_weather(my_api_full_day_forecast_bang)
        if float(result[4])>=35 or result[3]=="Yes":
            with smtplib.SMTP_SSL("smtp.gmail.com",465) as connection:
                connection.login(user=username, password=password)
                msg=EmailMessage()
                msg['Subject']="Weather Notifier-BANG"
                msg['From']=username
                msg['To']=bang_user

                # final_temp = email_content.replace("{TEMP_C}", str(result[0])) \
                #     .replace("{CURRENT_CONDITION}", str(result[1])) \
                #     .replace("{RAIN_PERCENTAGE}", str(result[2])) \
                #     .replace("{POSSIBILITY_OF_RAIN}", str(result[3])) \
                #     .replace("{Max}", str(result[4])) \
                #     .replace("{Min}", str(result[5]))

                final_temp = email_content.format(
                    TEMP_C=result[0],
                    CURRENT_CONDITION=result[1],
                    RAIN_PERCENTAGE=result[2],
                    POSSIBILITY_OF_RAIN=result[3],
                    Max=result[4],
                    Min=result[5]
                )
                msg.set_content(final_temp, charset="utf-8")
                connection.send_message(msg)
                #print("Email sent to Bangalore team!")

    elif val==2:
        result=get_current_weather(my_api_full_day_forecast_mum)
        if float(result[4]) >= 35 or result[3] == "Yes":
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
                connection.login(user=username, password=password)
                msg = EmailMessage()
                msg['Subject'] = "Weather Notifier-BANG"
                msg['From'] = username
                msg['To'] = mum_user

                # final_temp = email_content.replace("{TEMP_C}", str(result[0])) \
                #     .replace("{CURRENT_CONDITION}", str(result[1])) \
                #     .replace("{RAIN_PERCENTAGE}", str(result[2])) \
                #     .replace("{POSSIBILITY_OF_RAIN}", str(result[3])) \
                #     .replace("{Max}", str(result[4])) \
                #     .replace("{Min}", str(result[5]))

                final_temp = email_content.format(
                    TEMP_C=result[0],
                    CURRENT_CONDITION=result[1],
                    RAIN_PERCENTAGE=result[2],
                    POSSIBILITY_OF_RAIN=result[3],
                    Max=result[4],
                    Min=result[5]
                )
                msg.set_content(final_temp,charset="utf-8")

                connection.send_message(msg)
                #print("Email sent to Mumbai team!")

