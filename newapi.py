# 28-01-2021 Rev 1
# sudo ps -ax | grep python
# sudo kill <pid>
#
# https://github.com/StephenDsouza90/python-flask-restplus-rest-api


import RPi.GPIO as GPIO
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from flask import Flask, render_template, json, request
from flask_restplus import Api, Resource, fields
from datetime import datetime, time

# Threaded Timer
import time
from threading import Event, Thread

#GPIO Mode
GPIO.setmode(GPIO.BCM)
#Switch off the warnings
GPIO.setwarnings(False)

app = Flask(__name__)

api = Api(app, 
          version='1.0', 
          title='Vijver en tuin verlichting automation', 
          description='Een eenvoudige API-REST application',
          )
          
not_found = {"message": "Not Found"}
success = {"message": "Success"}
failed = {"message": "Failed"}

          
# Device Data Resource: A list of device data 
device_data = [
    {"device_name": "Main Pomp    ", "device_id": 1, "gpio_pin_num": 17, "relais_NO_NC" : "NC"},
    {"device_name": "UV Lamp      ", "device_id": 2, "gpio_pin_num": 18, "relais_NO_NC" : "NO"},
    {"device_name": "Waterval     ", "device_id": 3, "gpio_pin_num": 27, "relais_NO_NC" : "NO"},
    {"device_name": "Waterval Lamp", "device_id": 4, "gpio_pin_num": 22, "relais_NO_NC" : "NO"},
    {"device_name": "Schutting L  ", "device_id": 5, "gpio_pin_num": 26, "relais_NO_NC" : "NO"},
    {"device_name": "Schutting R  ", "device_id": 6, "gpio_pin_num": 25, "relais_NO_NC" : "NO"},
    {"device_name": "Lamp 1       ", "device_id": 7, "gpio_pin_num": 23, "relais_NO_NC" : "NO"},
    {"device_name": "Lamp 2       ", "device_id": 8, "gpio_pin_num": 24, "relais_NO_NC" : "NO"}
]

device = api.model("Device", {
    "device_name": fields.String("Device Name")
})

# Timer Data Resource: A list of timer data 
timer_data = [
    {"timer_id": 1, "device_id": 1, "timer_active": 0, "timer_start": "01:00", "timer_end": "00:00"},
    {"timer_id": 2, "device_id": 2, "timer_active": 0, "timer_start": "02:00", "timer_end": "00:00"},
    {"timer_id": 3, "device_id": 3, "timer_active": 0, "timer_start": "03:00", "timer_end": "00:00"},
    {"timer_id": 4, "device_id": 4, "timer_active": 0, "timer_start": "04:00", "timer_end": "00:00"},
    {"timer_id": 5, "device_id": 5, "timer_active": 0, "timer_start": "05:00", "timer_end": "00:00"},
    {"timer_id": 6, "device_id": 6, "timer_active": 0, "timer_start": "06:00", "timer_end": "00:00"},
    {"timer_id": 7, "device_id": 7, "timer_active": 0, "timer_start": "07:00", "timer_end": "00:00"},
    {"timer_id": 8, "device_id": 1, "timer_active": 0, "timer_start": "08:00", "timer_end": "00:00"}
]

timer = api.model("Timers", {
    "device_timer": fields.String("Timer Time")
}) 


# Assignment Data Resource: A list of timers assigned to devices 
assignment_data = [] # {"device_id": 1, "timer_id": 1},

assignment = api.model("Appliance", {
    "device_id": fields.Integer(),
    "timer_id": fields.Integer()
})

# *****************************************************************************
# Return all devices
# *****************************************************************************
@api.route("/devices")
class Devices(Resource):

    def get(self):
        return device_data

    @api.expect(device)
    def post(self):
        new_device = api.payload
        new_device["device_id"] = len(devices_data) + 1
        device_data.append(device_course)
        return success, 201

# *****************************************************************************
# Return single device id
# *****************************************************************************
@api.route("/devices/<int:device_id>")
class Devices(Resource):

    def get(self, device_id):
        for device in device_data:
            if device["device_id"] == device_id:
                return device
        return not_found, 404

# *****************************************************************************
# Return all timers
# *****************************************************************************
@api.route("/timers")
class Timers(Resource):

    def get(self):
        return timer_data

#    @api.expect(timer)
#    def post(self):
#        """ Add a new course """
#
#        new_device = api.payload
#        new_device["device_id"] = len(device_data) + 1
#        device_data.append(device_course)
#        return success, 201

# *****************************************************************************
# Return single timer id
# *****************************************************************************             
@api.route("/timers/<int:timer_id>")
class Timers(Resource):

    def get(self, timer_id):
        for timer in timer_data:
        
            print("timer_id = ", timer_id);
            
            if timer["timer_id"] == timer_id:
                return timer
            else:
                return not_found, 404
            
# *****************************************************************************
# Timer count per device id
# *****************************************************************************            
@api.route("/timers/count/<int:device_id>")
class Timers(Resource):

    def get(self, device_id):
      
        found_device = False
        count_timers = 0
        
        for timer in timer_data:
            if timer["device_id"] == device_id:
                count_timers += 1
                found_device = True

        if found_device:
            return count_timers
        else:
            return not_found, 404


# *****************************************************************************
# Return timer id's per device id
# *****************************************************************************  
@api.route("/timers/devices/<int:device_id>")
class Timers(Resource):

    def get(self, device_id):
      
        found_device = False
        count_timers = 0
        found_device_timers = []
        
        for timer in timer_data:
            if timer["device_id"] == device_id:
                found_device_timers.append(timer["timer_id"])
                count_timers += 1
                found_device = True
                
        print("count_timers = ", count_timers);
        print("found_device_timers = ", found_device_timers);        
                
        if found_device:
            return found_device_timers
        else:
            return not_found, 404

            
# *****************************************************************************
# *****************************************************************************
    
# --------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5010, host='0.0.0.0')     