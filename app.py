# http://localhost/tool to open the PyWebIO app.

from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
from pywebio.input import *
from pywebio.output import *
import argparse
from pywebio import start_server

import pickle
import numpy as np
model = pickle.load(open('regression_rf.pkl', 'rb'))
app = Flask(__name__)


def predict():
    Year = input("WHEN DID YOU BOUGHT YOUR CAR (YEAR)::", type=NUMBER)
    Year = 2021 - Year
    Present_Price = input("HOW MANY ROKDA'S WERE SPENT (in LAKHS)", type=FLOAT)
    Kms_Driven = input("KITNA CHALLI HAI (in KMS)：", type=FLOAT)
    Kms_Driven2 = np.log(Kms_Driven)
    Owner = input("NUMBER OF PEEPS OWNED THIS CAR BEFORE YOU (0 or 1 or 2 or 3)", type=NUMBER)
    Fuel_Type = select('FUEL TYPE', ['Petrol', 'Diesel','CNG'])
    if (Fuel_Type == 'Petrol'):
        Fuel_Type = 239

    elif (Fuel_Type == 'Diesel'):
        Fuel_Type = 60

    else:
        Fuel_Type = 2
    Seller_Type = select('YOU A BULK BUYER OR A LUXURY ONE', ['Dealer', 'Individual'])
    if (Seller_Type == 'Individual'):
        Seller_Type = 106

    else:
        Seller_Type = 195
    Transmission = select('ARE YOU INTO MUSCLES OR EV?', ['Manual Car', 'Automatic Car'])
    if (Transmission == 'Manual Car'):
        Transmission = 261
    else:
        Transmission = 40

    prediction = model.predict([[Present_Price, Kms_Driven2, Fuel_Type, Seller_Type, Transmission, Owner, Year]])
    output = round(prediction[0], 2)

    if output < 0:
        put_text("OOPS! SORRY, BUMMER - YOU CAN'T SOLD THIS CAR")

    else:
        put_text('YOU CAN SELL THIS CAR AT THE BEST PRICE OF::',output)

app.add_url_rule('/tool', 'webio_view', webio_view(predict),
            methods=['GET', 'POST', 'OPTIONS'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(predict, port=args.port)
#if __name__ == '__main__':
    #predict()

# app.run(host='localhost', port=8080)
