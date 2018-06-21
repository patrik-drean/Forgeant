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
from kivy.uix.label import Label


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

########################
### SetupApp Widgets ###
########################


class RootLayout(BoxLayout):
    pass

class HeaderLayout(Label):
    pass

class SaveButton(Button):
    def on_press(self):
        print(self.id)

class FormDropDown(DropDown):
    pass

class FormButton(Button):
    pass

class DropDownOptionButton(Button):
    pass
    # def on_press(self):
    #     print(self.id)

dropdown_list = []
category_list = ['Department','Team','Tenure','Generation','Manager','Location', 'Test', 'Test']
dropdown_options_list = [
    ['Production','Research and Development','Purchasing','Marketing','Sales','Human Resources','Accounting and Finance','Admin',],
    ['Team 1','Research and Development','Purchasing','Marketing','Sales','Human Resources','Accounting and Finance','Admin',],
    ['2-3 years','Research and Development','Purchasing','Marketing','Sales','Human Resources','Accounting and Finance','Admin',],
    ['50+','Research and Development','Purchasing','Marketing','Sales','Human Resources','Accounting and Finance','Admin',],
    ['Tom','Research and Development','Purchasing','Marketing','Sales','Human Resources','Accounting and Finance','Admin',],
    ['Chicago','Research and Development','Purchasing','Marketing','Sales','Human Resources','Accounting and Finance','Admin',],
    ['Chicago','Research and Development','Purchasing','Marketing','Sales','Human Resources','Accounting and Finance','Admin',],
    ['Chicago','Research and Development','Purchasing','Marketing','Sales','Human Resources','Accounting and Finance','Admin',],
    ]


for category_index, category in enumerate(category_list):
    dropdown = FormDropDown()
    dropdown_button = FormButton(text='Select an option')
    dropdown_list.append(dropdown_button)
    dropdown.bind(on_select=lambda instance, x: setattr(dropdown_list[0], 'text', x))

    for option_index, option in enumerate(dropdown_options_list[category_index]):
        btn = DropDownOptionButton(
            text='{}'.format(option),
            id= '{} {}'.format(category, option_index),
            size_hint_y=None,
            height=44)

        btn.bind(on_release=lambda btn: dropdown.select(btn.text))
        # btn.bind(on_press=print(btn.text))
        dropdown.add_widget(btn)


    # show the dropdown menu when the main button is released
    # note: all the bind() calls pass the instance of the caller (here, the
    # dropdown_button instance) as the first argument of the callback (here,
    # dropdown.open.).
    dropdown_button.bind(on_release=dropdown.open)
    dropdown_button.bind(on_release=lambda x: print(dropdown_button.text))

    # one last thing, listen for the selection in the dropdown list and
    # assign the data to the button text






# class LblTxt(BoxLayout):
#     theTxt = ObjectProperty(None)
#
# class MyLayout(BoxLayout):
#     pass

class SetupApp(App, BoxLayout):

    def build(self):
        Window.size = (1000, 600)
        root = RootLayout()
        layout = BoxLayout(orientation='vertical')
        dropdown_layout = BoxLayout(orientation='vertical')
        root.add_widget(layout)
        root.add_widget(dropdown_layout)
        
        dropdown_layout.add_widget(Label())

        for index, dropdown_item in enumerate(dropdown_list):
            # Pass if 3rd option. Bug TODO
            if index == 3:
                pass
            else:
                dropdown_layout.add_widget(dropdown_item)
                dropdown_layout.add_widget(Label())

        dropdown_layout.add_widget(Label())
        dropdown_layout.add_widget(SaveButton(text='Hello', id='2'))
        print(dropdown_button.id)
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







# 14.3 hours
