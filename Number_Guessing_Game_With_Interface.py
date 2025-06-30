import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
class NumberGuessingGame(BoxLayout):
    message = StringProperty("Do you want to play a game?")
    hint_text = StringProperty("")
    attempts_text = StringProperty("")
    game_active = BooleanProperty(False)
    number_to_guess = NumericProperty(0)
    attempts_left = NumericProperty(0)
    difficulty_level = StringProperty('')
    max_number = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        self.background_color = get_color_from_hex('#f0f0f0')  # Light gray background

        self.message_label = Label(text=self.message, font_size=24, color=get_color_from_hex('#333333')) # Dark gray text
        self.add_widget(self.message_label)

        self.yes_button = Button(text='YES', on_press=self.start_game_query, background_color=get_color_from_hex('#4CAF50'), color=get_color_from_hex('#ffffff')) # Green button
        self.no_button = Button(text='NO', on_press=self.exit_game, background_color=get_color_from_hex('#f44336'), color=get_color_from_hex('#ffffff')) # Red button
        self.choice_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        self.choice_layout.add_widget(self.yes_button)
        self.choice_layout.add_widget(self.no_button)
        self.add_widget(self.choice_layout)

        self.difficulty_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        self.easy_button = Button(text='EASY', on_press=lambda instance: self.set_difficulty('e'), background_color=get_color_from_hex('#2196F3'), color=get_color_from_hex('#ffffff')) # Blue button
        self.medium_button = Button(text='MEDIUM', on_press=lambda instance: self.set_difficulty('m'), background_color=get_color_from_hex('#FF9800'), color=get_color_from_hex('#ffffff')) # Orange button
        self.hard_button = Button(text='HARD', on_press=lambda instance: self.set_difficulty('h'), background_color=get_color_from_hex('#9C27B0'), color=get_color_from_hex('#ffffff')) # Purple button
        self.difficulty_layout.add_widget(self.easy_button)
        self.difficulty_layout.add_widget(self.medium_button)
        self.difficulty_layout.add_widget(self.hard_button)
        self.difficulty_layout.opacity = 0
        self.add_widget(self.difficulty_layout)

        self.hint_label = Label(text=self.hint_text, font_size=18, color=get_color_from_hex('#757575')) # Gray hint text
        self.hint_label.opacity = 0
        self.add_widget(self.hint_label)

        self.attempts_label = Label(text=self.attempts_text, font_size=16, color=get_color_from_hex('#616161')) # Darker gray attempts text
        self.attempts_label.opacity = 0
        self.add_widget(self.attempts_label)

        self.guess_input = TextInput(hint_text='Enter your guess', multiline=False, font_size=20, input_type='number')
        self.guess_input.opacity = 0
        self.add_widget(self.guess_input)

        self.guess_button = Button(text='Guess', on_press=self.check_guess, background_color=get_color_from_hex('#00897B'), color=get_color_from_hex('#ffffff')) # Teal button
        self.guess_button.opacity = 0
        self.add_widget(self.guess_button)

        self.play_again_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        self.play_again_yes_button = Button(text='YES', on_press=self.reset_game, background_color=get_color_from_hex('#4CAF50'), color=get_color_from_hex('#ffffff')) # Green button
        self.play_again_no_button = Button(text='NO', on_press=self.exit_game, background_color=get_color_from_hex('#f44336'), color=get_color_from_hex('#ffffff')) # Red button
        self.play_again_layout.add_widget(self.play_again_yes_button)
        self.play_again_layout.add_widget(self.play_again_no_button)
        self.play_again_layout.opacity = 0
        self.add_widget(self.play_again_layout)

    def start_game_query(self, instance):
        self.message = "Choose difficulty level:"
        self.message_label.text = self.message
        self.choice_layout.opacity = 0
        self.difficulty_layout.opacity = 1

    def set_difficulty(self, level):
        self.difficulty_level = level
        self.difficulty_layout.opacity = 0
        self.game_active = True
        self.guess_input.opacity = 1
        self.guess_button.opacity = 1
        self.hint_label.opacity = 1
        self.attempts_label.opacity = 1
        self.play_again_layout.opacity = 0
        self.guess_input.text = ''
        self.hint_text = ''

        if self.difficulty_level == 'h':
            self.max_number = 1000
            self.attempts_left = 5
            self.attempts_text = f'You have {self.attempts_left} attempts'
        elif self.difficulty_level == 'm':
            self.max_number = 100
            self.attempts_left = 10
            self.attempts_text = f'You have {self.attempts_left} attempts'
        elif self.difficulty_level == 'e':
            self.max_number = 10
            self.attempts_left = float('inf') # Unlimited attempts
            self.attempts_text = 'You have unlimited attempts'

        self.number_to_guess = random.randint(1, self.max_number)
        self.message = f'Number lies between 1 and {self.max_number}'
        self.message_label.text = self.message
        self.attempts_label.text = self.attempts_text

    def check_guess(self, instance):
        if not self.game_active:
            return

        try:
            guess = int(self.guess_input.text)
            self.guess_input.text = '' # Clear the input after guessing

            if guess == self.number_to_guess:
                self.message = "You guessed the number correctly! Do you want to play again?"
                self.message_label.text = self.message
                self.game_active = False
                self.guess_input.opacity = 0
                self.guess_button.opacity = 0
                self.hint_label.opacity = 0
                self.attempts_label.opacity = 0
                self.play_again_layout.opacity = 1
            else:
                self.attempts_left -= 1
                if self.number_to_guess > guess:
                    self.hint_text = f"The number is greater than {guess}"
                else:
                    self.hint_text = f"The number is less than {guess}"
                self.hint_label.text = self.hint_text

                if self.attempts_left > 0:
                    self.attempts_text = f'You have {self.attempts_left} attempts' if self.difficulty_level != 'e' else 'You have unlimited attempts'
                else:
                    self.message = "Better luck next time! Do you want to play again?"
                    self.message_label.text = self.message
                    self.hint_text = f"The number was: {self.number_to_guess}"
                    self.game_active = False
                    self.guess_input.opacity = 0
                    self.guess_button.opacity = 0
                    self.attempts_label.opacity = 0
                    self.play_again_layout.opacity = 1

            self.message_label.text = self.message
            self.attempts_label.text = self.attempts_text
            self.hint_label.text = self.hint_text

        except ValueError:
            self.hint_text = "Invalid input. Please enter a number."
            self.hint_label.text = self.hint_text

    def reset_game(self, instance):
        self.message = "Choose difficulty level:"
        self.message_label.text = self.message
        self.hint_text = ""
        self.hint_label.text = self.hint_text
        self.attempts_text = ""
        self.attempts_label.text = self.attempts_text
        self.play_again_layout.opacity = 0
        self.difficulty_layout.opacity = 1
        self.game_active = False
        self.guess_input.text = ''

    def exit_game(self, instance):
        App.get_running_app().stop()
class NumberGuessingApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex('#e0f7fa') # Light cyan background for the window
        return NumberGuessingGame()
if __name__ == '__main__':
    NumberGuessingApp().run()
