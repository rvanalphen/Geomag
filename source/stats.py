from typing import Union
import matplotlib.pyplot as plt 
from pandas.core.frame import DataFrame
from source.model_data import PloufModel
from numpy import histogram
from typing import List
from source.app import App
from numpy import linspace
from math import sqrt

class Stats():

    def _make_bins(self,obs: DataFrame, calc: DataFrame, bins : List[Union[float,int]] = None) -> List:
        if not bins:
            bins = linspace(0,225,9)
        
        data_in_bins= histogram(round(abs(obs['Mag_nT']),2), bins)[0]
        calc_in_bins= histogram(round(abs(calc['mag']),2), bins)[0]

        bin_frequency = list(data_in_bins)
        binned_data = list(bins[:-1])

        return calc_in_bins,bin_frequency,binned_data


    def _plot_ks(self,step,step_normal_ecdf,step_model_cdf,df):
        # Initialize the vertical-offset for the stacked bar chart.
        
        fig, ax = plt.subplots(figsize=(10, 10))
        fig.tight_layout()

        ax.plot(step, step_normal_ecdf)
        ax.plot(step, step_model_cdf)
        ax.table(cellText=df.values, colLabels=df.columns,
            loc='bottom', bbox=[0.25, -0.5, 0.5, 0.3])
        
        plt.subplots_adjust(left=0.2, bottom=0.1)
        plt.title('KS Test')
        plt.xlabel("Bins")
        plt.ylabel("Cumulative Probability")
        plt.show()

    def ks_test(self,observed: App, model: PloufModel,bins : List[Union[float,int]] = None,key_name='line 1'):
       
        model = model.results['df_model1']
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
        
        

        diff = []
        for i in range (len(binned_data)):
            diff.append(normal_ecdf[i]-model_cdf[i])

        max_diff = abs(max(diff))
        degrees_of_freedom = all_observations
        confidence_level = 1.36/sqrt(all_observations)
        
        df = DataFrame.from_dict(
            {'max difference':[max_diff],
                'degrees of freedom':[degrees_of_freedom],
                'at 95% confidence':[confidence_level]}
                )

        self._plot_ks(step,step_normal_ecdf,step_model_cdf,df)