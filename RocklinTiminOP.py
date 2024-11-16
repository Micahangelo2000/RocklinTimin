import rumps
from datetime import datetime, timedelta

class MyMenuApp(rumps.App):
    def __init__(self):
        super(MyMenuApp, self).__init__("Menu App")
        
        # Initial configuration
        self.icon = 'image.png'
        self.clock_status = False
        self.day_color = "R"
        self.period_var = 1
        self.get_second_time = False
        self.schedule_times = self.load_schedule_times()
        self.current_time_display = ""

        # Menu structure
        self.menu = [
            rumps.MenuItem('Hello', callback=self.say_hello, key='h'),
            "Settings",
            "Button",
            None,
            ["Test", [
                ["Depth", [
                    "It's pretty easy"
                ]]
            ]],
            rumps.MenuItem("Clock", callback=self.toggle_clock, key='c'),
            None,
        ]

        # Timer setup (start paused)
        self.timer = rumps.Timer(self.update_clock, 1)
        self.timer.stop()

    def load_schedule_times(self):
        try:
            with open('times.txt', 'r') as file:
                return file.readlines()
        except FileNotFoundError:
            print("The file times.txt does not exist.")
            return []

    def get_time_for_period(self, period, second_time=False):
        target_string = f'-{self.day_color}-Period {period}'
        index_shift = 2 if second_time else 1

        for i, line in enumerate(self.schedule_times):
            if target_string in line:
                return self.schedule_times[i + index_shift].strip() if i + index_shift < len(self.schedule_times) else None
        return None

    @rumps.clicked("Hello")
    def say_hello(self, _):
        rumps.notification("Hello", "Hello, World!", "This is a text message.")
        print("\n Hello Mate \n")

    @rumps.clicked("Settings")
    def sets(self, _):
        rumps.alert("No preferences available!")

    @rumps.clicked("Button")
    def onoff(self, sender):
        sender.state = not sender.state

    @rumps.clicked("Clock")
    def toggle_clock(self, _):
        self.clock_status = not self.clock_status
        if self.clock_status:
            self.title = "Updating..."
            self.icon = None
            self.timer.start()  # Start the timer to update the clock
        else:
            self.title = " "
            self.icon = 'image.png'
            self.timer.stop()  # Stop the timer to save CPU resources

    def update_clock(self, _):
        if self.clock_status:
            self.set_correct_period()
            new_time_display = self.countdown_timer()

            # Only update if the time display has changed
            if new_time_display != self.current_time_display:
                self.current_time_display = new_time_display
                self.title = new_time_display

    def countdown_timer(self):
        user_defined_time = self.get_time_for_period(self.period_var, self.get_second_time)
        if not user_defined_time:
            return "00:00:00"

        today_date = datetime.now().date()
        previous_time = datetime.combine(today_date, datetime.strptime(user_defined_time, "%H:%M").time())
        current_time = datetime.now()

        if previous_time < current_time:
            previous_time += timedelta(days=1)

        time_difference = int((previous_time - current_time).total_seconds())

        hours = time_difference // 3600
        minutes = (time_difference % 3600) // 60
        seconds = time_difference % 60

        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def set_correct_period(self):
        time_checks = [(1, False), (1, True), (2, False), (2, True), (2.5, False), 
                       (2.5, True), (3, False), (3, True), (4, False), (4, True), 
                       (5, False), (5, True)]

        for period, second_time in time_checks:
            self.period_var = period
            self.get_second_time = second_time

            scheduled_time = self.get_time_for_period(period, second_time)
            if scheduled_time:
                today_date = datetime.now().date()
                if datetime.now() < datetime.combine(today_date, datetime.strptime(scheduled_time, "%H:%M").time()):
                    return

        self.period_var = 1  # Reset to default if no match found
        self.get_second_time = False

    @rumps.clicked("Test", "Depth", "It's pretty easy")
    def does_sth(self, _):
        rumps.notification("Hi", "How are you?", "Subscribe to my channel!")
        print("\n Hello There Mate \n")

# Run the app
if __name__ == "__main__":
    MyMenuApp().run()
