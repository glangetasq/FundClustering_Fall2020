import unittest
import pandas as pd
from PortfolioMapping.PortfolioMappingStrategySQL import PortfolioMappingStrategySQL


class FundNotInMappingCase(unittest.TestCase):
    def setUp(self):
        self.model = PortfolioMappingStrategySQL()
        self.portfolio = pd.DataFrame(
            [[1, 0.4],
             [2, 0.6]],
            columns=['fundNo', 'weight'])

    def test_portfolio_to_sector(self):
        portfolio_sector_sql = self.model.portfolio_to_sector(self.portfolio, method='SQL')
        self.assertEqual(len(portfolio_sector_sql), 2)
        self.assertTrue(portfolio_sector_sql['main_cluster'].isna().all())
        self.assertTrue(portfolio_sector_sql['sub_cluster'].isna().all())

        portfolio_sector_inmemory = self.model.portfolio_to_sector(self.portfolio, method='InMemory')
        self.assertEqual(len(portfolio_sector_inmemory), 2)
        self.assertTrue(portfolio_sector_inmemory['main_cluster'].isna().all())
        self.assertTrue(portfolio_sector_inmemory['sub_cluster'].isna().all())

    def test_get_sector_weighting(self):
        sector_weighting_sql = self.model.get_sector_weighting(self.portfolio, method='SQL')
        self.assertEqual(len(sector_weighting_sql), 1)
        self.assertTrue(sector_weighting_sql.loc[0, 'main_cluster'] is None)
        self.assertTrue(sector_weighting_sql.loc[0, 'sub_cluster'] is None)

        sector_weighting_inmemory = self.model.get_sector_weighting(self.portfolio, method='InMemory')
        self.assertEqual(len(sector_weighting_inmemory), 1)
        self.assertTrue(sector_weighting_inmemory.loc[0, 'main_cluster'] is None)
        self.assertTrue(sector_weighting_inmemory.loc[0, 'sub_cluster'] is None)

    def test_load_underlying_ts(self):
        underlying_ts_sql = self.model.load_underlying_ts(self.portfolio, method='SQL')
        self.assertEqual(len(underlying_ts_sql), 0)

        underlying_ts_inmemory = self.model.load_underlying_ts(self.portfolio, method='SQL')
        self.assertEqual(len(underlying_ts_inmemory), 0)

    def test_generate_portfolio_ts(self):
        portfolio_ts_sql = self.model.generate_portfolio_ts(self.portfolio, method='SQL')
        self.assertEqual(len(portfolio_ts_sql), 0)

        portfolio_ts_inmemory = self.model.generate_portfolio_ts(self.portfolio, method='SQL')
        self.assertEqual(len(portfolio_ts_inmemory), 0)


class EmptyPortfolioCase(unittest.TestCase):
    def setUp(self):
        self.model = PortfolioMappingStrategySQL()
        self.portfolio = pd.DataFrame(columns=['fundNo', 'weight'])

    def test_portfolio_to_sector(self):
        portfolio_sector_sql = self.model.portfolio_to_sector(self.portfolio, method='SQL')
        self.assertEqual(len(portfolio_sector_sql), 0)

        portfolio_sector_inmemory = self.model.portfolio_to_sector(self.portfolio, method='InMemory')
        self.assertEqual(len(portfolio_sector_inmemory), 0)

    def test_get_sector_weighting(self):
        sector_weighting_sql = self.model.get_sector_weighting(self.portfolio, method='SQL')
        self.assertEqual(len(sector_weighting_sql), 0)

        sector_weighting_inmemory = self.model.get_sector_weighting(self.portfolio, method='InMemory')
        self.assertEqual(len(sector_weighting_inmemory), 0)

    def test_load_underlying_ts(self):
        underlying_ts_sql = self.model.load_underlying_ts(self.portfolio, method='SQL')
        self.assertEqual(len(underlying_ts_sql), 0)

        underlying_ts_inmemory = self.model.load_underlying_ts(self.portfolio, method='SQL')
        self.assertEqual(len(underlying_ts_inmemory), 0)

    def test_generate_portfolio_ts(self):
        portfolio_ts_sql = self.model.generate_portfolio_ts(self.portfolio, method='SQL')
        self.assertEqual(len(portfolio_ts_sql), 0)

        portfolio_ts_inmemory = self.model.generate_portfolio_ts(self.portfolio, method='SQL')
        self.assertEqual(len(portfolio_ts_inmemory), 0)


class TSMissingCase(unittest.TestCase):
    def setUp(self):
        self.model = PortfolioMappingStrategySQL()
        self.portfolio = pd.DataFrame(
            [[105, 0.4],
             [2704, 0.6]],
            columns=['fundNo', 'weight'])

    def test_load_underlying_ts(self):
        underlying_ts_sql = self.model.load_underlying_ts(self.portfolio, method='SQL')
        self.assertEqual(len(underlying_ts_sql), 0)

        underlying_ts_inmemory = self.model.load_underlying_ts(self.portfolio, method='SQL')
        self.assertEqual(len(underlying_ts_inmemory), 0)

    def test_generate_portfolio_ts(self):
        portfolio_ts_sql = self.model.generate_portfolio_ts(self.portfolio, method='SQL')
        self.assertEqual(len(portfolio_ts_sql), 0)

        portfolio_ts_inmemory = self.model.generate_portfolio_ts(self.portfolio, method='SQL')
        self.assertEqual(len(portfolio_ts_inmemory), 0)


if __name__ == '__main__':
    unittest.main()
