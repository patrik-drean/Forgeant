from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Color, Ellipse
from kivy.core.window import Window

wimg = Image(source='images/5_smile.png')

# Turn background clear
Window.clearcolor = (1, 1, 1, 1)

# 5 smile widget images
class SmileWidget1(Image):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print('1')

class SmileWidget2(Image):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print('2')

class SmileWidget3(Image):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print('3')

class SmileWidget4(Image):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print('4')

class SmileWidget5(Image):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print('5')






class RootWidget(Widget):
    pass


class ForgeantApp(App):

    def build(self):
        return RootWidget()



if __name__ == '__main__':
    ForgeantApp().run()
