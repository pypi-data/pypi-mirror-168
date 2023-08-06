from multiprocessing import Process, JoinableQueue
import time
import os
import glob


class TgHelper:
    def __init__(self, conn):
        self.conn = conn

    def execute_gsql(self, file_path):
        with open(file_path, "r") as text_file:
            gsql_txt = text_file.read()
        _result = self.conn.gsql(gsql_txt)
        return _result
    

class tg_upload:
    def __init__(self, source_file, tg_conn, job, job_filename, lines_per_file=1000000, no_workers=5,
                timeout = 500000):
        self.source_file = source_file
        self.lines_per_file = lines_per_file
        self.conn = tg_conn
        self.no_workers = no_workers
        self.q = JoinableQueue()
        self.job = job
        self.timeout = timeout
        self.job_filename = job_filename
        self.producers = []

    def producer(self):
        self.clean_up()
        smallfile = None
        with open(self.source_file) as bigfile:
            for lineno, line in enumerate(bigfile):
                if lineno % self.lines_per_file == 0:
                    if smallfile:
                        smallfile.close()
                        self.q.put(small_filename)
                    small_filename = 'small_file/small_file_{source_file}_{lno}.csv'.format(
                        lno=lineno + self.lines_per_file,source_file=self.source_file)
                    smallfile = open(small_filename, "w")
                smallfile.write(line)
            if smallfile:
                smallfile.close()
                self.q.put(small_filename)
        pid = os.getpid()
        print(f'producer {pid} done')


    def worker(self):
        while True:
            item = self.q.get()
            pid = os.getpid()
            print(f'pid {pid} Working on {item}')
            self.conn.runLoadingJobWithFile(item, self.job_filename, self.job,
                                            timeout=self.timeout, sizeLimit = 128000000)
            os.remove(item)
            print(f'pid {pid} Finished {item}')
            self.q.task_done()
            
    def start_workers(self):
        for i in range(self.no_workers):
            p = Process(target=self.worker, daemon=True).start()
    
    def start_producers(self):
        for i in range(1):
            p = Process(target=self.producer)
            self.producers.append(p)
            p.start()
            # make sure producers done
            for p in self.producers:
                p.join()
    
    def clean_up(self):
        dir_path = r'small_file/*{source_file}*'.format(source_file=self.source_file)
        res = glob.glob(dir_path)

        for file_path in res:
            try:
                os.remove(file_path)
            except:
                print("Error while deleting file : ", file_path)
        
    
    def run(self):
        self.start_workers()
        self.start_producers()
        self.q.join()
        self.clean_up()
        print('All work completed')


    