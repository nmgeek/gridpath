#!/usr/bin/env python
# Copyright 2017 Blue Marble Analytics LLC. All rights reserved.

"""

"""

from builtins import next
from builtins import str
import csv
import os.path
import pandas as pd
from pyomo.environ import Set, Param, Var, Constraint, NonNegativeReals, \
    PercentFraction, value

from gridpath.auxiliary.dynamic_components import required_reserve_modules, \
    reserve_variable_derate_params, \
    reserve_to_energy_adjustment_params
from gridpath.auxiliary.auxiliary import check_list_items_are_unique, \
    find_list_item_position


def generic_determine_dynamic_components(
        d, scenario_directory, horizon, stage,
        reserve_module,
        headroom_or_footroom_dict,
        ba_column_name,
        reserve_provision_variable_name,
        reserve_provision_derate_param_name,
        reserve_to_energy_adjustment_param_name,
        reserve_balancing_area_param_name
):
    """

    :param d:
    :param scenario_directory:
    :param horizon:
    :param stage:
    :param reserve_module:
    :param headroom_or_footroom_dict:
    :param ba_column_name:
    :param reserve_provision_variable_name:
    :param reserve_provision_derate_param_name:
    :param reserve_to_energy_adjustment_param_name:
    :param reserve_balancing_area_param_name:
    :return:
    """

    getattr(d, required_reserve_modules).append(reserve_module)

    with open(os.path.join(scenario_directory, "inputs", "projects.tab"),
              "r") as projects_file:
        projects_file_reader = csv.reader(projects_file, delimiter="\t")
        headers = next(projects_file_reader)
        # Check thant columns are not repeated
        check_list_items_are_unique(headers)
        for row in projects_file_reader:
            # Get generator name; we have checked that column names are unique
            # so can expect a single-item list here and get 0th element
            generator = row[find_list_item_position(headers, "project")[0]]

            # If we have already added this generator to the head/footroom
            # variables dictionary, move on; otherwise, create the
            # dictionary item
            if generator not in list(getattr(d, headroom_or_footroom_dict).keys()):
                getattr(d, headroom_or_footroom_dict)[generator] = list()
            # Some generators get the variables associated with
            # provision of various services (e.g. reserves) if flagged
            # Figure out which these are here based on whether a reserve zone
            # is specified ("." = no zone specified, so project does not
            # contribute to this reserve requirement)
            # The names of the reserve variables for each generator
            if row[find_list_item_position(
                    headers, ba_column_name)[0]] != ".":
                getattr(d, headroom_or_footroom_dict)[generator].append(
                    reserve_provision_variable_name)

    # The names of the headroom/footroom derate params for each reserve
    # variable
    # Will be used to get the right derate for each project providing a
    # particular reserve (derate can vary by reserve type)
    getattr(d, reserve_variable_derate_params)[
        reserve_provision_variable_name
    ] = reserve_provision_derate_param_name

    # The names of the subhourly energy adjustment params and project
    # balancing area param for each reserve variable (adjustment can vary by
    #  reserve type and by balancing area within each reserve type)
    # Will be used to get the right adjustment for each project providing a
    # particular reserve
    getattr(d, reserve_to_energy_adjustment_params)[
        reserve_provision_variable_name] = \
        (reserve_to_energy_adjustment_param_name,
         reserve_balancing_area_param_name)


def generic_add_model_components(m, d,
                                 reserve_projects_set,
                                 reserve_balancing_area_param,
                                 reserve_provision_derate_param,
                                 reserve_balancing_areas_set,
                                 reserve_project_operational_timepoints_set,
                                 reserve_provision_variable_name,
                                 reserve_to_energy_adjustment_param):
    """
    Reserve-related components that will be used by the operational_type
    modules
    :param m:
    :param d:
    :param reserve_projects_set:
    :param reserve_balancing_area_param:
    :param reserve_provision_derate_param:
    :param reserve_balancing_areas_set:
    :param reserve_project_operational_timepoints_set:
    :param reserve_provision_variable_name:
    :param reserve_to_energy_adjustment_param:
    :return:
    """

    setattr(m, reserve_projects_set, Set(within=m.PROJECTS))
    setattr(m, reserve_balancing_area_param,
            Param(getattr(m, reserve_projects_set),
                  within=getattr(m, reserve_balancing_areas_set)
                  )
            )

    setattr(m, reserve_project_operational_timepoints_set,
            Set(dimen=2,
                rule=lambda mod:
                set((g, tmp) for (g, tmp) in mod.PROJECT_OPERATIONAL_TIMEPOINTS
                    if g in getattr(mod, reserve_projects_set))
                )
            )

    setattr(m, reserve_provision_variable_name,
            Var(getattr(m, reserve_project_operational_timepoints_set),
                within=NonNegativeReals
                )
            )

    # Headroom/footroom derate -- this is how much extra footroom or
    # headroom must be available in order to provide 1 unit of up or down
    # reserves respectively
    # For example, if the derate is 0.5, the required headroom for providing
    # upward reserves is 1/0.5=2 -- twice the reserve that can be provided
    # Defaults to 1 if not specified
    # This param is used by the operational_type modules
    setattr(m, reserve_provision_derate_param,
            Param(getattr(m, reserve_projects_set),
                  within=PercentFraction, default=1)
            )

    # Energy adjustment from subhourly reserve provision
    # (e.g. for storage state of charge or how much variable RPS energy is
    # delivered because of subhourly reserve provision)
    # This is an optional param, which will default to 0 if not specified
    # This param is used by the operational_type modules
    setattr(m, reserve_to_energy_adjustment_param,
            Param(getattr(m, reserve_balancing_areas_set),
                  within=PercentFraction, default=0)
            )


def generic_load_model_data(
        m, d, data_portal, scenario_directory, horizon, stage,
        ba_column_name,
        derate_column_name,
        reserve_balancing_area_param,
        reserve_provision_derate_param,
        reserve_projects_set,
        reserve_to_energy_adjustment_param,
        reserve_balancing_areas_input_file):
    """

    :param m:
    :param d:
    :param data_portal:
    :param scenario_directory:
    :param horizon:
    :param stage:
    :param ba_column_name:
    :param derate_column_name:
    :param reserve_balancing_area_param:
    :param reserve_provision_derate_param:
    :param reserve_projects_set:
    :param reserve_to_energy_adjustment_param:
    :param reserve_balancing_areas_input_file:
    :return:
    """

    columns_to_import = ("project", ba_column_name,)
    params_to_import = (getattr(m, reserve_balancing_area_param),)
    projects_file_header = pd.read_csv(os.path.join(scenario_directory,
                                                    "inputs", "projects.tab"),
                                       sep="\t", header=None, nrows=1
                                       ).values[0]

    # Import reserve provision headroom/footroom de-rate parameter only if
    # column is present
    # Otherwise, the de-rate param goes to its default of 1
    if derate_column_name in projects_file_header:
        columns_to_import += (derate_column_name, )
        params_to_import += (getattr(m, reserve_provision_derate_param),)
    else:
        pass

    # Load the needed data
    data_portal.load(filename=os.path.join(scenario_directory,
                                           "inputs", "projects.tab"),
                     select=columns_to_import,
                     param=params_to_import
                     )

    data_portal.data()[reserve_projects_set] = {
        None: list(data_portal.data()[reserve_balancing_area_param].keys())
    }

    # Load reserve provision subhourly energy adjustment (e.g. for storage
    # state of charge adjustment or delivered variable RPS energy adjustment)
    # if specified; otherwise it will default to 0
    ba_file_header = pd.read_csv(os.path.join(
        scenario_directory, "inputs", reserve_balancing_areas_input_file),
        sep="\t", header=None, nrows=1).values[0]

    if "reserve_to_energy_adjustment" in ba_file_header:
        data_portal.load(filename=os.path.join(
            scenario_directory, "inputs", reserve_balancing_areas_input_file),
            select=("balancing_area",
                    "reserve_to_energy_adjustment"),
            param=reserve_to_energy_adjustment_param
                         )


def generic_export_module_specific_results(
        m, d, scenario_directory, horizon, stage,
        module_name,
        reserve_project_operational_timepoints_set,
        reserve_provision_variable_name,
        reserve_ba_param_name):
    """
    Export project-level reserves results
    :param m:
    :param d:
    :param scenario_directory:
    :param horizon:
    :param stage:
    :param module_name:
    :param reserve_project_operational_timepoints_set:
    :param reserve_provision_variable_name:
    :param reserve_ba_param_name:
    :return:
    """
    with open(os.path.join(scenario_directory, horizon, stage, "results",
                           "reserves_provision_" + module_name + ".csv"),
              "w") as f:
        writer = csv.writer(f)
        writer.writerow(["project", "period", "horizon", "timepoint",
                         "horizon_weight", "number_of_hours_in_timepoint",
                         "balancing_area", "load_zone", "technology",
                         "reserve_provision_mw"])
        for (p, tmp) in getattr(m, reserve_project_operational_timepoints_set):
            writer.writerow([
                p,
                m.period[tmp],
                m.horizon[tmp],
                tmp,
                m.horizon_weight[m.horizon[tmp]],
                m.number_of_hours_in_timepoint[tmp],
                getattr(m, reserve_ba_param_name)[p],
                m.load_zone[p],
                m.technology[p],
                value(getattr(m, reserve_provision_variable_name)[p, tmp])
            ])


def generic_import_results_into_database(
    scenario_id, c, db, results_directory, reserve_type
):
    """
    
    :param scenario_id: 
    :param c: 
    :param db: 
    :param results_directory: 
    :param reserve_type: 
    :return: 
    """
    c.execute(
        """DELETE FROM results_project_""" + reserve_type +
        """ WHERE scenario_id = {};""".format(
            scenario_id
        )
    )
    db.commit()

    # Create temporary table, which we'll use to sort results and then drop
    c.execute(
        """DROP TABLE IF EXISTS temp_results_project_""" + reserve_type
        + str(scenario_id) + """;"""
    )
    db.commit()

    c.execute(
        """CREATE TABLE temp_results_project_""" + reserve_type
        + str(scenario_id) + """(
            scenario_id INTEGER,
            project VARCHAR(64),
            period INTEGER,
            horizon INTEGER,
            timepoint INTEGER,
            horizon_weight FLOAT,
            number_of_hours_in_timepoint FLOAT,
            load_zone VARCHAR(32),""" +
        reserve_type + """_ba VARCHAR(32),
            technology VARCHAR(32),
            reserve_provision_mw FLOAT,
            PRIMARY KEY (scenario_id, project, timepoint)
                );"""
    )
    db.commit()

    # Load results into the temporary table
    with open(os.path.join(results_directory,
                           "reserves_provision_" + reserve_type + ".csv"
                           ), "r") as reserve_provision_file:
        reader = csv.reader(reserve_provision_file)

        next(reader)  # skip header
        for row in reader:
            project = row[0]
            period = row[1]
            horizon = row[2]
            timepoint = row[3]
            horizon_weight = row[4]
            number_of_hours_in_timepoint = row[5]
            ba = row[6]
            load_zone = row[7]
            technology = row[8]
            reserve_provision = row[9]
            c.execute(
                """INSERT INTO temp_results_project_""" + reserve_type
                + str(scenario_id) + """
                    (scenario_id, project, period, horizon, timepoint,
                    horizon_weight, number_of_hours_in_timepoint,
                    load_zone, """ + reserve_type + """_ba, technology, 
                    reserve_provision_mw)
                    VALUES ({}, '{}', {}, {}, {}, {}, {}, '{}', '{}', '{}',
                    {});""".format(
                    scenario_id, project, period, horizon, timepoint,
                    horizon_weight, number_of_hours_in_timepoint, ba,
                    load_zone, technology, reserve_provision
                )
            )
    db.commit()

    # Insert sorted results into permanent results table
    c.execute(
        """INSERT INTO results_project_""" + reserve_type + """
        (scenario_id, project, period, horizon, timepoint,
        horizon_weight, number_of_hours_in_timepoint, """
        + reserve_type + """_ba, load_zone, technology, reserve_provision_mw)
        SELECT
        scenario_id, project, period, horizon, timepoint,
        horizon_weight, number_of_hours_in_timepoint, """
        + reserve_type + """_ba, load_zone, technology, reserve_provision_mw
        FROM temp_results_project_""" + reserve_type + str(scenario_id) +
        """ ORDER BY scenario_id, project, timepoint;"""
    )
    db.commit()

    # Drop the temporary table
    c.execute(
        """DROP TABLE temp_results_project_""" + reserve_type
        + str(scenario_id) +
        """;"""
    )
    db.commit()
