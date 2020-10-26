import unittest
import pandas as pd
import numpy as np
import DataHelper
from Models import TwoLayerFundClustering



class NoFundCase(unittest.TestCase):
    def setUp(self):
        self.maker = DataHelper.get_data_maker()
        self.preprocessor = DataHelper.get_data_preprocessor()
        clustering_year = 2020
        self.cache = self.maker.convert_to_data_cache(self.preprocessor, clustering_year)
        self.model = TwoLayerFundClustering(clustering_year)
        self.model.fit(source_type='CustomCache', cache=self.cache)

    def test_first_layer_result(self):
        self.assertEqual(self.model.first_layer.label, np.array([]))

    def test_second_layer_result(self):
        self.assertEqual(self.model.second_layer.cluster_subcluster_dict, dict())



class OneFundCase(unittest.TestCase):
    def setUp(self):
        holding_asset_row = {'caldt': 2020, 'cash': 50, 'equity': 25, 'bond': 12.5, 'security': 12.5}
        daily_returns_ts = pd.Series(np.random.rand(9), index=pd.to_datetime([f"2020-10-0{i}" for i in range(1, 10)]))
        fund_mrnstar_row = {'caldt': 2020, 'lipser_class_name': 'No one cares'}

        self.maker = DataHelper.get_data_maker()
        self.maker.add_fake_fund(holding_asset_row, daily_returns_ts, fund_mrnstar_row)
        self.preprocessor = DataHelper.get_data_preprocessor()
        clustering_year = 2020
        self.cache = self.maker.convert_to_data_cache(self.preprocessor, clustering_year)
        self.model = TwoLayerFundClustering(clustering_year)
        self.model.fit(source_type='CustomCache', cache=self.cache)

    def test_first_layer_result(self):
        self.assertEqual(self.model.first_layer.label, np.array([0]))

    def test_second_layer_result(self):
        self.assertEqual(self.model.second_layer.cluster_subcluster_dict, {'0': (0, 0)})



class TwoFundCase(unittest.TestCase):
    def setUp(self):
        holding_asset_row = {'caldt': 2020, 'cash': 50, 'equity': 25, 'bond': 12.5, 'security': 12.5}
        daily_returns_ts = pd.Series(np.random.rand(9), index=pd.to_datetime([f"2020-10-0{i}" for i in range(1, 10)]))
        fund_mrnstar_row = {'caldt': 2020, 'lipser_class_name': 'No one cares'}

        holding_asset_row_2 = {'caldt': 2020, 'cash': 100, 'equity': 0, 'bond': 0, 'security': 0}
        daily_returns_ts_2 = pd.Series(np.random.rand(9), index=pd.to_datetime([f"2020-10-0{i}" for i in range(1, 10)]))
        fund_mrnstar_row_2 = {'caldt': 2020, 'lipser_class_name': 'No one cares'}

        self.maker = DataHelper.get_data_maker()
        self.maker.add_fake_fund(holding_asset_row, daily_returns_ts, fund_mrnstar_row)
        self.maker.add_fake_fund(holding_asset_row_2, daily_returns_ts_2, fund_mrnstar_row_2)
        self.preprocessor = DataHelper.get_data_preprocessor()
        clustering_year = 2020
        self.cache = self.maker.convert_to_data_cache(self.preprocessor, clustering_year)
        self.model = TwoLayerFundClustering(clustering_year)
        self.model.fit(source_type='CustomCache', cache=self.cache)

    def test_first_layer_result(self):
        self.assertIn(self.model.first_layer.label, [np. array([0, 0]), np.array([0, 1]), np.array([1, 0])])



class SameFundsCase(unittest.TestCase):
    def setUp(self):
        holding_asset_row = {'caldt': 2020, 'cash': 50, 'equity': 25, 'bond': 12.5, 'security': 12.5}
        daily_returns_ts = pd.Series(np.random.rand(9), index=pd.to_datetime([f"2020-10-0{i}" for i in range(1, 10)]))
        fund_mrnstar_row = {'caldt': 2020, 'lipser_class_name': 'No one cares'}

        self.n_funds = 100
        fund_bulk = [(holding_asset_row, daily_returns_ts, fund_mrnstar_row)] * self.n_funds
        self.maker = DataHelper.get_data_maker()
        self.maker.bulkadd_fake_fund(fund_bulk)
        self.preprocessor = DataHelper.get_data_preprocessor()
        clustering_year = 2020
        self.cache = self.maker.convert_to_data_cache(self.preprocessor, clustering_year)
        self.model = TwoLayerFundClustering(clustering_year)
        self.model.fit(source_type='CustomCache', cache=self.cache)

    def test_first_layer_result(self):
        self.assertEqual(self.model.first_layer.label, [np.array([0])] * self.n_funds)

    def test_second_layer_result(self):
        result_dict = dict()
        for i in range(self.n_funds):
            result_dict[str(i)] = (0, 0)
        self.assertEqual(self.model.second_layer.cluster_subcluster_dict, result_dict)



class MissingDataCase(unittest.TestCase):
    def setUp(self):
        holding_asset_row = {'caldt': 2020, 'cash': 50, 'equity': 25, 'bond': 12.5, 'security': 12.5}
        daily_returns_ts = pd.Series(np.random.rand(9), index=pd.to_datetime([f"2020-10-0{i}" for i in range(1, 10)]))
        fund_mrnstar_row = {'caldt': 2020, 'lipser_class_name': 'No one cares'}

        self.n_funds = 100
        fund_bulk = [(holding_asset_row, daily_returns_ts, fund_mrnstar_row)] * self.n_funds

        holding_asset_row_missing = {'caldt': 2020, 'cash': None, 'equity': None, 'bond': None, 'security': None}
        fund_bulk.append((holding_asset_row_missing, daily_returns_ts, fund_mrnstar_row))

        self.maker = DataHelper.get_data_maker()
        self.maker.bulkadd_fake_fund(fund_bulk)
        self.preprocessor = DataHelper.get_data_preprocessor()
        clustering_year = 2020
        self.cache = self.maker.convert_to_data_cache(self.preprocessor, clustering_year)
        self.model = TwoLayerFundClustering(clustering_year)
        self.model.fit(source_type='CustomCache', cache=self.cache)

    def test_first_layer_result(self):
        self.assertIsInstance(self.model.first_layer.label, np.ndarray)

    def test_second_layer_result(self):
        self.assertIsInstance(self.model.second_layer.cluster_subcluster_dict, dict)



if __name__ == '__main__':
    unittest.main()
