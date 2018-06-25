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


########################################################
############### Window & database setup  ###############
########################################################

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

#################################################################
###################### Methods to be called #####################
#################################################################

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

#######################################################
################# ForgeantApp Widgets #################
#######################################################

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

############################################################
##################### SetupApp Widgets #####################
############################################################

dropdown_button_list = {}
category_list = ['Department','Team','Tenure', 'Generation','Manager','Location',]
dropdown_options_list = [
    ['Production','Research and Development','Purchasing','Marketing','Sales','Human Resources','Accounting and Finance','Admin',],
    ['Team 1','Research and Development','Purchasing','Marketing','Sales','Human Resources','Accounting and Finance','Admin',],
    ['2-3 years','Research and Development','Purchasing','Marketing','Sales','Human Resources','Accounting and Finance','Admin',],
    ['50+','Research and Development','Purchasing','Marketing','Sales','Human Resources','Accounting and Finance','Admin',],
    ['Tom','Research and Development','Purchasing','Marketing','Sales','Human Resources','Accounting and Finance','Admin',],
    ['Chicago','Research and Development','Purchasing','Marketing','Sales','Human Resources','Accounting and Finance','Admin',],
    ]

def update_dropdown(btn, text):
    btn.text = text

class RootLayout(BoxLayout):
    pass

class HeaderLayout(Label):
    pass

class SaveButton(Button):

    # Submit response if valid
    def on_press(self):
        all_responses_valid = True
        for key, dropdown_button in dropdown_button_list.items():

            # Change text if a response is not selected
            if dropdown_button.text == 'Select an option':
                dropdown_button.markup = True
                dropdown_button.text = '[color=f45342][b]Select an option[/b][/color]'
                all_responses_valid = False
                print(dropdown_button.id)


        # Submit signup response if valid
        if all_responses_valid:
            print('you did it!')

class FormDropDown(DropDown):
    pass

class FormButton(Button):
    pass

class DropDownOptionButton(Button):

    # When an option is selected, make the option shown on the main dropdown button
    def on_press(self):
        dropdown_list[self.id].bind(
            on_select=lambda instance, x: setattr(dropdown_button_list[self.id], 'text', x)
            )
        self.bind(on_release=lambda self: dropdown_list[self.id].select(self.text))

dropdown_list = {}

for category_index, category in enumerate(category_list):


    # Create dropdown and associated main button
    dropdown = FormDropDown()
    dropdown_button = FormButton(
        text='Select an option',
        id='dropdown_button_{}'.format(category_index),
        )

    # Add to dictionaries
    dropdown_button_list[category] = dropdown_button
    dropdown_list[category] = dropdown

    # Add dropdown option buttons to dropdown
    for option_index, option in enumerate(dropdown_options_list[category_index]):
        btn = DropDownOptionButton(
            text='{}'.format(option),
            id= '{}'.format(category),
            size_hint_y=None,
            height=44,
            background_normal = '',
            background_color = (.1, .3, .8, 1),
           )

        dropdown.add_widget(btn)

    # Have button open dropdown
    dropdown_button_list[category].bind(on_release=dropdown_list[category].open)


class SetupApp(App, BoxLayout):

    # Build the layout together
    def build(self):

        # Window size
        Window.size = (800, 600)

        # Layouts
        root = RootLayout()
        label_layout = BoxLayout(orientation='vertical',)
        dropdown_layout = BoxLayout(orientation='vertical',)
        buffer_layout1 = BoxLayout(orientation='vertical')
        buffer_layout2 = BoxLayout(orientation='vertical')
        root.add_widget(buffer_layout1)
        root.add_widget(label_layout)
        root.add_widget(dropdown_layout)
        root.add_widget(buffer_layout2)

        # Labels on layout
        label_layout.add_widget(Label())
        for index, category_item in enumerate(category_list):
            label_layout.add_widget(
                Label(
                    text='[color=194CCC][b]{}[/b][/color]'.format(category_item),
                    markup = True,
                    )
                )
            label_layout.add_widget(Label())
        label_layout.add_widget(Label())
        label_layout.add_widget(Label())
        label_layout.add_widget(Label())

        # Dropdowns on layout
        dropdown_layout.add_widget(Label())
        for key, dropdown_item in dropdown_button_list.items():
            dropdown_layout.add_widget(dropdown_item)
            dropdown_layout.add_widget(Label())
        dropdown_layout.add_widget(Label())

        # Save button
        save_button = SaveButton(
                        text='Submit',
                        id='submission',
                        background_normal = '',
                        background_color = (.1, .3, .8, 1),
                        )
        dropdown_layout.add_widget(save_button)
        dropdown_layout.add_widget(Label())

        return root

####################################################
####### Main method to actually run the apps #######
####################################################

if __name__ == '__main__':

    # Run the normal app if the inital setup has already been completed
    if check_for_initial_setup():
        # ForgeantApp().run()
        SetupApp().run()
    else:
        SetupApp().run()
        ForgeantApp().run()







# 16.2 hours



# class LblTxt(BoxLayout):
#     theTxt = ObjectProperty(None)
#
# class MyLayout(BoxLayout):
#     pass
