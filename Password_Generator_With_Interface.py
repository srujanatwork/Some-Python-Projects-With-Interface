import random
import string
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.animation import Animation
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView  # Import ScrollView
# Set background color to dark blue
Window.clearcolor = get_color_from_hex("#1A237E")
class PasswordBox(TextInput):
    def __init__(self, **kwargs):
        super(PasswordBox, self).__init__(**kwargs)
        self.background_color = get_color_from_hex("#E8EAF6")
        self.foreground_color = get_color_from_hex("#303F9F")
        self.font_size = dp(18)
        self.readonly = True
        self.halign = 'center'
        self.size_hint = (1, None)
        self.height = dp(50)
        self.multiline = False
class PasswordGenerator(BoxLayout):
    password = StringProperty("")

    def __init__(self, **kwargs):
        super(PasswordGenerator, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(20)
        self.spacing = dp(15)

        # Title
        self.title = Label(
            text="Password Generator",
            font_size=dp(28),
            color=get_color_from_hex("#C5CAE9"),
            size_hint=(1, None),
            height=dp(60)
        )
        self.add_widget(self.title)

        # Password display
        self.password_box = PasswordBox(text="")
        self.add_widget(self.password_box)

        # Strength selection
        strength_label = Label(
            text="Password Strength:",
            font_size=dp(18),
            color=get_color_from_hex("#C5CAE9"),
            size_hint=(1, None),
            height=dp(40)
        )
        self.add_widget(strength_label)

        # Toggle buttons for strength
        strength_layout = BoxLayout(
            size_hint=(1, None),
            height=dp(50),
            spacing=dp(10)
        )

        self.less_secure_btn = ToggleButton(
            text="Less Secure (8 chars)",
            group="strength",
            state="down",
            background_color=get_color_from_hex("#5C6BC0"),
            background_normal="",
            color=get_color_from_hex("#FFFFFF")
        )

        self.highly_secure_btn = ToggleButton(
            text="Highly Secure (16 chars)",
            group="strength",
            background_color=get_color_from_hex("#5C6BC0"),
            background_normal="",
            color=get_color_from_hex("#FFFFFF")
        )

        strength_layout.add_widget(self.less_secure_btn)
        strength_layout.add_widget(self.highly_secure_btn)
        self.add_widget(strength_layout)

        # Generate button
        self.generate_btn = Button(
            text="Generate Password",
            size_hint=(1, None),
            height=dp(60),
            background_color=get_color_from_hex("#303F9F"),
            background_normal="",
            color=get_color_from_hex("#FFFFFF"),
            font_size=dp(18)
        )
        self.generate_btn.bind(on_press=self.generate_password)
        self.add_widget(self.generate_btn)

        # Copy button
        self.copy_btn = Button(
            text="Copy to Clipboard",
            size_hint=(1, None),
            height=dp(50),
            background_color=get_color_from_hex("#3F51B5"),
            background_normal="",
            color=get_color_from_hex("#FFFFFF")
        )
        self.copy_btn.bind(on_press=self.copy_to_clipboard)
        self.add_widget(self.copy_btn)

        # Reset button
        self.reset_btn = Button(
            text="Reset All",
            size_hint=(1, None),
            height=dp(50),
            background_color=get_color_from_hex("#F44336"),  # Red color
            background_normal="",
            color=get_color_from_hex("#FFFFFF")
        )
        self.reset_btn.bind(on_press=self.reset_all)
        self.add_widget(self.reset_btn)

        # Character types included (display only)
        char_types_label = Label(
            text="Includes: Uppercase, Lowercase, Numbers, Symbols",
            font_size=dp(14),
            color=get_color_from_hex("#C5CAE9"),
            size_hint=(1, None),
            height=dp(30)
        )
        self.add_widget(char_types_label)

        # Status label (for copy confirmation)
        self.status_label = Label(
            text="",
            font_size=dp(14),
            color=get_color_from_hex("#4CAF50"),
            size_hint=(1, None),
            height=dp(30)
        )
        self.add_widget(self.status_label)

        # Password history
        history_label = Label(
            text="Recent Passwords:",
            font_size=dp(16),
            color=get_color_from_hex("#C5CAE9"),
            size_hint=(1, None),
            height=dp(40),
            halign="left"
        )
        self.add_widget(history_label)

        # ScrollView for password history
        self.history_scrollview = ScrollView(size_hint=(1, 1))

        # Grid for password history
        self.history_grid = GridLayout(
            cols=1,
            spacing=dp(5),
            size_hint_y=None,  # Make height not fixed
            height=dp(400)
        )
        self.history_grid.bind(minimum_height=self.history_grid.setter('height'))  # Bind minimum_height

        self.history_scrollview.add_widget(self.history_grid)  # Add grid to scrollview
        self.add_widget(self.history_scrollview)  # Add scrollview

        # Password history (max 5)
        self.password_history = []

    def generate_password(self, instance):
        # Determine password strength
        if self.less_secure_btn.state == "down":
            password_strength = "less"
        else:
            password_strength = "high"

        # Generate password
        new_password = self.password_generator(password_strength)
        self.password = new_password
        self.password_box.text = new_password

        # Animate the password box
        anim = Animation(background_color=get_color_from_hex("#C5CAE9"), duration=0.3) + \
            Animation(background_color=get_color_from_hex("#E8EAF6"), duration=0.3)
        anim.start(self.password_box)

        # Add to history
        self.add_to_history(new_password)

    def password_generator(self, ps1):
        characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                      'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                      'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                      'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                      'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                      '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-',
                      '.', '/', ':', ';', '<', '=', '>', '?', '@']

        if ps1 == 'less':
            return ''.join(random.choices(characters, k=8))
        else:
            return ''.join(random.choices(characters, k=16))

    def copy_to_clipboard(self, instance):
        if self.password:
            from kivy.core.clipboard import Clipboard
            Clipboard.copy(self.password)

            # Show confirmation
            self.status_label.text = "Password copied to clipboard!"
            self.status_label.color = get_color_from_hex("#4CAF50")  # Green

            # Clear confirmation after 2 seconds
            Clock.schedule_once(self.clear_status, 2)

    def clear_status(self, dt):
        self.status_label.text = ""

    def add_to_history(self, password):
        # Add new password to history
        self.password_history.insert(0, password)

        # Keep only the last 5 passwords
        self.password_history = self.password_history[:5]

        # Clear and rebuild history display
        self.history_grid.clear_widgets()

        for pw in self.password_history:
            history_item = BoxLayout(
                size_hint=(1, None),
                height=dp(40),
                spacing=dp(10)
            )

            # Truncate long passwords in history view
            display_pw = pw
            if len(pw) > 16:
                display_pw = pw[:16] + "..."

            pw_label = Label(
                text=display_pw,
                color=get_color_from_hex("#C5CAE9"),
                size_hint=(0.7, 1),
                halign="left"
            )

            copy_btn = Button(
                text="Copy",
                size_hint=(0.3, 1),
                background_color=get_color_from_hex("#5C6BC0"),
                background_normal="",
                color=get_color_from_hex("#FFFFFF")
            )

            # Use lambda with default argument to keep reference to the current password
            copy_btn.bind(on_press=lambda btn, p=pw: self.copy_history_password(p))

            history_item.add_widget(pw_label)
            history_item.add_widget(copy_btn)
            self.history_grid.add_widget(history_item)

    def copy_history_password(self, password):
        from kivy.core.clipboard import Clipboard
        Clipboard.copy(password)

        # Show confirmation
        self.status_label.text = "History password copied!"
        self.status_label.color = get_color_from_hex("#4CAF50")  # Green

        # Clear confirmation after 2 seconds
        Clock.schedule_once(self.clear_status, 2)

    def reset_all(self, instance):
        # Clear current password
        self.password = ""
        self.password_box.text = ""

        # Clear password history
        self.password_history = []
        self.history_grid.clear_widgets()

        # Reset strength to default (Less Secure)
        self.less_secure_btn.state = "down"
        self.highly_secure_btn.state = "normal"

        # Show confirmation
        self.status_label.text = "All passwords cleared!"
        self.status_label.color = get_color_from_hex("#F44336")  # Red

        # Animate the password box
        anim = Animation(background_color=get_color_from_hex("#FFCDD2"), duration=0.3) + \
            Animation(background_color=get_color_from_hex("#E8EAF6"), duration=0.3)
        anim.start(self.password_box)

        # Clear confirmation after 2 seconds
        Clock.schedule_once(self.clear_status, 2)
class PasswordGeneratorApp(App):
    def build(self):
        self.title = 'Password Generator'
        return PasswordGenerator()
if __name__ == '__main__':
    PasswordGeneratorApp().run()
