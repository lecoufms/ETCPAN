from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior

class MyLabel(Label, ButtonBehavior):
	def __init__(self, **kwargs):
		super(MyLabel, self).__init__(**kwargs)

	def on_press(self):
		print('aeee')
		return True

	def on_release(self):
		print('aeee')
		return True