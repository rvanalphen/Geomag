from typing import Union
import matplotlib.pyplot as plt 
from pandas.core.frame import DataFrame
from source.model_data import PloufModel
from numpy import histogram
from typing import List
from source.app import MagApp
from numpy import linspace
from math import sqrt
from numpy import mean, std, var
from scipy.stats import kurtosis,skew,chisquare,chi2
from statsmodels.api import distributions

class Stats():

    def _ks_stats(self,length,y,y2):

        max_diff = abs(max(y-y2))

        degrees_of_freedom = length
        confidence_level = 1.36/sqrt(length)

        df = DataFrame.from_dict(
                {'max difference':[max_diff],
                'degrees of freedom':[degrees_of_freedom],
                'at 95% confidence':[confidence_level]})
        
        print("\n Confidence Table:")
        print(df)
        return df 

    def _plot_ks(self,x,y,y2,df):
        # Initialize the vertical-offset for the stacked bar chart.
        
        fig, axs = plt.subplots(figsize=(10, 10))

        fig.suptitle('KS Test')
        axs.step(x, y)
        axs.step(x, y2)
        axs.table(cellText=df.values, colLabels=df.columns,loc='top')

        plt.ylabel("Cumulative Probability")
        plt.xlabel("nanoTesla")
        plt.show()

    def ks_test(self,observed: MagApp, model: PloufModel,key_name='line 1'):
       
        model = model.results['model 1']
        observed = observed.lines[key_name]
        
        ecdf = distributions.ECDF(observed.Mag_nT)
        ecdf_model = distributions.ECDF(model.mag)
        
        x = linspace(min(observed.Mag_nT.values), max(observed.Mag_nT.values))
        y = ecdf(x)
        y2= ecdf_model(x)

        ks_stats = self._ks_stats(len(observed),y,y2)
        
        self._plot_ks(x,y,y2,ks_stats)

    def _critical_value(self,observed,confidnece):
        
        df = len(observed)-1
        conf = (100-confidnece)/100

        return chi2.ppf(1-conf, df)

    def chi_squared(self,observed: MagApp, model: PloufModel,confidnece: int = 95,key_name='line 1'):

        observed = observed.lines[key_name].Mag_nT
        model = model.results['model 1'].mag

        chi2_value,_ = chisquare(observed,model)
        critical_value = self._critical_value(observed,confidnece)

        print( 'Chi2: %f, Critical Value: %f' % (chi2_value,critical_value))

    def rmse(self,observed: MagApp, model: PloufModel,key_name='line 1'):

        observed = observed.lines[key_name].Mag_nT
        model = model.results['model 1'].mag

        rmse = sqrt(((model - observed) ** 2).mean())
        
        norm_rmse = rmse / (observed.max()-observed.min()) 

        return rmse,norm_rmse


    def get_stats(self,app: MagApp,bins=50):
        data = app.data.copy()

        df = DataFrame.from_dict(
            {   "mean" : [mean(data.Mag_nT.values)],
                "var"  : [var(data.Mag_nT.values)],
                "std"  : [std(data.Mag_nT.values)],
                "skew" : [skew(data.Mag_nT.values)],
                "kurt" : [kurtosis(data.Mag_nT.values)]
            }
        )

        length_max = max(data.Mag_nT)
        length_min = min(data.Mag_nT)

        bin_width = (length_max - length_min)/bins # notice the use of parentheses
        print("bin width = ", bin_width, "nT")

        fig, ax = plt.subplots(figsize=(15,15))
        fig.suptitle('Mag Signal Histogram')
        
        ax.hist(data.Mag_nT, bins=bins)
        ax.table(cellText=df.values, colLabels=df.columns,loc='top')
        
        plt.xlabel('Mag Siganl (nT)')
        plt.ylabel('Counts')
        plt.grid(True)

        data.Mag_nT.values.sort()
        y=[]
        for i in range (0,len(data.Mag_nT.values)):
            y_value = 1-(i/len(data.Mag_nT.values)) 
            y.append(y_value)

        fig, ax = plt.subplots(figsize=(10,10))
        plt.plot(data.Mag_nT,y)

        plt.title('Survivor Plot')
        plt.xlabel('Mag Siganl (nT)') 
        plt.ylabel('fraction')
        
        plt.show()
