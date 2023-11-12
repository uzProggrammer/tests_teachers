import subprocess
import os, time, psutil
from pathlib import Path
from . import errors

BASE_DIR = Path(__file__).resolve().parent


class Checker:
    def __init__(self, checker_code, code, testcase, username, out, in_, m_l, t_l, t,m,e,out1) -> None:
        self.m_l = m_l
        self.t=t
        self.out1=out1
        self.e=e
        self.m=m
        self.t_l = t_l
        self.code = code
        self.testcase = testcase
        self.username = username
        self.file = f'{BASE_DIR}\\checker{username}.py'
        self.out= out
        self.in_ = in_
        self.command = ['python', f"{BASE_DIR}\\checker{username}.py"]

        self.checker_code = f"""
from errors import MemoryLimitError, TimeLimitError, ComplationError, WrongAnswerError, ImprotError
code = \"\"\"{self.code}\"\"\"
in_ = \"\"\"{self.in_}\"\"\"
out = \"\"\"{self.out}\"\"\"
user_out = \"\"\"{self.out1}\"\"\"

{checker_code}
"""
    
    def create_checker_file(self):
        with open(self.file, 'w') as file:
            file.write(self.checker_code)
    
    def delete_file(self):
        os.remove(self.file)
        
    def run(self):
        global checker_procces
        self.create_checker_file()
        procces = subprocess.Popen(self.command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, text=True, universal_newlines=True, bufsize=1,close_fds=False)
        try:
            communicate = procces.communicate(timeout=10000)
            if communicate[1]=='':
                self.delete_file()
                return {'status': 'Qabul qilindi', 'time': self.t, 'memory': self.m}
            else:
                e = communicate[1]

                if 'errors.WrongAnswerError:' in e:
                    self.delete_file()
                    return {'status': 'Nato\'g\'ri javob', 'time': self.t, 'memory': self.m}
                
                elif 'errors.MemoryLimitError:' in e:
                    self.delete_file()
                    return {'status': 'Xotira chegararidan o\'tib ketdi', 'time': 0, 'memory': self.m_l}
                
                elif 'errors.TimeLimitError:' in e:
                    self.delete_file()
                    return {'status': 'Vaqt chegarasidan o\'tib ketdi', 'time': self.t, 'memory': self.m}
                
                elif 'errors.ComplationError:' in e:
                    print(e)
                    self.delete_file()
                    return {'status': 'Komplatsiya xatosi', 'time': 0, 'memory': 0, 'e': 'Error From Checker!!'}

                elif 'errors.ImprotError:' in e:
                    self.delete_file()
                    return {'status': 'Import Error', 'time': 0, 'memory': 0}

                self.delete_file()
                return False
        except subprocess.TimeoutExpired:
            self.delete_file()
            return False
        except Exception as error:
            return False

        


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
        self.command = ['python' if self.lang == 'python' else '/home/itmacomsc/.nvm/versions/node/v21.0.0/bin/node', f"{BASE_DIR}\\{username}.py" if self.lang=='python' else f'{BASE_DIR}\\{username}.js']
        self.file = f"{BASE_DIR}\\{username}.py" if self.lang=='python' else f'{BASE_DIR}\\{username}.js'
        
        

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
                if not self.checker:
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
                    try:
                        procces = subprocess.Popen(self.command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        procces.stdin.write(self._in)
                        start = time.time()
                        communicate = procces.communicate(timeout=self.time_limit/10)
                        end = time.time()
                        self.delta = (end - start) * 10
                        if communicate[1] == '':
                            outpoot1 = communicate[0][:-1]
                            checker = Checker(self.checker, self.body, 1,self.username,self.out,self._in,self.memory_limit,self.time_limit,t=self.delta,m=memory*1024, e=communicate[1], out1=outpoot1)
                            ch_r = checker.run()
                            if ch_r:
                                self.delete_file()
                                return ch_r
                            else:
                                self.delete_file()
                                return {'status': 'Chekerda Xatolik', 'time': self.delta1, 'memory': memory*1024}
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

