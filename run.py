import schedule, time, sys, os, runpy
from random import randint

print('script start')

# Set boolean value to keep looping until app is run
continue_loop = True

# Function to run application when triggered
def run_forgeant():

    # Run app
    file_globals = runpy.run_path('forgeant.py')

    # Set boolean to false to stop script
    global continue_loop
    continue_loop = False

# Set random time for the day

hour = randint(9, 16)
minute = randint(0, 59)

print('{}:{}'.format(hour,minute))

x = schedule.every().day.at('{}:{}'.format(hour, minute)).do(run_forgeant)
x = schedule.every(1).minutes.do(run_forgeant)

# Loop until time to run app
while continue_loop:

    # wait one minute
    time.sleep(5)

    # Run schedule
    schedule.run_pending()
