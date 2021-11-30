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

class Stats():

    def _make_bins(self,obs: DataFrame, calc: DataFrame, bins : List[Union[float,int]] = None) -> List:
        if not bins:
            bins = linspace(0,225,9)
        
        data_in_bins= histogram(round(abs(obs['Mag_nT']),2), bins)[0]
        calc_in_bins= histogram(round(abs(calc['mag']),2), bins)[0]

        bin_frequency = list(data_in_bins)
        binned_data = list(bins[:-1])

        return calc_in_bins,bin_frequency,binned_data


    def _ks_stats(self,binned_data,normal_ecdf,model_cdf,all_observations):
        diff = []
        for i in range (len(binned_data)):
            diff.append(normal_ecdf[i]-model_cdf[i])

        max_diff = abs(max(diff))
        degrees_of_freedom = all_observations
        confidence_level = 1.36/sqrt(all_observations)
        conficence_level90 = 1.22/sqrt(all_observations)

        df = DataFrame.from_dict(
                {'max difference':[max_diff],
                'degrees of freedom':[degrees_of_freedom],
                'at 95% confidence':[confidence_level],
                'at 90% confidence':[conficence_level90]}
                )
        
        return df 

    def _plot_ks(self,step,step_normal_ecdf,step_model_cdf,df):
        # Initialize the vertical-offset for the stacked bar chart.
        
        fig, axs = plt.subplots(figsize=(10, 10))

        fig.suptitle('KS Test')
        axs.plot(step, step_normal_ecdf)
        axs.plot(step, step_model_cdf)
        axs.table(cellText=df.values, colLabels=df.columns,loc='top')

        plt.ylabel("Cumulative Probability")
        plt.xlabel("Bins")
        plt.show()

    def ks_test(self,observed: MagApp, model: PloufModel,bins : List[Union[float,int]] = None,key_name='line 1'):
       
        model = model.results['model 1']
        observed = observed.lines[key_name]
        
        calc_in_bins,bin_frequency,binned_data = self._make_bins(observed,model)
        
        all_observations = sum(bin_frequency)
        model_bin_frequency =calc_in_bins

        running_total = 0
        step_normal_ecdf = []
        normal_ecdf = []
        model_running_total = 0
        model_cdf = []
        step_model_cdf = []
        step =[]

        for i in range (len(binned_data)):
            running_total += bin_frequency[i]/all_observations
            step.append(binned_data[i] - 5)
            step.append(binned_data[i] + 5)
            normal_ecdf.append(running_total)
            
            step_normal_ecdf.append(running_total)
            step_normal_ecdf.append(running_total)
            
            model_running_total += model_bin_frequency[i]/all_observations
            model_cdf.append(model_running_total)
            step_model_cdf.append(model_running_total)
            step_model_cdf.append(model_running_total)
        
        ks_stats = self._ks_stats(binned_data,normal_ecdf,model_cdf,all_observations)
        
        self._plot_ks(step,step_normal_ecdf,step_model_cdf,ks_stats)

    def _critical_value(self,observed,confidnece):
        
        df = len(observed)-1
        conf = (100-confidnece)/100

        return chi2.ppf(1-conf, df)

    def _chi_compare(self,chi2_value: Union[int,float], critical_value: Union[int,float]):

        if chi2_value > critical_value or chi2_value < 0:
            print( 'Chi2: %f > Critical Value: %f' % (chi2_value,critical_value))
            print("Model is not a good fit")
        else:
            print( 'Chi2: %f < Critical Value: %f' % (chi2_value,critical_value))
            print("Model is a good fit")

    def chi_squared(self,observed: MagApp, model: PloufModel,confidnece: int = 95,key_name='line 1'):

        observed = observed.lines[key_name].Mag_nT
        model = model.results['model 1'].mag

        chi2_value,_ = chisquare(observed,model)
        critical_value = self._critical_value(observed,confidnece)

        self._chi_compare(chi2_value,critical_value)

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
