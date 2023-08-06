"""
   Wrapper around the job class to build a workflow element (production step + job)
"""


__RCSID__ = "$Id$"


# DIRAC imports
import DIRAC
from CTADIRAC.Interfaces.API.MCPipeNSBJob import MCPipeNSBJob
from CTADIRAC.ProductionSystem.Client.WorkflowElement import WorkflowElement


class SimulationElement(WorkflowElement):
    """Composite class for workflow element (production step + job)"""

    #############################################################################

    def __init__(self, parent_prod_step):
        """Constructor"""
        WorkflowElement.__init__(self, parent_prod_step)
        self.job = MCPipeNSBJob()
        self.job.setOutputSandbox(["*Log.txt"])
        self.prod_step.Type = "MCSimulation"

    def build_job_attributes(self, user_job):
        """Set job attributes, with some limitations for corsika arguments which need default values"""
        with_sct = False
        for key, value in user_job.items():
            if key == "version":
                if value is None:
                    DIRAC.gLogger.error(
                        "Unknown software version for ProdStep %s" % user_job["ID"]
                    )
                    DIRAC.exit(-1)
                else:
                    self.job.version = str(value)
            elif key == "site":
                self.job.set_site(value)
            elif key == "particle":
                self.job.set_particle(value)
            elif key == "pointing_dir":
                self.job.set_pointing_dir(value)
            elif key == "sct":
                with_sct = value  # keep the value for later because we also need the version to call set_sct
            elif key == "moon":
                self.job.set_moon(value)
            elif key == "magic":
                self.job.set_magic(value)
            else:
                if value is not None:
                    setattr(self.job, key, value)
        self.job.set_sct_file(with_sct)

    def build_input_data(self, user_job):
        """Simulation Elements do not have input data"""
        self.prod_step.Inputquery = {}

    def build_element_config(self):
        """Set job and production step attributes specific to the configuration"""
        self.prod_step.Name = "MC_Simulation"
        self.job.set_output_metadata()
        self.job.set_executable_sequence(debug=False)
        self.prod_step.Body = self.job.workflow.toXML()

    def build_output_data(self):
        """Build output data from the job metadata and the metadata added on the files"""
        self.prod_step.Outputquery = self.job.output_metadata
        if self.job.moon == "--with-full-moon":
            self.prod_step.Outputquery["nsb"] = {"in": [1, 5, 19]}
        elif self.job.moon == "--with-half-moon":
            self.prod_step.Outputquery["nsb"] = {"in": [1, 5]}
        else:
            self.prod_step.Outputquery["nsb"] = {"in": [1]}

    #############################################################################
