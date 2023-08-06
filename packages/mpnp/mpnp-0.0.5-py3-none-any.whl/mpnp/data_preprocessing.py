#coding=utf-8
import numpy as np











# Papers Based

# 2014 Regression as Classification. Raied Salman and Vojislav Kecman.


def v_discretization( y, bins = 3 ):


	ndim = y.ndim
	if ndim > 1: ndim = y.shape[ 1 ]


	hists = []
	count = [ 0 ] * bins
	mat_count = []



	if ndim == 1: 
		hists.append( np.histogram( y, bins = bins ) )
		mat_count.append( count )
	else:
		for j in range( ndim ):
			hists.append( np.histogram( y[ :, j ], bins = bins ) )
			mat_count.append( count )

	mat_count = np.array( mat_count )



	mat = []

	for i in range( y.shape[ 0 ] ):

		row = [ -1 ] * ndim

		for j in range( ndim ): 
			
			for b in range( bins ):

				if ndim == 1: y_ij = y[ i ]
				else: y_ij = y[ i, j ]

				if ( y_ij >= hists[ j ][ 1 ][ b ] ) and ( ( y_ij < hists[ j ][ 1 ][ b + 1 ] ) or ( b == bins - 1 ) ):

					mat_count[ j, b ] += 1
					row[ j ] = b
					break

		mat.append( row )

	mat = np.array( mat )



	result = True
	for j in range( ndim ):
		for r in ( hists[ j ][ 0 ] == mat_count[ j, : ] ):
			if r == False:
				result = False
				break
		if result == False: break

	if result == False: raise Exception('mat_count is not equal to the values of the histogram.')



	return mat, hists