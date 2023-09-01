import subprocess
import os, re, time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class MemoryLimit(Exception):
    pass


class Complier:
    def __init__(self, body:str, time_limit:int, memory_limit:int, username:str, _in:str, out:str, checker:str = None, lang='python'):
        self.body = body
        self.time_limit = time_limit
        self.memory_limit = memory_limit*(1024)
        self._in = _in
        self.out = out
        self.username = username
        self.lang = lang
        self.checker = checker
        self.delta1 = 0.0
        self.delta = 0.0
        self.command = [self.lang, f"{BASE_DIR}\\{username}.py" if self.lang=='python' else f'{BASE_DIR}\\{username}.js']
        self.file = f"{BASE_DIR}\\{username}.py" if self.lang=='python' else f'{BASE_DIR}\\{username}.js'
        if self.checker:
            self.checker_command = ['python', f"{BASE_DIR}\\checker.py"]
            self.checker_file = f"{BASE_DIR}\\checker.py"

    def get_size(self,unit='mb'):
        file_size = os.path.getsize(self.file)
        exponents_map = {'bytes': 0, 'kb': 1, 'mb': 2, 'gb': 3}
        if unit not in exponents_map:
            raise ValueError("Must select from \
            ['bytes', 'kb', 'mb', 'gb']")
        else:
            size = file_size / 1024 ** exponents_map[unit]
            return round(size, 3)

    def get_memory(self):
        with open(self.file, 'w') as file:
            file.write(self.body)
        if self.checker:
            with open(self.checker_file, 'w') as file:
                file.write(self.checker)
    def delete_file(self):
        os.remove(self.file)
    def get_run_memory(self):
        return self.get_size('bytes')/1024

    def run(self):
        global procces
        self.get_memory()
        if self.get_run_memory() <= self.memory_limit:
            if 'sys' in self.body or 'os' in self.body or 'subprocess' in self.body or 'tkinter' in self.body or 'turtle' in self.body or 'subprocess' in self.body:
                return {'status': 'Import Error', 'time': 0, 'memory': 0}
            
            else:
                memory = self.get_run_memory()
                if self.checker:
                    try:
                        procces = subprocess.Popen(self.command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        procces.stdin.write(self._in)
                        start = time.time()
                        communicate = procces.communicate(timeout=self.time_limit/10)
                        self.delta1 = (time.time() - start) * 10
                        a = False
                        chcker_proccess = subprocess.Popen(self.checker_command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        chcker_proccess.stdin.write(str({'code': str(self.body), 'in': self._in, 'out': self.out}))
                        try:
                            checker_communicate = chcker_proccess.communicate(timeout=10)
                            if checker_communicate[1] == '':
                                if checker_communicate[0] == '1\n':
                                    a = True
                            else:
                                a = True
                        except:
                            a = True
                        if communicate[1] == '':
                            outpoot1 = communicate[0][:-1]
                            if a:
                                if a:
                                    self.delete_file()
                                    return {'status': 'Qabul qilindi', 'time': self.delta1, 'memory': memory*1024}
                                else:
                                    self.delete_file()
                                    return {'status': 'Nato\'g\'ri javob', 'time': self.delta1, 'memory': memory*1024}
                            else:
                                self.delete_file()
                                return {'status': 'Nato\'g\'ri javob', 'time': self.delta1, 'memory': memory*1024}
                        else:
                            self.delete_file()
                            return {'status': 'Komplatsiya xatosi', 'time': self.delta1, 'memory': memory*1024, 'e': communicate[1]}
                    except subprocess.TimeoutExpired:
                        self.delete_file()
                        return {'status': 'Vaqt chegarasidan o\'tib ketdi', 'time': self.delta1, 'memory': memory*1024}
                else:
                    try:
                        procces = subprocess.Popen(self.command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        procces.stdin.write(self._in)
                        start = time.time()
                        communicate = procces.communicate(timeout=self.time_limit/10)
                        end = time.time()
                        self.delta = (end - start) * 10
                        if communicate[1] == '':
                            outpoot1 = communicate[0][:-1]
                            if outpoot1 == self.out:
                                self.delete_file()
                                return {'status': 'Qabul qilindi', 'time': self.delta, 'memory': memory*1024}
                            else:
                                self.delete_file()
                                return {'status': 'Nato\'g\'ri javob', 'time': self.delta, 'memory': memory*1024}
                        
                        else:
                            self.delete_file()
                            return {'status': 'Komplatsiya xatosi', 'time': self.delta1, 'memory': memory*1024, 'e': communicate[1]}
                    except subprocess.TimeoutExpired:
                        self.delete_file()
                        return {'status': 'Vaqt chegarasidan o\'tib ketdi', 'time': self.delta, 'memory': memory*1024}
        else:
            return {'status': 'Xotira chegararidan o\'tib ketdi', 'time': 0, 'memory': memory*1024}

    def __str__(self) -> str:
        return self.body

