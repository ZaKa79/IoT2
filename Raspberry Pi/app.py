#!/usr/bin/env python3

from time import sleep
import base64
from io import BytesIO
from matplotlib.figure import Figure
import sqlite3
from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def hello():
    while True:
        sleep(1)
        # connect to the database
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT datetime, lys FROM data ORDER BY id DESC LIMIT 50")
        data = cursor.fetchall()

        # separate the columns into x and y lists (pop removes date)
        time = [row[0].split(' ').pop(1) for row in data]
        lys = [row[1] for row in data]

        # close the connection
        conn.close()        
        
        # Generate the figure without using pyplot.
        fig = Figure(figsize=(14, 8))  # set the width to 8 inches and height to 6 inches

        ax = fig.subplots()
        y = [lys[49], lys[40], lys[30], lys[20], lys[10], lys[0]]
        x = [time[49], time[40], time[30], time[20], time[10], time[0]]

        #Navngivning af akser
        ax.set_xlabel('Tid')
        ax.set_ylabel('Lysniveau')

        #Farver
        ax.set_facecolor("#7C8281") #baggrund i figur
        fig.patch.set_facecolor('#1a936f') #baggrund på site
        ax.plot(x, y, c = '#11f', linewidth = '1.5',marker = 'd', mec = 'green', ms = 10, mfc = 'green' )

        ax.set_ylim([0, 4096 ]) # set the y-axis range
    
        # Save it to a temporary buffer.
        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")

        image = f"data:image/png;base64,{data}"
        return render_template("index.html", image=image, logo=url_for('static', filename='SL_LOGO.png'))


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)

