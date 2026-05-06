from keyboard import on_release
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
import random

class battle_botApp(App):
    def build(self):
        self.difficulty = 4

        self.user_ships_count = 0
        self.killed_bots_ships = 0
        self.killed_users_ships = 0
        self.turns_count = 0

        self.sabattle_main_layout = FloatLayout()
        self.bot_layout = GridLayout(cols=5,
                                     rows=5,
                                     size_hint=(.4, .4),
                                     pos_hint={'x': .05, 'y': .01})
        self.user_layout = GridLayout(cols=5,
                                      rows=5,
                                      size_hint=(.4, .4),
                                      pos_hint={'x': .55, 'y': .01})
        self.place_ships_text = Label(text = 'place your ships (1x1 X5)',
                                      color = (1, 1, 1, 1),
                                      font_size=30,
                                      size_hint=(1, .1),
                                      pos_hint={'x': 0, 'y': .7})
        self.confirm_button = Button(text = 'confirm >',
                                     font_size=30,
                                     color=(1, 1, 1, 1),
                                     size_hint=(.3, .1),
                                     pos_hint={'x': .05, 'y': .01},
                                     on_release = self.confirm_user_ships)
        self.you_text = Label(text = 'you',
                                      color = (1, 1, 1, 1),
                                      font_size=30,
                                      size_hint=(.1, .1),
                                      pos_hint={'x': .7, 'y': .5})
        self.opponent_text = Label(text = 'opponent',
                                      color = (1, 1, 1, 1),
                                      font_size=30,
                                      size_hint=(.1, .1),
                                      pos_hint={'x': .2, 'y': .5})
        self.you_win_text = Label(text = 'YOU WIN !!!',
                                      color = (0, 1, 0, 1),
                                      font_size=50,
                                      bold = 1,
                                      size_hint=(1, .1),
                                      pos_hint={'x': 0, 'y': .7})
        self.you_lose_text = Label(text = 'YOU LOSE !!!',
                                      color = (1, 0, 0, 1),
                                      font_size=50,
                                      bold = 1,
                                      size_hint=(1, .1),
                                      pos_hint={'x': 0, 'y': .7})
        self.list_with_bot_buttons = []
        self.list_with_user_buttons = []
        for x in range(0, 25):
            bot_button = Button(font_size=30,
                                 color=(0, 0, 0, 1),
                                 on_release = self.click_on_bots_button)
            user_button = Button(font_size=30,
                                 color=(1, 1, 1, 1),
                                 on_release = self.place_ship_user)
            self.bot_layout.add_widget(bot_button)
            self.user_layout.add_widget(user_button)
            self.list_with_bot_buttons.append(bot_button)
            self.list_with_user_buttons.append(user_button)
        self.sabattle_main_layout.add_widget(self.place_ships_text)
        self.sabattle_main_layout.add_widget(self.user_layout)
        return self.sabattle_main_layout

    def place_ship_user(self, instance):
        if instance.text != 'S':
            self.user_ships_count += 1
            if self.user_ships_count <= 5:
                instance.text = 'S'
            if self.user_ships_count == 5:
                try:
                    self.sabattle_main_layout.add_widget(self.confirm_button)
                except:
                    pass
    def confirm_user_ships(self, instance):
        self.sabattle_main_layout.remove_widget(self.place_ships_text)
        self.sabattle_main_layout.remove_widget(self.confirm_button)
        self.sabattle_main_layout.add_widget(self.bot_layout)
        self.sabattle_main_layout.add_widget(self.you_text)
        self.sabattle_main_layout.add_widget(self.opponent_text)
    def click_on_bots_button(self, instance):
        if instance.text != 'X':
            if random.randint(0, self.difficulty) == 1:
                instance.background_color = (1, 0, 0, 1)
                instance.text = 'X'
                self.killed_bots_ships += 1
            else:
                instance.text = 'X'
        if self.killed_bots_ships == 5:
            self.end_game('user_win')
        for x in self.list_with_bot_buttons:
            x.disabled = 1
        Clock.schedule_once(self.bots_turn, 2)
    def bots_turn(self, instance):
        self.turns_count += 1
        for x in self.list_with_bot_buttons:
            x.disabled = 0
        self.button_to_press = random.choice(self.list_with_user_buttons)
        if self.button_to_press.text == 'S':
            self.button_to_press.color = (0, 0, 0, 1)
            self.button_to_press.text = 'X'
            self.button_to_press.background_color = (1, 0, 0, 1)
            self.killed_users_ships += 1
        elif self.button_to_press.text == 'X':
            Clock.schedule_once(self.bots_turn, 0)
        else:
            self.button_to_press.color = (0, 0, 0, 1)
            self.button_to_press.text = 'X'
        if self.killed_users_ships == 5:
            self.end_game('bot_win')
        if self.turns_count == 25:
            if self.killed_bots_ships >= self.killed_users_ships:
                self.sabattle_main_layout.clear_widgets()
                self.sabattle_main_layout.add_widget(self.you_win_text)
            else:
                self.sabattle_main_layout.clear_widgets()
                self.sabattle_main_layout.add_widget(self.you_lose_text)
    def end_game(self, data):
        self.sabattle_main_layout.clear_widgets()
        if data == 'user_win':
            self.sabattle_main_layout.add_widget(self.you_win_text)
        elif data == 'bot_win':
            self.sabattle_main_layout.add_widget(self.you_lose_text)
        else:
            if self.killed_bots_ships >= self.killed_users_ships:
                self.end_game('user_win')
            else:
                self.end_game('bot_win')

battle_botApp().run()




