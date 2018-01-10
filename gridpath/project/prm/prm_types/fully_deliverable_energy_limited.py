#!/usr/bin/env python
# Copyright 2017 Blue Marble Analytics LLC. All rights reserved.

"""
Storage projects with additional constraints on deliverability based on their 
duration
"""

import csv
import os.path
from pyomo.environ import Param, Var, Set, Constraint, NonNegativeReals


def add_module_specific_components(m, d):
    """
    FDDL: Fully Deliverable Duration Limited
    :param m: 
    :param d: 
    :return: 
    """

    m.FDDL_PRM_PROJECTS = Set(
        within=m.PRM_PROJECTS,
        initialize=lambda mod:
        [p for p in mod.PRM_PROJECTS if mod.prm_type[p] ==
         "fully_deliverable_energy_limited"]
    )

    # Will limit this to storage project operational periods in addition to
    # PRM project operational periods
    m.FDDL_PRM_PROJECT_OPERATIONAL_PERIODS = Set(
        dimen=2,
        within=m.PRM_PROJECT_OPERATIONAL_PERIODS &
        m.STORAGE_OPERATIONAL_PERIODS,
        initialize=lambda mod: [
            (project, period)
            for (project, period) in mod.PRM_PROJECT_OPERATIONAL_PERIODS
            if project in mod.FDDL_PRM_PROJECTS
        ]
    )
    
    m.min_duration_for_full_capacity_credit = Param(
        m.FDDL_PRM_PROJECTS,
        within=NonNegativeReals
    ) 
    
    m.FDDL_Project_Capacity_Credit_Eligible_Capacity_MW = Var(
        m.FDDL_PRM_PROJECT_OPERATIONAL_PERIODS, 
        within=NonNegativeReals
    )

    def eligible_capacity_is_less_than_total_capacity_rule(mod, g, p):
        """
        The ELCC capacity can't exceed the total project capacity
        :param mod: 
        :param g: 
        :param p: 
        :return: 
        """
        return mod.FDDL_Project_Capacity_Credit_Eligible_Capacity_MW[g, p] \
            <= mod.Capacity_MW[g, p]

    m.Max_FDDL_Project_Capacity_Credit_Constraint = Constraint(
        m.FDDL_PRM_PROJECT_OPERATIONAL_PERIODS,
        rule=eligible_capacity_is_less_than_total_capacity_rule
    )

    def eligible_capacity_duration_derate_rule(mod, g, p):
        """
        The ELCC capacity can't exceed the total project capacity
        :param mod: 
        :param g: 
        :param p: 
        :return: 
        """
        return mod.FDDL_Project_Capacity_Credit_Eligible_Capacity_MW[g, p] \
            <= mod.Energy_Capacity_MWh[g, p] \
            / mod.min_duration_for_full_capacity_credit[g]

    m.FDDL_Project_Capacity_Credit_Duration_Derate_Constraint = Constraint(
        m.FDDL_PRM_PROJECT_OPERATIONAL_PERIODS,
        rule=eligible_capacity_duration_derate_rule
    )
    

def elcc_eligible_capacity_rule(mod, g, p):
    """
    
    :param mod: 
    :param g: 
    :param p: 
    :return: 
    """
    return mod.FDDL_Project_Capacity_Credit_Eligible_Capacity_MW[g, p]


def load_module_specific_data(
            m, data_portal, scenario_directory, horizon, stage
    ):
    """

    :param m:
    :param data_portal:
    :param scenario_directory:
    :param horizon:
    :param stage:
    :return:
    """
    data_portal.load(filename=os.path.join(scenario_directory,
                                           "inputs", "projects.tab"),
                     select=("project",
                             "minimum_duration_for_full_capacity_credit_hours"
                             ),
                     param=m.min_duration_for_full_capacity_credit
                     )


def get_module_specific_inputs_from_database(
        subscenarios, c, inputs_directory
):
    """

    :param subscenarios
    :param c:
    :param inputs_directory:
    :return:
    """
    
    project_zone_dur = c.execute(
        """SELECT project, prm_zone, 
        min_duration_for_full_capacity_credit_hours
        FROM 
        (SELECT project, prm_zone
        FROM inputs_project_prm_zones
        WHERE prm_zone_scenario_id = {}
        AND project_prm_zone_scenario_id = {}) as prj_tbl
        LEFT OUTER JOIN 
        (SELECT project, min_duration_for_full_capacity_credit_hours 
        FROM inputs_project_elcc_chars
        WHERE project_elcc_chars_scenario_id = {}) as min_dur_tbl
        USING (project);""".format(
            subscenarios.PRM_ZONE_SCENARIO_ID,
            subscenarios.PROJECT_PRM_ZONE_SCENARIO_ID,
            subscenarios.PROJECT_ELCC_CHARS_SCENARIO_ID
        )
    ).fetchall()

    # Make a dict for easy access
    # Only assign a min duration to projects that contribute to a PRM zone in
    # case we have projects with missing zones here
    prj_zone_dur_dict = dict()
    for (prj, zone, min_dur) in project_zone_dur:
        prj_zone_dur_dict[str(prj)] = \
            "." if zone is None else min_dur

    with open(os.path.join(inputs_directory, "projects.tab"), "r"
              ) as projects_file_in:
        reader = csv.reader(projects_file_in, delimiter="\t")

        new_rows = list()

        # Append column header
        header = reader.next()
        header.append("minimum_duration_for_full_capacity_credit_hours")
        new_rows.append(header)

        # Append correct values
        for row in reader:
            if row[0] in prj_zone_dur_dict.keys():
                row.append(".") if prj_zone_dur_dict[row[0]] is None \
                    else row.append(prj_zone_dur_dict[row[0]])
                new_rows.append(row)
            # If project not specified
            else:
                row.append(".")
                new_rows.append(row)

    with open(os.path.join(inputs_directory, "projects.tab"), "w") as \
            projects_file_out:
        writer = csv.writer(projects_file_out, delimiter="\t")
        writer.writerows(new_rows)