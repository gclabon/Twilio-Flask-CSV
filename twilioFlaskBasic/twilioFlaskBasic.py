import configobj, csv
from twilio.rest import TwilioRestClient
from operator import itemgetter
from flask import Flask, render_template, request
#----------------------------------------------------------------------
app = Flask(__name__)

@app.route('/', methods= ['GET'])
def returnForm():
    return render_template('./form.html')

@app.route('/', methods=['POST'])
def formPost():
    def send():
        """Open CSV file for contacts, define message content & send to each contact"""
        with open("contacts.csv") as csvfile:
            reader = csv.reader(csvfile)
            msg=request.form['msg']
            #ensure message length short enough for single message
            while len(msg) > 145:
                print ("Error! Only 145 characters allowed!")
                msg = input("Enter the message to send: ")
            for row in reader:
                #remove header line from CSV file
                if reader.line_num ==1:
                    continue
                to = itemgetter(2)(row)
                name = itemgetter(0)(row)
                msgNamed = (("Hi %s " + msg) %name)
                sendSms(msgNamed, to=to)

    def sendSms(msgNamed, to):
        """Get Twilio details from config file & send messages"""
        cfg = configobj.ConfigObj("./config.ini")
        sid = cfg["Twilio"]["sid"]
        authToken = cfg["Twilio"]["authToken"]
        twilioNumber = cfg["Twilio"]["twilioNumber"]
        client = TwilioRestClient(sid, authToken)
        message = client.messages.create(body=msgNamed, from_=twilioNumber, to=to,)
 
    send()
    return render_template('success.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)