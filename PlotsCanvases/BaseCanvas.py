from abc import ABC, abstractmethod

class BaseCanvas(ABC)
    
	@abstractmethod
	def update_plot(self):
	    pass
	
	@abstractmethod
	def show(self):
	    pass
		
	@abstractmethod
	def set_grid(self):
	    pass
		
	@abstractmethod
	def set_line(self):
	    pass

class NotImplementedError(Exception):
    def __init__(self, error_code, error_msg, exit_code):
	    self.error_code = error_code
		self.error_msg = error_msg
		self.exit_code = exit_code
	
	def __str__(self):
	    return 'NotImplementedError: error_code : {0!s}, error_msg : {1}, exit_code : {2!s}'.format(self.error_code, self.error_msg, self.exit_code)

