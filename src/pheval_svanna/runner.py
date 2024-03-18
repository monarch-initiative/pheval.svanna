"""SvAnna Runner"""

from dataclasses import dataclass
from pathlib import Path

from pheval.runners.runner import PhEvalRunner

from pheval_svanna.post_process.post_process import post_process_results_format
from pheval_svanna.run.run import prepare_svanna_commands, run_svanna_local
from pheval_svanna.tool_specific_configuration_parser import SvAnnaToolSpecificConfigurations


@dataclass
class SvAnnaPhEvalRunner(PhEvalRunner):
    """_summary_"""

    input_dir: Path
    testdata_dir: Path
    tmp_dir: Path
    output_dir: Path
    config_file: Path
    version: str

    def prepare(self):
        """prepare"""
        print("preparing")

    def run(self):
        """run"""
        print("running with SvAnna")
        config = SvAnnaToolSpecificConfigurations.parse_obj(
            self.input_dir_config.tool_specific_configuration_options
        )
        prepare_svanna_commands(
            input_dir=self.input_dir,
            testdata_dir=self.testdata_dir,
            raw_results_dir=self.raw_results_dir,
            tool_input_commands_dir=self.tool_input_commands_dir,
            tool_specific_configurations=config,
        )
        run_svanna_local(
            testdata_dir=self.testdata_dir, tool_input_commands_dir=self.tool_input_commands_dir
        )

    def post_process(self):
        """post_process"""
        print("post processing")
        config = SvAnnaToolSpecificConfigurations.parse_obj(
            self.input_dir_config.tool_specific_configuration_options
        )
        post_process_results_format(
            raw_results_dir=self.raw_results_dir, output_dir=self.output_dir, config=config
        )
