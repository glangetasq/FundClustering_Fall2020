import unittest
import pandas as pd
import numpy as np
from Config import UNITTEST_SEED
import DataHelper
from Models import TwoLayerFundClustering



class NoFundCase(unittest.TestCase):
    def setUp(self):
        maker = DataHelper.get_data_maker()
        clustering_year = 2020

        self.model = TwoLayerFundClustering(clustering_year)
        self.model.load_raw_data(maker)
        self.model.fit()

    def test_first_layer_result(self):
        self.assertTrue((self.model.first_layer.label == np.array([])).all())

    def test_second_layer_result(self):
        self.assertEqual(self.model.second_layer.cluster_subcluster_dict, dict())



class OneFundCase(unittest.TestCase):
    def setUp(self):

        np.random.seed(UNITTEST_SEED)

        clustering_year = 2020
        maker = DataHelper.get_data_maker()

        m_days = 9

        mrnstar_row = [1, f'{clustering_year}-12-31', 50, 25, 12.5, 12.5, 'Class 1']
        returns = pd.Series(np.random.rand(m_days), index=pd.date_range(f'{clustering_year}-10-01', periods=m_days))
        maker.add_fake_fund(mrnstar_row, returns)

        self.model = TwoLayerFundClustering(clustering_year)
        self.model.load_raw_data(maker)
        self.model.fit()

    def test_first_layer_result(self):
        self.assertTrue((self.model.first_layer.label == np.array([0])).all())

    def test_second_layer_result(self):
        self.assertEqual(self.model.second_layer.cluster_subcluster_dict, {0: (0, 0)})



class TwoFundCase(unittest.TestCase):
    def setUp(self):

        np.random.seed(UNITTEST_SEED)

        clustering_year = 2020
        maker = DataHelper.get_data_maker()

        m_days = 9

        mrnstar_row = [1, f'{clustering_year}-12-31', 50, 25, 12.5, 12.5, 'Class 1']
        returns = pd.Series(np.random.rand(m_days), index=pd.date_range(f'{clustering_year}-10-01', periods=m_days))
        maker.add_fake_fund(mrnstar_row, returns)

        mrnstar_row = [2, f'{clustering_year}-12-31', 100, 0, 0, 0, 'Class 2']
        returns = pd.Series(np.random.rand(m_days), index=pd.date_range(f'{clustering_year}-10-01', periods=m_days))
        maker.add_fake_fund(mrnstar_row, returns)

        self.model = TwoLayerFundClustering(clustering_year)
        self.model.load_raw_data(maker)
        self.model.fit()

    def test_first_layer_result(self):
        self.assertTrue((self.model.first_layer.label == np.array([0,1])).all())

    def test_second_layer_result(self):
        self.assertIsInstance(self.model.second_layer.cluster_subcluster_dict, dict)
        self.assertEqual(len(self.model.second_layer.cluster_subcluster_dict), 2)



class ThreeFundCase(unittest.TestCase):
    def setUp(self):

        np.random.seed(UNITTEST_SEED)

        clustering_year = 2020
        maker = DataHelper.get_data_maker()

        m_days = 9

        mrnstar_row = [1, f'{clustering_year}-12-31', 50, 25, 12.5, 12.5, 'Class 1']
        returns = pd.Series(np.random.rand(m_days), index=pd.date_range(f'{clustering_year}-10-01', periods=m_days))
        maker.add_fake_fund(mrnstar_row, returns)

        mrnstar_row = [2, f'{clustering_year}-12-31', 100, 0, 0, 0, 'Class 2']
        returns = pd.Series(np.random.rand(m_days), index=pd.date_range(f'{clustering_year}-10-01', periods=m_days))
        maker.add_fake_fund(mrnstar_row, returns)

        mrnstar_row = [3, f'{clustering_year}-12-31', 20, 10, 60, 10, 'Class 3']
        returns = pd.Series(np.random.rand(m_days), index=pd.date_range(f'{clustering_year}-10-01', periods=m_days))
        maker.add_fake_fund(mrnstar_row, returns)

        self.model = TwoLayerFundClustering(clustering_year)
        self.model.load_raw_data(maker)
        self.model.fit()

    def test_first_layer_result(self):
        self.assertTrue(set(self.model.first_layer.label) == set(np.array([0,1,2])))

    def test_second_layer_result(self):
        self.assertIsInstance(self.model.second_layer.cluster_subcluster_dict, dict)
        self.assertEqual(len(self.model.second_layer.cluster_subcluster_dict), 3)



class SameFundsCase(unittest.TestCase):
    def setUp(self):

        self.n_funds = 100

        np.random.seed(UNITTEST_SEED)

        clustering_year = 2020
        maker = DataHelper.get_data_maker()

        m_days = 9

        mrnstar_row = [1, f'{clustering_year}-12-31', 50, 25, 12.5, 12.5, 'Class 1']
        returns = pd.Series(np.random.rand(m_days), index=pd.date_range(f'{clustering_year}-10-01', periods=m_days))
        maker.bulk_add_fake_fund( self.n_funds * [[ mrnstar_row, returns ]] )

        self.model = TwoLayerFundClustering(clustering_year)
        self.model.load_raw_data(maker)
        self.model.fit()


    def test_first_layer_result(self):
        self.assertTrue((self.model.first_layer.label == [np.array([0])] * self.n_funds).all())

    def test_second_layer_result(self):
        result_dict = dict()
        for i in range(self.n_funds):
            result_dict[i] = (0, 0)
        self.assertEqual(self.model.second_layer.cluster_subcluster_dict, result_dict)



class MissingDataCase(unittest.TestCase):
    def setUp(self):

        np.random.seed(UNITTEST_SEED)

        clustering_year = 2020
        maker = DataHelper.get_data_maker()

        m_days = 9

        mrnstar_row = [1, f'{clustering_year}-12-31', 50, 25, 12.5, 12.5, 'Class 1']
        returns = pd.Series(np.random.rand(m_days), index=pd.date_range(f'{clustering_year}-10-01', periods=m_days))
        maker.add_fake_fund(mrnstar_row, returns)

        mrnstar_row = [2, f'{clustering_year}-12-31', 100, 0, 0, 0, 'Class 2']
        returns = pd.Series(np.random.rand(m_days), index=pd.date_range(f'{clustering_year}-10-01', periods=m_days))
        maker.add_fake_fund(mrnstar_row, returns)

        mrnstar_row = [3, f'{clustering_year}-12-31', None, None, None, None, 'Class 3']
        returns = pd.Series(np.random.rand(m_days), index=pd.date_range(f'{clustering_year}-10-01', periods=m_days))
        maker.add_fake_fund(mrnstar_row, returns)

        self.model = TwoLayerFundClustering(clustering_year)
        self.model.load_raw_data(maker)
        self.model.fit()

    def test_first_layer_result(self):
        self.assertIsInstance(self.model.first_layer.label, np.ndarray)

    def test_second_layer_result(self):
        self.assertIsInstance(self.model.second_layer.cluster_subcluster_dict, dict)


if __name__ == '__main__':
    unittest.main()
