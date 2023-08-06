#!/usr/bin/env python
"""
Launch a production from a workflow description submitted by the user.

Usage:
    cta-prod-submit <name of the production> <YAML file of the production steps description>

Example:
    cta-prod-submit TestProd production_config.yml
"""

__RCSID__ = "$Id$"

from DIRAC.Core.Utilities.DIRACScript import DIRACScript as Script

Script.parseCommandLine()
import DIRAC
import yaml
import json

from DIRAC.ProductionSystem.Client.ProductionClient import ProductionClient

from CTADIRAC.ProductionSystem.Client.SimulationElement import SimulationElement
from CTADIRAC.ProductionSystem.Client.CtapipeModelingElement import (
    CtapipeModelingElement,
)
from CTADIRAC.ProductionSystem.Client.EvnDispElement import EvnDispElement
from CTADIRAC.ProductionSystem.Client.MergingElement import MergingElement


def check_id(job_list):
    """Check jobID values"""
    for job in job_list:
        if not job.get("ID"):
            DIRAC.gLogger.error("Unknown job ID")
            DIRAC.exit(-1)
        elif not isinstance(job["ID"], int):
            DIRAC.gLogger.error("job ID must be integer")
            DIRAC.exit(-1)
    return True


def sort_by_id(job_list):
    """Sort production steps by ID"""
    return sorted(job_list, key=lambda k: k["ID"])


def check_parents(job_list):
    """Check if parent step is listed before child step"""
    for job in job_list:
        if job.get("parentID"):
            if job["parentID"] > job["ID"]:
                DIRAC.gLogger.error(
                    "A step can only have a parent which ID is inferior to its ID"
                )
                DIRAC.exit(-1)
    return True


def instantiate_workflow_element_from_type(job, parent_prod_step):
    """Instantiate workflow element class based on the job type required"""
    wf_elt = None
    if job["type"].lower() == "mcsimulation":
        wf_elt = SimulationElement(parent_prod_step)
    elif job["type"].lower() == "ctapipeprocessing":
        wf_elt = CtapipeModelingElement(parent_prod_step)
    elif job["type"].lower() == "evndispprocessing":
        wf_elt = EvnDispElement(parent_prod_step)
    elif job["type"].lower() == "merging":
        wf_elt = MergingElement(parent_prod_step)
    else:
        DIRAC.gLogger.error("Unknown job type")
        DIRAC.exit(-1)
    return wf_elt


def find_parent_prod_step(prod_step_list, user_job):
    """Find parent step ID for a given job"""
    parent_prod_step = None
    if "parentID" in user_job:
        if user_job["parentID"] is not None:
            parent_prod_step = prod_step_list[
                user_job["parentID"] - 1
            ]  # Python starts indexing at 0
    return parent_prod_step


def parse_jobs(job_list, prod_sys_client):
    """For each workflow element, build its job and production step"""
    prod_step_list = []
    check_id(job_list["ProdSteps"])
    job_list["ProdSteps"] = sort_by_id(job_list["ProdSteps"])
    check_parents(job_list["ProdSteps"])

    for job in job_list["ProdSteps"]:
        parent_prod_step = find_parent_prod_step(prod_step_list, job)
        workflow_element = instantiate_workflow_element_from_type(job, parent_prod_step)
        workflow_element.build_job_attributes(job)
        workflow_element.build_job_common_attributes(job_list)
        workflow_element.build_input_data(job)
        workflow_element.build_element_config()
        workflow_element.build_output_data()

        DIRAC.gLogger.notice(
            "\tBuilt Production step: %s" % workflow_element.prod_step.Name
        )

        prod_step_list.append(workflow_element.prod_step)
        prod_sys_client.addProductionStep(workflow_element.prod_step)


@Script()
def main():
    arguments = Script.getPositionalArgs()
    if len(arguments) != 2:
        Script.showHelp()

    with open(arguments[1], "r") as stream:
        user_sub = yaml.safe_load(stream)

    ##################################
    # Create the production
    prod_name = "Prod6Test_workflow_%s" % arguments[0]
    DIRAC.gLogger.notice("Building new production: %s" % prod_name)
    prod_sys_client = ProductionClient()

    ##################################
    # Build production steps according to the user submission of the workflow
    parse_jobs(user_sub, prod_sys_client)

    ##################################
    # Get the production description
    prod_description = prod_sys_client.prodDescription
    # Create the production
    DIRAC.gLogger.notice("Creating production.")
    res = prod_sys_client.addProduction(prod_name, json.dumps(prod_description))
    if not res["OK"]:
        DIRAC.gLogger.error(res["Message"])
        DIRAC.exit(-1)

    # Start the production, i.e. instantiate the transformation steps
    res = prod_sys_client.startProduction(prod_name)

    if not res["OK"]:
        DIRAC.gLogger.error(res["Message"])
        DIRAC.exit(-1)

    DIRAC.gLogger.notice("Production %s successfully created" % prod_name)


########################################################
if __name__ == "__main__":
    main()
