#!/usr/bin/env python
# Copyright 2017 Blue Marble Analytics LLC. All rights reserved.

from collections import OrderedDict
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
     "temporal.investment.periods",
     "geography.load_zones", "geography.load_following_up_balancing_areas",
     "project", "project.capacity.capacity",
     "project.operations.reserves.lf_reserves_up"]
NAME_OF_MODULE_BEING_TESTED = "system.reserves.lf_reserves_up"
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


class TestLFReservesUp(unittest.TestCase):
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
                              horizon="",
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
                                     horizon="",
                                     stage=""
                                     )

    def test_data_loaded_correctly(self):
        """
        Test components initialized with expected data
        :return:
        """
        m, data = add_components_and_load_data(
            prereq_modules=IMPORTED_PREREQ_MODULES,
            module_to_test=MODULE_BEING_TESTED,
            test_data_dir=TEST_DATA_DIRECTORY,
            horizon="",
            stage=""
        )
        instance = m.create_instance(data)

        # Set:
        expected_ba_tmps = sorted([
            ("Zone1", 20200101),
            ("Zone1", 20200102),
            ("Zone1", 20200103),
            ("Zone1", 20200104),
            ("Zone1", 20200105),
            ("Zone1", 20200106),
            ("Zone1", 20200107),
            ("Zone1", 20200108),
            ("Zone1", 20200109),
            ("Zone1", 20200110),
            ("Zone1", 20200111),
            ("Zone1", 20200112),
            ("Zone1", 20200113),
            ("Zone1", 20200114),
            ("Zone1", 20200115),
            ("Zone1", 20200116),
            ("Zone1", 20200117),
            ("Zone1", 20200118),
            ("Zone1", 20200119),
            ("Zone1", 20200120),
            ("Zone1", 20200121),
            ("Zone1", 20200122),
            ("Zone1", 20200123),
            ("Zone1", 20200124),
            ("Zone1", 20200201),
            ("Zone1", 20200202),
            ("Zone1", 20200203),
            ("Zone1", 20200204),
            ("Zone1", 20200205),
            ("Zone1", 20200206),
            ("Zone1", 20200207),
            ("Zone1", 20200208),
            ("Zone1", 20200209),
            ("Zone1", 20200210),
            ("Zone1", 20200211),
            ("Zone1", 20200212),
            ("Zone1", 20200213),
            ("Zone1", 20200214),
            ("Zone1", 20200215),
            ("Zone1", 20200216),
            ("Zone1", 20200217),
            ("Zone1", 20200218),
            ("Zone1", 20200219),
            ("Zone1", 20200220),
            ("Zone1", 20200221),
            ("Zone1", 20200222),
            ("Zone1", 20200223),
            ("Zone1", 20200224),
            ("Zone2", 20200101),
            ("Zone2", 20200102),
            ("Zone2", 20200103),
            ("Zone2", 20200104),
            ("Zone2", 20200105),
            ("Zone2", 20200106),
            ("Zone2", 20200107),
            ("Zone2", 20200108),
            ("Zone2", 20200109),
            ("Zone2", 20200110),
            ("Zone2", 20200111),
            ("Zone2", 20200112),
            ("Zone2", 20200113),
            ("Zone2", 20200114),
            ("Zone2", 20200115),
            ("Zone2", 20200116),
            ("Zone2", 20200117),
            ("Zone2", 20200118),
            ("Zone2", 20200119),
            ("Zone2", 20200120),
            ("Zone2", 20200121),
            ("Zone2", 20200122),
            ("Zone2", 20200123),
            ("Zone2", 20200124),
            ("Zone2", 20200201),
            ("Zone2", 20200202),
            ("Zone2", 20200203),
            ("Zone2", 20200204),
            ("Zone2", 20200205),
            ("Zone2", 20200206),
            ("Zone2", 20200207),
            ("Zone2", 20200208),
            ("Zone2", 20200209),
            ("Zone2", 20200210),
            ("Zone2", 20200211),
            ("Zone2", 20200212),
            ("Zone2", 20200213),
            ("Zone2", 20200214),
            ("Zone2", 20200215),
            ("Zone2", 20200216),
            ("Zone2", 20200217),
            ("Zone2", 20200218),
            ("Zone2", 20200219),
            ("Zone2", 20200220),
            ("Zone2", 20200221),
            ("Zone2", 20200222),
            ("Zone2", 20200223),
            ("Zone2", 20200224),
            ("Zone1", 20300101),
            ("Zone1", 20300102),
            ("Zone1", 20300103),
            ("Zone1", 20300104),
            ("Zone1", 20300105),
            ("Zone1", 20300106),
            ("Zone1", 20300107),
            ("Zone1", 20300108),
            ("Zone1", 20300109),
            ("Zone1", 20300110),
            ("Zone1", 20300111),
            ("Zone1", 20300112),
            ("Zone1", 20300113),
            ("Zone1", 20300114),
            ("Zone1", 20300115),
            ("Zone1", 20300116),
            ("Zone1", 20300117),
            ("Zone1", 20300118),
            ("Zone1", 20300119),
            ("Zone1", 20300120),
            ("Zone1", 20300121),
            ("Zone1", 20300122),
            ("Zone1", 20300123),
            ("Zone1", 20300124),
            ("Zone1", 20300201),
            ("Zone1", 20300202),
            ("Zone1", 20300203),
            ("Zone1", 20300204),
            ("Zone1", 20300205),
            ("Zone1", 20300206),
            ("Zone1", 20300207),
            ("Zone1", 20300208),
            ("Zone1", 20300209),
            ("Zone1", 20300210),
            ("Zone1", 20300211),
            ("Zone1", 20300212),
            ("Zone1", 20300213),
            ("Zone1", 20300214),
            ("Zone1", 20300215),
            ("Zone1", 20300216),
            ("Zone1", 20300217),
            ("Zone1", 20300218),
            ("Zone1", 20300219),
            ("Zone1", 20300220),
            ("Zone1", 20300221),
            ("Zone1", 20300222),
            ("Zone1", 20300223),
            ("Zone1", 20300224),
            ("Zone2", 20300101),
            ("Zone2", 20300102),
            ("Zone2", 20300103),
            ("Zone2", 20300104),
            ("Zone2", 20300105),
            ("Zone2", 20300106),
            ("Zone2", 20300107),
            ("Zone2", 20300108),
            ("Zone2", 20300109),
            ("Zone2", 20300110),
            ("Zone2", 20300111),
            ("Zone2", 20300112),
            ("Zone2", 20300113),
            ("Zone2", 20300114),
            ("Zone2", 20300115),
            ("Zone2", 20300116),
            ("Zone2", 20300117),
            ("Zone2", 20300118),
            ("Zone2", 20300119),
            ("Zone2", 20300120),
            ("Zone2", 20300121),
            ("Zone2", 20300122),
            ("Zone2", 20300123),
            ("Zone2", 20300124),
            ("Zone2", 20300201),
            ("Zone2", 20300202),
            ("Zone2", 20300203),
            ("Zone2", 20300204),
            ("Zone2", 20300205),
            ("Zone2", 20300206),
            ("Zone2", 20300207),
            ("Zone2", 20300208),
            ("Zone2", 20300209),
            ("Zone2", 20300210),
            ("Zone2", 20300211),
            ("Zone2", 20300212),
            ("Zone2", 20300213),
            ("Zone2", 20300214),
            ("Zone2", 20300215),
            ("Zone2", 20300216),
            ("Zone2", 20300217),
            ("Zone2", 20300218),
            ("Zone2", 20300219),
            ("Zone2", 20300220),
            ("Zone2", 20300221),
            ("Zone2", 20300222),
            ("Zone2", 20300223),
            ("Zone2", 20300224)
        ])
        actual_ba_tmps = sorted([
            (z, tmp) for (z, tmp) in instance.LF_RESERVES_UP_ZONE_TIMEPOINTS
        ])
        self.assertListEqual(expected_ba_tmps, actual_ba_tmps)

        # Param: lf_reserves_up_violation_penalty_per_mw
        expected_penalty = OrderedDict(sorted({
            "Zone1": 99999999, "Zone2": 99999999
                                              }.items()
                                              )
                                       )
        actual_penalty = OrderedDict(sorted({
            z: instance.lf_reserves_up_violation_penalty_per_mw[z]
            for z in instance.LF_RESERVES_UP_ZONES
                                              }.items()
                                            )
                                     )
        self.assertDictEqual(expected_penalty, actual_penalty)

        # Param: lf_reserves_up_requirement_mw
        expected_req = OrderedDict(sorted({
            ("Zone1", 20200101): 5,
            ("Zone1", 20200102): 4,
            ("Zone1", 20200103): 4,
            ("Zone1", 20200104): 5,
            ("Zone1", 20200105): 5,
            ("Zone1", 20200106): 4,
            ("Zone1", 20200107): 4,
            ("Zone1", 20200108): 5,
            ("Zone1", 20200109): 5,
            ("Zone1", 20200110): 4,
            ("Zone1", 20200111): 4,
            ("Zone1", 20200112): 5,
            ("Zone1", 20200113): 5,
            ("Zone1", 20200114): 4,
            ("Zone1", 20200115): 4,
            ("Zone1", 20200116): 5,
            ("Zone1", 20200117): 5,
            ("Zone1", 20200118): 4,
            ("Zone1", 20200119): 4,
            ("Zone1", 20200120): 5,
            ("Zone1", 20200121): 5,
            ("Zone1", 20200122): 4,
            ("Zone1", 20200123): 4,
            ("Zone1", 20200124): 5,
            ("Zone1", 20200201): 5,
            ("Zone1", 20200202): 4,
            ("Zone1", 20200203): 4,
            ("Zone1", 20200204): 5,
            ("Zone1", 20200205): 5,
            ("Zone1", 20200206): 4,
            ("Zone1", 20200207): 4,
            ("Zone1", 20200208): 5,
            ("Zone1", 20200209): 5,
            ("Zone1", 20200210): 4,
            ("Zone1", 20200211): 4,
            ("Zone1", 20200212): 5,
            ("Zone1", 20200213): 5,
            ("Zone1", 20200214): 4,
            ("Zone1", 20200215): 4,
            ("Zone1", 20200216): 5,
            ("Zone1", 20200217): 5,
            ("Zone1", 20200218): 4,
            ("Zone1", 20200219): 4,
            ("Zone1", 20200220): 5,
            ("Zone1", 20200221): 5,
            ("Zone1", 20200222): 4,
            ("Zone1", 20200223): 4,
            ("Zone1", 20200224): 5,
            ("Zone2", 20200101): 5,
            ("Zone2", 20200102): 4,
            ("Zone2", 20200103): 4,
            ("Zone2", 20200104): 5,
            ("Zone2", 20200105): 5,
            ("Zone2", 20200106): 4,
            ("Zone2", 20200107): 4,
            ("Zone2", 20200108): 5,
            ("Zone2", 20200109): 5,
            ("Zone2", 20200110): 4,
            ("Zone2", 20200111): 4,
            ("Zone2", 20200112): 5,
            ("Zone2", 20200113): 5,
            ("Zone2", 20200114): 4,
            ("Zone2", 20200115): 4,
            ("Zone2", 20200116): 5,
            ("Zone2", 20200117): 5,
            ("Zone2", 20200118): 4,
            ("Zone2", 20200119): 4,
            ("Zone2", 20200120): 5,
            ("Zone2", 20200121): 5,
            ("Zone2", 20200122): 4,
            ("Zone2", 20200123): 4,
            ("Zone2", 20200124): 5,
            ("Zone2", 20200201): 5,
            ("Zone2", 20200202): 4,
            ("Zone2", 20200203): 4,
            ("Zone2", 20200204): 5,
            ("Zone2", 20200205): 5,
            ("Zone2", 20200206): 4,
            ("Zone2", 20200207): 4,
            ("Zone2", 20200208): 5,
            ("Zone2", 20200209): 5,
            ("Zone2", 20200210): 4,
            ("Zone2", 20200211): 4,
            ("Zone2", 20200212): 5,
            ("Zone2", 20200213): 5,
            ("Zone2", 20200214): 4,
            ("Zone2", 20200215): 4,
            ("Zone2", 20200216): 5,
            ("Zone2", 20200217): 5,
            ("Zone2", 20200218): 4,
            ("Zone2", 20200219): 4,
            ("Zone2", 20200220): 5,
            ("Zone2", 20200221): 5,
            ("Zone2", 20200222): 4,
            ("Zone2", 20200223): 4,
            ("Zone2", 20200224): 5,
            ("Zone1", 20300101): 5,
            ("Zone1", 20300102): 4,
            ("Zone1", 20300103): 4,
            ("Zone1", 20300104): 5,
            ("Zone1", 20300105): 5,
            ("Zone1", 20300106): 4,
            ("Zone1", 20300107): 4,
            ("Zone1", 20300108): 5,
            ("Zone1", 20300109): 5,
            ("Zone1", 20300110): 4,
            ("Zone1", 20300111): 4,
            ("Zone1", 20300112): 5,
            ("Zone1", 20300113): 5,
            ("Zone1", 20300114): 4,
            ("Zone1", 20300115): 4,
            ("Zone1", 20300116): 5,
            ("Zone1", 20300117): 5,
            ("Zone1", 20300118): 4,
            ("Zone1", 20300119): 4,
            ("Zone1", 20300120): 5,
            ("Zone1", 20300121): 5,
            ("Zone1", 20300122): 4,
            ("Zone1", 20300123): 4,
            ("Zone1", 20300124): 5,
            ("Zone1", 20300201): 5,
            ("Zone1", 20300202): 4,
            ("Zone1", 20300203): 4,
            ("Zone1", 20300204): 5,
            ("Zone1", 20300205): 5,
            ("Zone1", 20300206): 4,
            ("Zone1", 20300207): 4,
            ("Zone1", 20300208): 5,
            ("Zone1", 20300209): 5,
            ("Zone1", 20300210): 4,
            ("Zone1", 20300211): 4,
            ("Zone1", 20300212): 5,
            ("Zone1", 20300213): 5,
            ("Zone1", 20300214): 4,
            ("Zone1", 20300215): 4,
            ("Zone1", 20300216): 5,
            ("Zone1", 20300217): 5,
            ("Zone1", 20300218): 4,
            ("Zone1", 20300219): 4,
            ("Zone1", 20300220): 5,
            ("Zone1", 20300221): 5,
            ("Zone1", 20300222): 4,
            ("Zone1", 20300223): 4,
            ("Zone1", 20300224): 5,
            ("Zone2", 20300101): 5,
            ("Zone2", 20300102): 4,
            ("Zone2", 20300103): 4,
            ("Zone2", 20300104): 5,
            ("Zone2", 20300105): 5,
            ("Zone2", 20300106): 4,
            ("Zone2", 20300107): 4,
            ("Zone2", 20300108): 5,
            ("Zone2", 20300109): 5,
            ("Zone2", 20300110): 4,
            ("Zone2", 20300111): 4,
            ("Zone2", 20300112): 5,
            ("Zone2", 20300113): 5,
            ("Zone2", 20300114): 4,
            ("Zone2", 20300115): 4,
            ("Zone2", 20300116): 5,
            ("Zone2", 20300117): 5,
            ("Zone2", 20300118): 4,
            ("Zone2", 20300119): 4,
            ("Zone2", 20300120): 5,
            ("Zone2", 20300121): 5,
            ("Zone2", 20300122): 4,
            ("Zone2", 20300123): 4,
            ("Zone2", 20300124): 5,
            ("Zone2", 20300201): 5,
            ("Zone2", 20300202): 4,
            ("Zone2", 20300203): 4,
            ("Zone2", 20300204): 5,
            ("Zone2", 20300205): 5,
            ("Zone2", 20300206): 4,
            ("Zone2", 20300207): 4,
            ("Zone2", 20300208): 5,
            ("Zone2", 20300209): 5,
            ("Zone2", 20300210): 4,
            ("Zone2", 20300211): 4,
            ("Zone2", 20300212): 5,
            ("Zone2", 20300213): 5,
            ("Zone2", 20300214): 4,
            ("Zone2", 20300215): 4,
            ("Zone2", 20300216): 5,
            ("Zone2", 20300217): 5,
            ("Zone2", 20300218): 4,
            ("Zone2", 20300219): 4,
            ("Zone2", 20300220): 5,
            ("Zone2", 20300221): 5,
            ("Zone2", 20300222): 4,
            ("Zone2", 20300223): 4,
            ("Zone2", 20300224): 5
                                              }.items()
                                              )
                                       )
        actual_req = OrderedDict(sorted({
            (z, tmp): instance.lf_reserves_up_requirement_mw[z, tmp]
            for (z, tmp) in instance.LF_RESERVES_UP_ZONE_TIMEPOINTS
                                              }.items()
                                            )
                                     )
        self.assertDictEqual(expected_req, actual_req)

        # Set: LF_RESERVES_UP_PROJECTS_OPERATIONAL_IN_TIMEPOINT
        projects_2020 = sorted(["Gas_CCGT", "Gas_CCGT_New", "Gas_CCGT_z2",
                                "Battery", "Battery_Specified", "Hydro"])
        projects_2030 = sorted(["Gas_CCGT", "Gas_CCGT_New", "Gas_CCGT_z2",
                                "Battery", "Hydro"])
        expected_projects = OrderedDict(sorted({
            20200101: projects_2020,
            20200102: projects_2020,
            20200103: projects_2020,
            20200104: projects_2020,
            20200105: projects_2020,
            20200106: projects_2020,
            20200107: projects_2020,
            20200108: projects_2020,
            20200109: projects_2020,
            20200110: projects_2020,
            20200111: projects_2020,
            20200112: projects_2020,
            20200113: projects_2020,
            20200114: projects_2020,
            20200115: projects_2020,
            20200116: projects_2020,
            20200117: projects_2020,
            20200118: projects_2020,
            20200119: projects_2020,
            20200120: projects_2020,
            20200121: projects_2020,
            20200122: projects_2020,
            20200123: projects_2020,
            20200124: projects_2020,
            20200201: projects_2020,
            20200202: projects_2020,
            20200203: projects_2020,
            20200204: projects_2020,
            20200205: projects_2020,
            20200206: projects_2020,
            20200207: projects_2020,
            20200208: projects_2020,
            20200209: projects_2020,
            20200210: projects_2020,
            20200211: projects_2020,
            20200212: projects_2020,
            20200213: projects_2020,
            20200214: projects_2020,
            20200215: projects_2020,
            20200216: projects_2020,
            20200217: projects_2020,
            20200218: projects_2020,
            20200219: projects_2020,
            20200220: projects_2020,
            20200221: projects_2020,
            20200222: projects_2020,
            20200223: projects_2020,
            20200224: projects_2020,
            20300101: projects_2030,
            20300102: projects_2030,
            20300103: projects_2030,
            20300104: projects_2030,
            20300105: projects_2030,
            20300106: projects_2030,
            20300107: projects_2030,
            20300108: projects_2030,
            20300109: projects_2030,
            20300110: projects_2030,
            20300111: projects_2030,
            20300112: projects_2030,
            20300113: projects_2030,
            20300114: projects_2030,
            20300115: projects_2030,
            20300116: projects_2030,
            20300117: projects_2030,
            20300118: projects_2030,
            20300119: projects_2030,
            20300120: projects_2030,
            20300121: projects_2030,
            20300122: projects_2030,
            20300123: projects_2030,
            20300124: projects_2030,
            20300201: projects_2030,
            20300202: projects_2030,
            20300203: projects_2030,
            20300204: projects_2030,
            20300205: projects_2030,
            20300206: projects_2030,
            20300207: projects_2030,
            20300208: projects_2030,
            20300209: projects_2030,
            20300210: projects_2030,
            20300211: projects_2030,
            20300212: projects_2030,
            20300213: projects_2030,
            20300214: projects_2030,
            20300215: projects_2030,
            20300216: projects_2030,
            20300217: projects_2030,
            20300218: projects_2030,
            20300219: projects_2030,
            20300220: projects_2030,
            20300221: projects_2030,
            20300222: projects_2030,
            20300223: projects_2030,
            20300224: projects_2030
                                               }.items()
                                               )
                                        )
        actual_projects = OrderedDict(sorted({
            tmp:
                sorted([prj for prj in
                        instance.
                        LF_RESERVES_UP_PROJECTS_OPERATIONAL_IN_TIMEPOINT[tmp]
                        ]) for tmp in instance.TIMEPOINTS
                                             }.items()
                                             )
                                      )
        self.assertDictEqual(expected_projects, actual_projects)

if __name__ == "__main__":
    unittest.main()
