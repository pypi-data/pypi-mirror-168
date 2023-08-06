#!/usr/bin/env python3

"""Module containing the GOdMDRun class and the command line interface."""
import argparse
import shutil, re, os
from pathlib import Path, PurePath
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_godmd.godmd.common import *

class GOdMDRun(BiobbObject):
    """
    | biobb_godmd GOdMDRun
    | Wrapper of the `GOdMD tool <http://mmb.irbbarcelona.org/GOdMD/>`_ module.
    | Computes conformational transition trajectories for proteins using GOdMD tool.

    Args:
        input_pdb_orig_path (str): Input PDB file to be used as origin in the conformational transition. File type: input. `Sample file <https://github.com/bioexcel/biobb_godmd/raw/master/biobb_godmd/test/data/godmd/1ake_A.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_pdb_target_path (str): Input PDB file to be used as target in the conformational transition. File type: input. `Sample file <https://github.com/bioexcel/biobb_godmd/raw/master/biobb_godmd/test/data/godmd/4ake_A.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_aln_orig_path (str): Input GOdMD alignment file corresponding to the origin structure of the conformational transition. File type: input. `Sample file <https://github.com/bioexcel/biobb_godmd/raw/master/biobb_godmd/test/data/godmd/1ake_A.aln>`_. Accepted formats: aln (edam:format_2330), txt (edam:format_2330).
        input_aln_target_path (str): Input GOdMD alignment file corresponding to the target structure of the conformational transition. File type: input. `Sample file <https://github.com/bioexcel/biobb_godmd/raw/master/biobb_godmd/test/data/godmd/4ake_A.aln>`_. Accepted formats: aln (edam:format_2330), txt (edam:format_2330).
        input_config_path (str) (Optional): Input GOdMD configuration file. File type: input. `Sample file <https://github.com/bioexcel/biobb_godmd/raw/master/biobb_godmd/test/data/godmd/params.in>`_. Accepted formats: in (edam:format_2330), txt (edam:format_2330).
        output_log_path (str): Output log file. File type: output. `Sample file <https://github.com/bioexcel/biobb_godmd/raw/master/biobb_godmd/test/reference/godmd/godmd.log>`_. Accepted formats: log (edam:format_2330), out (edam:format_2330), txt (edam:format_2330), o (edam:format_2330).
        output_ener_path (str): Output energy file. File type: output. `Sample file <https://github.com/bioexcel/biobb_godmd/raw/master/biobb_godmd/test/reference/godmd/godmd_ene.out>`_. Accepted formats: log (edam:format_2330), out (edam:format_2330), txt (edam:format_2330), o (edam:format_2330).
        output_trj_path (str): Output trajectory file. File type: output. `Sample file <https://github.com/bioexcel/biobb_godmd/raw/master/biobb_godmd/test/reference/godmd/godmd_trj.mdcrd>`_. Accepted formats: trj (edam:format_3878), crd (edam:format_3878), mdcrd (edam:format_3878), x (edam:format_3878).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **godmdin** (*dict*) - ({}) GOdMD options specification. 
            * **binary_path** (*str*) - ("discrete") Binary path.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_godmd.godmd.godmd_run import godmd_run
            prop = {
                'remove_tmp': True
            }
            godmd_run(   input_pdb_orig_path='/path/to/pdb_orig.pdb',
                         input_pdb_target_path='/path/to/pdb_target.pdb',
                         input_aln_orig_path='/path/to/aln_orig.aln',
                         input_aln_target_path='/path/to/aln_target.aln',
                         output_log_path='/path/to/godmd_log.log',
                         output_ene_path='/path/to/godmd_ene.txt',
                         output_trj_path='/path/to/godmd_trj.mdcrd',
                         properties=prop)

    Info:
        * wrapped_software:
            * name: GOdMD
            * version: >=1.0
            * license: Apache-2.0
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """
    def __init__(self, input_pdb_orig_path: str, input_pdb_target_path: str,
    input_aln_orig_path: str, input_aln_target_path: str, input_config_path: str,
    output_log_path: str, output_ene_path: str, output_trj_path: str, 
    properties: dict = None, **kwargs) -> None:

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)

        # Input/Output files
        self.io_dict = {
            'in': { 'input_pdb_orig_path': input_pdb_orig_path,
                    'input_pdb_target_path': input_pdb_target_path,
                    'input_aln_orig_path': input_aln_orig_path,
                    'input_aln_target_path': input_aln_target_path,
                    'input_config_path': input_config_path,
            },
            'out': { 'output_log_path': output_log_path,
                     'output_ene_path': output_ene_path,
                     'output_trj_path': output_trj_path 
            }
        }

        # Properties specific for BB
        self.properties = properties
        self.godmdin = {k: str(v) for k, v in properties.get('godmdin', dict()).items()}
        self.binary_path = properties.get('binary_path', "discrete")

        # Check the properties
        self.check_properties(properties)

    def check_data_params(self, out_log, out_err):
        """ Checks input/output paths correctness """

        # Check input(s)
        self.io_dict["in"]["input_pdb_orig_path"] = check_input_path(self.io_dict["in"]["input_pdb_orig_path"], "input_pdb_orig_path", False, out_log, self.__class__.__name__)
        self.io_dict["in"]["input_pdb_target_path"] = check_input_path(self.io_dict["in"]["input_pdb_target_path"], "input_pdb_target_path", False, out_log, self.__class__.__name__)
        self.io_dict["in"]["input_aln_orig_path"] = check_input_path(self.io_dict["in"]["input_aln_orig_path"], "input_aln_orig_path", False, out_log, self.__class__.__name__)
        self.io_dict["in"]["input_aln_target_path"] = check_input_path(self.io_dict["in"]["input_aln_target_path"], "input_aln_target_path", False, out_log, self.__class__.__name__)
        self.io_dict["in"]["input_config_path"] = check_input_path(self.io_dict["in"]["input_config_path"], "input_config_path", True, out_log, self.__class__.__name__)

        # Check output(s)
        self.io_dict["out"]["output_log_path"] = check_output_path(self.io_dict["out"]["output_log_path"],"output_log_path", False, out_log, self.__class__.__name__)
        self.io_dict["out"]["output_ene_path"] = check_output_path(self.io_dict["out"]["output_ene_path"],"output_ene_path", False, out_log, self.__class__.__name__)
        self.io_dict["out"]["output_trj_path"] = check_output_path(self.io_dict["out"]["output_trj_path"],"output_trj_path", False, out_log, self.__class__.__name__)

    def create_godmdin(self, path: str = None) -> str:
        """Creates a GOdMD configuration file (godmdin) using the properties file settings"""
        godmdin_list = []

        self.output_godmdin_path = path

        if self.io_dict['in']['input_config_path']:
            # GOdMD input parameters read from an input godmdin file
            with open(self.io_dict['in']['input_config_path']) as input_params:
                for line in input_params:
                    if '=' in line:
                        godmdin_list.append(line.upper())
        else:
            # Pre-configured simulation type parameters
            godmdin_list.append("  TSNAP = 500 ! BioBB GOdMD default params \n")
            godmdin_list.append("  TEMP = 300 ! BioBB GOdMD default params \n")
            godmdin_list.append("  SEED = 2525 ! BioBB GOdMD default params \n")
            godmdin_list.append("  ENER_EVO_SIZE = 20 ! BioBB GOdMD default params \n")
            godmdin_list.append("  NBLOC = 10000 ! BioBB GOdMD default params \n")
            godmdin_list.append("  ERRORACCEPTABLE = 1.5 ! BioBB GOdMD default params \n")

        # Adding the rest of parameters in the config file to the mdin file
        # if the parameter has already been added replace the value
        parameter_keys = [parameter.split('=')[0].strip() for parameter in godmdin_list]
        for k, v in self.godmdin.items():
            config_parameter_key = str(k).strip().upper()
            if config_parameter_key in parameter_keys:
                godmdin_list[parameter_keys.index(config_parameter_key)] = '\t' + config_parameter_key + ' = ' + str(v) + ' ! BioBB property \n'
            else:
                godmdin_list.append('\t' + config_parameter_key + ' = '+str(v) + ' ! BioBB property \n')

        # Writing MD configuration file (mdin)
        with open(self.output_godmdin_path, 'w') as godmdin:

            # GOdMDIN parameters added by the biobb_godmd module
            godmdin.write("!This godmdin file has been created by the biobb_godmd module from the BioBB library \n\n")

            godmdin.write("&INPUT\n")

            # MD config parameters
            for line in godmdin_list:
                godmdin.write(line)

            godmdin.write("&END\n")

        return self.output_godmdin_path


    @launchlogger
    def launch(self):
        """Launches the execution of the GOdMDRun module."""

        # check input/output paths and parameters
        self.check_data_params(self.out_log, self.err_log)

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir()
        fu.log('Creating %s temporary folder' % self.tmp_folder, self.out_log)

        # Creating GOdMD input file
        self.output_godmdin_path = self.create_godmdin(path=str(Path(self.tmp_folder).joinpath("godmd.in")))

        # Command line
        # discrete -i $fileName.in -pdbin $pdbch1 -pdbtarg $pdbch2 -ener $fileName.ene -trj $fileName.crd -p1 $alignFile1 -p2 $alignFile2 -o $fileName.log >& $fileName.out
        self.cmd = [self.binary_path,
               #'-i', self.io_dict["in"]["input_config_path"],
               '-i', self.output_godmdin_path,
               '-pdbin', self.io_dict["in"]["input_pdb_orig_path"],
               '-pdbtarg', self.io_dict["in"]["input_pdb_target_path"],
               '-p1', self.io_dict["in"]["input_aln_orig_path"],
               '-p2', self.io_dict["in"]["input_aln_target_path"],
               '-o', self.io_dict["out"]["output_log_path"],
               '-ener', self.io_dict["out"]["output_ene_path"],
               '-trj', self.io_dict["out"]["output_trj_path"]
               ]

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        # Remove temporary folder(s)
        if self.remove_tmp:
            self.tmp_files.append(self.tmp_folder)
            self.remove_tmp_files()

        return self.return_code

def godmd_run(input_pdb_orig_path: str, input_pdb_target_path: str,
    input_aln_orig_path: str, input_aln_target_path: str, 
    output_log_path: str, output_ene_path: str, output_trj_path: str,
    input_config_path: str = None, properties: dict = None, **kwargs) -> int:
    """Create :class:`GOdMDRun <godmd.godmd_run.GOdMDRun>`godmd.godmd_run.GOdMDRun class and
    execute :meth:`launch() <godmd.godmd_run.GOdMDRun.launch>` method"""

    return GOdMDRun( input_pdb_orig_path=input_pdb_orig_path,
                    input_pdb_target_path=input_pdb_target_path,
                    input_aln_orig_path=input_aln_orig_path,
                    input_aln_target_path=input_aln_target_path,
                    input_config_path=input_config_path,
                    output_log_path=output_log_path,
                    output_ene_path=output_ene_path,
                    output_trj_path=output_trj_path,
                    properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Computing conformational transition trajectories for proteins using GOdMD tool.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pdb_orig_path', required=True, help='Input PDB file to be used as origin in the conformational transition. Accepted formats: pdb.')
    required_args.add_argument('--input_pdb_target_path', required=True, help='Input PDB file to be used as target in the conformational transition. Accepted formats: pdb.')
    required_args.add_argument('--input_aln_orig_path', required=True, help='Input GOdMD alignment file corresponding to the origin structure of the conformational transition. Accepted formats: aln, txt.')
    required_args.add_argument('--input_aln_target_path', required=True, help='Input GOdMD alignment file corresponding to the target structure of the conformational transition. Accepted formats: aln, txt.')
    required_args.add_argument('--input_config_path', required=False, help='Input configuration file (GOdMD run options). Accepted formats: in, txt.')
    required_args.add_argument('--output_log_path', required=True, help='Output log file. Accepted formats: log, out, txt.')
    required_args.add_argument('--output_ene_path', required=True, help='Output energy file. Accepted formats: log, out, txt.')
    required_args.add_argument('--output_trj_path', required=True, help='Output trajectory file. Accepted formats: mdcrd.')

    args = parser.parse_args()
    #config = args.config if args.config else None
    args.config = args.config or "{}"
    #properties = settings.ConfReader(config=config).get_prop_dic()
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call
    godmd_run(      input_pdb_orig_path=args.input_pdb_orig_path,
                    input_pdb_target_path=args.input_pdb_target_path,
                    input_aln_orig_path=args.input_aln_orig_path,
                    input_aln_target_path=args.input_aln_target_path,
                    input_config_path=args.input_config_path,
                    output_log_path=args.output_log_path,
                    output_ene_path=args.output_ene_path,
                    output_trj_path=args.output_trj_path,
                    properties=properties)

if __name__ == '__main__':
    main()
