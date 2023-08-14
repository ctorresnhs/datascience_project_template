
def timed_function(msg):
    def outer_wrapper(function):
        def inner_wrapper(*args, **kwargs):
            import time
            start_time = time.time()
            if msg is None:
                print(f" Running: {function.__name__} ...")
            else:
                print(msg)
            result = function(*args,**kwargs)
            end_time = time.time()
            elapsed = round(end_time-start_time,2)
            print(f"[{elapsed} seconds]")
            return result
        return inner_wrapper
    return outer_wrapper


class project_logger():
    def __init__(self,
                 project_name:str = "NEW PROJECT",
                 screen_log_on:bool=True,
                 screen_log_level_debug:bool=True, 
                 screen_log_time_on:bool = True,
                 file_log_on:bool = True,
                 file_log_level_debug:bool=True,
                 file_log_time_on:bool=True,
                 file_log_path:str = "./project.log",
                 file_log_mode_append = True
                 ) -> None:
        self.project_name = project_name
        self.screen_log_on = screen_log_on
        self.file_log_on = file_log_on
        import logging
        self.log = logging.getLogger('project_logger')
        self.log.setLevel(logging.DEBUG)
        # set formatting
        date_fmt = '%Y-%m-%d %H:%M:%S'
        if screen_log_time_on:
            screen_fmt = '[%(asctime)s] %(levelname)-6s %(message)s'
        else:
            screen_fmt = '%(levelname)-6s %(message)s'
        self.screen_formatter = logging.Formatter(fmt=screen_fmt,datefmt=date_fmt)
        if file_log_time_on:
            file_fmt = '[%(asctime)s] %(levelname)-6s %(message)s'
        else:
            file_fmt = '%(levelname)-6s %(message)s'
        self.file_formatter = logging.Formatter(fmt=file_fmt,datefmt=date_fmt)
        # create screen handler
        sh = logging.StreamHandler()
        sh.name = "screen_handler"
        if screen_log_level_debug:
            sh.setLevel(logging.DEBUG)
        else:
            sh.setLevel(logging.INFO)
        if screen_log_time_on:
            sh.setFormatter(self.screen_formatter)
        if screen_log_on:
            self.log.addHandler(sh)
        # create file handler
        if file_log_mode_append:
            fh = logging.FileHandler(filename=file_log_path, mode='a', encoding='utf-8')
        else: 
            fh = logging.FileHandler(filename=file_log_path, mode='w', encoding='utf-8')
        fh.name = "file_handler"
        if file_log_level_debug:
            fh.setLevel(logging.DEBUG)
        else:
            fh.setLevel(logging.INFO)
        if file_log_time_on:
            fh.setFormatter(self.file_formatter)
        if file_log_on:
            self.log.addHandler(fh)
        self.log_header() # prints the header of the log
    def get_info(self):
        return self.log.info
    def get_debug(self):
        return self.log.debug
    def log_header(self):
        import logging
        self.header_formatter = logging.Formatter(fmt=f"===========================> %(asctime)s %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
        msg = f"{self.project_name} log begins"
        if self.screen_log_on:
            screen_handler:logging.StreamHandler    = self.log.handlers[0]
            screen_handler.setFormatter             (self.header_formatter)
        if self.file_log_on:
            file_handler:logging.FileHandler        = self.log.handlers[1]
            file_handler.setFormatter               (self.header_formatter)
        self.log.debug(msg)
        if self.screen_log_on:
            screen_handler.setFormatter             (self.screen_formatter)
        if self.file_log_on:
            file_handler.setFormatter               (self.file_formatter)
    def timed_info(self,msg):
        def outer_wrapper(function):
            def inner_wrapper(*args, **kwargs):
                import time
                start_time = time.time()
                if msg is None:
                    self.log.info(f"Executing: {function.__name__} ...")
                else:
                    self.log.info(f"{msg} (executing)")
                result = function(*args,**kwargs)
                end_time = time.time()
                elapsed = round(end_time-start_time,2)
                self.log.info(f"{msg} (completed in {elapsed} seconds)")
                return result
            return inner_wrapper
        return outer_wrapper
    def timed_debug(self,msg):
        def outer_wrapper(function):
            def inner_wrapper(*args, **kwargs):
                import time
                start_time = time.time()
                if msg is None:
                    self.log.info(f"Executing: {function.__name__} ...")
                else:
                    self.log.debug(f"{msg} (executing)")
                result = function(*args,**kwargs)
                end_time = time.time()
                elapsed = round(end_time-start_time,2)
                self.log.info(f"{msg} (completed in {elapsed} seconds)")
                return result
            return inner_wrapper
        return outer_wrapper

