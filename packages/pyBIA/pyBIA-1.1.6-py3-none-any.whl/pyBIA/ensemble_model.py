#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 8 10:04:23 2021

@author: daniel
"""
import os
import joblib 
import random
import itertools
import numpy as np
import matplotlib.pyplot as plt
plt.rc('font', family='serif')
from warnings import warn
from pathlib import Path
from collections import Counter  

from sklearn import decomposition
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, auc, RocCurveDisplay
from sklearn.model_selection import KFold, StratifiedKFold, train_test_split
from sklearn.manifold import TSNE

from pyBIA.optimization import hyper_opt, borutashap_opt, KNN_imputation, MissForest_imputation
from optuna.visualization.matplotlib import plot_optimization_history
from xgboost import XGBClassifier
import scikitplot as skplt

class Classifier:
    """
    Creates a machine learning classifier object.
    The built-in methods can be used to optimize the engine
    and output visualizations.

    Attributes:
        model (object): The machine learning model that is created
        
        imputer (object): The imputer created during model creation
        
        feats_to_use (ndarray): Array of indices containing the metrics
            that contribute to classification accuracy.

        plot_tsne (AxesImage): Plots the data_x parameter space using t-SNE

        plot_conf_matrix (AxesImage): Plots the confusion matrix, assessed with data_x.

        plot_roc_curve (AxesImage): Plots ROC curve, assessed with data_x

    Args:
        data_x (ndarray): 2D array of size (n x m), where n is the
            number of samples, and m the number of features.
        data_y (ndarray, str): 1D array containing the corresponing labels.
        clf (str): The machine learning classifier to optimize. Can either be
            'rf' for Random Forest, 'nn' for Neural Network, or 'xgb' for Extreme Gradient Boosting. 
            Defaults to 'rf'.
        optimize (bool): If True the Boruta algorithm will be run to identify the features
            that contain useful information, after which the optimal Random Forest hyperparameters
            will be calculated using Bayesian optimization. 
        impute (bool): If False no data imputation will be performed. Defaults to True,
            which will result in two outputs, the classifier and the imputer to save
            for future transformations. 
        imp_method (str): The imputation techinque to apply, can either be 'KNN' for k-nearest
            neighbors imputation, or 'MissForest' for the MissForest machine learning imputation
            algorithm. Defaults to 'KNN'.
        n_iter (int): The maximum number of iterations to perform during 
            the hyperparameter search. Defaults to 25. 
        boruta_trials (int): The number of trials to run when running Boruta for
            feature selection. Set to 0 for no feature selection. Defaults to 50.
        balance (bool, optional): If True, a weights array will be calculated and used
            when fitting the classifier. This can improve classification when classes
            are imbalanced. This is only applied if the classification is a binary task. 
            Defaults to True.        
        
    Returns:
        Trained machine learning model.

    """
    def __init__(self, data_x=None, data_y=None, clf='rf', optimize=True, limit_search=True, impute=True, imp_method='KNN', 
        n_iter=25, boruta_trials=50, balance=True):

        self.data_x = data_x
        self.data_y = data_y
        self.clf = clf
        self.optimize = optimize 
        self.limit_search = limit_search
        self.impute = impute
        self.imp_method = imp_method
        self.n_iter = n_iter
        self.boruta_trials = boruta_trials
        self.balance = balance 

        self.model = None
        self.imputer = None
        self.feats_to_use = None

        self.feature_history = None  
        self.optimization_results = None 
        self.best_params = None 

        if self.data_x is None or self.data_y is None:
            print('NOTE: data_x and data_y parameters are required if you wish to output visualizations.')
        
        if self.clf == 'xgb':
            if all(isinstance(val, (int, str)) for val in self.data_y):
                print('XGBoost classifier requires numerical class labels! Converting class labels as follows:')
                print('________________________________')
                y = np.zeros(len(self.data_y))
                for i in range(len(np.unique(self.data_y))):
                    print(str(np.unique(self.data_y)[i]).ljust(10)+'  ------------->     '+str(i))
                    index = np.where(self.data_y == np.unique(self.data_y)[i])[0]
                    y[index] = i
                self.data_y = y 
                print('________________________________')

    def create(self):
        """
        Creates the machine learning engine, current options are either a
        Random Forest, XGBoost, or a Neural Network classifier. 
        
        Returns:
            Trained and optimized classifier.
        """
        if self.optimize is False:
            if len(np.unique(self.data_y)) == 2:
                counter = Counter(self.data_y)
                if counter[np.unique(self.data_y)[0]] != counter[np.unique(self.data_y)[1]]:
                    if self.balance:
                        print('Unbalanced dataset detected, to apply weights set optimize=True.')

        if self.clf == 'rf':
            model = RandomForestClassifier()
        elif self.clf == 'nn':
            model = MLPClassifier()
        elif self.clf == 'xgb':
            model = XGBClassifier()
            if all(isinstance(val, (int, str)) for val in self.data_y):
                print('XGBoost classifier requires numerical class labels! Converting class labels as follows:')
                print('________________________________')
                y = np.zeros(len(self.data_y))
                for i in range(len(np.unique(self.data_y))):
                    print(str(np.unique(self.data_y)[i]).ljust(10)+'  ------------->     '+str(i))
                    index = np.where(self.data_y == np.unique(self.data_y)[i])[0]
                    y[index] = i
                self.data_y = y 
                print('________________________________')

        else:
            raise ValueError('clf argument must either be "rf", "nn", or "xgb".')
        
        if self.impute is False and self.optimize is False:
            print("Returning base model...")
            model.fit(self.data_x, self.data_y)
            self.model = model
            return

        if self.impute:
            if self.imp_method == 'KNN':
                data, self.imputer = KNN_imputation(data=self.data_x, imputer=None)
            elif self.imp_method == 'MissForest':
                warn('MissForest does not create imputer, it re-fits every time therefore cannot be used to impute new data! Returning imputer=None.')
                data, self.imputer = MissForest_imputation(data=self.data_x), None 
            else:
                raise ValueError('Invalid imputation method, currently only k-NN and MissForest algorithms are supported.')
            
            if self.optimize:
                self.data_x = data
            else:
                model.fit(data, self.data_y)
                self.model = model 
                return

        self.feats_to_use, self.feature_history = borutashap_opt(data, self.data_y, boruta_trials=self.boruta_trials)
        if len(self.feats_to_use) == 0:
            print('No features selected, increase the number of n_trials when running pyBIA.optimization.borutashap_opt(). Using all features...')
            self.feats_to_use = np.arange(data.shape[1])
        #Re-construct the imputer with the selected features as
        #new predictions will only compute these metrics, need to fit again!
        if self.imp_method == 'KNN':
            self.data_x, self.imputer = KNN_imputation(data=self.data_x[:,self.feats_to_use], imputer=None)
        elif self.imp_method == 'MissForest':
            self.data_x, self.imputer = MissForest_imputation(data=self.data_x[:,self.feats_to_use]), None 
        else: 
            self.data_x = self.data_x[:,self.feats_to_use]

        self.model, self.best_params, self.optimization_results = hyper_opt(self.data_x, self.data_y, clf=self.clf, n_iter=self.n_iter, 
            balance=self.balance, return_study=True, limit_search=self.limit_search)
        print("Fitting and returning final model...")
        self.model.fit(self.data_x, self.data_y)
        
    def save(self, path=None, overwrite=False):
        """
        Saves the trained classifier in a new directory named 'pyBIA_models', 
        as well as the imputer and the features to use attributes, if not None.
        
        Args:
            path (str): Absolute path where the data folder will be saved
                Defaults to None, in which case the directory is saved to the
                local home directory.
            overwrite (bool, optional): If True the 'pyBIA_models' folder this
                function creates in the specified path will be deleted if it exists
                and created anew to avoid duplicate files. 
        """
        if self.model is None and self.imputer is None and self.feats_to_use is None:
            raise ValueError('The models have not been created! Run classifier.create() first.')

        if path is None:
            path = str(Path.home())
        if path[-1] != '/':
            path+='/'

        try:
            os.mkdir(path+'pyBIA_ensemble_model')
        except FileExistsError:
            if overwrite:
                try:
                    os.rmdir(path+'pyBIA_ensemble_model')
                except OSError:
                    for file in os.listdir(path+'pyBIA_ensemble_model'):
                        os.remove(path+'pyBIA_ensemble_model/'+file)
                    os.rmdir(path+'pyBIA_ensemble_model')
                os.mkdir(path+'pyBIA_ensemble_model')
            else:
                raise ValueError('Tried to create "pyBIA_ensemble_model" directory in specified path but folder already exists! If you wish to overwrite set overwrite=True.')
        
        path += 'pyBIA_ensemble_model/'
        if self.model is not None:
            joblib.dump(self.model, path+'Model')
        if self.imputer is not None:
            joblib.dump(self.imputer, path+'Imputer')
        if self.feats_to_use is not None:
            joblib.dump(self.feats_to_use, path+'Feats_Index')
        if self.optimization_results is not None:
            joblib.dump(self.optimization_results, path+'HyperOpt_Results')
        if self.best_params is not None:
            joblib.dump(self.best_params, path+'Best_Params')
        print('Files saved in: {}'.format(path))
        return 

    def load(self, path=None):
        """ 
        Loads the model, imputer, and feats to use, if created and saved.
        This function will look for a folder named 'pyBIA_models' in the
        local home directory, unless a path argument is set. 

        Args:
            path (str): Path where the directory 'pyBIA_models' is saved. 
            Defaults to None, in which case the folder is assumed to be in the 
            local home directory.
        """

        if path is None:
            path = str(Path.home())
        if path[-1] != '/':
            path+='/'

        path += 'pyBIA_ensemble_model/'

        try:
            self.model = joblib.load(path+'Model')
            model = 'model'
        except FileNotFoundError:
            model = ''
            pass

        try:
            self.imputer = joblib.load(path+'Imputer')
            imputer = 'imputer'
        except FileNotFoundError:
            imputer = ''
            pass 

        try:
            self.feats_to_use = joblib.load(path+'Feats_Index')
            feats_to_use = 'feats_to_use'
        except FileNotFoundError:
            feats_to_use = ''
            pass

        try:
            self.optimization_results = joblib.load(path+'HyperOpt_Results')
            optimization_results = 'optimization_results'
        except FileNotFoundError:
            optimization_results = '' 
            pass

        print('Successfully loaded the following class attributes: {}, {}, {}, {}'.format(model, imputer, feats_to_use, optimization_results))
        
        return

    def predict(self, data):
        """
        Predics the class label of new, unseen data
        Args:
            data (ndarray): 2D array of size (n x m), where n is the
                number of samples, and m the number of features.
            model: The machine learning model to use for predictions.
            imputer: The imputer to use for imputation transformations.
                Defaults to None, in which case no imputation is performed.
            feats_to_use (ndarray): Array containing indices of features
                to use. This will be used to index the columns in the data array.
                Defaults to None, in which case all columns in the data array are used.
        Returns:
            2D array containing the classes and the corresponding probability prediction
        """

        classes = self.model.classes_
        output = []

        if self.imputer is None and self.feats_to_use is None:
            proba = self.model.predict_proba(data)
            for i in range(len(proba)):
                index = np.argmax(proba[i])
                output.append([classes[index], proba[i][index]])
            return np.array(output)

        if self.feats_to_use is not None:
            if len(data.shape) == 1:
                data = data[self.feats_to_use].reshape(1,-1)
            else:
                data = data[:,self.feats_to_use]
                
            if self.imputer is not None:
                data = self.imputer.transform(data)

            proba = self.model.predict_proba(data)

            for i in range(len(proba)):
                index = np.argmax(proba[i])
                output.append([classes[index], proba[i][index]])
            return np.array(output)

        if self.imputer is not None:
            data = self.imputer.transform(data)

        proba = self.model.predict_proba(data)
        for i in range(len(proba)):
            index = np.argmax(proba[i])
            output.append([classes[index], proba[i][index]])
            
        return np.array(output)

    def plot_tsne(self, norm=True, pca=False, title='Feature Parameter Space', 
        savefig=False):
        """
        Plots a t-SNE projection using the sklearn.manifold.TSNE() method.

        Args:
            data_x (ndarray): 2D array of size (n x m), where n is the
                number of samples, and m the number of features.
            data_y (ndarray, str): 1D array containing the corresponing labels.
            norm (bool): If True the data will be min-max normalized. Defaults
                to True.
            pca (bool): If True the data will be fit to a Principal Component
                Analysis and all of the corresponding principal components will 
                be used to generate the t-SNE plot. Defaults to False.
            title (str): Title 
        Returns:
            AxesImage. 
        """
        if np.any(np.isnan(self.data_x)):
            print('Automatically imputing NaN values with KNN imputation.')
            data = KNN_imputation(data=self.data_x)[0]
        else:
            data = self.data_x[:]

        if self.feats_to_use is not None:
            if len(data.shape) == 1:
                data = data[self.feats_to_use].reshape(1,-1)
            else:
                data = data[:,self.feats_to_use]

        if len(data) > 5e3:
            method = 'barnes_hut' #Scales with O(N)
        else:
            method = 'exact' #Scales with O(N^2)

        if norm:
            scaler = MinMaxScaler()
            data = scaler.fit_transform(data)

        if pca:
            pca_transformation = decomposition.PCA(n_components=data.shape[1], whiten=True, svd_solver='auto')
            pca_transformation.fit(data) 
            data = pca_transformation.transform(data)

        feats = TSNE(n_components=2, method=method, learning_rate=1000, 
            perplexity=35, init='random').fit_transform(data)
        x, y = feats[:,0], feats[:,1]
     
        markers = ['o', '+', '*', 's', 'v', '.', 'x', 'h', 'p', '<', '>']
        feats = np.unique(self.data_y)

        for count, feat in enumerate(feats):
            if count+1 > len(markers):
                count = -1
            mask = np.where(self.data_y == feat)[0]
            plt.scatter(x[mask], y[mask], marker=markers[count], label=str(feat), alpha=0.7)

        plt.legend(prop={'size': 16})
        plt.title(title, size=18)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        if savefig:
            plt.savefig('tSNE_Projection.png', bbox_inches='tight', dpi=300)
            plt.clf()
        else:
            plt.show()

    def plot_conf_matrix(self, norm=True, pca=False, k_fold=10, normalize=True, 
        title='Confusion Matrix', savefig=False):
        """
        Returns a confusion matrix with k-fold validation.

        Args:
            data_x (ndarray): 2D array of size (n x m), where n is the
                number of samples, and m the number of features.
            data_y (ndarray, str): 1D array containing the corresponing labels.
            norm (bool): If True the data will be min-max normalized. Defaults
                to True.
            pca (bool): If True the data will be fit to a Principal Component
                Analysis and all of the corresponding principal components will 
                be used to evaluate the classifier and construct the matrix. 
                Defaults to False.
            k_fold (int, optional): The number of cross-validations to perform.
                The output confusion matrix will display the mean accuracy across
                all k_fold iterations. Defaults to 10.
            normalize (bool, optional): If False the confusion matrix will display the
                total number of objects in the sample. Defaults to True, in which case
                the values are normalized between 0 and 1.
            classes (list): A list containing the label of the two training bags. This
                will be used to set the axis. Defaults to a list containing 'DIFFUSE' & 'OTHER'. 
            title (str, optional): The title of the output plot. 

        Returns:
            AxesImage.
        """
        
        classes = [str(label) for label in np.unique(self.data_y)]
        if np.any(np.isnan(self.data_x)):
            print('Automatically imputing NaN values with KNN imputation.')
            data = KNN_imputation(data=self.data_x)[0]
        else:
            data = self.data_x
     
        if norm:
            scaler = MinMaxScaler()
            scaler.fit_transform(data)

        if self.feats_to_use is not None:
            if len(data.shape) == 1:
                data = data[self.feats_to_use].reshape(1,-1)
            else:
                data = data[:,self.feats_to_use]
        
        if pca:
            pca_transformation = decomposition.PCA(n_components=data.shape[1], whiten=True, svd_solver='auto')
            pca_transformation.fit(data) 
            pca_data = pca_transformation.transform(data)
            data = np.asarray(pca_data).astype('float64')

        predicted_target, actual_target = evaluate_model(self.model, data, self.data_y, normalize=normalize, k_fold=k_fold)
        generate_matrix(predicted_target, actual_target, classes, normalize=normalize, title=title, savefig=savefig)

    def plot_roc_curve(self, k_fold=10, title="Receiver Operating Characteristic Curve", 
        savefig=False):
        """
        Plots ROC curve with k-fold cross-validation, as such the 
        standard deviation variations are plotted.
        
        Args:
            classifier: The machine learning classifier to optimize.
            data_x (ndarray): 2D array of size (n x m), where n is the
                number of samples, and m the number of features.
            data_y (ndarray, str): 1D array containing the corresponing labels.
            k_fold (int, optional): The number of cross-validations to perform.
                The output confusion matrix will display the mean accuracy across
                all k_fold iterations. Defaults to 10.
            title (str, optional): The title of the output plot. 
        
        Returns:
            AxesImage
        """
        if np.any(np.isnan(self.data_x)):
            print('Automatically imputing NaN values with KNN imputation.')
            data = KNN_imputation(data=self.data_x)[0]
        else:
            data = self.data_x
        
        model0 = self.model
        if len(np.unique(self.data_y)) != 2:
            X_train, X_test, y_train, y_test = train_test_split(data, self.data_y, test_size=0.2, random_state=0)
            model0.fit(X_train, y_train)
            y_probas = model0.predict_proba(X_test)
            skplt.metrics.plot_roc(y_test, y_probas, text_fontsize='large', title='ROC Curve', cmap='cividis', plot_macro=False, plot_micro=False)
            plt.show()
            return

        cv = StratifiedKFold(n_splits=k_fold)
        
        tprs = []
        aucs = []
        mean_fpr = np.linspace(0, 1, 100)

        train = data
        fig, ax = plt.subplots()
        for i, (data_x, test) in enumerate(cv.split(train, self.data_y)):
            model0.fit(train[data_x], self.data_y[data_x])
            viz = RocCurveDisplay.from_estimator(
                model0,
                train[test],
                self.data_y[test],
                name="ROC fold {}".format(i+1),
                alpha=0.3,
                lw=1,
                ax=ax,
            )
            interp_tpr = np.interp(mean_fpr, viz.fpr, viz.tpr)
            interp_tpr[0] = 0.0
            tprs.append(interp_tpr)
            aucs.append(viz.roc_auc)

        ax.plot([0, 1], [0, 1], linestyle="--", lw=2, color="r", label="Random Chance", alpha=0.8)

        mean_tpr = np.mean(tprs, axis=0)
        mean_tpr[-1] = 1.0
        mean_auc = auc(mean_fpr, mean_tpr)
        std_auc = np.std(aucs)
        ax.plot(
            mean_fpr,
            mean_tpr,
            color="b",
            label=r"Mean ROC (AUC = %0.2f $\pm$ %0.2f)" % (mean_auc, std_auc),
            lw=2,
            alpha=0.8,
        )

        std_tpr = np.std(tprs, axis=0)
        tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
        tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
        ax.fill_between(
            mean_fpr,
            tprs_lower,
            tprs_upper,
            color="grey",
            alpha=0.2,
            label=r"$\pm$ 1 std. dev.",
        )

        ax.set(
            xlim=[0, 1.0],
            ylim=[0.0, 1.0],
            title="Receiver Operating Characteristic Curve",
        )
        ax.legend(loc="lower right")
        plt.ylabel('True Positive Rate', size=14)
        plt.xlabel('False Positive Rate', size=14)
        plt.title(label=title,fontsize=18)
        if savefig:
            plt.savefig('Ensemble_ROC_Curve.png', bbox_inches='tight', dpi=300)
            plt.clf()
        else:
            plt.show()

    def plot_hyper_opt(self, xlim=None, ylim=None, xlog=True, ylog=False, 
        savefig=False):
        """
        Plots the hyperparameter optimization history.
    
        Args:
            xlim: Limits for the x-axis. Ex) xlim = (0, 1000)
            ylim: Limits for the y-axis. Ex) ylim = (0.9, 0.94)
            xlog (boolean): If True the x-axis will be log-scaled.
                Defaults to True.
            ylog (boolean): If True the y-axis will be log-scaled.
                Defaults to False.

        Returns:
            AxesImage
        """

        fig = plot_optimization_history(self.optimization_results)
        if xlog:
            plt.xscale('log')
        if ylog:
            plt.yscale('log')
        plt.xlabel('Trial #', size=16)
        plt.ylabel('10-Fold CV Accuracy', size=16)
        plt.title(('Hyperparameter Optimization History'), size=18)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.grid(True, color='k', alpha=0.35, linewidth=1.5, linestyle='--')
        plt.legend(prop={'size': 16}, loc=2)
        if xlim is not None:
            plt.xlim(xlim)
        if ylim is not None:
            plt.ylim(ylim)
        plt.tight_layout()
        if savefig:
            plt.savefig('Ensemble_Hyperparameter_Optimization.png', bbox_inches='tight', dpi=300)
            plt.clf()
        else:
            plt.show()

    def plot_feature_opt(self, feats='all'):
        """
        Returns whisker plot displaying the z-score distribution of each feature
        across all trials.

        Args:
            feats (str): Defines what features to show, can either be
                'accepted', 'rejected', or 'all'.

        Returns:
            AxesImage
        """

        self.feat_selector.plot(which_features=feats, X_size=14)


#Helper functions below to generate confusion matrix
def evaluate_model(classifier, data_x, data_y, normalize=True, k_fold=10):
    """
    Cross-checks model accuracy and outputs both the predicted
    and the true class labels. 

    Args:
        classifier: The machine learning classifier to optimize.
        data_x (ndarray): 2D array of size (n x m), where n is the
            number of samples, and m the number of features.
        data_y (ndarray, str): 1D array containing the corresponing labels.
        k_fold (int, optional): The number of cross-validations to perform.
            The output confusion matrix will display the mean accuracy across
            all k_fold iterations. Defaults to 10.

    Returns:
        The first output is the 1D array of the true class labels.
        The second output is the 1D array of the predicted class labels.
    """

    k_fold = KFold(k_fold, shuffle=True, random_state=1)

    predicted_targets = np.array([])
    actual_targets = np.array([])

    for train_ix, test_ix in k_fold.split(data_x):
        train_x, train_y, test_x, test_y = data_x[train_ix], data_y[train_ix], data_x[test_ix], data_y[test_ix]
        # Fit the classifier
        classifier.fit(train_x, train_y)
        # Predict the labels of the test set samples
        predicted_labels = classifier.predict(test_x)
        predicted_targets = np.append(predicted_targets, predicted_labels)
        actual_targets = np.append(actual_targets, test_y)

    return predicted_targets, actual_targets

def generate_matrix(predicted_labels_list, actual_targets, classes, normalize=True, 
    title='Confusion Matrix', savefig=False):
    """
    Generates the confusion matrix using the output from the evaluate_model() function.

    Args:
        predicted_labels_list: 1D array containing the predicted class labels.
        actual_targets: 1D array containing the actual class labels.
        classes (list): A list containing the label of the two training bags. This
            will be used to set the axis. Ex) classes = ['DIFFUSE', 'OTHER']
        normalize (bool, optional): If True the matrix accuracy will be normalized
            and displayed as a percentage accuracy. Defaults to True.
        title (str, optional): The title of the output plot. 

    Returns:
        AxesImage.
    """

    conf_matrix = confusion_matrix(actual_targets, predicted_labels_list)
    np.set_printoptions(precision=2)

    plt.figure()
    if normalize:
        generate_plot(conf_matrix, classes=classes, normalize=normalize, title=title)
    elif normalize == False:
        generate_plot(conf_matrix, classes=classes, normalize=normalize, title=title)
    if savefig:
        plt.savefig('Ensemble_Confusion_Matrix.png', bbox_inches='tight', dpi=300)
        plt.clf()
    else:
        plt.show()

def generate_plot(conf_matrix, classes, normalize=False, title='Confusion Matrix'):
    """
    Generates the confusion matrix figure object, but does not plot.
    
    Args:
        conf_matrix: The confusion matrix generated using the generate_matrix() function.
        classes (list): A list containing the label of the two training bags. This
            will be used to set the axis. Defaults to a list containing 'DIFFUSE' & 'OTHER'. 
        normalize (bool, optional): If True the matrix accuracy will be normalized
            and displayed as a percentage accuracy. Defaults to True.
        title (str, optional): The title of the output plot. 

    Returns:
        AxesImage object. 
    """

    if normalize:
        conf_matrix = conf_matrix.astype('float') / conf_matrix.sum(axis=1)[:, np.newaxis]
    
    plt.imshow(conf_matrix, interpolation='nearest', cmap=plt.get_cmap('Blues'))
    plt.title(title, fontsize=20)
    plt.colorbar()

    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45, fontsize=14)
    plt.yticks(tick_marks, classes, fontsize=14)
    #plt.xticks(tick_marks, ['DIFFUSE','OTHER'], rotation=45, fontsize=14)
    #plt.yticks(tick_marks, ['DIFFUSE','OTHER'], fontsize=14)

    fmt = '.2f' if normalize is True else 'd'
    thresh = conf_matrix.max() / 2.

    for i, j in itertools.product(range(conf_matrix.shape[0]), range(conf_matrix.shape[1])):
        plt.text(j, i, format(conf_matrix[i, j], fmt), fontsize=14, horizontalalignment="center",
                 color="white" if conf_matrix[i, j] > thresh else "black")

    plt.ylabel('True label',fontsize=18)
    plt.xlabel('Predicted label',fontsize=18)
    plt.tight_layout()

    return conf_matrix

def min_max_norm(data_x):
    """
    Normalizes the data to be between 0 and 1. NaN values are ignored.
    The transformation matrix will be returned as it will be needed
    to consitently normalize new data.
    
    Args:
        data_x (ndarray): 2D array of size (n x m), where n is the
            number of samples, and m the number of features.

    Returns:
        Normalized data array.
    """

    Ny, Nx = data_x.shape
    new_array = np.zeros((Ny, Nx))
    
    for i in range(Nx):
        print((np.max(data_x[:,i]) - np.min(data_x[:,i])))
        new_array[:,i] = (data_x[:,i] - np.min(data_x[:,i])) / (np.max(data_x[:,i]) - np.min(data_x[:,i]))

    return new_array
    