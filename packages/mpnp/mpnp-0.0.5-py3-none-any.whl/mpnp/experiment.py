#coding=utf-8
import numpy as np
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
import math
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import sklearn.metrics as skm
import pandas as pd
import csv
import glob
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib import colors











# Papers Based

## In favor: 
# 2006 Bias in error estimation when using cross-validation for model selection. Sudhir Varma and Richard Simon.
# 2015 Performance-Estimation Properties of Cross-Validation-Based Protocols with Simultaneous Hyper-Parameter Optimization. Ioannis Tsamardinos and Amin Rakhshani.
## Arguing that is overzealous procedure:
# 2021 Nested cross-validation when selecting classifiers is overzealous for most practical applications. Jacques Wainer and Gavin Cawley.


def nkcv( X, y, k_outer, k_inner, model = 'DT', param_grid = None, scoring = 'accuracy', check_balance = True, n_jobs = None, verbose = 1, experiment_name = '', results_folder = './', random_state = None ):

	
	n_classes = np.unique( y ).shape[ 0 ]
	if n_classes == 2: experiment_name += '-BIN'
	elif n_classes > 2: experiment_name += '-MULTCLASS'


	experiment_name += '-NKCV-'


	### DATASET SPLIT

	if k_outer == 'loocv':

		k_outer = X.shape[ 0 ]

		cv_outer = KFold( n_splits = k_outer, shuffle = True, random_state = random_state )
		split_outer = cv_outer.split( X )

		experiment_name += str( k_outer ) + '_LOOCVx'

	else:

		if( is_allclasses( y, k_outer ) == False ):
			raise ValueError('k_outer must not be higher than the number of instances on each class.')

		cv_outer = StratifiedKFold( n_splits = k_outer, shuffle = True, random_state = random_state )
		split_outer = cv_outer.split( X, y )

		experiment_name += str( k_outer ) + 'x'



	if k_inner == 'loocv':

		if k_outer == 'loocv':

			k_inner = k_outer - 1

			cv_inner = KFold( n_splits = k_inner, shuffle = True, random_state = random_state )

		else:

			k_inner = math.floor( X.shape[ 0 ] - ( X.shape[ 0 ] / k_outer ) )

			cv_inner = KFold( n_splits = k_inner, shuffle = True, random_state = random_state )

		experiment_name += str( k_inner ) + '_LOOCV'


	elif k_inner == 'oob': # out-of-bag >> RF only

		## IMPORTANT: In the 'oob' case, RF model ( 'bootstrap = True' e 'oob_score = True' ) must be trained with all instances, and out-of-bag samples are used as test score, that is:
		# cv_inner = [ ( list( range( X_train.shape[ 0 ] ) ), [ 0 ] ) ] # 100% train and 1 "symbolic" test instance. The test instance is symbolic since oob score is used.

		## Papers Based:
		# 2009 Prediction of DNA-binding residues in proteins from amino acid sequences using a random forest model with a hybrid feature. Jiansheng Wu et. al.
		# 2014 Sequence-based predictor of ATP-binding residues using random forest and mRMR-IFS feature selection. Xin Ma and Xiao Sun.

		experiment_name += 'OOB'


	else:

		cv_inner = StratifiedKFold( n_splits = k_inner, shuffle = True, random_state = random_state )
		experiment_name += str( k_inner )


	if model == 'DT': experiment_name += '-DT'
	elif model == 'RF': experiment_name += '-RF'


	if verbose > 0:
		print( '---' ) 
		print( 'experiment_name', experiment_name, '\n' )






	### SET PARAM GRID

	if ( param_grid is None ): param_grid = [ { } ]

	external_max_depth = True
	if 'max_depth' not in param_grid[ 0 ]: external_max_depth = False

	balance = None
	if 'class_weight' in param_grid[ 0 ]:

		balance = param_grid[ 0 ][ 'class_weight' ][ 0 ]

	elif check_balance == True:

		if ( is_balanced( y ) == False ): balance = 'balanced'

	param_grid = set_param_grid( X, y, model, k_inner, balance, param_grid, random_state )
	if verbose > 0: print( 'param_grid', param_grid )







	### NESTED KFOLD CROSS-VALIDATION FOR ERROR ESTIMATE


	if verbose > 0: print( '\n## KCV x KCV -- Performance Estimation' )


	outer_results = []

	outer_results_accuracy = []
	outer_results_f1 = []
	outer_results_precision = []
	outer_results_recall = [] # a.k.a. sensitivity
	outer_results_specificity = []

	k = 0
	for train_indexes, test_indexes in split_outer:


		if verbose > 0: print( '\nk_outer', k + 1 )


		# print( "TRAIN:", train_indexes, "TEST:", test_indexes )
		# print( "TRAIN:", y[ train_indexes ], "TEST:", y[ test_indexes ] )


		X_train, X_test = X[ train_indexes, : ], X[ test_indexes, : ]
		y_train, y_test = y[ train_indexes ], y[ test_indexes ]



		if external_max_depth == False: 

			max_depth = [ None ]  # int, default=None

			## Paper based:
			# The max_depth upperbound is based on a tree over X and y followwing: https://scikit-learn.org/stable/auto_examples/tree/plot_cost_complexity_pruning.html#sphx-glr-auto-examples-tree-plot-cost-complexity-pruning-py

			max_depth_value = DecisionTreeClassifier( criterion = param_grid[ 0 ][ 'criterion' ][ 0 ], splitter = 'best', max_depth = None, min_samples_split = 2, min_samples_leaf = 1, max_features = None, class_weight = balance, random_state = random_state ).fit( X_train, y_train ).tree_.max_depth
			max_depth.extend( list( range( 1, max_depth_value + 1 ) ) ) 
			# max_depth.extend( list( range( MIN, MAX + 1 ) ) ) # list( range( 5, 22 ) ) = [ 5, 6, ..., 20, 21 ]

			param_grid[ 0 ][ 'max_depth' ] = max_depth

		if verbose > 0: print( 'max_depth', param_grid[ 0 ][ 'max_depth' ] )


		
		if model == 'DT':

			search = GridSearchCV( DecisionTreeClassifier(), param_grid, scoring = scoring, n_jobs = n_jobs, refit = True, cv = cv_inner, verbose = verbose )

		elif model == 'RF':

			if k_inner == 'oob':

				cv_inner = [ ( list( range( X_train.shape[ 0 ] ) ), [ 0 ] ) ] 

				search = GridSearchCV( RandomForestClassifier(), param_grid, scoring = f_oob_score, n_jobs = n_jobs, refit = True, cv = cv_inner, verbose = verbose )

			else:

				search = GridSearchCV( RandomForestClassifier(), param_grid, scoring = scoring, n_jobs = n_jobs, refit = True, cv = cv_inner, verbose = verbose )

		search.fit( X_train, y_train )
		

		
		df = pd.DataFrame.from_dict( search.cv_results_ )
		df.to_csv( results_folder + experiment_name + '_results-k_outer' + str( k + 1 ) + '.csv', sep = ';' )


		best_model = search.best_estimator_
		y_pred = best_model.predict( X_test )


		if scoring == 'accuracy':
			score = skm.accuracy_score( y_test, y_pred )
		elif scoring == 'f1':
			score = skm.f1_score( y_test, y_pred )
		elif scoring == 'precision':
			score = skm.precision_score( y_test, y_pred )
		elif scoring == 'recall':
			score = skm.recall_score( y_test, y_pred ) # a.k.a. sensitivity

		outer_results.append( score )


		cm = skm.confusion_matrix( y_test, y_pred )
		if k == 0:

			with open( results_folder + experiment_name +  '_confusion-matrices.csv', 'w' ) as csvfile:
				writer = csv.writer( csvfile, delimiter = ';' )

				writer.writerow( [ "k outer " + str( k + 1 ) ] )

				writer.writerows( cm )

		else:

			with open( results_folder + experiment_name +  '_confusion-matrices.csv', 'a' ) as csvfile:
				writer = csv.writer( csvfile, delimiter = ';' )

				writer.writerow( [ "k outer " + str( k + 1 ) ] )

				writer.writerows( cm )
		
		outer_results_accuracy.append( skm.accuracy_score( y_test, y_pred ) )

		if n_classes == 2:

			outer_results_f1.append( skm.f1_score( y_test, y_pred ) )
			outer_results_precision.append( skm.precision_score( y_test, y_pred ) )
			outer_results_recall.append( skm.recall_score( y_test, y_pred ) ) # a.k.a. sensitivity

			## https://en.wikipedia.org/wiki/Sensitivity_and_specificity
			tn, fp, fn, tp = cm.ravel()
			outer_results_specificity.append( ( tn ) / ( tn + fp ) )

		elif n_classes > 2: 

			row = []
			row.append( skm.f1_score( y_test, y_pred, average = 'micro' ) )
			row.append( skm.f1_score( y_test, y_pred, average = 'macro' ) )
			row.append( skm.f1_score( y_test, y_pred, average = 'weighted' ) )
			outer_results_f1.append( row )

			row = []
			row.append( skm.precision_score( y_test, y_pred, average = 'micro' ) )
			row.append( skm.precision_score( y_test, y_pred, average = 'macro' ) )
			row.append( skm.precision_score( y_test, y_pred, average = 'weighted' ) )
			outer_results_precision.append( row )

			row = []
			row.append( skm.recall_score( y_test, y_pred, average = 'micro' ) )  # a.k.a. sensitivity
			row.append( skm.recall_score( y_test, y_pred, average = 'macro' ) )
			row.append( skm.recall_score( y_test, y_pred, average = 'weighted' ) )
			outer_results_recall.append( row )


		k += 1



	outer_results_accuracy = np.array( outer_results_accuracy )
	outer_results_f1 = np.array( outer_results_f1 )
	outer_results_precision = np.array( outer_results_precision )
	outer_results_recall = np.array( outer_results_recall )
	outer_results_specificity = np.array( outer_results_specificity )

	with open( results_folder + experiment_name +  '_confusion-matrices.csv', 'a' ) as csvfile:
		writer = csv.writer( csvfile, delimiter = ';' )

		writer.writerow( [ 'accuracy' ] )
		header	= [ 'k' + str( k + 1 ) for k in range( k_outer ) ]
		header.append( 'mean' )
		header.append( 'std' )
		writer.writerow( header )
		data = outer_results_accuracy.tolist()
		data.append( outer_results_accuracy.mean() )
		data.append( outer_results_accuracy.std() )
		writer.writerow( data )

		if n_classes == 2:

			writer.writerow( [ 'f1' ] )
			writer.writerow( header )
			data = outer_results_f1.tolist()
			data.append( outer_results_f1.mean() )
			data.append( outer_results_f1.std() )
			writer.writerow( data )

			writer.writerow( [ 'precision' ] )
			writer.writerow( header )
			data = outer_results_precision.tolist()
			data.append( outer_results_precision.mean() )
			data.append( outer_results_precision.std() )
			writer.writerow( data )

			writer.writerow( [ 'recall (a.k.a sensitivity)' ] )
			writer.writerow( header )
			data = outer_results_recall.tolist()
			data.append( outer_results_recall.mean() )
			data.append( outer_results_recall.std() )
			writer.writerow( data )

			writer.writerow( [ 'specificity' ] )
			writer.writerow( header )
			data = outer_results_specificity.tolist()
			data.append( outer_results_specificity.mean() )
			data.append( outer_results_specificity.std() )
			writer.writerow( data )

		elif n_classes > 2:

			writer.writerow( [ 'f1' ] )
			header = [ 'average' ]
			aux = [ 'k' + str( k + 1 ) for k in range( k_outer ) ]
			header.extend( aux )
			header.append( 'mean' )
			header.append( 'std' )
			writer.writerow( header )
			data = [ 'micro' ]
			data.extend( outer_results_f1[ :, 0 ].tolist() )
			data.append( outer_results_f1[ :, 0 ].mean() )
			data.append( outer_results_f1[ :, 0 ].std() )
			writer.writerow( data )
			data = [ 'macro' ]
			data.extend( outer_results_f1[ :, 1 ].tolist() )
			data.append( outer_results_f1[ :, 1 ].mean() )
			data.append( outer_results_f1[ :, 1 ].std() )
			writer.writerow( data )
			data = [ 'weighted' ]
			data.extend( outer_results_f1[ :, 2 ].tolist() )
			data.append( outer_results_f1[ :, 2 ].mean() )
			data.append( outer_results_f1[ :, 2 ].std() )
			writer.writerow( data )

			writer.writerow( [ 'precision' ] )
			writer.writerow( header )
			data = [ 'micro' ]
			data.extend( outer_results_precision[ :, 0 ].tolist() )
			data.append( outer_results_precision[ :, 0 ].mean() )
			data.append( outer_results_precision[ :, 0 ].std() )
			writer.writerow( data )
			data = [ 'macro' ]
			data.extend( outer_results_precision[ :, 1 ].tolist() )
			data.append( outer_results_precision[ :, 1 ].mean() )
			data.append( outer_results_precision[ :, 1 ].std() )
			writer.writerow( data )
			data = [ 'weighted' ]
			data.extend( outer_results_precision[ :, 2 ].tolist() )
			data.append( outer_results_precision[ :, 2 ].mean() )
			data.append( outer_results_precision[ :, 2 ].std() )
			writer.writerow( data )

			writer.writerow( [ 'recall (a.k.a sensitivity)' ] )
			writer.writerow( header )
			data = [ 'micro' ]
			data.extend( outer_results_recall[ :, 0 ].tolist() )
			data.append( outer_results_recall[ :, 0 ].mean() )
			data.append( outer_results_recall[ :, 0 ].std() )
			writer.writerow( data )
			data = [ 'macro' ]
			data.extend( outer_results_recall[ :, 1 ].tolist() )
			data.append( outer_results_recall[ :, 1 ].mean() )
			data.append( outer_results_recall[ :, 1 ].std() )
			writer.writerow( data )
			data = [ 'weighted' ]
			data.extend( outer_results_recall[ :, 2 ].tolist() )
			data.append( outer_results_recall[ :, 2 ].mean() )
			data.append( outer_results_recall[ :, 2 ].std() )
			writer.writerow( data )
			


	outer_results = np.array( outer_results )
	if verbose > 0: 
		print( '\nouter_results', outer_results )
		print( 'outer_results.mean()', outer_results.mean() )
		print( 'outer_results.std()', outer_results.std() )


	with open( results_folder + experiment_name +  '_errorestimate.csv', 'w' ) as csvfile:	
		writer = csv.writer( csvfile, delimiter = ';' )

		header	= [ 'k' + str( k + 1 ) for k in range( k_outer ) ]
		header.append( 'mean' )
		header.append( 'std' )
		writer.writerow( header )

		data = outer_results.tolist()
		data.append( outer_results.mean() )
		data.append( outer_results.std() )		
		writer.writerow( data )

		csvfile.close()





	###  KFOLD CROSS-VALIDATION FOR PARAM TUNING

	## cv_outer is used since the first split with k_outer tends to be more precise and 'oob' may be used in cv_inner.


	if verbose > 0: print( '\n## KCV -- Param Tuning' )


	if external_max_depth == False: 

		max_depth = [ None ]  # int, default=None

		## Paper based:
		# The max_depth upperbound is based on a tree over X and y followwing: https://scikit-learn.org/stable/auto_examples/tree/plot_cost_complexity_pruning.html#sphx-glr-auto-examples-tree-plot-cost-complexity-pruning-py

		max_depth_value = DecisionTreeClassifier( criterion = param_grid[ 0 ][ 'criterion' ][ 0 ], splitter = 'best', max_depth = None, min_samples_split = 2, min_samples_leaf = 1, max_features = None, class_weight = balance, random_state = random_state ).fit( X, y ).tree_.max_depth
		max_depth.extend( list( range( 1, max_depth_value + 1 ) ) ) 
		# max_depth.extend( list( range( MIN, MAX + 1 ) ) ) # list( range( 5, 22 ) ) = [ 5, 6, ..., 20, 21 ]

		param_grid[ 0 ][ 'max_depth' ] = max_depth

	if verbose > 0: print( '\nmax_depth', param_grid[ 0 ][ 'max_depth' ] )


	if model == 'DT':

		search = GridSearchCV( DecisionTreeClassifier(), param_grid, scoring = scoring, n_jobs = n_jobs, refit = False, cv = cv_outer, verbose = verbose )

	elif model == 'RF':

		if k_inner == 'oob':

			cv_outer = [ ( list( range( X_train.shape[ 0 ] ) ), [ 0 ] ) ] 

			search = GridSearchCV( RandomForestClassifier(), param_grid, scoring = f_oob_score, n_jobs = n_jobs, refit = False, cv = cv_outer, verbose = verbose )

		else:

			search = GridSearchCV( RandomForestClassifier(), param_grid, scoring = scoring, n_jobs = n_jobs, refit = False, cv = cv_outer, verbose = verbose )

	search.fit( X, y )


	df = pd.DataFrame.from_dict( search.cv_results_ )
	df.to_csv( results_folder + experiment_name + '_results.csv', sep = ';' )


	print( '---\n' )











## If param_grid changes the MPNP package must increase.

def set_param_grid( X, y, model, k_inner, balance, param_grid, random_state ):


	if 'criterion' not in param_grid[ 0 ]:
		criterion = [ 'gini' ] # {“gini”, “entropy”}, default=”gini”
		param_grid[ 0 ][ 'criterion' ] = criterion


	# # It was replaced to avoid data leakage.

	# if 'max_depth' not in param_grid[ 0 ]: 

	# 	max_depth = [ None ]  # int, default=None

	# 	## Paper based:
	# 	# The max_depth upperbound is based on a tree over X and y followwing: https://scikit-learn.org/stable/auto_examples/tree/plot_cost_complexity_pruning.html#sphx-glr-auto-examples-tree-plot-cost-complexity-pruning-py

	# 	max_depth_value = DecisionTreeClassifier( criterion = param_grid[ 0 ][ 'criterion' ][ 0 ], splitter = 'best', max_depth = None, min_samples_split = 2, min_samples_leaf = 1, max_features = None, random_state = random_state ).fit( X, y ).tree_.max_depth
	# 	max_depth.extend( list( range( 1, max_depth_value + 1 ) ) ) 
	# 	# max_depth.extend( list( range( MIN, MAX + 1 ) ) ) # list( range( 5, 22 ) ) = [ 5, 6, ..., 20, 21 ]

	# 	param_grid[ 0 ][ 'max_depth' ] = max_depth


	if 'min_samples_split' not in param_grid[ 0 ]: 
		min_samples_split = [ 2 ] # int or float, default=2
		param_grid[ 0 ][ 'min_samples_split' ] = min_samples_split


	if 'min_samples_leaf' not in param_grid[ 0 ]: 
		min_samples_leaf = [ 1 ] # min_samples_leafint or float, default=1
		param_grid[ 0 ][ 'min_samples_leaf' ] = min_samples_leaf


	if 'min_weight_fraction_leaf' not in param_grid[ 0 ]: 
		min_weight_fraction_leaf = [ 0.0 ] # min_weight_fraction_leaf
		param_grid[ 0 ][ 'min_weight_fraction_leaf' ] = min_weight_fraction_leaf


	if 'max_features' not in param_grid[ 0 ]:  # int, float or {“auto”, “sqrt”, “log2”}, default= 'None' for DT and 'auto' for RF

		max_features = [ None ]
		aux = []

		n = int( math.sqrt( X.shape[ 1 ] ) )
		if ( n != 0 ) and ( n not in aux ): 
			max_features.append( 'sqrt' )
			aux.append( n )

		n = int( math.log2( X.shape[ 1 ] ) )
		if ( n != 0 ) and ( n not in aux ): 
			max_features.append( 'log2' )
			aux.append( n )

		n = int( X.shape[ 1 ] * 0.2 )
		if ( n != 0 ) and ( n not in aux ): 
			max_features.append( 0.2 )
			aux.append( n )

		n = int( X.shape[ 1 ] * 0.5 )
		if ( n != 0 ) and ( n not in aux ): 
			max_features.append( 0.5 )
			aux.append( n )

		param_grid[ 0 ][ 'max_features' ] = max_features # The numbers 0.2 and 0.5 are taken of my head. ??


	random_state = [ random_state ] # int, RandomState instance or None, default=None
	param_grid[ 0 ][ 'random_state' ] = random_state


	if 'max_leaf_nodes' not in param_grid[ 0 ]: 
		max_leaf_nodes = [ None ] # int, default=None
		param_grid[ 0 ][ 'max_leaf_nodes' ] = max_leaf_nodes


	if 'min_impurity_decrease' not in param_grid[ 0 ]: 
		min_impurity_decrease = [ 0.0 ] # float, default=0.0
		param_grid[ 0 ][ 'min_impurity_decrease' ] = min_impurity_decrease


	if 'class_weight' not in param_grid[ 0 ]:

		class_weight = [ balance ] # dict, list of dict or “balanced”, default=None
		param_grid[ 0 ][ 'class_weight' ] = class_weight


	if 'ccp_alpha' not in param_grid[ 0 ]: 

		# path = DecisionTreeClassifier( max_depth = None, random_state = random_seed ).cost_complexity_pruning_path( X, y )
		# # The last value in ccp_alphas is the alpha value that prunes the whole tree, leaving the tree with one node. The maximum effective alpha value is removed, because it is the trivial tree with only one node.
		# # https://scikit-learn.org/stable/auto_examples/tree/plot_cost_complexity_pruning.html#sphx-glr-auto-examples-tree-plot-cost-complexity-pruning-py
		# ccp_alphas = path.ccp_alphas[ :-1 ]
		# param_grid[ 0 ][ 'ccp_alpha' ] = ccp_alphas.tolist()

		ccp_alpha = [ 0.0 ] # non-negative float, default=0.0
		param_grid[ 0 ][ 'ccp_alpha' ] = ccp_alpha	



	if model == 'DT':

		## Papers Based:
		# 2014 Parameter Optimization in Decision Tree Learning by using Simple Genetic Algorithms. Michel Camilleri. #  Max. depth of a tree, 
		# 2018 Tuning Hyperparameters of Decision Tree Classifiers Using Computationally Efficient Schemes. Wedad Alawad Mohamed Zohdy Debatosh Debnath. # Max. depth of a tree,
		# 2015 Efficient and Robust Automated Machine Learning - Auto-sklearn 1. # The number of parameters are shown but not explict.
		# 2015 Automatic problem-specific hyperparameter optimization and model selection for supervised machine learning: Technical Report. Roger Bermúdez-Chacón. # Max. number of features analyzed by split are illustrated but not explict used. 
		# 2019 An empirical study on hyperparameter tuning of decision tree. Rafael Gomes Mantovani. # Max. depth of a tree, Max. number of features analyzed by split ... # It is a reference (apud), but the original reference doest not make it clear.
		# 2021 Auto-Sklearn 2.0: Hands-free AutoML via Meta-Learning. Matthias Feurer. # Max. depth of a tree, 

		# criterion='gini', splitter='best', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=None, random_state=None, max_leaf_nodes=None, min_impurity_decrease=0.0, class_weight=None, ccp_alpha=0.0		


		if 'splitter' not in param_grid[ 0 ]: 
			splitter = [ 'best' ] # {“best”, “random”}, default=”best”
			param_grid[ 0 ][ 'splitter' ] = splitter		


	elif model == 'RF':

		## Papers Based:
		# 2015 Initializing Bayesian Hyperparameter Optimization via Meta-Learning. Matthias Feurer. # Max. number of features analyzed by split,
		# 2021 Nested cross-validation when selecting classifiers is overzealous for most practical applications. Jacques Wainer and Gavin Cawley. # Number of trees and number of features. 
		# 2019 Hyperparameters and tuning strategies for random forest. Philipp Probst. # Number of trees, Max. number of features analyzed by split, sample size and replacement, spltting rule, and node size ("similar" to Max. depth).
		# 2021 Auto-Sklearn 2.0: Hands-free AutoML via Meta-Learning. Matthias Feurer. # bootstrap = True and False.


		# n_estimators=100, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=None, min_impurity_decrease=0.0, bootstrap=True, oob_score=False, n_jobs=None, random_state=None, verbose=0, warm_start=False, class_weight=None, ccp_alpha=0.0, max_samples=None

		
		if 'n_estimators' not in param_grid[ 0 ]:

			## Paper Based:
			# 2012 How Many Trees in a Random Forest. Thais Mayumi Oshiro.

			# if k_inner == 'oob': n_estimators = [ 32, 64, 128, 256, 512, 1024, 2048, 4096 ] # int, default=100
			# else: n_estimators = [ 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096 ]
			n_estimators = [ 32, 64, 128, 256, 512, 1024, 2048, 4096 ] # It does not make sense to create RFs with fewer DTs

			param_grid[ 0 ][ 'n_estimators' ] = n_estimators


		if 'bootstrap' not in param_grid[ 0 ]:

			if k_inner == 'oob': bootstrap = [ True ] # bool, default=True
			else: bootstrap = [ True, False ] # [ True, False ] ??
 
			param_grid[ 0 ][ 'bootstrap' ] = bootstrap


		if 'oob_score' not in param_grid[ 0 ]: 
			
			if k_inner == 'oob': oob_score = [ True ] # bool, default=False
			else: oob_score = [ False ]

			param_grid[ 0 ][ 'oob_score' ] = oob_score


		if 'n_jobs' not in param_grid[ 0 ]: 
			n_jobs = [ None ] # int, default=None
			param_grid[ 0 ][ 'n_jobs' ] = n_jobs


		if 'verbose' not in param_grid[ 0 ]: 
			verbose = [ 0 ] # int, default=0
			param_grid[ 0 ][ 'verbose' ] = verbose


		if 'warm_start' not in param_grid[ 0 ]: 
			warm_start = [ False ] # bool, default=False
			param_grid[ 0 ][ 'warm_start' ] = warm_start


		if 'max_samples' not in param_grid[ 0 ]:

			max_samples = [ None, 0.7, 0.80, 0.90 ] # int or float, default=None # If bootstrap = False float numbers do not result in error # The numbers 0.7, 0.80, 0.90 are taken of my head. ??

			if ( len( param_grid[ 0 ][ 'bootstrap' ] ) == 1 ) and ( param_grid[ 0 ][ 'bootstrap' ][ 0 ] == False ):
				max_samples = [ None ]

			param_grid[ 0 ][ 'max_samples' ] = max_samples	


		
	return param_grid











def is_allclasses( y, k ):

	allclasses = True

	for c in np.unique( y ):

		if ( np.count_nonzero( y == c ) < k ):
			allclasses = False
			break

	return allclasses











def is_balanced( y ):

	balanced = True

	n = -1
	for c in np.unique( y ):

		if ( n == -1 ): n = np.count_nonzero( y == c )

		if ( n != np.count_nonzero( y == c ) ):

			balanced = False
			break

	if ( n == -1 ): balanced = False

	return balanced










def f_oob_score( estimator, X, y ):
    return estimator.oob_score_











def summarize_results( results_folder = './', fold_results = False, calc_ss_matrix = False, equal_var = True ):


	if calc_ss_matrix == True: fold_results = True


	files = glob.glob( results_folder + '*errorestimate.csv' )


	for i in range( len( files ) ):

		file = files[ i ]
		experiment = file.partition( '_errorestimate.csv' )[ 0 ].partition( results_folder )[ 2 ]

		results = np.genfromtxt( results_folder + experiment + '_results.csv', delimiter = ';', skip_header = 0, dtype = str )
		i_rank_1 = np.argwhere( results[ :, -1 ] == '1' )[ 0 ][ 0 ]
		i_params = np.argwhere( results[ 0, : ] == 'params' )[ 0 ][ 0 ]
		params = results[ i_rank_1, i_params ]

		with open( file, 'r' ) as reader:

			lines = reader.readlines()

			if i == 0: writer = open( results_folder + 'Summarized_Results.csv', 'w' )
			else: writer = open( results_folder + 'Summarized_Results.csv', 'a' )

			if fold_results == True: writer.write( experiment + ';' + lines[ 1 ].replace( '\n', '' ) + ';' + params + '\n' )
			else:

				values = lines[1].split(';')
				writer.write( experiment + ';' + values[ -2 ] + ';' + values[ -1 ].replace( '\n', '' ) + ';' + params + '\n' )

			writer.close()

	
	if calc_ss_matrix == True:

		

		# The T-test measures whether the average (expected) value differs significantly across samples. If we observe a large p-value, for example larger than 0.05 or 0.1, then we cannot reject the null hypothesis of identical average scores. If the p-value is smaller than the threshold, e.g. 1%, 5% or 10%, then we reject the null hypothesis of equal averages. [R1] Hence, with threshold = 0.05,

		# (A) p > 0.05 | ACCEPT the null hypothesis of identical average scores, MEANING NONE statistically significant difference.

		# (B) p < 0.05 | REJECT the null hypothesis of identical average scores, MEANING statistically significant DIFFERENCE.

		# In statistical hypothesis testing, a TYPE I error is the mistaken rejection of an actually true null hypothesis (also known as a "false positive" finding or conclusion; example: "an innocent person is convicted"), while a TYPE II error is the failure to reject a null hypothesis that is actually false (also known as a "false negative" finding or conclusion; example: "a guilty person is not convicted"). [R2]

		# The 10-fold cross-validated t-test has high type I error. However, it also has high power, and hence, it can be recommended in those cases where type II error (the failure to detect a real difference between algorithms) is more important. [R3]

		# Thus, with 10-fold cross-validated t-test, 

		# (A) p > 0.05 | NONE difference is RELIABLE, since type II error may be modest.

		# (B) p < 0.05 | DIFFERENCE is NOT reliable, since type I error is high.

		# Based on Occam's razor,

		# (C) Occam's razor can be interpreted in two ways, one favoring the simpler of two models with the same generalization error (expected performance on data not seen during training), because simplicity is a goal in itself [R4].

		# In  conclusion, for the case where the purpose is to choose a DT instead of an RF, based on (A) NONE statistically significant difference at mean accuracy and (C), the 10-fold cross-validated t-test IS USEFUL.

		# References

		# [R1] https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html

		# [R2] https://en.wikipedia.org/wiki/Type_I_and_type_II_errors

		# [R3] DIETTERICH, Thomas G. Approximate statistical tests for comparing supervised classification learning algorithms. Neural computation, v. 10, n. 7, p. 1895-1923, 1998.

		# [R4] DOMINGOS, Pedro. Occam's two razors: The sharp and the blunt. In: KDD. 1998. p. 37-43.

		

		summarized_results = np.genfromtxt( results_folder + 'Summarized_Results.csv', delimiter = ';', skip_header = 0, dtype = str )

		row = [ '(pvalue)' ]
		row.extend( summarized_results[ :, 0 ].tolist() )


		# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html
		# Calculate the T-test for the means of two independent samples of scores. This is a two-sided test for the null hypothesis that 2 independent samples have identical average (expected) values. This test assumes that the populations have identical variances by default.We can use this test, if we observe two independent samples from the same or different population, e.g. exam scores of boys and girls or of two ethnic groups. The test measures whether the average (expected) value differs significantly across samples. If we observe a large p-value, for example larger than 0.05 or 0.1, then we cannot reject the null hypothesis of identical average scores. If the p-value is smaller than the threshold, e.g. 1%, 5% or 10%, then we reject the null hypothesis of equal averages.


		# If equal_var is True (default), perform a standard independent 2 sample test that assumes equal population variances [1]. If False, perform Welch’s t-test, which does not assume equal population variance [2].

		# [1] https://en.wikipedia.org/wiki/T-test#Independent_two-sample_t-test
		# The t-test is any statistical hypothesis test in which the test statistic follows a Student's t-distribution under the null hypothesis.
		# A t-test is the most commonly applied when the test statistic would follow a normal distribution if the value of a scaling term in the test statistic were known. When the scaling term is unknown and is replaced by an estimate based on the data, the test statistics (under certain conditions) follow a Student's t distribution. The t-test can be used, for example, to determine if the means of two sets of data are significantly different from each other.

		# [2] https://en.wikipedia.org/wiki/Welch%27s_t-test
		# In statistics, Welch's t-test, or unequal variances t-test, is a two-sample location test which is used to test the hypothesis that two populations have equal means. It is named for its creator, Bernard Lewis Welch, is an adaptation of Student's t-test,[1] and is more reliable when the two samples have unequal variances and/or unequal sample sizes.[2][3] These tests are often referred to as "unpaired" or "independent samples" t-tests, as they are typically applied when the statistical units underlying the two samples being compared are non-overlapping.

		# Needs to be 'True' following the papers that bring the text "the paired Student’s t-test". So, equal_var = 'True' may be indicated to samples with same and paired size (KCV explements with one value for k), while equal_var = 'False' may be suggested to samples with different and unpaired sizes (KCV explements with different values for k).
		# equal_var = True or False


		with open( results_folder + 'Statistical_Significance_Matrix.csv', 'w' ) as csvfile:	
			writer = csv.writer( csvfile, delimiter = ';' )

			writer.writerow( row )

			for i in range( summarized_results.shape[ 0 ] ):

				row = [ summarized_results[ i, 0 ] ]

				for j in range( summarized_results.shape[ 0 ] ):

					pvalue = stats.ttest_ind( summarized_results[ i, 1:-2 ].astype( float ), summarized_results[ j, 1:-2 ].astype( float ), equal_var = equal_var )[ 1 ]
					row.append( pvalue )

				writer.writerow( row )

			csvfile.close()











def plot_ss_matrix( results_folder = './', file = 'Statistical_Significance_Matrix.csv', label_fontsize = 8, xlabels_rotation = -30, ylabels_rotation = 30, marging_left = 0.25, marging_bottom = 0.35, marging_right = 0.925, marging_top = 0.925):


	dataset = np.genfromtxt( results_folder + file, delimiter = ';', skip_header = 0, dtype = str )
	labels = dataset[ 0, 1: ]
	matrix = dataset[ 1:, 1: ].astype(float)


	cmap = colors.ListedColormap( [ '#4daf4a', '#984ea3' ] )
	bounds = [ 0, 0.05, 1 ]
	norm = colors.BoundaryNorm( bounds, cmap.N )


	plt.figure()


	plt.rcParams["figure.figsize"] = ( 16, 9 )
	img = plt.imshow( matrix, interpolation = 'nearest', aspect='auto', cmap = cmap, norm = norm)


	names = [ '<0.05', '>0.05' ]
	formatter = plt.FuncFormatter( lambda val, pos: names[ val ] )
	cbar = plt.colorbar( img,  ticks = [ 0, 1 ], format = formatter, shrink = 0.5 )
	cbar.ax.set_ylabel( 'p-value', rotation = -90, va = "bottom" )


	plt.xticks( np.arange( labels.shape[ 0 ] ), labels = labels, fontsize = label_fontsize, rotation = xlabels_rotation, ha = "left" )
	plt.yticks( np.arange( labels.shape[ 0 ] ), labels = labels, fontsize = label_fontsize, rotation = ylabels_rotation, ha = "right" )


	ax = plt.gca()

	ax.spines['left'].set_visible( False )
	ax.spines['right'].set_visible( False )
	ax.spines['top'].set_visible( False )
	ax.spines['bottom'].set_visible( False )

	ax.set_xticks( np.arange( matrix.shape[ 1 ] + 1 )-.5, minor = True )
	ax.set_yticks( np.arange( matrix.shape[ 0 ] + 1 )-.5, minor = True )

	ax.grid( which = "minor", color = "w", linestyle = '-', linewidth = 3 )


	plt.subplots_adjust( left = marging_left, bottom = marging_bottom, right = marging_right, top = marging_top )
	plt.savefig( fname = results_folder + 'Statistical_Significance_Matrix.png', dpi = 300 )











# checar pasta KFold Cross Validation quando se for implementar