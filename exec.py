import os
import pandas as pd 
from smoldyn.biosimulators.combine import exec_sed_doc
from biosimulators_utils.report.data_model import ReportFormat
from biosimulators_utils.config import Config
from smoldyn import Simulation 


class SmoldynSimulation:

   def __init__(self, working_dir: str):
      self.working_dir = working_dir

   def run(self):
      current_dir = os.getcwd()
      all_paths = [os.path.join(current_dir, f) for f in os.listdir(self.working_dir)]
      for p in all_paths:
         if 'sedml' in p:
            config = Config(REPORT_FORMATS=[ReportFormat.csv])
            exec_sed_doc(doc=p, working_dir=self.working_dir, base_out_path=current_dir)
         if 'model.txt' in p:
            simulation = Simulation.fromFile(p)
            simulation.addOutputData('molecules')
            simulation.addCommand(cmd='listmols molecules', cmd_type='E')
            simulation.run(simulation.stop, simulation.dt)
            outputs = simulation.getOutputData('molecules')
            cols = ['identity', 'state', 'x', 'y', 'z', 'serial_number']
            df = pd.DataFrame(data=outputs, columns=cols)
            df.to_csv(os.path.join(os.getcwd(), 'MinE_output.csv'), index=False)



sim = SmoldynSimulation(os.getcwd())
sim.run()