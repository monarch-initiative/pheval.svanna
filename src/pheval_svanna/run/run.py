import subprocess
from pathlib import Path

from pheval.utils.file_utils import all_files

from pheval_svanna.prepare.prepare_commands import prepare_commands
from pheval_svanna.tool_specific_configuration_parser import SvAnnaToolSpecificConfigurations


def prepare_svanna_commands(
    input_dir: Path,
    tool_input_commands_dir: Path,
    raw_results_dir: Path,
    testdata_dir: Path,
    tool_specific_configurations: SvAnnaToolSpecificConfigurations,
):
    """Write commands to run SvAnna."""
    phenopacket_dir = Path(testdata_dir).joinpath("phenopackets")
    vcf_dir = Path(testdata_dir).joinpath("vcf")
    prepare_commands(
        svanna_jar_file=input_dir.joinpath(tool_specific_configurations.svanna_jar_executable),
        output_dir=tool_input_commands_dir,
        file_prefix=Path(testdata_dir).name,
        phenopacket_dir=phenopacket_dir,
        vcf_dir=vcf_dir,
        results_dir=raw_results_dir,
        output_format=["tsv"],
        input_data=input_dir,
    )


def run_svanna_local(tool_input_commands_dir: Path, testdata_dir: Path):
    """Run SvAnna locally."""
    batch_file = [
        file
        for file in all_files(Path(tool_input_commands_dir))
        if file.name.startswith(Path(testdata_dir).name)
    ][0]
    print("running SvAnna")
    subprocess.run(
        ["bash", str(batch_file)],
        shell=False,
    )
