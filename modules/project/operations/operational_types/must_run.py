#!/usr/bin/env python

"""
Operations of must-run generators. Can't provide reserves.
"""

from pyomo.environ import Constraint, Set

from modules.auxiliary.auxiliary import generator_subset_init


def add_module_specific_components(m, d):
    """

    :param m:
    :return:
    """

    m.MUST_RUN_GENERATORS = Set(within=m.PROJECTS,
                                initialize=generator_subset_init(
                                    "operational_type", "must_run")
                                )

    m.MUST_RUN_GENERATOR_OPERATIONAL_TIMEPOINTS = \
        Set(dimen=2,
            rule=lambda mod:
            set((g, tmp) for (g, tmp) in mod.PROJECT_OPERATIONAL_TIMEPOINTS
                if g in mod.MUST_RUN_GENERATORS))


def power_provision_rule(mod, g, tmp):
    """
    Power provision for must run generators is their capacity.
    :param mod:
    :param g:
    :param tmp:
    :return:
    """
    return mod.Capacity_MW[g, mod.period[tmp]]


def max_power_rule(mod, g, tmp):
    """
    No variables to constrain for must-run generators.
    :param mod:
    :param g:
    :param tmp:
    :return:
    """
    return Constraint.Skip


def min_power_rule(mod, g, tmp):
    """
    No variables to constrain for must-run generators.
    :param mod:
    :param g:
    :param tmp:
    :return:
    """
    return Constraint.Skip


def curtailment_rule(mod, g, tmp):
    """
    Can't dispatch down and curtailment not allowed
    :param mod:
    :param g:
    :param tmp:
    :return:
    """
    return 0


# TODO: add data check that minimum_input_mmbtu_per_hr is 0 for must-run gens
# TODO: change when can-build-new
def fuel_cost_rule(mod, g, tmp):
    """
    Output doesn't vary, so this is
    :param mod:
    :param g:
    :param tmp:
    :return:
    """
    return mod.inc_heat_rate_mmbtu_per_mwh[g] * mod.Power_Provision_MW[g, tmp] \
        * mod.fuel_price_per_mmbtu[mod.fuel[g]]


def startup_rule(mod, g, tmp):
    """
    Must-run generators are never started up.
    :param mod:
    :param g:
    :param tmp:
    :return:
    """
    raise(ValueError(
        "ERROR! Must-run generators should not incur startup costs." + "\n" +
        "Check input data for generator '{}'".format(g) + "\n" +
        "and change its startup costs to '.' (no value).")
    )


def shutdown_rule(mod, g, tmp):
    """
    Must-run generators are never started up.
    :param mod:
    :param g:
    :param tmp:
    :return:
    """
    raise(ValueError(
        "ERROR! Must-run generators should not incur shutdown costs." + "\n" +
        "Check input data for generator '{}'".format(g) + "\n" +
        "and change its shutdown costs to '.' (no value).")
    )