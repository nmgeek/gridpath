#!/usr/bin/env python
# Copyright 2017 Blue Marble Analytics LLC. All rights reserved.

from __future__ import print_function

from builtins import str
from importlib import import_module
import os.path
import sys
import unittest

from tests.common_functions import create_abstract_model, \
    add_components_and_load_data

TEST_DATA_DIRECTORY = \
    os.path.join(os.path.dirname(__file__), "..", "..", "test_data")

# Import prerequisite modules
PREREQUISITE_MODULE_NAMES = [
    "temporal.operations.timepoints", "temporal.operations.horizons",
    "temporal.investment.periods", "geography.load_zones",
    "geography.markets"]
NAME_OF_MODULE_BEING_TESTED = "system.load_balance.market_participation"
IMPORTED_PREREQ_MODULES = list()
for mdl in PREREQUISITE_MODULE_NAMES:
    try:
        imported_module = import_module("." + str(mdl), package="gridpath")
        IMPORTED_PREREQ_MODULES.append(imported_module)
    except ImportError:
        print("ERROR! Module " + str(mdl) + " not found.")
        sys.exit(1)
# Import the module we'll test
try:
    MODULE_BEING_TESTED = import_module("." + NAME_OF_MODULE_BEING_TESTED,
                                        package="gridpath")
except ImportError:
    print("ERROR! Couldn't import module " + NAME_OF_MODULE_BEING_TESTED +
          " to test.")


class TestMarketParticipation(unittest.TestCase):
    """

    """
    def test_add_model_components(self):
        """
        Test that there are no errors when adding model components
        :return:
        """
        create_abstract_model(prereq_modules=IMPORTED_PREREQ_MODULES,
                              module_to_test=MODULE_BEING_TESTED,
                              test_data_dir=TEST_DATA_DIRECTORY,
                              subproblem="",
                              stage=""
                              )

    def test_load_model_data(self):
        """
        Test that data are loaded with no errors
        :return:
        """
        add_components_and_load_data(prereq_modules=IMPORTED_PREREQ_MODULES,
                                     module_to_test=MODULE_BEING_TESTED,
                                     test_data_dir=TEST_DATA_DIRECTORY,
                                     subproblem="",
                                     stage=""
                                     )

    def test_data_loaded_correctly(self):
        """
        Test components initialized with data as expected
        :return:
        """
        m, data = add_components_and_load_data(
            prereq_modules=IMPORTED_PREREQ_MODULES,
            module_to_test=MODULE_BEING_TESTED,
            test_data_dir=TEST_DATA_DIRECTORY,
            subproblem="",
            stage=""
        )
        instance = m.create_instance(data)

        # Set: LZ_MARKETS
        expected_lz_markets = sorted([
            ("Zone1", "Market_Hub_1"),
            ("Zone1", "Market_Hub_2"),
            ("Zone2", "Market_Hub_1")
        ])
        actual_lz_markets = sorted([
            (z, mrk) for (z, mrk) in instance.LZ_MARKETS
        ])
        self.assertListEqual(expected_lz_markets, actual_lz_markets)

        # Set: MARKET_LZS
        expected_market_lzs = sorted(["Zone1", "Zone2"])
        actual_market_lzs = sorted([z for z in instance.MARKET_LZS])
        self.assertListEqual(expected_market_lzs, actual_market_lzs)

        # Set: MARKETS_BY_LZ
        expected_markets_by_lz = {
            "Zone1": ["Market_Hub_1", "Market_Hub_2"],
            "Zone2": ["Market_Hub_1"]
        }

        actual_markets_by_lz = {
            z: [mrkt for mrkt in instance.MARKETS_BY_LZ[z]]
            for z in instance.MARKET_LZS
        }
        self.assertDictEqual(expected_markets_by_lz, actual_markets_by_lz)


if __name__ == "__main__":
    unittest.main()
