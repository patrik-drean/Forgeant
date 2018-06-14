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
from kivy.base import runTouchApp
from kivy.properties import ObjectProperty


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

def initial_setup_submit():
    print('hi')

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



######################################################################

from kivy.uix.spinner import Spinner

class CustomSpinner(Spinner):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            initial_setup_submit()



class CustomDropDown(DropDown):
    pass


dropdown = CustomDropDown()
mainbutton = Button(text='Hello', size_hint=(None, None))
mainbutton.bind(on_release=dropdown.open)
dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))


# create a dropdown with 10 buttons
dropdown = DropDown()
for index in range(10):
    # When adding widgets, we need to specify the height manually
    # (disabling the size_hint_y) so the dropdown can calculate
    # the area it needs.

    btn = Button(text='Value %d' % index, size_hint_y=None, height=44)

    # for each button, attach a callback that will call the select() method
    # on the dropdown. We'll pass the text of the button as the data of the
    # selection.
    btn.bind(on_release=lambda btn: dropdown.select(btn.text))

    # then add the button inside the dropdown
    dropdown.add_widget(btn)

# create a big main button
mainbutton = Button(text='Hello', size_hint=(None, None))

# show the dropdown menu when the main button is released
# note: all the bind() calls pass the instance of the caller (here, the
# mainbutton instance) as the first argument of the callback (here,
# dropdown.open.).
mainbutton.bind(on_release=dropdown.open)

# one last thing, listen for the selection in the dropdown list and
# assign the data to the button text.
dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))

# runTouchApp(mainbutton)

########################
### SetupApp Widgets ###
########################

# spinner = Spinner(
#     # default value shown
#     text='Home',
#     # available values
#     values=('Home', 'Work', 'Other', 'Custom'),
#     # just for positioning in our example
#     size_hint=(None, None),
#     size=(100, 44),
#     pos_hint={'center_x': .5, 'center_y': .5})
#
# def show_selected_value(spinner, text):
#     print('The spinner', spinner, 'have text', text)
#
# spinner.bind(text=show_selected_value)
#
# runTouchApp(spinner)



class LblTxt(BoxLayout):
    # self.ids.my_spinner.values = ['A', 'B']
    theTxt = ObjectProperty(None)

class MyLayout(BoxLayout):
    pass

class SetupApp(App):

    def build(self):

        root = MyLayout()
        root.add_widget(mainbutton)
        return root

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







# 12.8 hours
