"""
   Wrapper around the job class to build a workflow element (production step + job)
"""

__RCSID__ = "$Id$"

# DIRAC imports
import DIRAC
from DIRAC.Interfaces.API.Job import Job
from DIRAC.ProductionSystem.Client.ProductionStep import ProductionStep
from CTADIRAC.Core.Utilities.tool_box import get_dataset_MQ


class WorkflowElement:
    """Composite class for workflow element (production step + job)"""

    #############################################################################

    def __init__(self, parent_prod_step):
        """Constructor"""
        self.job = Job()
        self.job.setOutputSandbox(["*Log.txt"])
        self.prod_step = ProductionStep()
        self.parent_step = parent_prod_step

    def build_job_attributes(self, user_job):
        """Set job attributes"""
        for key, value in user_job.items():
            if key == "version":
                if value is None:
                    DIRAC.gLogger.error(
                        "Unknown software version for ProdStep %s" % user_job["ID"]
                    )
                    DIRAC.exit(-1)
                else:
                    self.job.version = value
            else:
                if value is not None:
                    setattr(self.job, key, value)

    def build_job_common_attributes(self, user_sub):
        """Set job attributes concerning the whole production"""
        if "base_path" in user_sub["Common"]:
            if user_sub["Common"]["base_path"]:
                self.job.base_path = user_sub["Common"]["base_path"]
        if "MCCampaign" in user_sub["Common"]:
            if user_sub["Common"]["MCCampaign"]:
                self.job.MCCampaign = user_sub["Common"]["MCCampaign"]
            else:
                DIRAC.gLogger.error("MCCampaign is mandatory")
                DIRAC.exit(-1)
        if "configuration_id" in user_sub["Common"]:
            if user_sub["Common"]["configuration_id"]:
                self.job.configuration_id = user_sub["Common"]["configuration_id"]
            else:
                DIRAC.gLogger.error("configuration_id is mandatory")
                DIRAC.exit(-1)

    def build_input_data(self, user_job):
        """Build input data from the parent output data or from the dataset metadata"""
        if self.parent_step:
            self.prod_step.Inputquery = self.parent_step.Outputquery
            for key, value in self.job.output_file_metadata.items():
                self.prod_step.Inputquery[key] = value

        else:
            if user_job.get("dataset"):
                self.prod_step.Inputquery = get_dataset_MQ(user_job["dataset"])

            else:
                DIRAC.gLogger.error(
                    "A step without parent step must take a dataset as input"
                )
                DIRAC.exit(-1)

    def build_output_data(self):
        """Build output data from the job metadata and the metadata added on the files"""
        self.prod_step.Outputquery = self.job.output_metadata
        for key, value in self.job.output_file_metadata.items():
            self.prod_step.Outputquery[key] = value


#############################################################################
