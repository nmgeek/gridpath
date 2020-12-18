# Copyright 2016-2020 Blue Marble Analytics LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from __future__ import absolute_import

from .reserve_balance import generic_add_model_components, \
    generic_export_results, generic_save_duals, \
    generic_import_results_to_database


def add_model_components(m, d, subproblem_stage_directory):
    """

    :param m:
    :param d:
    :return:
    """

    generic_add_model_components(
        m=m,
        d=d,
        reserve_zone_set="SPINNING_RESERVES_ZONES",
        reserve_violation_variable="Spinning_Reserves_Violation_MW",
        reserve_violation_expression
        ="Spinning_Reserves_Violation_MW_Expression",
        reserve_violation_allowed_param="spinning_reserves_allow_violation",
        reserve_requirement_expression="Spin_Requirement",
        total_reserve_provision_expression
        ="Total_Spinning_Reserves_Provision_MW",
        meet_reserve_constraint="Meet_Spinning_Reserves_Constraint"
        )


def export_results(scenario_directory, subproblem, stage, m, d, subproblem_stage_directory):
    """

    :param scenario_directory:
    :param subproblem:
    :param stage:
    :param m:
    :param d:
    :return:
    """
    generic_export_results(subproblem_stage_directory, m, d,
                           "spinning_reserves_violation.csv",
                           "spinning_reserves_violation_mw",
                           "SPINNING_RESERVES_ZONES",
                           "Spinning_Reserves_Violation_MW_Expression"
                           )


def save_duals(m):
    """

    :param m:
    :return:
    """
    generic_save_duals(m, "Meet_Spinning_Reserves_Constraint")


def import_results_into_database(
        scenario_id, subproblem, stage, c, db, results_directory, quiet
):
    """

    :param scenario_id:
    :param c:
    :param db:
    :param results_directory:
    :param quiet:
    :return:
    """
    if not quiet:
        print("system spinning reserves balance")

    generic_import_results_to_database(
        scenario_id=scenario_id,
        subproblem=subproblem,
        stage=stage,
        c=c,
        db=db,
        results_directory=results_directory,
        reserve_type="spinning_reserves"
    )
