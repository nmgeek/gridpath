#!/usr/bin/env python
# Copyright 2019 Blue Marble Analytics LLC. All rights reserved.

import os.path


def determine_scenario_directory(scenario_location, scenario_name):
    """
    :param scenario_location: string, the base directory
    :param scenario_name: string, the scenario name
    :return: the scenario directory (string)

    Determine the scenario directory given a base directory and the scenario
    name. If no base directory is specified, use a directory named
    'scenarios' in the root directory (one level down from the current
    working directory).
    """
    if scenario_location is None:
        main_directory = os.path.join(
            os.getcwd(), "..", "scenarios")
    else:
        main_directory = scenario_location

    scenario_directory = os.path.join(
        main_directory, str(scenario_name)
    )

    return scenario_directory


def create_directory_if_not_exists(directory):
    """
    :param directory: string; the directory path

    Check if a directory exists and create it if not.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
