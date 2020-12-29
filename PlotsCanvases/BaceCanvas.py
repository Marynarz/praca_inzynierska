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
