# Download the helper library from https://www.twilio.com/docs/python/install
import os
import argparse
from datetime import datetime
from twilio.rest import Client
import time

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ["KEY1"]
auth_token = os.environ["KEY2"]
client = Client(account_sid, auth_token)



def main():

    parser = argparse.ArgumentParser(prog= 'send_sms.py', description= 'send a text message with the timestamp conveying the condition of the patient')
    parser.add_argument('-i', '--input', type = str, help = 'text file from which timestamps are read', default = 'sample_timestamps.txt')
    args = parser.parse_args()

    file1 = open("sample_timestamps.txt", "r")
    lines = file1.readlines()

    statusfile = os.path.expanduser("~/.sample_sms_status.txt")
    if statusfile:
        file2 = open("sample_sms_status.txt", "r")
        secondLine = file2.readline()
        print(secondLine)
        count = 0
        for line in lines:
            message = client.messages.create(
                      body=line,
                      from_="+18636177312",
                      to="+918329514909",
                    )
            print(message.body)

            if "OK" in line:
                count += 1
                print(line)
            else:
                datetime_format = "%Y-%m-%d %H:%M:%S"
                line1 = line[:19]
                line2 = secondLine[:19]
                print(line1)
                print(line2)
                datetime1 = datetime.strptime(line1, datetime_format)
                datetime2 = datetime.strptime(line2, datetime_format)
                if datetime1 < datetime2:
                #Go to the next line in the file
                    count += 1
                    print(line)
                    file3 = "sample_sms_status.txt"
                    with open(file3, 'w') as file:
                        file.write(line1)
                    
    else:
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        file4 = "sample_sms_status.txt"
        with open(file4, 'w') as file:
            file.write(timestamp)
    time.sleep(30)

    
main()
                

