from flask import Flask, render_template, url_for, request
from flask_cors import CORS
import boto3
from requests.auth import HTTPBasicAuth
from datetime import datetime
import pytz
import requests
import json
import os
import http.client
import mimetypes

url = "https://calendly.com/api/event_type_single_use_links"

payload = "{\"event_type_id\":replace_with_event_id}"
headers = {"add request headers":"here"}


fd_api = os.environ["FD_API_KEY"]
fd_check_ticket_url = "https://<replace_with_fd_site_name>.freshdesk.com/api/v2/tickets/"
fd_add_note_url=fd_check_ticket_url+"/notes"


tz = pytz.timezone('Asia/Kolkata')


# EB looks for an 'application' callable by default.
application = Flask(__name__, static_url_path='', static_folder="templates")
CORS(application, resources={r'/*': {'origins': '*'}})

@application.route('/')
def index():
    return render_template("index.html")


@application.route('/api/calendly', methods=['GET', 'POST'])
def create_calendly():
    ticket_id = request.args['ticket_id']
    add_to_ticket = request.args['add_to_ticket']
    print("Add to Ticket:{} and Type:{}".format(add_to_ticket,type(add_to_ticket)))

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    
    requestJSON = json.loads(response.text)
    bookingURL = requestJSON['booking_url']
    print(bookingURL)
    if(add_to_ticket=="true"):
        add_note(ticket_id,bookingURL)
    timestamp=datetime.now(tz)
    write_to_db(ticket_id,bookingURL,timestamp)
    return {"url": bookingURL}


def write_to_db(ticket_id,url,timestamp):
    print("Starting Procedure to write to DB")
    dynamodb = boto3.resource('dynamodb', region_name='replace_with_db_region_name')
    table = dynamodb.Table('replace_with_table_id')
    put_item=table.put_item(Item={'ticket_id': int(ticket_id),'url':url,'timestamp':str(timestamp)})
    return put_item


@application.route('/api/check_ticket', methods=['POST'])
def check_ticket():
    ticket_id = request.args['ticket_id']
    response = requests.request("GET", fd_check_ticket_url+ticket_id, auth=(fd_api,''))
    if(response.status_code == 200):
        return {"url_status": "valid"}
    else:
        return {"url_status": "invalid"}

def add_note(ticket_id,booking_url):
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    ticket_url = fd_check_ticket_url+ticket_id+''+"/notes"
    # print(ticket_url)
    message="One Time Calendly link is "+booking_url
    payload = "{\"body\":\""+message+"\"}"
    # print("Payload is {}".format(payload))
    response = requests.request("POST",ticket_url,auth=(fd_api,''), headers=headers ,data = payload)


# run the app.
if __name__ == "__main__":
    application.debug = False
    application.run()
