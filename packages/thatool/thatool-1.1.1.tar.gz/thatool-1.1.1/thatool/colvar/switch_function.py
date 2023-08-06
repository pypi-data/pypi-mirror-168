import numpy as np


### ============================================================================
## Switching functions class:
### ============================================================================
class SwitchFunction:   
	"""NOTE: Dmin != D0
	D0, R0    : are the parameter of switching function 
	Dmin, Dmax : are the bounds at which the switching take affect"""
	
	# def __init__(self):
	# 	"create some intiatial attributes..."
		# self.r0 = None        

	class RATIONAL:
		""" Create an Object of SWITCHING FUNCTION
		* Attributes:
			swType       : (default='RATIONAL') Type of witching function, 
			r0, d0       : The r_0 parameter of the switching function
			n            : (default=6) The n parameter of the switching function    
			m            : (default=2*m) The m parameter of the switching function 
			Dmin, Dmax   : interval in which scaling take effect
			
		* Methods:
			fFunc    : compute & return value and derivation of sw function
			fDmax    : estimate value of Dmax
			
		Ex: sw = thaTool.SwitchFunc(r0=6.3, swType='RATIONAL', d0=0.0, n=10)
		"""
		def __init__(self, r0, d0=0.0, n=6, m=12, dmax_tol=1e-3):
			"create some intiatial attributes..."
			self.r0 = r0;         
			self.d0 = d0
			self.n = n
			self.m = m
			self.dmax = self.fCalDmax(dmax_tol)
			self.name = 'RATIONAL'
			
		## Compute SW
		def Evaluate(self, x):
			"""Input x can be a scalar or a 1d numpy ndarray"""
			# check x >=0
			if np.any(x<0): raise Exception("exist x < 0, Inputs must be >= 0")  
			# Compute SW
			r0 = self.r0;   d0 = self.d0;  n = self.n;   m = self.m
			#-- Check If input is not a single value
			if type(x) != int and type(x) != float:
				x = np.asarray(x)
				f = np.zeros(len(x));   df =np.zeros(len(x))
				u = np.zeros(len(x));  du = np.zeros(len(x));   v = np.zeros(len(x));   dv = np.zeros(len(x))
			#-- compute f			
			u = 1-((x-d0)/r0)**n   ;  du = -(n*(x-d0)**(n-1))/r0**n
			v = 1-((x-d0)/r0)**m   ;  dv = -(m*(x-d0)**(m-1))/r0**m
			#--
			f = u/v
			df = (du*v-dv*u)/(v*v)

			# Output
			return f, df
			#-------

		## compute dmax
		def fCalDmax(self, dmax_tol):
			x = np.linspace(0, 300, num=int(300/0.001))
			f,_ = self.Evaluate(x)
			index = np.where(f<dmax_tol)[0][0]     # find which index that f<dtol
			dmax=x[index]
			#--
			return dmax
	##----------------------------------------------------------------##

	class HEAVISIDE:
		def __init__(self, r0):
			"create some intiatial attributes..." 
			self.r0 = r0;   self.d0 = r0;     self.dmax = r0
			self.name = 'HEAVISIDE'

		## Compute SW
		def Evaluate(self, x):
			r0 = self.r0
			#-- Check If input is not a single value
			if type(x) != int and type(x) != float:
				x = np.asarray(x)
				f = np.zeros(len(x));   df =np.zeros(len(x))
				#-- compute f			
				f[(x<= r0)] = 1     # check elements <= r0
				f[(x > r0)] = 0     # check elements <= r0
				df[:] = 0
			else:
				if x<= r0: f=1
				if x > r0: f=0
				df = 0

			#-- Output
			return f, df
	##----------------------------------------------------------------##

	class CUBIC:
		def __init__(self, d0, dmax):
			"create some intiatial attributes..."       
			self.d0 = d0
			self.dmax = dmax
			self.name = 'CUBIC'

		## Compute SW
		def Evaluate(self, x):
			d0 = self.d0 ;    dmax = self.dmax
			#-- Check If input is not a single value
			if type(x) != int and type(x) != float:
				x = np.asarray(x)
				f = np.zeros(x.size);   df =np.zeros(x.size)
				##-- compute f	
				f[(x<d0)]= 1;   df[(x<d0)] = 0	
				f[(x>dmax)]= 0;   df[(x>dmax)] = 0	
				#--
				x1 = x[((x>=d0) & (x<=dmax))]
				y = (x1-d0)/(dmax-d0);       dy = 1/(dmax-d0)
				f[((x>=d0) & (x<=dmax))] = ((y-1)**2)*(1+2*y)
				df[((x>=d0) & (x<=dmax))] = (2*(y-1)*(1+2*y) + 2*(y-1)**2)*dy
	
			else:  #-- Check If input is a single value
				if x<d0:		
					f= 1;   df = 0	
				if x>dmax:
					f= 0;   df = 0	
				if x>=d0 and x<=dmax:
					x1 = x
					y = (x1-d0)/(dmax-d0);       dy = 1/(dmax-d0)
					f = ((y-1)**2)*(1+2*y)
					df = (2*(y-1)*(1+2*y) + 2*(y-1)**2)*dy

			#-- Output
			return f, df

		##--------
			# for i, elem in enumerate(x):
			# 	if elem<=d0: 
			# 		f[i] = 1;   df[i] = 0		
			# 	elif elem>d0 and elem<dmax:
			# 		y = (elem-d0)/(dmax-d0)
			# 		f[i] = ((y-1)**2)*(1+2*y)
			# 		#-- 
			# 		dy = 1/(dmax-d0)
			# 		df[i] = (2*(y-1)*(1+2*y) + 2*(y-1)**2)*dy
			# 	else: 
			# 		f[i] = 0;   df[i] = 0		
			# #--
		
	##-------------------------- end Child Class -----------------------------##

	class SMAP:
		def __init__(self, r0, a=8, b=8, d0=0, tol=1e-4):
			"create some intiatial attributes..."   
			self.name = 'SMAP' 
			self.a = a
			self.b = b
			self.d0 = d0
			self.r0 = r0
			
		## Compute SW
		def Evaluate(self, x):
			d0 = self.d0 ;    r0 = self.r0;   a = self.a;    b = self.b
			#-- Check If input is not a single value
			if type(x) != int and type(x) != float:
				x = np.asarray(x)
				f = np.zeros(x.size);   df =np.zeros(x.size)
			#-- compute f
			f = ( 1 + (2**(a/b)-1)* (((x-d0)/r0)**a)  )**(-b/a)	
			df = (-b/a)* (1 + (2**(a/b)-1)*((x-d0)/r0)**a)**(-b/a-1) *(a/r0**a) *(x-d0)**(a-1)
			#--
			return f, df

		## Find dmax
		def findDmax(self, tol=None, DmaxBound=100, gridSize=1e-4):
			if tol==None: tol = self.tol
			else: tol = tol
			r0 = self.r0
			#--
			x = np.linspace(r0, DmaxBound, num=int( (DmaxBound-r0)/gridSize))
			f,_ = self.Evaluate(x)
			#--find limits
			findMax = np.where(f<tol)[0]
			if len(findMax)!=0: 
				indexMAX = findMax[0]  
				Dmax=x[indexMAX]                
			else:                 #   raise Exception("Please Inscrease DmaxBound") 
				tmp = f[-1]; rep=0
				while tmp > tol:
					rep = rep+1
					x = np.linspace(DmaxBound*rep, DmaxBound*(rep+1), num=int( (DmaxBound-r0)/gridSize))
					f,_ = self.Evaluate(x)
					findMax = np.where(f<tol)[0]
					if len(findMax)!=0: 
						indexMAX = findMax[0]  
						Dmax=x[indexMAX] 
					else: tmp = f[-1]
			#--
			return Dmax

		def findDmin(self, tol=None, DminBound=None, gridSize=1e-4):
			if tol==None: tol = self.tol
			else: tol = tol
			if DminBound==None: DminBound = self.d0
			else: DminBound = DminBound
			r0 = self.r0
			#--
			x = np.linspace(DminBound, r0, num=int( (r0-DminBound)/gridSize))
			f,_ = self.Evaluate(x)
			#--find limits
			indexMIN= np.where(f>(1-tol))[0][-1]     # find which index that f<dtol
			Dmin=x[indexMIN]
			#--
			return Dmin
		##--------

	##-------------------------- end Child Class -----------------------------##
### =======================  End Class  ========================================
