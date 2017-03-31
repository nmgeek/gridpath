#!/usr/bin/env python
# Copyright 2017 Blue Marble Analytics LLC. All rights reserved.

"""
Describe operational costs.
"""

import csv
import os.path
from pyomo.environ import Var, Expression, Constraint, NonNegativeReals, value

from gridpath.auxiliary.dynamic_components import required_operational_modules
from gridpath.auxiliary.auxiliary import load_operational_type_modules


def add_model_components(m, d):
    """
    Sum up all operational costs and add to the objective function.
    :param m:
    :param d:
    :return:
    """

    # ### Aggregate operational costs for objective function ### #
    # Add cost to objective function
    def variable_om_cost_rule(m, g, tmp):
        """
        Power production cost for each generator.
        :param m:
        :return:
        """
        return m.Power_Provision_MW[g, tmp] * m.variable_om_cost_per_mwh[g]

    m.Variable_OM_Cost = Expression(m.PROJECT_OPERATIONAL_TIMEPOINTS,
                                    rule=variable_om_cost_rule)

    # From here, the operational modules determine how the model components are
    # formulated
    # Import needed operational modules
    imported_operational_modules = \
        load_operational_type_modules(getattr(d, required_operational_modules))

    # ### Fuel cost ### #
    def fuel_cost_rule(mod, g, tmp):
        """

        :param mod:
        :param g:
        :param tmp:
        :return:
        """
        gen_op_type = mod.operational_type[g]
        return imported_operational_modules[gen_op_type].\
            fuel_burn_rule(mod, g, tmp,
                           "Error calling fuel_cost_rule function in "
                           "aggregate_operational_costs.py") * \
            mod.fuel_price_per_mmbtu[
                mod.fuel[g], mod.period[tmp], mod.month[mod.horizon[tmp]]]

    m.Fuel_Cost = Expression(m.FUEL_PROJECT_OPERATIONAL_TIMEPOINTS,
                             rule=fuel_cost_rule)

    # ### Startup and shutdown costs ### #
    def startup_rule(mod, g, tmp):
        """
        Track units started up from timepoint to timepoint; get appropriate
        expression from the generator's operational module.
        :param mod:
        :param g:
        :param tmp:
        :return:
        """
        gen_op_type = mod.operational_type[g]
        return imported_operational_modules[gen_op_type]. \
            startup_rule(mod, g, tmp)

    m.Startup_Expression = Expression(
        m.STARTUP_COST_PROJECT_OPERATIONAL_TIMEPOINTS,
        rule=startup_rule)

    def shutdown_rule(mod, g, tmp):
        """
        Track units shut down from timepoint to timepoint; get appropriate
        expression from the generator's operational module.
        :param mod:
        :param g:
        :param tmp:
        :return:
        """
        gen_op_type = mod.operational_type[g]
        return imported_operational_modules[gen_op_type]. \
            shutdown_rule(mod, g, tmp)

    m.Shutdown_Expression = Expression(
        m.SHUTDOWN_COST_PROJECT_OPERATIONAL_TIMEPOINTS,
        rule=shutdown_rule)
    m.Startup_Cost = Var(m.STARTUP_COST_PROJECT_OPERATIONAL_TIMEPOINTS,
                         within=NonNegativeReals)
    m.Shutdown_Cost = Var(m.SHUTDOWN_COST_PROJECT_OPERATIONAL_TIMEPOINTS,
                          within=NonNegativeReals)

    def startup_cost_rule(mod, g, tmp):
        """
        Startup expression is positive when more units are on in the current
        timepoint that were on in the previous timepoint. Startup_Cost is
        defined to be non-negative, so if Startup_Expression is 0 or negative
        (i.e. no units started or units shut down since the previous timepoint),
        Startup_Cost will be 0.
        If horizon is circular, the last timepoint of the horizon is the
        previous_timepoint for the first timepoint if the horizon;
        if the horizon is linear, no previous_timepoint is defined for the first
        timepoint of the horizon, so skip constraint.
        :param mod:
        :param g:
        :param tmp:
        :return:
        """
        if tmp == mod.first_horizon_timepoint[mod.horizon[tmp]] \
                and mod.boundary[mod.horizon[tmp]] == "linear":
            return Constraint.Skip
        else:
            return mod.Startup_Cost[g, tmp] \
                   >= mod.Startup_Expression[g, tmp] \
                      * mod.startup_cost_per_unit[g]

    m.Startup_Cost_Constraint = \
        Constraint(m.STARTUP_COST_PROJECT_OPERATIONAL_TIMEPOINTS,
                   rule=startup_cost_rule)

    def shutdown_cost_rule(mod, g, tmp):
        """
        Shutdown expression is positive when more units were on in the previous
        timepoint that are on in the current timepoint. Shutdown_Cost is
        defined to be non-negative, so if Shutdown_Expression is 0 or negative
        (i.e. no units shut down or units started since the previous timepoint),
        Shutdown_Cost will be 0.
        If horizon is circular, the last timepoint of the horizon is the
        previous_timepoint for the first timepoint if the horizon;
        if the horizon is linear, no previous_timepoint is defined for the first
        timepoint of the horizon, so skip constraint.
        :param mod:
        :param g:
        :param tmp:
        :return:
        """
        if tmp == mod.first_horizon_timepoint[mod.horizon[tmp]] \
                and mod.boundary[mod.horizon[tmp]] == "linear":
            return Constraint.Skip
        else:
            return mod.Shutdown_Cost[g, tmp] \
                   >= mod.Shutdown_Expression[g, tmp] \
                      * mod.shutdown_cost_per_unit[g]

    m.Shutdown_Cost_Constraint = Constraint(
        m.SHUTDOWN_COST_PROJECT_OPERATIONAL_TIMEPOINTS,
        rule=shutdown_cost_rule)



def export_results(scenario_directory, horizon, stage, m, d):
    """
    Export operations results.
    :param scenario_directory:
    :param horizon:
    :param stage:
    :param m:
    The Pyomo abstract model
    :param d:
    Dynamic components
    :return:
    Nothing
    """
    with open(os.path.join(scenario_directory, horizon, stage, "results",
                           "costs_operations_variable_om.csv"), "wb") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["project", "period", "horizon", "timepoint", "horizon_weight",
             "number_of_hours_in_timepoint", "load_zone",
             "technology", "variable_om_cost"]
        )
        for (p, tmp) in m.PROJECT_OPERATIONAL_TIMEPOINTS:
            writer.writerow([
                p,
                m.period[tmp],
                m.horizon[tmp],
                tmp,
                m.horizon_weight[m.horizon[tmp]],
                m.number_of_hours_in_timepoint[tmp],
                m.load_zone[p],
                m.technology[p],
                value(m.Variable_OM_Cost[p, tmp])
            ])

    with open(os.path.join(scenario_directory, horizon, stage, "results",
                           "costs_operations_fuel.csv"), "wb") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["project", "period", "horizon", "timepoint", "horizon_weight",
             "number_of_hours_in_timepoint", "load_zone",
             "technology", "fuel_cost"]
        )
        for (p, tmp) in m.FUEL_PROJECT_OPERATIONAL_TIMEPOINTS:
            writer.writerow([
                p,
                m.period[tmp],
                m.horizon[tmp],
                tmp,
                m.horizon_weight[m.horizon[tmp]],
                m.number_of_hours_in_timepoint[tmp],
                m.load_zone[p],
                m.technology[p],
                value(m.Fuel_Cost[p, tmp])
            ])

    with open(os.path.join(scenario_directory, horizon, stage, "results",
                           "costs_operations_startup.csv"), "wb") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["project", "period", "horizon", "timepoint", "horizon_weight",
             "number_of_hours_in_timepoint", "load_zone",
             "technology", "startup_cost"]
        )
        for (p, tmp) in m.STARTUP_COST_PROJECT_OPERATIONAL_TIMEPOINTS:
            writer.writerow([
                p,
                m.period[tmp],
                m.horizon[tmp],
                tmp,
                m.horizon_weight[m.horizon[tmp]],
                m.number_of_hours_in_timepoint[tmp],
                m.load_zone[p],
                m.technology[p],
                value(m.Startup_Cost[p, tmp])
            ])

    with open(os.path.join(scenario_directory, horizon, stage, "results",
                           "costs_operations_shutdown.csv"), "wb") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["project", "period", "horizon", "timepoint", "horizon_weight",
             "number_of_hours_in_timepoint", "load_zone",
             "technology", "shutdown_cost"]
        )
        for (p, tmp) in m.SHUTDOWN_COST_PROJECT_OPERATIONAL_TIMEPOINTS:
            writer.writerow([
                p,
                m.period[tmp],
                m.horizon[tmp],
                tmp,
                m.horizon_weight[m.horizon[tmp]],
                m.number_of_hours_in_timepoint[tmp],
                m.load_zone[p],
                m.technology[p],
                value(m.Shutdown_Cost[p, tmp])
            ])


def import_results_into_database(scenario_id, c, db, results_directory):
    """

    :param scenario_id:
    :param c:
    :param db:
    :param results_directory:
    :return:
    """
    print("project costs operations")

    # costs_operations_variable_om.csv
    c.execute(
        """DELETE FROM results_project_costs_operations_variable_om
        WHERE scenario_id = {};""".format(
            scenario_id
        )
    )
    db.commit()

    # Create temporary table, which we'll use to sort results and then drop
    c.execute(
        """DROP TABLE IF EXISTS
        temp_results_project_costs_operations_variable_om"""
        + str(scenario_id) + """;"""
    )
    db.commit()

    c.execute(
        """CREATE TABLE temp_results_project_costs_operations_variable_om"""
        + str(scenario_id) + """(
        scenario_id INTEGER,
        project VARCHAR(64),
        period INTEGER,
        horizon INTEGER,
        timepoint INTEGER,
        horizon_weight FLOAT,
        number_of_hours_in_timepoint FLOAT,
        load_zone VARCHAR(32),
        technology VARCHAR(32),
        variable_om_cost FLOAT,
        PRIMARY KEY (scenario_id, project, timepoint)
            );"""
    )
    db.commit()

    # Load results into the temporary table
    with open(os.path.join(results_directory,
                           "costs_operations_variable_om.csv"), "r") as \
            dispatch_file:
        reader = csv.reader(dispatch_file)

        reader.next()  # skip header
        for row in reader:
            project = row[0]
            period = row[1]
            horizon = row[2]
            timepoint = row[3]
            horizon_weight = row[4]
            number_of_hours_in_timepoint = row[5]
            load_zone = row[6]
            technology = row[7]
            variable_om_cost = row[8]
            c.execute(
                """INSERT INTO
                temp_results_project_costs_operations_variable_om"""
                + str(scenario_id) + """
                (scenario_id, project, period, horizon, timepoint,
                horizon_weight, number_of_hours_in_timepoint,
                load_zone, technology, variable_om_cost)
                VALUES ({}, '{}', {}, {}, {}, {}, {}, '{}', '{}',
                {});""".format(
                    scenario_id, project, period, horizon, timepoint,
                    horizon_weight, number_of_hours_in_timepoint,
                    load_zone, technology, variable_om_cost
                )
            )
    db.commit()

    # Insert sorted results into permanent results table
    c.execute(
        """INSERT INTO results_project_costs_operations_variable_om
        (scenario_id, project, period, horizon, timepoint,
        horizon_weight, number_of_hours_in_timepoint,
        load_zone, technology, variable_om_cost)
        SELECT
        scenario_id, project, period, horizon, timepoint,
        horizon_weight, number_of_hours_in_timepoint,
        load_zone, technology, variable_om_cost
        FROM temp_results_project_costs_operations_variable_om""" + str(
            scenario_id) + """
        ORDER BY scenario_id, project, timepoint;"""
    )
    db.commit()

    # Drop the temporary table
    c.execute(
        """DROP TABLE temp_results_project_costs_operations_variable_om""" + str(
            scenario_id) +
        """;"""
    )
    db.commit()

    # costs_operations_fuel.csv
    c.execute(
        """DELETE FROM results_project_costs_operations_fuel
        WHERE scenario_id = {};""".format(
            scenario_id
        )
    )
    db.commit()

    # Create temporary table, which we'll use to sort results and then drop
    c.execute(
        """DROP TABLE IF EXISTS
        temp_results_project_costs_operations_fuel"""
        + str(scenario_id) + """;"""
    )
    db.commit()

    c.execute(
        """CREATE TABLE temp_results_project_costs_operations_fuel"""
        + str(scenario_id) + """(
            scenario_id INTEGER,
            project VARCHAR(64),
            period INTEGER,
            horizon INTEGER,
            timepoint INTEGER,
            horizon_weight FLOAT,
            number_of_hours_in_timepoint FLOAT,
            load_zone VARCHAR(32),
            technology VARCHAR(32),
            fuel_cost FLOAT,
            PRIMARY KEY (scenario_id, project, timepoint)
                );"""
    )
    db.commit()

    # Load results into the temporary table
    with open(os.path.join(results_directory,
                           "costs_operations_fuel.csv"), "r") as \
            dispatch_file:
        reader = csv.reader(dispatch_file)

        reader.next()  # skip header
        for row in reader:
            project = row[0]
            period = row[1]
            horizon = row[2]
            timepoint = row[3]
            horizon_weight = row[4]
            number_of_hours_in_timepoint = row[5]
            load_zone = row[6]
            technology = row[7]
            fuel_cost = row[8]
            c.execute(
                """INSERT INTO
                temp_results_project_costs_operations_fuel"""
                + str(scenario_id) + """
                    (scenario_id, project, period, horizon, timepoint,
                    horizon_weight, number_of_hours_in_timepoint,
                    load_zone, technology, fuel_cost)
                    VALUES ({}, '{}', {}, {}, {}, {}, {}, '{}', '{}',
                    {});""".format(
                    scenario_id, project, period, horizon, timepoint,
                    horizon_weight, number_of_hours_in_timepoint,
                    load_zone, technology, fuel_cost
                )
            )
    db.commit()

    # Insert sorted results into permanent results table
    c.execute(
        """INSERT INTO results_project_costs_operations_fuel
        (scenario_id, project, period, horizon, timepoint,
        horizon_weight, number_of_hours_in_timepoint,
        load_zone, technology, fuel_cost)
        SELECT
        scenario_id, project, period, horizon, timepoint,
        horizon_weight, number_of_hours_in_timepoint,
        load_zone, technology, fuel_cost
        FROM temp_results_project_costs_operations_fuel""" + str(
            scenario_id) + """
            ORDER BY scenario_id, project, timepoint;"""
    )
    db.commit()

    # Drop the temporary table
    c.execute(
        """DROP TABLE temp_results_project_costs_operations_fuel""" + str(
            scenario_id) +
        """;"""
    )
    db.commit()

    # costs_operations_startup.csv
    c.execute(
        """DELETE FROM results_project_costs_operations_startup
        WHERE scenario_id = {};""".format(
            scenario_id
        )
    )
    db.commit()

    # Create temporary table, which we'll use to sort results and then drop
    c.execute(
        """DROP TABLE IF EXISTS
        temp_results_project_costs_operations_startup"""
        + str(scenario_id) + """;"""
    )
    db.commit()

    c.execute(
        """CREATE TABLE temp_results_project_costs_operations_startup"""
        + str(scenario_id) + """(
            scenario_id INTEGER,
            project VARCHAR(64),
            period INTEGER,
            horizon INTEGER,
            timepoint INTEGER,
            horizon_weight FLOAT,
            number_of_hours_in_timepoint FLOAT,
            load_zone VARCHAR(32),
            technology VARCHAR(32),
            startup_cost FLOAT,
            PRIMARY KEY (scenario_id, project, timepoint)
                );"""
    )
    db.commit()

    # Load results into the temporary table
    with open(os.path.join(results_directory,
                           "costs_operations_startup.csv"), "r") as \
            dispatch_file:
        reader = csv.reader(dispatch_file)

        reader.next()  # skip header
        for row in reader:
            project = row[0]
            period = row[1]
            horizon = row[2]
            timepoint = row[3]
            horizon_weight = row[4]
            number_of_hours_in_timepoint = row[5]
            load_zone = row[6]
            technology = row[7]
            startup_cost = row[8]
            c.execute(
                """INSERT INTO
                temp_results_project_costs_operations_startup"""
                + str(scenario_id) + """
                    (scenario_id, project, period, horizon, timepoint,
                    horizon_weight, number_of_hours_in_timepoint,
                    load_zone, technology, startup_cost)
                    VALUES ({}, '{}', {}, {}, {}, {}, {}, '{}', '{}',
                    {});""".format(
                    scenario_id, project, period, horizon, timepoint,
                    horizon_weight, number_of_hours_in_timepoint,
                    load_zone, technology, startup_cost
                )
            )
    db.commit()

    # Insert sorted results into permanent results table
    c.execute(
        """INSERT INTO results_project_costs_operations_startup
        (scenario_id, project, period, horizon, timepoint,
        horizon_weight, number_of_hours_in_timepoint,
        load_zone, technology, startup_cost)
        SELECT
        scenario_id, project, period, horizon, timepoint,
        horizon_weight, number_of_hours_in_timepoint,
        load_zone, technology, startup_cost
        FROM temp_results_project_costs_operations_startup""" + str(
            scenario_id) + """
            ORDER BY scenario_id, project, timepoint;"""
    )
    db.commit()

    # Drop the temporary table
    c.execute(
        """DROP TABLE temp_results_project_costs_operations_startup""" + str(
            scenario_id) +
        """;"""
    )
    db.commit()

    # costs_operations_shutdown.csv
    c.execute(
        """DELETE FROM results_project_costs_operations_shutdown
        WHERE scenario_id = {};""".format(
            scenario_id
        )
    )
    db.commit()

    # Create temporary table, which we'll use to sort results and then drop
    c.execute(
        """DROP TABLE IF EXISTS
        temp_results_project_costs_operations_shutdown"""
        + str(scenario_id) + """;"""
    )
    db.commit()

    c.execute(
        """CREATE TABLE temp_results_project_costs_operations_shutdown"""
        + str(scenario_id) + """(
            scenario_id INTEGER,
            project VARCHAR(64),
            period INTEGER,
            horizon INTEGER,
            timepoint INTEGER,
            horizon_weight FLOAT,
            number_of_hours_in_timepoint FLOAT,
            load_zone VARCHAR(32),
            technology VARCHAR(32),
            shutdown_cost FLOAT,
            PRIMARY KEY (scenario_id, project, timepoint)
                );"""
    )
    db.commit()

    # Load results into the temporary table
    with open(os.path.join(results_directory,
                           "costs_operations_shutdown.csv"), "r") as \
            dispatch_file:
        reader = csv.reader(dispatch_file)

        reader.next()  # skip header
        for row in reader:
            project = row[0]
            period = row[1]
            horizon = row[2]
            timepoint = row[3]
            horizon_weight = row[4]
            number_of_hours_in_timepoint = row[5]
            load_zone = row[6]
            technology = row[7]
            shutdown_cost = row[8]
            c.execute(
                """INSERT INTO
                temp_results_project_costs_operations_shutdown"""
                + str(scenario_id) + """
                    (scenario_id, project, period, horizon, timepoint,
                    horizon_weight, number_of_hours_in_timepoint,
                    load_zone, technology, shutdown_cost)
                    VALUES ({}, '{}', {}, {}, {}, {}, {}, '{}', '{}',
                    {});""".format(
                    scenario_id, project, period, horizon, timepoint,
                    horizon_weight, number_of_hours_in_timepoint,
                    load_zone, technology, shutdown_cost
                )
            )
    db.commit()

    # Insert sorted results into permanent results table
    c.execute(
        """INSERT INTO results_project_costs_operations_shutdown
        (scenario_id, project, period, horizon, timepoint,
        horizon_weight, number_of_hours_in_timepoint,
        load_zone, technology, shutdown_cost)
        SELECT
        scenario_id, project, period, horizon, timepoint,
        horizon_weight, number_of_hours_in_timepoint,
        load_zone, technology, shutdown_cost
        FROM temp_results_project_costs_operations_shutdown""" + str(
            scenario_id) + """
            ORDER BY scenario_id, project, timepoint;"""
    )
    db.commit()

    # Drop the temporary table
    c.execute(
        """DROP TABLE temp_results_project_costs_operations_shutdown""" + str(
            scenario_id) +
        """;"""
    )
    db.commit()