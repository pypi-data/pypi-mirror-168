import numpy as np
import pandas as pd
from numpy.linalg import norm



def dist2_point2points(point, points):
	"""Compute bond_len and postion_vetors from 1 point to a list of points

	Args:
		point (list/array): coordinate of 1 point.
		points (2d-list/2d-array): list of coordinates of points/point.

	Returns:
		df (pd.DataFrame): pd.DataFrame constains distance and component of connecting vectors.
	"""
	## inputs
	point = np.asarray(point);  points = np.asarray(points)
	## compute
	d = points - point                                  # Nx3 array of Rij postion_vetors
	dist2 = np.sqrt(np.einsum('ij,ij->i', d, d))      # Nx1 array of distances
	## Out a df
	df = pd.DataFrame(np.column_stack((dist2,d)), columns=['bond_len','bx','by','bz'])
	return df
	##--------



def dist2_points2line(points, line=[(0,0,0), (0,0,0)]):
	"""Compute bond_len and postion_vetors from 1 point to a list of points
	Ref: https://stackoverflow.com/questions/39840030/distance-between-point-and-a-line-from-two-points

	Args:
		points (list/array/DataFrame: list of coordinates of points/point.
		line (2d-list/2d-array): contains coordinates to define a line.

	Returns:
		d (float/list): distances between points and a line.
	"""
	## refine input
	if isinstance(points, pd.DataFrame):
		points = points[['x','y','z']].values
	if isinstance(points, list) or isinstance(points, np.ndarray):
		points = np.asarray(points)

	line = np.asarray(line)
	if line.ndim!=2:
		raise ValueError('Line must be defined in 2d dimensions array.')
	## assume a line formed by p1 and p2
	p1 = line[0,:]
	p2 = line[1,:]
	cr = np.cross(p2-p1,points-p1)/norm(p2-p1)
	if points.ndim<2:
		d = norm(cr)
	else:
		d = [norm(item) for item in cr.tolist()]
	return d


def closest_points2line(points, line=[(0,0,0), (0,0,0)], distance=0, Xbound=None, Ybound=None, Zbound=None):
	"""Find all points locate inside a checkin-distance "dist" from a line.

	Args:
		points (list/array): list of coordinates of points/point.
		line (2d-list/2d-array) = [[x1,y1,z1], [x1,y2,z2]]: contains coordinates to define a line.
		distance (float): the checkin-distance.
		Xbound, Ybound, Zbound (tuple) : define the boundaries for checking.
			Xbound='line': use the lengths of lines as bounds.
			Xbound=None: extend to INF.
			Xbound = (xlo, xhi)

	Returns:
		ds_idx (Series): Series of indices of points within the checkin-distance
	"""
	## refine input
	if isinstance(points, pd.DataFrame): df = points
	if isinstance(points, list):         df = pd.DataFrame(points, columns=['x','y','z'] )
	if isinstance(points, np.ndarray):   df = pd.DataFrame(points.tolist(), columns=['x','y','z'] )
	if 'idx' not in df.columns.tolist():
		df['idx'] = np.arange(df.shape[0])
	df['near_point'] = 0               # 'near_point' to remark a point is near the line or not.

	line = np.asarray(line)
	if line.ndim!=2:
		raise ValueError('Line must be defined in 2d dimensions array.')

	if Xbound is None:
		Xbound = (-np.inf, np.inf)
	elif Xbound=='line':
		Xbound = ( min(line[:,0]),  max(line[:,0]) )

	if Ybound is None:
		Ybound = (-np.inf, np.inf)
	elif Ybound=='line':
		Ybound = ( min(line[:,1]),  max(line[:,1]) )

	if Zbound is None:
		Zbound = (-np.inf, np.inf)
	elif Zbound=='line':
		Zbound = ( min(line[:,2]), max(line[:,2]) )

	##
	df['d'] = dist2_points2line(points, line)
	for i,row in df.iterrows():
		if row['d']<=distance:
			cond = True
			if Xbound is not None:
				cond = cond and (Xbound[0] <= df.at[i,'x']) and (df.at[i,'x'] <= Xbound[1])
			if Ybound is not None:
				cond = cond and (Ybound[0] <= df.at[i,'y']) and (df.at[i,'y'] <= Ybound[1])
			if Zbound is not None:
				cond = cond and (Zbound[0] <= df.at[i,'z']) and (df.at[i,'z'] <= Zbound[1])

			if cond:
				df.at[i,'near_point'] = 1

	ds_idx = df[df['near_point']==1]['idx']
	return ds_idx


def closest_points2multilines(points, multilines=[], distance=0, Xbound=None, Ybound=None, Zbound=None):
	"""Find all points locate inside a checkin-distance "dist" from multilines.
	The Bound is set as the line-lengths.

	Args:
		points (list/array): list of coordinates of points/point.
		multilines (list): list of pair-points, each pair-point contains coordinates of 2 points to define a line used in 'closest_points2line'.
		distance (float): the checkin-distance.

	Returns:
		ds_idx (Series): Series of indices of points within the checkin-distance
	"""
	if not isinstance(multilines,list):
		raise ValueError('multilines param must be a list of pair-points, each pair-point contains coordinates of 2 points to define a line')

	ds_idx = pd.Series(name='idx')
	for line in multilines:
		newidx = closest_points2line(points, line, distance, Xbound, Ybound, Zbound)
		pd.concat([ds_idx,newidx])

	ds_idx.drop_duplicates(inplace=True)  # remove duplicates
	return ds_idx