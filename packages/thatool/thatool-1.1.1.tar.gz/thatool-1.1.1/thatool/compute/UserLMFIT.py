







		




### ============================================================================
### Library of Curves
### ============================================================================
class UserLMFIT:   
	"""The class contains set of objective function of fitting use by LMFIT package
	NOTEs: 
	- defined function followed the convection of LMFIT: the first argument of the function is taken 
	as the independent variable, held in independent_vars, and the rest of the functions positional 
	arguments (and, in certain cases, keyword arguments – see below) are used for Parameter names.
	https://lmfit.github.io/lmfit-py/model.html
	- This Class defines curve-forms that are not vailable in LMFIT's built-in models

	* Attributes:
		swType       : (default='RATIONAL') Type of witching function, 
		r0, d0       : The r_0 parameter of the switching function
		
	* Methods:
		fFunc    : compute & return value and derivation of sw function
		fDmax    : estimate value of Dmax
		
	Ex: func = thaTool.CurveLib.Linear(x)
	"""
	# def __init__(self):
	# 	return
		
	### ========================================================================		
	## Define Some basic Functions
	def Linear(x, a0, a1):   
		"this func is available in LMFIT, just play as an example here"
		return a0 + a1*x
	##-----

	def inverseTemperature(x,a,b):
		return a*np.exp(-b/x)
	##-----
 
	def ExpDecay(x,A,lambd):
		return A*np.exp(-lambd*x)
	##-----

	def sizeEffect(x,a,b):
		"system size-dependence on term N^(2/3"
		return a*x**(b*2/3)
	##-----

	### ========================================================================
	### Define unNormalize vs Normalize Gaussian
	def unNormalGaussian(x, amp, cen, sig):
		"The unNormalize Gaussian function"   
		x = np.asarray(x)
		y = amp*np.exp(-(x-cen)**2 / (2.*sig**2))
		return y
	##-----
	
	def NormalGaussian(x, amp, cen, sig):
		"The Normalize Gaussian function"   
		x = np.asarray(x)
		y = (amp/np.sqrt(2*np.pi*sig**2)) *np.exp(-(x-cen)**2 / (2.*sig**2))
		return y
	##-----
	
	### Define sum of unNormalize Gaussian    
	def sum_2unNormalGaussian(x,amp1,amp2,cen1,cen2,sig1,sig2):
		"The sum of 2 Gaussian function"   
		x = np.asarray(x)
		y = amp1*np.exp(-(x-cen1)**2 / (2.*sig1**2))  + amp2*np.exp(-(x-cen2)**2 / (2.*sig2**2))
		return y
	##-----

	def sum_3unNormalGaussian(x,amp1,amp2,amp3,cen1,cen2,cen3,sig1,sig2,sig3):
		"The sum of 3 Gaussian function"   
		x = np.asarray(x)
		y = amp1*np.exp(-(x-cen1)**2 / (2.*sig1**2))  + amp2*np.exp(-(x-cen2)**2 / (2.*sig2**2)) \
			+ amp3*np.exp(-(x-cen3)**2 / (2.*sig3**2))
		return y
	##-----

	def sum_4unNormalGaussian(x,amp1,amp2,amp3,amp4,cen1,cen2,cen3,cen4,sig1,sig2,sig3,sig4):
		"The sum of 4 Gaussian function"   
		x = np.asarray(x)
		y = amp1*np.exp(-(x-cen1)**2 / (2.*sig1**2))  + amp2*np.exp(-(x-cen2)**2 / (2.*sig2**2)) \
			+ amp3*np.exp(-(x-cen3)**2 / (2.*sig3**2))  + amp4*np.exp(-(x-cen4)**2 / (2.*sig4**2))
		return y
	##-----
   
	def sum_5unNormalGaussian(self,x,amp1,amp2,amp3,amp4,amp5,cen1,cen2,cen3,cen4,cen5,sig1,sig2,sig3,sig4,sig5):
		"The sum of 5 Gaussian function"   
		x = np.asarray(x)
		y = amp1*np.exp(-(x-cen1)**2 / (2.*sig1**2))  + amp2*np.exp(-(x-cen2)**2 / (2.*sig2**2)) \
			+ amp3*np.exp(-(x-cen3)**2 / (2.*sig3**2))  + amp4*np.exp(-(x-cen4)**2 / (2.*sig4**2)) \
			+ amp5*np.exp(-(x-cen5)**2 / (2.*sig5**2))
		return y
	##-----

	### Define sum of Normalize Gaussian
	def sum_2NormalGaussian(x,amp1,amp2,cen1,cen2,sig1,sig2):
		"The sum of 2 Gaussian function"   
		x = np.asarray(x)
		y = (amp1/np.sqrt(2*np.pi*sig1**2)) *np.exp(-(x-cen1)**2 / (2.*sig1**2)) \
			  + (amp2/np.sqrt(2*np.pi*sig2**2)) *np.exp(-(x-cen2)**2 / (2.*sig2**2)) 
		return y
	##-----

	def sum_3NormalGaussian(x,amp1,amp2,amp3,cen1,cen2,cen3,sig1,sig2,sig3):
		"The sum of 3 Gaussian function"   
		x = np.asarray(x)
		y = (amp1/np.sqrt(2*np.pi*sig1**2)) *np.exp(-(x-cen1)**2 / (2.*sig1**2)) \
			  + (amp2/np.sqrt(2*np.pi*sig2**2)) *np.exp(-(x-cen2)**2 / (2.*sig2**2)) \
			 + (amp3/np.sqrt(2*np.pi*sig3**2)) *np.exp(-(x-cen3)**2 / (2.*sig3**2)) 
		return y
	##-----

	def sum_4NormalGaussian(x,amp1,amp2,amp3,amp4,cen1,cen2,cen3,cen4,sig1,sig2,sig3,sig4):
		"The sum of 4 Gaussian function"   
		x = np.asarray(x)
		y = (amp1/np.sqrt(2*np.pi*sig1**2)) *np.exp(-(x-cen1)**2 / (2.*sig1**2)) \
			  + (amp2/np.sqrt(2*np.pi*sig2**2)) *np.exp(-(x-cen2)**2 / (2.*sig2**2)) \
			 + (amp3/np.sqrt(2*np.pi*sig3**2)) *np.exp(-(x-cen3)**2 / (2.*sig3**2)) \
			+ (amp4/np.sqrt(2*np.pi*sig4**2)) *np.exp(-(x-cen4)**2 / (2.*sig4**2)) 
		return y
	##-----
   
	def sum_5NormalGaussian(x,amp1,amp2,amp3,amp4,amp5,cen1,cen2,cen3,cen4,cen5,sig1,sig2,sig3,sig4,sig5):
		"The sum of 5 Gaussian function"   
		x = np.asarray(x)
		y = (amp1/np.sqrt(2*np.pi*sig1**2)) *np.exp(-(x-cen1)**2 / (2.*sig1**2)) \
			  + (amp2/np.sqrt(2*np.pi*sig2**2)) *np.exp(-(x-cen2)**2 / (2.*sig2**2)) \
			 + (amp3/np.sqrt(2*np.pi*sig3**2)) *np.exp(-(x-cen3)**2 / (2.*sig3**2)) \
			+ (amp4/np.sqrt(2*np.pi*sig4**2)) *np.exp(-(x-cen4)**2 / (2.*sig4**2)) \
			+ (amp5/np.sqrt(2*np.pi*sig5**2)) *np.exp(-(x-cen5)**2 / (2.*sig5**2)) 
		return y
	##-----



	### ========================================================================
	### Some general curve             
	def DoseResp(x, A1=-3.3, A2=-2.9, LOGx0=480000, p=1.2):
		"""Dose-response curve with variable Hill slope given by parameter 'p'.
		Origin's Category: Pharmacology 
		* Params:
				Names=A1,A2,LOGx0,p
				Meanings=bottom asymptote,top asymptote, center, hill slope
		Initiate params: pars = mod.make_params(A1=-3.3, A2=-2.9, LOGx0=480000, p=1.2)
		""" 
		x = np.asarray(x)
		##--
		y = A1 + (A2-A1)/(1 + 10^((LOGx0-x)*p))
		return y
	##-----

	def BiDoseResp(x, A1=-3.3, A2=-2.9, LOGx01=175000, LOGx02=480000, h1=0.1, h2=0.2, p=0.5):
		"""Biphasic Dose Response Function, 
		Origin's Category: Pharmacology 
		* Params:
				Names=A1, A2, LOGx01, LOGx02, h1, h2, p
				Meanings=Bottom, Top, 1st EC50, 2nd EC50, slope1, slope2, proportion
		Initiate params: pars = mod.make_params(A1=0, A2=100, LOGx01=-8, LOGx02=-4, h1=0.8, h2=1.2, p=0.5)
		""" 
		x = np.asarray(x)
		##--
		span = A2 - A1
		Section1 = span*p/(1+np.power(10,(LOGx01-x)*h1))
		Section2 = span* (1-p)/(1+np.power(10,(LOGx02-x)*h2))
		y = A1 + Section1 +Section2
		return y
	##-----
	
	def Carreau(x, A1=60, A2=3, t=3.0, a=2.2, n=0.3):
		"""Carreau-Yasuda model to describe pseudoplastic flow with asymptotic viscosities at zero and infinite shear rates
		Origin's Category: Rheology
		* Params:
				Names = A1,A2,t,a,n    >0         (lower bound)
				Meanings = zero shear viscosity,infinite shear viscosity,time constant,transition control factor,power index
		Initiate params: pars = mod.make_params(A1=-3.3, A2=-2.9, t=2.0, a=2.2, n=0.2)
		""" 
		## Set Constraints on params

		##--
		x = np.asarray(x)
		##--
		temp = 1 + np.power(t*x, a)
		exponent = (n-1)/a
		y = A2 + (A1 - A2) * np.power( temp, exponent )
		return y
	##-----

	def Cross(x, A1=0.1, A2=3, t=1000, m=0.9):
		"""Cross model to describe pseudoplastic flow with asymptotic viscosities at zero and infinite shear rates
		Origin's Category: Rheology 
		* Params:
				Names = A1,A2,t,m      >0         (lower bound)
				Meanings = zero shear viscosity,infinite shear viscosity,time constant,power index
		Initiate params: pars = mod.make_params(A1=0.1, A2=3, t=1000, m=0.9)
		""" 
		x = np.asarray(x)
		##--
		temp = 1 + np.power(t*x, m)
		y = A2 + (A1 - A2)/temp
		return y
	##-----

	def GammaCFD(x, y0,A1,a,b):
		"""Gamma cumulative distribution function
		Origin's Category: Statistics
		* Params:
				Names = y0,A1,a,b          (A1,a,b >0)
				Meanings = Offset,Amplitude,Shape,Scale
		Initiate params: pars = mod.make_params(A1=0.1, A2=3, t=1000, m=0.9)
		""" 
		from scipy import stats
		##--
		x = np.asarray(x)
		##--
		y=y0+A1*stats.gamma.cdf( x, a, b )
		return y
	##-----

### =======================  End Class  ========================================




