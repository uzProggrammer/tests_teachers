import threading

class UrinishYaratuvchiThread(threading.Thread):
    def __init__(self, username, masala, lang, urinish):
        self.username = username
        self.masala = masala
        self.lang = lang
        self.urinish = urinish
        threading.Thread.__init__(self)

    def run(self):
        self.masala.run(self.username, self.lang, self.urinish)