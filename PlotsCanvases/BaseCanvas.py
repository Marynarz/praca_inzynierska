from abc import ABC, abstractmethod

class BaseCanvas(ABC)
    
	@abstractmethod
	def update_plot(self):
	    raise NotImplementedError('Not implemented yet')
	
	@abstractmethod
	def show(self):
	    raise NotImplementedError('Not implemented yet')
		
	@abstractmethod
	def set_grid(self):
	    raise NotImplementedError('Not implemented yet')
		
	@abstractmethod
	def set_line(self):
	    raise NotImplementedError('Not implemented yet')
