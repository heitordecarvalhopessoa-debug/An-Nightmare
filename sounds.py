import winsound

class Sound:
    def __init__(self, game):
        self.game = game

    def play_menu_beep(self):
        winsound.Beep(750, 100)

    def play_collect_file(self):
        winsound.Beep(1200, 100)

    def play_nightmare_alert(self):
        winsound.Beep(220, 100)

    def play_clock_ticking(self):
        winsound.Beep(2500, 100)

    def play_typewriter_click(self):
        winsound.Beep(800, 15)