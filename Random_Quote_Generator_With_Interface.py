import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import ListProperty
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle
# Set window size
Window.size = (800, 600)
class QuotesDatabase:
    content = [
    "The welfare of humanity is always the alibi of tyrants.",
    "Until the great mass of the people shall be filled with the sense of responsibility for each other's welfare, social justice can never be attained.",
    "Our true progress can be measured by how well we provide for the most vulnerable among us.",
    "The test of our civilization is the way that society cares for its members.",
    "We have the means to end poverty, the only thing missing is the will.",
    "Global welfare depends on recognizing our shared humanity.",
    "Injustice anywhere is a threat to justice everywhere.",
    "Peace cannot exist without justice, equity, and opportunity for all.",
    "The earth provides enough to satisfy every man's needs, but not every man's greed.",
    "The future of humanity lies in our ability to cooperate globally for the common good.",
    "Let us not be satisfied with just giving money. Money is not enough, money can be got, but they need your hearts to love them. So, spread your love everywhere you go.",
    "The best way to find yourself is to lose yourself in the service of others.",
    "Be the change that you wish to see in the world.",
    "An eye for an eye will only make the whole world blind.",
    "You must not lose faith in humanity. Humanity is an ocean; if a few drops of the ocean are dirty, the ocean does not become dirty.",
    # ... The rest of the quotes from the original code ...
    "The seeds of global welfare are sown through acts of kindness and cooperation.",
    "A world united in purpose can overcome any challenge.",
    "The strength of our humanity lies in our ability to care for one another.",
    "In the end, we will remember not the words of our enemies, but the silence of our friends.",
    "The greatest glory in living lies not in never falling, but in rising every time we fall.",
    "The way to get started is to quit talking and begin doing.",
    "You cannot shake hands with a clenched fist.",
    "The best way to predict the future is to create it.",
    "The only limit to our realization of tomorrow will be our doubts of today.",
    "Success is not how high you have climbed, but how you make a positive difference to the world.",
    "The best way to find yourself is to lose yourself in the service of others.",
    "The greatest use of a life is to spend it on something that will outlast it.",
    ]

    @staticmethod
    def get_random_quote():
        return random.choice(QuotesDatabase.content)
class QuoteGeneratorWidget(BoxLayout):
    background_color = ListProperty([0.1, 0.1, 0.2, 1])
    
    def __init__(self, **kwargs):
        super(QuoteGeneratorWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [20, 20]
        self.spacing = 20
        
        # Add a background color
        with self.canvas.before:
            Color(self.background_color[0], self.background_color[1], self.background_color[2], self.background_color[3])
            self.rect = Rectangle(size=self.size, pos=self.pos)
            
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        # Title
        self.title = Label(
            text="Random Quote Generator",
            font_size=32,
            size_hint=(1, 0.1),
            color=get_color_from_hex('#FFD700')  # Gold color
        )
        self.add_widget(self.title)
        
        # Create a ScrollView for the quote
        self.scroll_view = ScrollView(
            size_hint=(1, 0.6),
            do_scroll_x=False
        )
        
        # Quote content
        self.quote_label = Label(
            text="Press the button below to generate a random quote.",
            font_size=24,
            size_hint_y=None,
            padding=(20, 20),
            color=get_color_from_hex('#FFFFFF'),
            halign='center',
            valign='middle'
        )
        
        # Make the label expand to the height of its text
        self.quote_label.bind(width=lambda *x: self.quote_label.setter('text_size')(self.quote_label, (self.quote_label.width, None)))
        self.quote_label.bind(texture_size=lambda *x: self.quote_label.setter('height')(self.quote_label, self.quote_label.texture_size[1]))
        
        self.scroll_view.add_widget(self.quote_label)
        self.add_widget(self.scroll_view)
        
        # Buttons container
        buttons_layout = BoxLayout(
            size_hint=(1, 0.2),
            spacing=20,
            padding=[10, 10]
        )
        
        # Generate button
        self.generate_button = Button(
            text="Generate Quote",
            font_size=20,
            size_hint=(0.5, 1),
            background_color=get_color_from_hex('#4CAF50'),  # Green
            background_normal=''
        )
        self.generate_button.bind(on_press=self.generate_quote)
        buttons_layout.add_widget(self.generate_button)
        
        # Exit button
        self.exit_button = Button(
            text="Exit",
            font_size=20,
            size_hint=(0.5, 1),
            background_color=get_color_from_hex('#F44336'),  # Red
            background_normal=''
        )
        self.exit_button.bind(on_press=self.exit_app)
        buttons_layout.add_widget(self.exit_button)
        
        self.add_widget(buttons_layout)
        
        # Footer label
        self.footer = Label(
            text="Thank you for using Random Quote Generator",
            font_size=14,
            size_hint=(1, 0.1),
            color=get_color_from_hex('#CCCCCC')  # Light grey
        )
        self.add_widget(self.footer)
        
        # Colors for animation
        self.colors = [
            get_color_from_hex('#673AB7'),  # Deep Purple
            get_color_from_hex('#3F51B5'),  # Indigo
            get_color_from_hex('#2196F3'),  # Blue
            get_color_from_hex('#009688'),  # Teal
            get_color_from_hex('#4CAF50'),  # Green
            get_color_from_hex('#FF9800'),  # Orange
            get_color_from_hex('#FF5722'),  # Deep Orange
            get_color_from_hex('#795548')   # Brown
        ]
        
        # Start background color animation
        Clock.schedule_interval(self.animate_background, 10)
        
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
    def generate_quote(self, instance):
        # Animate the button
        anim = Animation(size_hint_y=1.1, duration=0.1) + Animation(size_hint_y=1, duration=0.1)
        anim.start(instance)
        
        # Get and display a random quote
        quote = QuotesDatabase.get_random_quote()
        self.quote_label.text = quote
        
        # Animate the quote appearance
        self.quote_label.opacity = 0
        anim = Animation(opacity=1, duration=0.5)
        anim.start(self.quote_label)
        
    def exit_app(self, instance):
        App.get_running_app().stop()
        
    def animate_background(self, dt):
        next_color = random.choice(self.colors)
        r, g, b, a = next_color
        
        # Animate the background color change
        anim = Animation(background_color=[r, g, b, a], duration=2)
        anim.start(self)
class QuoteGeneratorApp(App):
    def build(self):
        return QuoteGeneratorWidget()      
if __name__ == '__main__':
    QuoteGeneratorApp().run()
