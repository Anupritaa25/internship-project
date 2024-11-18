
from openai import OpenAI
import os
from datetime import datetime
import time
import subprocess

client = OpenAI()
os.environ.get("OPENAI_API_KEY")

file1 = open('observe.output', "r")
lines = file1.readlines()
count = 0
for line in lines:
    print(line)
    line2 = line[:19]
    os.chdir(dir)

    statusfile = os.path.expanduser("~/.decision_status.txt")
   
    if statusfile:
        file = open("decision_status.txt", "r")
        line1 = file.readline()
        datetime_format = "%Y-%m-%d %H:%M:%S"
        datetime1 = datetime.strptime(line1, datetime_format)
        datetime2 = datetime.strptime(line2, datetime_format)
        if datetime2 > datetime1:
            count += 1
    else:
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        file2 = "decision_status.txt"
        with (file2, 'w') as file:
            file2.write(timestamp)


    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
        "role": "system",
        "content": [
            {
            "text": "This is a patient monitoring system. You are an expert at monitoring the status of patients, and you will be given the description of the hospital room and asked to judge the status of the patient.\nThe expected state of the room is as follows: the patient should be lying on the bed. If there is no person in the room referred to in the description of the room, or there is a person on the floor, or the person has raised a hand, we need to alert the nursing staff.\nIf the current state is alarming, respond with \"ALARM\" followed by a message to the nursing staff. If not, respond with \"OK\". No yapping.",
            "type": "text"
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "The current state of the room is as follows:\n" + line
            }
        ]
        },

    ],
    temperature=1,
    max_tokens=512,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    response_format={
        "type": "text"
    }
    )

    print(line2 + " " + response.choices[0].message.content)

    file3 = open('sample_timestamps.txt', "w")
    file3.write(line2 + " " + response.choices[0].message.content)
    file3.close()

    subprocess.run(['python', 'send_sms.py'])



    time.sleep(30)


    
    
    
    
    
    


