import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
import math
import warnings

warnings.filterwarnings('ignore')
sns.set_style('whitegrid')


from outliers import remove_outliers

def eda_data_quality (data):
    
    """
    Function for performing data quality checks on data set
    
    Args:
        data (dataframe) data on which checks are to be performed
        
    Returns:
        dataframe: results for quality checks
    """
    
    df_results = pd.DataFrame(data.dtypes)
    
    df_results.columns = ['type']
    
    df_uniq = pd.DataFrame(data.nunique())
    
    df_uniq.columns = ['unique']
    
    df_results = df_results.merge(df_uniq, how='left', left_index=True, right_index=True)
    
    missing = pd.DataFrame(data.isnull().sum())
    
    missing.columns = ['missing']
    
    df_results = df_results.merge(missing, how='left', left_index=True, right_index=True)
    
    df_results['pct.missing'] = (df_results['missing']/len(data)).apply(lambda x: '{:.1%}'.format(x))
    
    df_summar = pd.DataFrame(data.describe()).T
    
    df_summar = df_summar[['mean', 'std', 'min', '25%', '50%', '75%', 'max']]
    
    df_results = df_results.merge(df_summar, how='left', left_index=True, right_index=True)
    
    df_skew = pd.DataFrame(data.skew())
    
    df_skew.columns = ['skewness']
    
    df_results = df_results.merge(df_skew, how='left', left_index=True, right_index=True)
    
    df_kurtosis = pd.DataFrame(data.kurtosis())
    
    df_kurtosis.columns = ['kurtosis']
    
    df_results = df_results.merge(df_kurtosis, how='left', left_index=True, right_index=True)
    
    return df_results


class binary_eda_plot:
    
    """
    Class for visualizing data fro explatory analysis
    
    Attributes:
        data (dataframe) data for explatory analysis
        plot_columns (dic) columns to visualize
        log_columns (list) columns to use log scale
        columns (int) number of columns in the matplotlib subplots
        target_palette (dic) palette for the labels
        
    """
    
    def __init__(self, data, 
                 target='target', 
                 plot_columns=None, 
                 log_columns=[None], 
                 exclude_cols=[None], 
                 columns=6, 
                 target_palette={1:'red', 0:'deepskyblue'}
                ):
        
        self.data = data
        
        self.target = target
        
        self.exclude_cols = exclude_cols

        if not plot_columns:
            
            self.plot_columns = {'target': [], 'discrete' : [], 'numeric': []}
            
            for col in self.data.columns:
            
                if col==self.target:
                    self.plot_columns['target']= col

                elif len(self.data[col].unique()) < 50:
                    self.plot_columns['discrete'].append(col)

                elif self.data[col].dtype in ('float', 'int') and col not in self.exclude_cols:
                    self.plot_columns['numeric'].append(col)
        else:
            self.plot_columns = plot_columns
        
        self.log_columns = log_columns
        
        # self.columns = columns
        
        self.target = target
        
        self.target_palette = target_palette

        
        self.plot_vars = [self.plot_columns.get('target') ] + self.plot_columns.get('discrete') + self.plot_columns.get('numeric') 
        
        self.plot_vars = sorted(set(self.plot_vars), key=self.plot_vars.index)
        
        # double number of discrete variables for split between labels
        
        self.numb_vars = len(self.plot_vars) 
        self.columns = self.numb_vars
        
        # self.rows = math.ceil(self.numb_vars/self.columns)
        self.rows = 1
        
        self.length = self.rows * 6
        
        self.width = self.columns * 6
        
    def label_bar(self, axes, size):
        
        for ax in axes.patches:
            
            if ax.get_height()>0:
                
                value = '{:.0%}'.format(ax.get_height() / size)

                axes.text(ax.get_x() + (ax.get_width() * 0.5 )
                         ,ax.get_height() + (ax.get_height() * 0.025)
                         ,value
                         ,ha='center' 
                         ,va='center'
                         ,fontsize=10
                        )

    def format_ax(ax, colors = ['black', 'black', 'black', 'None']):
        ax.spines['left'].set_color(colors[0])
        
        ax.spines['left'].set_linewidth(1.5)
        
        ax.spines['bottom'].set_color(colors[1])
        
        ax.spines['bottom'].set_linewidth(1.5)
        
        ax.spines['right'].set_color(colors[1])
        
        ax.spines['right'].set_linewidth(1.5)
        
        ax.spines['top'].set_color(None)
  


    def plot_target(self, ax):
        
        sns.countplot(x=self.target, data=self.data, 
                      hue=self.target,
                      dodge=False, 
                      palette=self.target_palette, 
                      ax=ax
                     )
        
        plt.ticklabel_format(style='plain', axis='y')
        
        plt.title(self.target, fontsize=14, fontname='georgia', fontweight='bold')
        
        plt.xlabel('')
        
        self.label_bar(ax, len(self.data))
        
        plt.legend(loc='upper right')

    def gen_plot_data(self, col, trend=True):
        
        a = self.data[col].value_counts(sort=trend)
        a.name = 'total'
        
        b = self.data[self.data[self.target]==1][col].value_counts()
        b.name = 'goods'
        
        c = self.data[self.data[self.target]==1][col].value_counts(normalize=True)
        c.name = 'distr_goods'
        
        d = self.data[self.data[self.target]==0][col].value_counts()
        d.name = 'bads'
        
        e = self.data[self.data[self.target]==0][col].value_counts(normalize=True)
        e.name = 'distr_bads'
        
        f = self.data.groupby(col)[self.target].mean()
        f.name = 'target_rate'

        g = a/len(self.data)
        g.name = 'attr_rate'

        results = pd.concat([a, b, c, d, e, f, g], axis=1)

        results.index = results.index.map(str)

        return results
        
    def plot_discrete(self, col, ax):

        results = self.gen_plot_data(col)


        
        # a = self.data[col].value_counts(sort=False)
        # a.name = 'total'
        
        # b = self.data[self.data[self.target]==1][col].value_counts()
        # b.name = 'goods'
        
        # c = self.data[self.data[self.target]==1][col].value_counts(normalize=True)
        # c.name = 'distr_goods'
        
        # d = self.data[self.data[self.target]==0][col].value_counts()
        # d.name = 'bads'
        
        # e = self.data[self.data[self.target]==0][col].value_counts(normalize=True)
        # e.name = 'distr_bads'
        
        # f = self.data.groupby(col)[self.target].mean()
        # f.name = 'target_rate'

        # g = a/len(self.data)
        # g.name = 'attr_rate'
        
        # results = pd.concat([a, b, c, d, e, f, g], axis=1)
        
        # results.index = results.index.map(str)
        
        ax.bar(results.index, results['goods'], color='#ff2e63')
        
        ax.bar(results.index, results['bads'], bottom=results['goods'], color='deepskyblue')
        
#         self.format_ax(ax)
        
        ax2 = ax.twinx()
        
        ax2.plot(results['distr_goods'], marker='o', color='#0000FF', label='event_rate')
        
        ax2.plot(results['distr_bads'], marker='o', color='black', label='non-event_rate')
        
        ax2.plot(results['target_rate'], marker='o', color='red', label='target_rate')

        # ax2.plot(results['attr_rate'], marker='o', color='#00FF00', label='attr_rate')
        
        ax2.set_yticklabels(['{:.0%}'.format(x) for x in ax2.get_yticks()])
        
        ax2.grid(False)
        
        ax.tick_params(axis='x', rotation=90)
        
        plt.title(col, fontsize=14, fontname='georgia', fontweight='bold')
        
        ax2.legend()
        
        plt.xlabel('')
        
    def plot_numeric(self, col, ax):
        
#         data = remove_outliers(self.data, [col], target=self.target)
        
        data = remove_outliers(self.data, [col]).percentile_method(threshold=0.95)
        
        sns.kdeplot(
            data=data,
            x=col,
            hue='target',
            log_scale=True if col in self.log_columns else False,
            fill=True,
            palette=self.target_palette,
            ax=ax,
            legend = False
        )  
        
        plt.title(col, fontsize=14, fontname='georgia', fontweight='bold')
        
        plt.xlabel('')
        
    def get_plots(self):  

        fig2 = plt.figure(figsize=(self.width, self.length), constrained_layout=True)

        j = 0

        for n, col in enumerate(self.plot_vars):

            if self.plot_columns.get('target') == col:

                j += 1

                axes = plt.subplot(self.rows, self.columns, j)
                
                self.plot_target(axes)

            elif col in self.plot_columns.get('discrete'):

                j += 1

                ax1 = plt.subplot(self.rows, self.columns, j)
                
                self.plot_discrete(col, ax1)

            elif col in self.plot_columns.get('numeric'):

                j += 1


                ax2 = plt.subplot(self.rows, self.columns, j)
                
                self.plot_numeric(col, ax2)

        plt.tight_layout()
