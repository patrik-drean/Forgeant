import schedule, time, sys, os, runpy
from random import randint
import psycopg2, pprint, os.path, csv, datetime, schedule, time
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Color, Ellipse
from kivy import core
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy import uix
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from uuid import getnode as get_mac

print('script start')

# Set boolean value to keep looping until app is run
continue_loop = True

# Function to run application when triggered
def run_forgeant():
    # Set boolean to false to stop script
    global continue_loop
    continue_loop = False

    # Run app
    file_globals = runpy.run_path('forgeant.py')



# Set random time for the day

hour = randint(9, 16)
minute = randint(0, 59)

print('{}:{}'.format(hour,minute))

x = schedule.every().day.at('{}:{}'.format(hour, minute)).do(run_forgeant)
# x = schedule.every(1).minutes.do(run_forgeant)

# Loop until time to run app
while continue_loop:

    # Check if setup was done
    if os.path.exists('data/demographic_info.csv') == False:
        run_forgeant()

    if continue_loop:
        # wait one minute
        time.sleep(59)

    # Run schedule
    schedule.run_pending()
