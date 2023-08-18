import subprocess
import os, re, time


body = '''

'''

class MemoryLimit(Exception):
    pass


class Complier:
    def __init__(self, body, time_limit, memory_limit, tests):
        self.body = body
        self.time_limit = time_limit
        self.memory_limit = memory_limit
        self.tests = tests
        self.command = ["python", "problems/main.py"]
        self.file = 'D:/Django/tests_teachers/problems/main.py'

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
            if self.get_size('mb') < self.memory_limit:
                return True
            else:
                raise MemoryLimit('Algiritm xato')
    def get_run_memory(self):
        return self.get_size('kb')
    def run(self):
        if 'sys' in self.body or 'os' in self.body or 'subprocess' in self.body or 'tkinter' in self.body or 'turtle' in self.body:
            return {'status':'ImportError', 'time':0}
        test_n = 1
        for test_k, test_v in self.tests.items():
            start = time.time()
            try:
                global procces
                self.get_memory()
                procces = subprocess.Popen(self.command,stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                procces.stdin.write(test_k)
                if procces.communicate(timeout=self.time_limit/1000)[1] == '':
                    outpoot1 = procces.communicate()[0].replace('\n', '')
                    if outpoot1 == test_v:
                        outpoot = 'Accepted'
                    else:
                        outpoot = f'WrongAnswer({test_n})'
                        end = time.time()
                        break
                else:
                    outpoot = f'CE'
                    print(procces.communicate(timeout=self.time_limit/1000)[1])
            except subprocess.TimeoutExpired:
                outpoot = f'TimeLimit({test_n})'
                end = time.time()
                break
            except MemoryLimit:
                outpoot = f'MemoryLimit({test_n})'
                end = time.time()
                break
            test_n+=1
            end = time.time()
        return {"status": f"{outpoot}", 'time': end - start}

    def __str__(self) -> str:
        return self.body

# print(Complier(body=body, time_limit=1000,memory_limit=16,tests={'1 2':'3','5 4':'9', '342 28':'370'}).run())