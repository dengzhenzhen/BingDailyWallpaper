#encoding=utf-8  
import win32serviceutil   
import win32service   
import win32event  
import os   
import logging  
import inspect
import servicemanager
import sys
import win32timezone
import threading
from main import Bing
bing = Bing()

class PythonService(win32serviceutil.ServiceFramework):   
  
    _svc_name_ = "BingWallpaper"  #服务名 
    _svc_display_name_ = "BingWallpaper Service"  #服务在windows系统中显示的名称
    _svc_description_ = "BingWallpaper Service Collector "  #服务的描述
  
    def __init__(self, args):   
        win32serviceutil.ServiceFramework.__init__(self, args)   
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)  
        self.logger = self._getLogger()  
        self.run = True  
          
    def _getLogger(self):  
          
        logger = logging.getLogger('[PythonService]')  
          
        this_file = inspect.getfile(inspect.currentframe())  
        dirpath = os.path.abspath("D:\\Repositories\\BingDailyWallpaper\\logs")  
        handler = logging.FileHandler(os.path.join(dirpath, "service.log"))  
          
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')  
        handler.setFormatter(formatter)  
          
        logger.addHandler(handler)  
        logger.setLevel(logging.INFO)  
          
        return logger  
  
    def SvcDoRun(self):  
        import time
        # try:
        #     from main import Bing
        #     bing = Bing()
        #     thread = threading.Thread(target=bing.run, kwargs={"waiting":10})
        #     thread.start()
        # except Exception as err:
        #     self.logger.info(str(err))
        # self.logger.info("service is run....")
        # while self.run:  
        #     # self.logger.info("I am runing....")  
        #     time.sleep(2)  
        bing.run()
              
    def SvcStop(self):   
        self.logger.info("service is stop....")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)   
        win32event.SetEvent(self.hWaitStop)
        os.system("taskkill /IM Win32Service.exe /F")
        self.run = False  
  
if __name__=='__main__':   
    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(PythonService)
            servicemanager.Initialize('PythonService', evtsrc_dll)
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            pass
    else:
        win32serviceutil.HandleCommandLine(PythonService)