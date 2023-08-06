import 	numpy  as np
import 	pandas as pd
from 	lmfit  import models               # load built-in models

def find_slope(points):
	"""Compute slope of a linear relation

	Args:
		points (array/DataFram/list): 2d array, contains XY data.

	Return:
		slope (float): the slope to linear relation
		model_fit (Obj): An object of lmfit, the fitted of linear model.
	"""
	## refine input
	if isinstance(points, pd.DataFrame):
		df = points.copy()
		df.columns = ['x','y']
	if isinstance(points, list):
		df = pd.DataFrame(points, columns=['x','y'] )
	if isinstance(points, np.ndarray):
		df = pd.DataFrame(points.tolist(), columns=['x','y'] )

	if df.shape[0]<2:
		raise ValueError("Number of input points is too small for reasonable fitting, please increase data")

	## fitting
	x1, y1 = df['x'], df['y']
	model = models.LinearModel()             # PolynomialModel(1)
	model_fit = model.fit(y1, model.guess(y1,x=x1), x=x1)
	slope = model_fit.best_values['slope']

	return slope, model_fit

