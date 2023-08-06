"""
   Wrapper around the job class to build a workflow element (production step + job)
"""


__RCSID__ = "$Id$"


# generic imports
from copy import deepcopy

# DIRAC imports
import DIRAC
from CTADIRAC.Interfaces.API.Prod5CtaPipeModelingJob import Prod5CtaPipeModelingJob
from CTADIRAC.ProductionSystem.Client.WorkflowElement import WorkflowElement


class CtapipeModelingElement(WorkflowElement):
    """Composite class for workflow element (production step + job)"""

    #############################################################################

    def __init__(self, parent_prod_step):
        """Constructor"""
        WorkflowElement.__init__(self, parent_prod_step)
        self.job = Prod5CtaPipeModelingJob(cpuTime=259200.0)
        self.prod_step.Type = "DataReprocessing"

    def build_job_attributes(self, user_job):
        """Set job attributes, with some limitations for file-specific arguments"""
        for key, value in user_job.items():
            if key == "version":
                if value is None:
                    DIRAC.gLogger.error(
                        "Unknown software version for ProdStep %s" % user_job["ID"]
                    )
                    DIRAC.exit(-1)
                else:
                    self.job.version = value
            elif (key == "nsb") & (value is not None):
                self.job.set_output_file_metadata(key, value)
            elif (key == "split") & (value is not None):
                self.job.set_output_file_metadata(key, value)
            else:
                if value is not None:
                    setattr(self.job, key, value)

    def build_element_config(self):
        """Set job and production step attributes specific to the configuration"""
        self.prod_step.Name = "Modeling_ctapipe"
        self.prod_step.GroupSize = self.job.group_size
        meta_data = deepcopy(self.prod_step.Inputquery)
        self.job.set_output_metadata(meta_data)
        self.job.set_executable_sequence(debug=False)
        self.prod_step.Body = self.job.workflow.toXML()

    #############################################################################
