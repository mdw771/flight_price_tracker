import logging
import os.path
import datetime
import sys

import pandas as pd
import matplotlib.pyplot as plt

import retriever


class FlightRateTracker:

    def __init__(self, retriever):
        self.retriever = retriever
        self.log_dir = os.path.join(os.path.dirname(__file__), 'log')
        self.log_filename = 'log.csv'
        self.log_table = None

    def run(self):
        price_dict = retriever.retrieve_prices()
        self.read_log()
        self.append_to_log(price_dict)
        self.save_log()
        self.plot_history()

    def plot_history(self):
        logging.info('Plotting results...')
        dates = pd.to_datetime(self.log_table['date'], format='%Y-%m-%d')
        temp_table = pd.DataFrame()
        temp_table['price_recommended'] = self.log_table['price_recommended']
        temp_table['price_cheapest'] = self.log_table['price_cheapest']
        temp_table = temp_table.set_index(dates)

        plt.figure()
        temp_table.plot()
        plt.gcf().autofmt_xdate()
        plt.legend()
        plt.show()

    def create_log_dir(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def initialize_log_table(self):
        self.log_table = pd.DataFrame(columns=['date', 'price_recommended', 'price_cheapest'])

    def read_log(self):
        if not os.path.exists(os.path.join(self.log_dir, self.log_filename)):
            self.create_log_dir()
            self.initialize_log_table()
        else:
            self.log_table = pd.read_csv(os.path.join(self.log_dir, self.log_filename), index_col=False)

    def save_log(self):
        self.create_log_dir()
        self.log_table.to_csv(os.path.join(self.log_dir, self.log_filename), index=False)

    def append_to_log(self, price_dict):
        if self.log_table.shape[0] > 0 and str(datetime.datetime.now().date()) == self.log_table.iloc[-1]['date']:
            logging.info("This data won't be recorded because the price today is already logged.")
            return
        self.log_table = self.log_table.append({'date': str(datetime.datetime.now().date()),
                                                'price_recommended': price_dict['recommended'],
                                                'price_cheapest': price_dict['cheapest']},
                                               ignore_index=True)


if __name__ == '__main__':
    retriever = retriever.Retriever()
    retriever.set_url('https://www.flychina.com/LFW/LowFare.aspx?DNMOrI9lgR%2bPKjBOiyQzc4zjQYwT5C%2bT9%2bwx5j3gL7A8l5mtwIRZRhjI4%2f63D1DtSO45W4sOkSnjGpRMsbASOys0I1FlEy4fYqRohITbZPEPSazKdZdoL6H20YqDpneAJnKzI7kj4Um22Upu9%2b4VQdJk2UmtBgCa9Zte%2bqapDzUa6IstTcI35%2blTjY14OryIV8wSfb%2fr%2fIYNQuV9C3ACchJIsgieX2jpBb26eq9G4BCwxnlVMWGWTrPS9wjBwjVW')
    tracker = FlightRateTracker(retriever=retriever)
    tracker.run()