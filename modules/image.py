from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

class MyImage(ButtonBehavior, Image):
	def __init__(self, **kwargs):
		super(MyImage, self).__init__(**kwargs)

	def on_press(self):
		return True	

	def on_release(self):
		return True
