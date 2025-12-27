import pandas as pd 
import numpy as np
import random
import datetime

import matplotlib.pyplot as plt
class Expenses:
    def __init__(self, df):
        
        self.df = self.clean_df(df)
        self.last_month = self.df.sort_values("date", ascending=True).iloc[-1].month
        self.last_df = self.df[self.df.month==self.last_month]

    @staticmethod
    def clean_df(df):
        df['fixed_variable'] = np.where(df['category'].isin(['Rent', 'Utilities', 'Subscription', 'Healthcare']), 'Fixed', 'Variable')
        df['date'] = pd.to_datetime(df['timestamp']).dt.strftime('%F') 
        df['month'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m')
        df['year'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y')
        df['weekday'] = pd.to_datetime(df['timestamp']).dt.strftime('%A')
        return df
    
    def summary_by_category(self, byc='category'):
        fig, ax = plt.subplots(1, 2,figsize=(10, 4))
        test = self.df.groupby([byc]).amount.mean()
        test_last = self.last_df.groupby([byc]).amount.mean()
        ax[0].pie(test, labels=test.index, autopct='%1.1f%%', startangle=140)
        ax[1].pie(test_last, labels=test_last.index, autopct='%1.1f%%', startangle=140)
        ax[0].set_title('Overall Average Expense by ' + byc.capitalize())  
        ax[1].set_title('Last Month Average Expense by ' + byc.capitalize())
        fig.show()

        return fig
    

    def monthly_expense_trend(self, byc='month', as_index=False):

        monthly = self.df.groupby(byc, as_index=as_index)["amount"].sum()
        return monthly
    
    def summary_two(self, index, columns, as_pct=False):
        fig, ax = plt.subplots(figsize=(12, 7))
        pivot_table = (self.df
        .pivot_table(index=index, columns=columns, values='amount', aggfunc='sum')
        .fillna(0)
        )
        if as_pct: pivot_table = pivot_table.div(pivot_table.sum(axis=1), axis=0)

        pivot_table.plot(kind='bar', stacked=True, title=f'Expenses by {index} & {columns}', figsize=(12, 7), ax=ax)
        
        return fig
    


def generate_expenses(n=100, start_date='2025-01-01', end_date='2025-12-31'):

    providers = ['Amazon', 'Starbucks', 'Walmart', 'Target', 'Uber', 'Lyft', 'Shell', 'Chevron', 'Whole Foods', 'Apple']
    categories = ['Groceries', 'Transport', 'Entertainment', 'Utilities', 'Dining', 'Subscription', 'Healthcare', 'Rent', 'Shopping', 'Travel']
    start = datetime.datetime.fromisoformat(start_date)
    end = datetime.datetime.fromisoformat(end_date)
    total_seconds = (end - start).total_seconds()

    amounts = [round(random.uniform(3.0, 500.0), 2) for _ in range(n)]
    timestamps = [(start + datetime.timedelta(seconds=random.uniform(0, total_seconds))).isoformat() for _ in range(n)]
    providers_list = [random.choice(providers) for _ in range(n)]
    categories_list = [random.choice(categories) for _ in range(n)]

    return {
        'amount': amounts,
        'timestamp': timestamps,
        'provider': providers_list,
        'category': categories_list
    }

if __name__ == "__main__":
    print('Hello world')