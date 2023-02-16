import os
from time import sleep
from pystyle import Center
from time import monotonic
from colorama import Fore, init
from textual.reactive import reactive
from textual.containers import Container
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Button

if os.name == "nt": os.system("title Timer - spy404#6985")
init()
print(Center.XCenter(Center.YCenter(Fore.GREEN + "Developed with love by spy404! loading...")))
sleep(3)
os.system("cls" if os.name == "nt" else "clear")

class display_time(Static):
    
    start_time = reactive(monotonic)
    time = reactive(0.0)
    total = reactive(0.0)

    def on_mount(self) -> None:
        
        self.update_timer = self.set_interval(1 / 60, self.update_time, pause=True)

    def update_time(self) -> None:
        
        self.time = self.total + (monotonic() - self.start_time)

    def watch_time(self, time: float) -> None:
        
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")

    def start(self) -> None:
        
        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self):
        
        self.update_timer.pause()
        self.total += monotonic() - self.start_time
        self.time = self.total

    def reset(self):
        
        self.total = 0
        self.time = 0

class main_page(Static):
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        
        button_id = event.button.id
        time_display = self.query_one(display_time)

        if button_id == "start":
            time_display.start()
            self.add_class("started")
        
        elif button_id == "stop":
            time_display.stop()
            self.remove_class("started")
        
        elif button_id == "reset":
            time_display.reset()

    def compose(self) -> ComposeResult:

        yield Button(
            "Start!",
            id = "start",
            variant = "success",
        )

        yield Button(
            "Stop!",
            id = "stop",
            variant = "error",
        )

        yield Button(
            "Reset!",
            id = "reset",
        )

        yield display_time("00:00:00:00")

class timer(App):
    
    CSS_PATH = "styles.css"
    BINDINGS = [
        (
            "D",
            "toggle_dark",
            "Toggle Dark Mode"
        ),

        (
            "A",
            "add_main_page",
            "Add!",
        ),

        (
            "R",
            "remove_main_page",
            "Remove!"
        ),

        (
            "Q",
            "quit",
            "Quit!"
        ),
    ]

    def compose(self) -> ComposeResult:
        
        yield Header()
        yield Footer()
        yield Container(
            main_page(),
            main_page(),
            main_page(),
            id = "timers",
        )

    def action_add_main_page(self) -> None:
        
        new_stopwatch = main_page()
        self.query_one("#timers").mount(new_stopwatch)
        new_stopwatch.scroll_visible()

    def action_remove_main_page(self) -> None:
        
        timers = self.query("main_page")
        
        if timers:
            timers.last().remove()

    def action_toggle_dark(self) -> None:

        self.dark = not self.dark

if __name__ == "__main__":
    timer().run()