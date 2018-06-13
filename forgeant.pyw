import psycopg2, pprint, os.path, csv
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Color, Ellipse
from kivy.core.window import Window
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

################################
### Window & database setup  ###
################################

# Indicate position of app window
# Window.left = 500
# Window.top = 400

pp = pprint.PrettyPrinter(indent=4)

# Connect to database
conn = psycopg2.connect(
    database='incasokh',
    user='incasokh',
    password='tmWwE8HPOYjJmAOymB16_vtNO2GILb1i',
    host='elmer.db.elephantsql.com',
    port='5432')

# Open cursor to interact with database
cur = conn.cursor()

# Set initial window size
Window.size = (700, 350)

# Turn off ability to exit screen
Window.borderless = True

# Turn background clear
Window.clearcolor = (1, 1, 1, 1)

############################
### Methods to be called ###
############################

# Record response and close app in ForgeantApp
def record_feeling_submission_to_db(feeling_response):

    # Developer printout
    print('The employee feeling response is: {}'.format(feeling_response))

    # Connect to database to record response
    query = """INSERT INTO employee_submission (submission_value, submission_date)
        VALUES ({}, current_timestamp)""".format(feeling_response)

    cur.execute(query)

    # cur.execute('select * from employee_submission;')
    # x = cur.fetchall()
    # pp.pprint(x)

    # Commit changes
    conn.commit()

    # Close db connection
    cur.close()
    conn.close()

    # Close app
    ForgeantApp().stop()

# Check if file exists that already has demographic info
def check_for_initial_setup():
    return os.path.exists('data/demographic_info.csv')

# Prompt for employee information on first startup
def run_initial_setup():
    print('*' * 80)

    # Create csv file
    with open('data/demographic_info.csv', 'w', newline='') as csvfile:
        fieldnames = [
            '',
            'Name',
            'Street',
            'City',
            'Country',
            'Zipcode',
            'Category',
            'Description',]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Write each household to individual rows
        writer.writerow({
            'Name': 'hi',
            })

###########################
### ForgeantApp Widgets ###
###########################

# 5 smile widget images
class SmileWidget1(Image):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            record_feeling_submission_to_db(1)

class SmileWidget2(Image):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            record_feeling_submission_to_db(2)

class SmileWidget3(Image):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            record_feeling_submission_to_db(3)

class SmileWidget4(Image):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            record_feeling_submission_to_db(4)

class SmileWidget5(Image):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            record_feeling_submission_to_db(5)

# Base ForgeantApp root widget
class ForgeantRootWidget(Widget):
    pass

# Forgeant App
class ForgeantApp(App):
    def build(self):
        root = ForgeantRootWidget()
        return root

########################
### SetupApp Widgets ###
########################

class SetupRootWidget(Widget):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            record_feeling_submission_to_db(5)

from kivy.uix.boxlayout import BoxLayout

class LblTxt(BoxLayout):
    from kivy.properties import ObjectProperty
    theTxt = ObjectProperty(None)

class CustomDropDown(DropDown):
    pass

dropdown = CustomDropDown()
mainbutton = Button(text='Hello', size_hint=(None, None))
mainbutton.bind(on_release=dropdown.open)
dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))

class SetupApp(App):

    def build(self):
        return


############################################
### Main method to actually run the apps ###
############################################

if __name__ == '__main__':

    # Run the normal app if the inital setup has already been completed
    if check_for_initial_setup():
        # ForgeantApp().run()
        SetupApp().run()
    else:
        SetupApp().run()
        ForgeantApp().run()







# 11 hours
