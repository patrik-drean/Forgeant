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
from uuid import getnode as get_mac
import datetime


########################################################
################## General Variables  ##################
########################################################
db_name = 'incasokh'
db_password = 'tmWwE8HPOYjJmAOymB16_vtNO2GILb1i'

# Test data TODO
category_list = ['Department','Team','Tenure', 'Age','Manager','Location',]
dropdown_options_list = [
    ['Production','Research and Development','Purchasing','Marketing','Sales','Human Resources','Accounting and Finance','Admin', 'Other'],
    ['Team 1','Team 2', 'Team 3','Other'],
    ['<1 year','2-3 years','4-5 years','5-10 years','10-20 years','20+ years','Other'],
    ['<18', '19-24', '25-34', '35-44', '45-54', '55+', 'Other'],
    ['Tommy','Alexander','Joey', 'Other'],
    ['Chicago','Boston','Provo', 'Other'],
    ]
company_id = '1'

today_date = datetime.datetime.now().today().strftime('%Y-%m-%d')

pp = pprint.PrettyPrinter(indent=4)

########################################################
#################### Window setup  #####################
########################################################

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

    # Grab employee id to record
    with open('data/demographic_info.csv', newline='') as csvfile:
        employee_id = [row for row in csv.reader(csvfile)][1][0]

    # catch exception if too many connections
    try:
        # Connect to database
        conn = psycopg2.connect(
            database=db_name,
            user=db_name,
            password=db_password,
            host='elmer.db.elephantsql.com',
            port='5432')

        # Open cursor to interact with database
        cur = conn.cursor()

        # If employee has not been saved to db, update it
        if employee_id == '-1':

            # Connect to database to get next employee id
            query = """
                        select (max(id) + 1)
                        from employee
                    """

            cur.execute(query)

            employee_id = cur.fetchone()[0]

            # Grab cached employee row by row
            with open('data/demographic_info.csv', newline='') as csvfile:
                for row in csv.reader(csvfile):
                    company_id = row[1]
                    mac_address = row[2]
                    department = row[3]
                    team = row[4]
                    tenure = row[5]
                    age = row[6]
                    manager = row[7]
                    location = row[8]
                    create_date = row[9]
                    modified_date = row[10]

            # Record employee in db
            query = """
                        insert into employee
                        values({},'{}','{}','{}','{}','{}','{}', '{}','{}', '{}', '{}')
                    """.format(
                            employee_id,
                            company_id,
                            mac_address,
                            department,
                            team,
                            tenure,
                            age,
                            manager,
                            location,
                            create_date,
                            today_date,
                            )

            cur.execute(query)

            # Commit changes
            conn.commit()

            # Update csv file
            with open('data/demographic_info.csv', 'w', newline='') as csvfile:
                fieldnames = [
                    'id',
                    'company_id',
                    'mac_address',
                    'department_name',
                    'team_name',
                    'tenure_name',
                    'age_name',
                    'manager_name',
                    'location_name',
                    'create_date',
                    'last_modified_date',
                    ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                # Write employee to row
                writer.writerow({
                    'id': employee_id,
                    'company_id': company_id,
                    'mac_address': mac_address,
                    'department_name': department,
                    'team_name': team,
                    'tenure_name': tenure,
                    'age_name': age,
                    'manager_name': manager,
                    'location_name': location,
                    'create_date': create_date,
                    'last_modified_date': today_date,
                    })

        # Upload any cached_submissions if they exist
        if os.path.exists('data/cached_submissions.csv'):

            # Grab cached submission row by row and update in db
            with open('data/cached_submissions.csv', newline='') as csvfile:
                for row in csv.reader(csvfile):
                    cached_feeling_response = row[0]
                    cached_date = row[1]
                    cached_employee_id = row[2]

                    # change employee id if it wasn't set prior
                    if cached_employee_id == '-1':
                        cached_employee_id = employee_id

                    # Connect to database to record response
                    query = """
                                INSERT INTO employee_submission (submission_value, submission_date, employee_id)
                                VALUES ({}, '{}',  '{}')
                            """.format(cached_feeling_response, cached_date, cached_employee_id)

                    cur.execute(query)

                    # Commit changes
                    conn.commit()

            # Delete csv file
            os.remove('data/cached_submissions.csv')

        # Developer printout
        print('The employee feeling response is: {}'.format(feeling_response))

        # Connect to database to record response
        query = """
                    INSERT INTO employee_submission (submission_value, submission_date, employee_id)
                    VALUES ({}, current_timestamp,  '{}')
                """.format(feeling_response, employee_id)

        cur.execute(query)

        # Commit changes
        conn.commit()

        # Close db connection
        cur.close()
        conn.close()

        # Close app
        ForgeantApp().stop()

    # If too many connections write to csv file to be uploaded later
    except psycopg2.OperationalError as e:

        # Create csv file
        new_row = [feeling_response, datetime.datetime.now().today(), employee_id]
        with open('data/cached_submissions.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write cached response to csv file
            writer.writerow(new_row)

        print('Database has too many connections. Submsission will not be recorded until later.')

        # Close app
        ForgeantApp().stop()


# Check if file exists that already has demographic info
def check_for_initial_setup():
    return os.path.exists('data/demographic_info.csv')

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

dropdown_list = {}
dropdown_button_list = {}

class RootLayout(BoxLayout):
    pass

class SaveButton(Button):

    # Submit response if valid
    def on_press(self):
        all_responses_valid = True

        for key, dropdown_button in dropdown_button_list.items():

            # Change text color if a response is not selected
            if dropdown_button.text == 'Select an option' or dropdown_button.text == '[color=f45342][b]Select an option[/b][/color]':
                dropdown_button.markup = True
                dropdown_button.text = '[color=f45342][b]Select an option[/b][/color]'
                all_responses_valid = False

            print(dropdown_button.text)

        # Submit signup responses and create csv file if valid
        if all_responses_valid:

            # grab mac address
            mac_address = get_mac()

            ###################
            # Grab next employee id from db
            ###################

            try:
                # Connect to database
                conn = psycopg2.connect(
                    database=db_name,
                    user=db_name,
                    password=db_password,
                    host='elmer.db.elephantsql.com',
                    port='5432')

                # Open cursor to interact with database
                cur = conn.cursor()

                # Connect to database to get next employee id
                query = """
                            select (max(id) + 1)
                            from employee
                        """

                cur.execute(query)

                employee_id = cur.fetchone()[0]

                # Record employee in db
                query = """
                            insert into employee
                            values({},'{}','{}','{}','{}','{}','{}', '{}','{}', '{}', '{}')
                        """.format(
                                employee_id,
                                company_id,
                                mac_address,
                                dropdown_button_list['Department'].text,
                                dropdown_button_list['Team'].text,
                                dropdown_button_list['Tenure'].text,
                                dropdown_button_list['Age'].text,
                                dropdown_button_list['Manager'].text,
                                dropdown_button_list['Location'].text,
                                today_date,
                                today_date,
                                )

                cur.execute(query)

                conn.commit()

                # Close db connection
                cur.close()
                conn.close()

            # Assign an id as a flag if db error
            except psycopg2.OperationalError as e:
                employee_id = -1

            # Create csv file
            with open('data/demographic_info.csv', 'w', newline='') as csvfile:
                fieldnames = [
                    'id',
                    'company_id',
                    'mac_address',
                    'department_name',
                    'team_name',
                    'tenure_name',
                    'age_name',
                    'manager_name',
                    'location_name',
                    'create_date',
                    'last_modified_date',
                    ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                # Write each household to individual rows
                writer.writerow({
                    'id': employee_id,
                    'company_id': company_id,
                    'mac_address': mac_address,
                    'department_name': dropdown_button_list['Department'].text,
                    'team_name': dropdown_button_list['Team'].text,
                    'tenure_name': dropdown_button_list['Tenure'].text,
                    'age_name': dropdown_button_list['Age'].text,
                    'manager_name': dropdown_button_list['Manager'].text,
                    'location_name': dropdown_button_list['Location'].text,
                    'create_date': today_date,
                    'last_modified_date': today_date,
                    })

            SetupApp().stop()

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
        self.bind(
            on_release=lambda self: dropdown_list[self.id].select(self.text)
            )

# Create a dropdown for each category
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
                        background_color = (.2, .2, .2, 1),
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
        ForgeantApp().run()
    else:
        SetupApp().run()
        ForgeantApp().run()





# 31 hours
