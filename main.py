from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore

store = JsonStore('config.json')

class TiendaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text='KAIROS SHOP', font_size=30, bold=True, size_hint_y=None, height=60))
        layout.add_widget(Label(text='Bomba Autocebante 1/2 HP Saco Naranja', font_size=18, bold=True, size_hint_y=None, height=40))
        layout.add_widget(Label(text='Potencia: 1/2 HP (375W)\nCaudal: 40L/min\nAltura max: 40m\nSuccion: 8m\nEntrada: 1 pulgada\nVoltaje: 110V / 220V\nPeso: 4.2kg', font_size=14, size_hint_y=None, height=150))
        
        btn_config = Button(text='⚙️ Configuracion Correo', size_hint_y=None, height=50)
        btn_config.bind(on_press=lambda x: setattr(self.manager, 'current', 'config'))
        layout.add_widget(btn_config)
        
        btn_pedir = Button(text='PEDIR AHORA', size_hint_y=None, height=60, background_color=(1,0.5,0,1))
        btn_pedir.bind(on_press=self.pedir)
        layout.add_widget(btn_pedir)
        
        self.msg = Label(text='')
        layout.add_widget(self.msg)
        self.add_widget(layout)

    def pedir(self, instance):
        if store.exists('user'):
            email = store.get('user')['email']
        else:
            email = 'kairos.shop@gmail.com'
        self.msg.text = f'Pedido enviado a: {email}'

class ConfigScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text='CAMBIAR CORREO', font_size=24, bold=True, size_hint_y=None, height=50))
        
        if store.exists('user'):
            correo_actual = store.get('user')['email']
        else:
            correo_actual = 'kairos.shop@gmail.com'
            
        self.email_input = TextInput(text=correo_actual, multiline=False, font_size=18, size_hint_y=None, height=50)
        layout.add_widget(self.email_input)
        
        btn = Button(text='GUARDAR NUEVO CORREO', size_hint_y=None, height=60, background_color=(0.13,0.27,0.53,1))
        btn.bind(on_press=self.guardar)
        layout.add_widget(btn)
        
        self.mensaje = Label(text='')
        layout.add_widget(self.mensaje)
        
        btn_volver = Button(text='Volver a la tienda', size_hint_y=None, height=50)
        btn_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'tienda'))
        layout.add_widget(btn_volver)
        self.add_widget(layout)

    def guardar(self, instance):
        nuevo = self.email_input.text.strip()
        if '@' in nuevo:
            store.put('user', email=nuevo)
            self.mensaje.text = f'Guardado: {nuevo}'
        else:
            self.mensaje.text = 'Correo no valido'

class KairosApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(TiendaScreen(name='tienda'))
        sm.add_widget(ConfigScreen(name='config'))
        return sm

KairosApp().run()

