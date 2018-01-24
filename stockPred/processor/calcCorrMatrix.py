import os
import pandas as pd

class CalcCorrMatrix(object):
    # Jia heng Li

    def __init__(self):
        pass

    def run(self):
        result = []
        stock_panel = self.getfiles()
        key = ['p_change']
        corr = []
        for key_iterator in range(len(key)):
            compare = []
            for item, value in stock_panel.iteritems():
                compare.append(value[key[key_iterator]].tolist())
            df = pd.DataFrame(compare)
            df = df.transpose()
            corr = df.corr()
            corr = pd.DataFrame(corr.values, index=stock_panel.items, columns=stock_panel.items)
        corr[corr == 1.0]=0
        corr = corr[corr>0.5]
        corr = corr.dropna(axis=1, how='all').drop(axis=0, how='all')
        for index, items in corr.iterrows():
            for columns in items.index:
                if items[columns]>0:
                    result.append([index, columns])

        return result

    def getfiles(self):
        path = os.walk('/bbox/data/5min')
        root = ""
        files = []
        for root_path, dirs, contained_files in path:
            root = root_path
            files = contained_files[0:10]   #test_data

        stock_dict = {}
        for one_file in files:
            stock_data = pd.read_csv(root + '/' + one_file)
            if stock_data.empty:
                continue
            stock_code = one_file.split('.')[0]
            stock_dict[stock_code] = stock_data
        stock_panel = pd.Panel(stock_dict)

        return stock_panel