from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Color, Ellipse
from kivy.core.window import Window
from kivy.config import Config
from kivy.core.window import Window
import psycopg2, pprint

##################### Initial Setup #######################
# Indicate position of app window
Window.left = 500
Window.top = 400

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

##################### Function to record response and close app #######################
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

##################### Smile and Root Widgets #######################
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

if 31>5:
    # Base root widget
    class RootWidget(Widget):
        remove_widget(SmileWidget1) 

class ForgeantApp(App):

    def build(self):
        return RootWidget()

##################### Run the app #######################
if __name__ == '__main__':
    ForgeantApp().run()
