#!/usr/bin/env python
# Copyright 2017 Blue Marble Analytics LLC. All rights reserved.

import csv
import os.path
from pyomo.environ import Set


def add_model_components(m, d):
    """

    :param m:
    :param d:
    :return:
    """
    m.LF_RESERVES_DOWN_ZONES = Set()


def load_model_data(m, d, data_portal, scenario_directory, horizon, stage):
    """

    :param m:
    :param d:
    :param data_portal:
    :param scenario_directory:
    :param horizon:
    :param stage:
    :return:
    """
    data_portal.load(
        filename=os.path.join(scenario_directory, "inputs",
                              "load_following_down_balancing_areas.tab"),
        select=("balancing_area",),
        index=m.LF_RESERVES_DOWN_ZONES,
        param=()
    )


def get_inputs_from_database(subscenarios, c, inputs_directory):
    """

    :param subscenarios
    :param c:
    :param inputs_directory:
    :return:
    """
    # load_following_down_balancing_areas.tab
    with open(os.path.join(inputs_directory,
                           "load_following_down_balancing_areas.tab"),
              "w") as \
            lf_down_bas_tab_file:
        writer = csv.writer(lf_down_bas_tab_file, delimiter="\t")

        # Write header
        writer.writerow(["balancing_area",
                         "violation_penalty_per_mw"])

        lf_down_bas = c.execute(
            """SELECT lf_reserves_down_ba, violation_penalty_per_mw
               FROM inputs_geography_lf_reserves_down_bas
               WHERE lf_reserves_down_ba_scenario_id = {};""".format(
                subscenarios.LF_RESERVES_DOWN_BA_SCENARIO_ID
            )
        ).fetchall()

        for row in lf_down_bas:
            writer.writerow(row)