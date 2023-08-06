#coding=utf-8
from datetime import datetime
import platform
import numpy as np
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import csv











def create_readme( author = 'Mário Popolin Neto (mariopopolin@gmail.com)', msg = '', folder = './' ):


	writer = open( folder + 'README.txt', 'w' )
	separator = '-----------------------------------\n\n\n'

	
	writer.write( 'Author: ' + author + '\n' )
	now = datetime.now()
	writer.write( now.strftime( '%d/%m/%Y %H:%M:%S' ) + '\n\n' )
	writer.write( 'This project can not be used without its author\'s full and express authorization.\n' )
	writer.write( 'Este projeto não pode ser utilizado sem a completa e expressa autorização de seu autor.\n' )
	writer.write( separator )

	
	if msg != '':
		writer.write( msg + '\n' )
		writer.write( separator )

	
	writer.write( 'System: ' + platform.system() + '\n' )
	writer.write( 'Processor: ' + platform.processor() + '\n' )
	writer.write( 'Python Version: ' + platform.python_version() + '\n' )
	writer.write( 'Python Implementation: ' + platform.python_implementation() + '\n' )
	writer.write( separator )

	
	writer.write( 'Python Packages (pip freeze):\n\n' )

	try:
	    from pip._internal.operations import freeze
	except ImportError:  # pip < 10.0
	    from pip.operations import freeze

	for p in freeze.freeze():
		writer.write( p  + '\n' )

	writer.write( separator )


	writer.close()











def txtfiles_comparator( folder = './', extension = None, threshold = 0.95, hide_file_name = False ):

	# https://stackoverflow.com/questions/8897593/how-to-compute-the-similarity-between-two-text-documents


	documents = []
	header = [ ]
	count = 1
	meta_data = []


	for path, subdirs, files in os.walk(folder):
	    for name in files:

	    	add = True
	    	if ( extension is not None ):
	    		if( name.split('.')[ -1 ].lower() != extension.lower() ): add = False

	    	if add == True:

		    	file = os.path.join( path, name )

		    	header.append( 'f' + str(count) )
		    	meta_data.append( [ count, file ] )
		    	documents.append( open( file, errors = 'ignore' ).read()  )

		    	count = count + 1


	tfidf = TfidfVectorizer().fit_transform( documents )
	pairwise_similarity = tfidf * tfidf.T


	files_similarity_matrix = pairwise_similarity.toarray()
	np.fill_diagonal( files_similarity_matrix, 0 )


	meta_data = np.array( meta_data )


	with open( 'files_similarity_matrix-meta_data.csv', 'w' ) as csvfile:
		writer = csv.writer( csvfile, delimiter = ';' )
		writer.writerows( meta_data )
		csvfile.close()

	
	with open( 'files_similarity_matrix.csv', 'w' ) as csvfile:
		writer = csv.writer( csvfile, delimiter = ';' )

		
		row = [ '-' ]

		if hide_file_name == True:
			row.extend( header )
			rows_labels = np.array( [ header ] )
		else: 
			row.extend( meta_data[ :, 1 ].tolist() )
			rows_labels = np.array( [ meta_data[ :, 1 ] ] )

		writer.writerow( row )
		
		
		data = np.hstack( ( rows_labels.T, files_similarity_matrix ) )
		
		writer.writerows( data )
		csvfile.close()

	
	with open( 'files_similarity_matrix-above_threshold.csv', 'w' ) as csvfile:
		writer = csv.writer( csvfile, delimiter = ';' )

		indexes = np.argwhere( files_similarity_matrix >= threshold )

		for i in range( indexes.shape[ 0 ] ):
			
			if hide_file_name == True:
				writer.writerow( [ header[ indexes[ i, 0 ] ], header[ indexes[ i, 1 ] ], files_similarity_matrix[ indexes[ i, 0 ], indexes[ i, 1 ] ] ] )
			else:
				writer.writerow( [ meta_data[ indexes[ i, 0 ], 1 ], meta_data[ indexes[ i, 1 ], 1 ], files_similarity_matrix[ indexes[ i, 0 ], indexes[ i, 1 ] ] ] )

		csvfile.close()