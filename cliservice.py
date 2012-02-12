import threading
import time
import signal
import os
import sys
import traceback
import argparse

def _interrupt_handler(signum, frame):
    if signal.SIGINT == signum:
        raise KeyboardInterrupt
    
def _get_pid(pidfile):
    try:
        pid_file = open(pidfile, 'r')
    except IOError as err:
        if 2 == err.errno:
            return None # pidfile not exist
        else:
            raise # dont know what happend, let propagete
    else:
        pid = int(pid_file.read())
        pid_file.close()
        return pid    

class BaseCliService(threading.Thread):
    '''A framework for commandline service script
    
    extend this class and implement 'serve' method
    '''
    # after a successful run, sleep for this time
    # 0 for not sleep
    _BREATH_TIMEOUT_SUCCESS = 0
    # if err accurs in a run, sleep for this time(sec)
    # return False in server() treated as err 
    _BREATH_TIMEOUT_ERR = 5 
    
    _NUM_WORKERS = 1 # number of worker threads
    
    _workers = [] 
    
    def __init__(self):
        '''DO call super in subclass at first line'''
        threading.Thread.__init__(self)
        self.__shutdown_flag = False
        
    def run(self):
        '''control execution flow in this method'''
        while not self.__shutdown_flag:
            try:
                if False == self.serve():
                    time.sleep(self._BREATH_TIMEOUT_ERR)  
                elif self._BREATH_TIMEOUT_SUCCESS:
                    time.sleep(self._BREATH_TIMEOUT_SUCCESS)
            except:
                # @todo: increase sleep time by error count
                time.sleep(self._BREATH_TIMEOUT_ERR)
                
                traceback.print_exception(*sys.exc_info(), file=sys.stdout)
                
    def serve(self):
        '''Subclass MUST override this method and put business logic here'''
        raise NotImplementedError()
    
    def _shutdown(self):
        '''DO call super in subclass'''
        self.__shutdown_flag = True
    
    @classmethod
    def _init_workers(cls):
        for i in range(cls._NUM_WORKERS):                   
            worker = cls()
            worker.daemon = True
            worker.start()
            cls._workers.append(worker)
            
    @classmethod
    def _shutdown_workers(cls):
        for worker in cls._workers:                    
            worker._shutdown()
        
        for worker in cls._workers:                    
            if worker.is_alive():
                worker.join()
                
    @classmethod
    def _on_exception(cls, err):
        ''''''
                
    @classmethod
    def start_(cls, pidfile):
        ''''''
        if not _get_pid(pidfile):
            try:
                f = open(pidfile, 'w')
                f.write(str(os.getpid()))
                f.flush()
                # force SIGINT go to main thread
                signal.signal(signal.SIGINT, _interrupt_handler)
                
                cls._init_workers()
                
                while 1 < threading.active_count(): # more threads than the main
                    time.sleep(0.1) # just waiting for KeyboardInterrupt...
                    
            except KeyboardInterrupt:
                print 'shutting down...'                
                cls._shutdown_workers() 
                                       
            except Exception as err:
                if not cls._on_exception(err):
                    raise
            
            finally:
                f.close()
                os.remove(pidfile)
        else:
            print '{} is already running'.format(cls.__name__)            
            
    @classmethod
    def stop_(cls, pidfile):
        pid = _get_pid(pidfile)
        if pid:
            try:
                os.kill(pid, signal.SIGINT)
            except OSError as err:
                if 3 == err.errno:
                    os.remove(pidfile)
                else:
                    raise
        else:
            print '{} is not running'.format(cls.__name__)
            
    @classmethod
    def do_cli(cls, pidfile):
        parser = argparse.ArgumentParser(description='parse gerneral cli commands')
        parser.add_argument('ACTION', default='start', nargs='?', 
                            choices=('start', 'stop'))
        parser.add_argument('-d', action='store_true', dest='DEBUG', 
                            help='enable debug mode')
        args = parser.parse_args()
        
        if 'start' == args.ACTION:
            cls.start_(pidfile)
            
        elif 'stop' == args.ACTION:        
            cls.stop_(pidfile)        

#
# example for script below
# ===========================
#
#class SomeService(BaseCmdService):
#    def serve(self):
#        ''''''
#        # some business logic
#            
#if '__main__' == __name__:
#        pidfile = '{}.pid'.format(splitext(abspath(__file__))[0])
#        GrubService.do_cli(pidfile)