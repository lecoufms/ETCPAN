#-*- coding: utf-8 -*-
import kivy
from modules import rest,label, cpf
from kivy.app import App
from kivy.clock import Clock
from functools import partial
import os,time, threading, io
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.progressbar import ProgressBar
from kivy.storage.jsonstore import JsonStore
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition

Builder.load_file("main.kv")

"""
if platform == 'android': 
    from androidbrowser import open_url
else:
    from mockbrowser import open_url
"""

class CustomPopup(Popup):
    def __init__(self, d, **kwargs):
        super(CustomPopup, self).__init__(**kwargs)
        self.size_hint = (.9, .6)
        self.auto_dismiss = True
        self.title = d['evento']
        layout = BoxLayout(orientation='vertical',spacing=5)
        try:
            if 'descricao' in d:
                    layout.add_widget(Label(text=str('Descrição'+ ': ' + str(d['descricao'])), text_size = (Window.width - 100, None)))
            if 'Local' in d:
                layout.add_widget(Label(text=str('Local' + ': ' + str(d['Local'])), text_size = (Window.width - 100, None)))      
            layout.add_widget(Label(text=str('Horário' + ': ' + str(d['horario'])), text_size = (Window.width - 100, None)))
        except:
            pass
        layout.add_widget(Button(text='Voltar', on_press=self.dismiss))
        self.add_widget(layout)

class NotifyPopup(Popup):
    def __init__(self, d, **kwargs):
        super(NotifyPopup, self).__init__(**kwargs)
        self.size_hint = (.9, .6)
        self.auto_dismiss = True
        self.title = 'Notificações'
        layout = GridLayout(cols=1, size_hint=(1,None))
        layout.bind(minimum_height=layout.setter('height'))
        for info in d:
            layout.add_widget(Label(text=str(info['tipo'])))
            layout.add_widget(Label(text=str('descrição'+': '+info['descricao'])))
            if info['link'] != '':
                l = Label(text=str('link'+': '+'[b][ref=touch]'+info['link']+'[/ref][/b]'), markup=True, color=(1,1,1,1))
                l.bind(on_ref_press = self.callback)
                layout.add_widget(l)
            layout.add_widget(Label(text='---------------------------------------------'))
        layout.add_widget(Button(text='Voltar', on_press=self.dismiss))
        root = ScrollView(size_hint=(1, None), size=(self.width, self.height))
        root.add_widget(layout)
        self.content=root

    def callback(self, *args):
        return True

"""class PresencePopup(Popup):
    text = StringProperty()
    r = rest.REST()
    def __init__(self,**kwargs):
        super(PresencePopup, self).__init__(**kwargs)
        self.size_hint = (.6, .3)
        self.auto_dismiss = True
        self.title = 'Insira o código do curso.'
        mycontent = BoxLayout(orientation='vertical')
        t = TextInput(id='tinput',multiline=False)
        t.bind(text=self.callback, on_enter=self.gettext)
        mycontent.add_widget(t)
        btn = Button(text='Enviar', on_press=self.gettext)
        mycontent.add_widget(btn)
        self.content = mycontent

    def callback(instance, value, *args):
        instance.text = value.text

    def gettext(self,*args):
        self.validate(self.text,*args)

    def validate(self,t,*args):
        self.t = t
        if t == '' or None:
            self.title = 'Insira o código (se não tiver, solicite ao professor da Oficina)'
            return False
        else:
            self.reg_on_log(self.text)
            return True

    def reg_on_log(self,t,*args):
        if rest.is_connected():
            answer = self.r.send_request(store.get('cpf')['cpf'],t)
        else:
            answer = {'msg': 'Não há conexão! ', 'result':'Conecte-se para registrar presença'}
            self.content = Button(text=str(answer['msg']+answer['result']), on_press=partial(self.dismiss, force=True))

"""
        
class ProgramScreen(Screen):
    """
Classe 
    """
    def __init__(self, **kwargs):
        super(ProgramScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.__rest = rest.REST()
        self.__programacao = []
        self.build()

    def show_popup(self, _dict, *args):
        pop = CustomPopup(_dict)
        pop.open()
        return True

    def build(self):
        layout = GridLayout(id='layout', cols=1,spacing=16 , size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        btn = Label(text='')
        layout.add_widget(btn)
        with io.open('data/programacao.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if line != '\n':
                    x = eval(line)
                    string = ''
                    if 'dia' in x:
                        btn = Label(text=str('Dia:' + str(x['dia']) + '\n'))
                        layout.add_widget(btn)
                    elif 'periodo' in x:
                        if 'horario' in x:
                            string = str('        ' + x['periodo'] + '\n' + x['horario'] + '\n')
                        else:
                            string = str(x['periodo'] + '\n')
                        btn = Label(text=string)
                        layout.add_widget(btn)
                    else:
                        if 'evento' in x:
                            string = str(x['evento'])
                            btn = Button(text=string, size_hint_y=None, height=40, background_color= (1,1,1,.4))
                            btn.bind(on_press=partial(self.show_popup, x))
                            btn.halign = 'center'
                            btn.text_size = (Window.height - 100, None)
                            layout.add_widget(btn)
                            btn = Label(text='\n\n')
                            layout.add_widget(btn)
        btn = Label(text='')
        layout.add_widget(btn)
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        root.add_widget(layout)
        self.add_widget(root)



class ProgramScreensw(Screen):

    def __init__(self, **kwargs):
        super(ProgramScreensw, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.__rest = rest.REST()
        self.__programacao = []
        self.build()
    
    def show_popup(self, _dict, *args):
        pop = CustomPopup(_dict)
        pop.open()
        return True

    def build(self):
        layout = GridLayout(id='layout', cols=1,spacing=20 , size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        layout.add_widget(Label(text=''))
        layout.add_widget(Label(text=''))
        layout.add_widget(Label(text=''))
        layout.add_widget(Label(text=''))
        layout.add_widget(Label(text=''))
        
        with io.open('data/programsw.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if line != '\n':
                    x = eval(line)
                    string = ''
                    if 'dia' in x:
                        btn = Label(text=str('[b][color=#000000]' + 'Dia:' + str(x['dia']) + '[/color][/b]' + '\n'), markup=True)
                        layout.add_widget(btn)
                    elif 'periodo' in x:
                        if 'horario' in x:
                            string = str('[b][color=#000000]' + '        ' + x['periodo'] + '\n' + x['horario'] + '[/color][/b]' + '\n')
                        else:
                            string = str('[b][color=#000000]' + x['periodo'] + '[/color][/b]' + '\n' )
                        btn = Label(text=string, markup=True)
                        layout.add_widget(btn)
                    else:
                        if 'evento' in x:
                            string = str(x['evento'])
                            btn = Button(text=str("[color=333333]"+string+"[/color]"), size_hint_y=None, height=40, background_color= (0,0,0,.1),markup=True)
                            btn.bind(on_press=partial(self.show_popup, x))
                            btn.halign = 'center'
                            btn.text_size = (Window.height - 100, None)
                            layout.add_widget(btn)
                            btn = Label(text='\n\n')
                            layout.add_widget(btn)
        btn = Label(text='')
        layout.add_widget(btn)
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        root.add_widget(layout)
        self.add_widget(root)

class LoginPopup(Popup):
    text = StringProperty()


    def __init__(self,**kwargs):
        super(LoginPopup, self).__init__(**kwargs)
        self.size_hint = (.9, .4)
        self.auto_dismiss = False
        self.title = 'Insira seu CPF:'
        mycontent = BoxLayout(orientation='vertical')
        t = TextInput(id='tinput',multiline=False)
        t.bind(text=self.callback, on_enter=self.gettext)
        mycontent.add_widget(t)
        btn = Button(text='Submeter', on_press=self.gettext)
        mycontent.add_widget(btn)
        self.content = mycontent

    def callback(instance, value, *args):
        instance.text = value.text

    def gettext(self,*args):
        self.validate(self.text,*args)

    def on_dismiss(self,*args):
        return True

    def validate(self,t,*args):
        self.t = t
        if t == '' or None or not cpf.valido(t):
            self.title = 'Insira seu CPF (É obrigatório para continuar)'
            return False
        else:
            self.dismiss(force=True)
            try:
                t = t.replace( ".", "" )
                t = t.replace( "-", "" )
            except:
                pass
            self.text = t
            self.create_file(self.text)
            return True

    def create_file(self,t,*args):
        store.put('cpf', cpf=t)

class MainScreen(Screen):
    pop = LoginPopup()
    rest_manager = rest.REST()
    progress = ObjectProperty()
    progressPopup = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.pop = LoginPopup()
        self.progress = ProgressBar()
        self.progressPopup = Popup(title='loading', content=self.progress, background_color=(1,1,4,.9))
        self.progressPopup.bind(on_open=self.puopen)
    
    def puopen(self, *instance):
        Clock.schedule_interval(self.wait_for_it,1/25)

    def popP(self, *instance):
        self.progress.value = 1
        self.progressPopup.open()

    def wait_for_it(self,*args):
        if self.progress.value>=100:
            self.progressPopup.dismiss()
            return False
        self.progress.value+=1

    def NotifyPopup(self):
        Clock.schedule_once(self.popP, -1)
        if rest.is_connected():
            d = self.rest_manager.getRequest()
            p = NotifyPopup(d)
        else:
            p = CustomPopup({'evento': 'Não há notificações (Você está desconectado)', 'descricao': 'Conecte-se para obter informações'})
        p.open()

    def PresencePopup(self):
        p = PresencePopup()
        p.open()

class MainScreenSW(Screen):
    #pop = LoginPopup()
    rest_manager = rest.REST()
    progress = ObjectProperty()
    progressPopup = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainScreenSW, self).__init__(**kwargs)
     #   self.pop = LoginPopup()
        self.progress = ProgressBar()
        self.progressPopup = Popup(title='loading', content=self.progress, background_color=(1,1,4,.9))
        self.progressPopup.bind(on_open=self.puopen)

    """def show_popup(self,*args):
        if store.exists('cpf') and store.get('cpf')['cpf'] == '':
                self.pop.open()
        else:
            store.put('cpf', cpf='')
            self.pop.open()
"""
    def puopen(self, *instance):
        Clock.schedule_interval(self.wait_for_it,1/25)

    def popP(self, *instance):
        self.progress.value = 1
        self.progressPopup.open()

    def wait_for_it(self,*args):
        if self.progress.value>=100:
            self.progressPopup.dismiss()
            return False
        self.progress.value+=1

    def NotifyPopup(self):
        Clock.schedule_once(self.popP, -1)
        if rest.is_connected():
            d = self.rest_manager.getRequest()
            p = NotifyPopup(d)
        else:
            p = CustomPopup({'evento': 'Não há notificações (Você está desconectado)', 'descricao': 'Conecte-se para obter informações'})
        p.open()

    def PresencePopup(self):
        p = PresencePopup()
        p.open()


class ScreenManagment(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagment, self).__init__(**kwargs)

    def update(self, *args):
        for child in self.children:
            child.update()

class EtcpanApp(App):
    nextScreen = 1
    screens = ['main','programacao','startup','programacaosw']
    sm = ScreenManagment()
    sm.transition = FadeTransition()
    sm.add_widget(MainScreen(name = screens[0]))
    sm.add_widget(ProgramScreen(name = screens[1]))
    sm.add_widget(MainScreenSW(name = screens[2]))
    sm.add_widget(ProgramScreensw(name = screens[3]))
    def __init__(self, **kwargs):
        super(EtcpanApp, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.onBackBtn)
        self.lastScreen = []

    def build(self):
        Window.size = (520,740)
#        Clock.schedule_once(self.sm.get_screen('main').show_popup, 1)
        return self.sm

    def onBackBtn(self,window,key,*args):
        if key == 27:
            try:
                self.sm.current = self.lastScreen.pop()
                return True
            except:
                self.stop()
        return False

    def NextScreen(self,l):
        self.lastScreen.append(l)

    def on_pause(self):
        return True

    def on_stop(self):
        return True

if __name__ == '__main__':
    EtcpanApp().run()
    
