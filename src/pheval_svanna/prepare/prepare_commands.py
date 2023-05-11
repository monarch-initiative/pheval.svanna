from dataclasses import dataclass
from pathlib import Path

import click
from pheval.utils.file_utils import all_files
from pheval.utils.phenopacket_utils import PhenopacketUtil, phenopacket_reader


@dataclass
class SvAnnaCommandLineArguments:
    svanna_jar_file: Path
    phenopacket_path: Path
    vcf_path: Path
    output_dir: Path
    input_data: Path
    output_format: list[str]


def get_vcf_path(phenopacket_path: Path, vcf_dir: Path):
    phenopacket_util = PhenopacketUtil(phenopacket_reader(phenopacket_path))
    return phenopacket_util.vcf_file_data(phenopacket_path, vcf_dir).uri


def create_command_line_arguments(
    svanna_jar_file: Path,
    phenopacket_path: Path,
    vcf_path: Path,
    output_dir: Path,
    input_data: Path,
    output_format: list[str],
):
    return SvAnnaCommandLineArguments(
        svanna_jar_file=svanna_jar_file,
        phenopacket_path=phenopacket_path,
        output_dir=output_dir,
        input_data=input_data,
        vcf_path=vcf_path,
        output_format=output_format,
    )


class CommandWriter:
    def __init__(self, output_file: Path):
        self.output_file = output_file
        self.file = open(output_file, "w")

    def write_java_command(self, command_line_arguments: SvAnnaCommandLineArguments):
        self.file.write(
            "java " + "-jar " + str(command_line_arguments.svanna_jar_file) + " prioritize "
        )

    def write_phenopacket(self, command_line_arguments: SvAnnaCommandLineArguments):
        self.file.write("--phenopacket " + str(command_line_arguments.phenopacket_path))

    def write_vcf(self, command_line_arguments: SvAnnaCommandLineArguments):
        self.file.write(" --vcf " + str(command_line_arguments.vcf_path))

    def write_output_directory(self, command_line_arguments: SvAnnaCommandLineArguments):
        self.file.write(" --out-dir " + str(command_line_arguments.output_dir))

    def write_data_directory(self, command_line_arguments: SvAnnaCommandLineArguments):
        self.file.write(" --data-directory " + str(command_line_arguments.input_data))

    def write_output_format(self, command_line_arguments: SvAnnaCommandLineArguments):
        self.file.write(" --output-format " + ",".join(command_line_arguments.output_format))

    def write_uncompressed(self):
        self.file.write(" --uncompressed-output")

    def write_command(self, command_line_arguments: SvAnnaCommandLineArguments):
        try:
            self.write_java_command(command_line_arguments)
            self.write_phenopacket(command_line_arguments)
            self.write_vcf(command_line_arguments)
            self.write_output_directory(command_line_arguments)
            self.write_data_directory(command_line_arguments)
            self.write_output_format(command_line_arguments)
            self.write_uncompressed()
            self.file.write("\n")
        except IOError:
            print(f"Error writing {self.output_file}")

    def close(self):
        self.file.close()


def write_command(
    command_writer: CommandWriter,
    svanna_jar_file: Path,
    phenopacket_path: Path,
    vcf_path: Path,
    output_dir: Path,
    input_data: Path,
    output_format: list[str],
):
    command_line_arguments = create_command_line_arguments(
        svanna_jar_file=svanna_jar_file,
        phenopacket_path=phenopacket_path,
        vcf_path=vcf_path,
        output_dir=output_dir,
        input_data=input_data,
        output_format=output_format,
    )
    command_writer.write_command(command_line_arguments)


def write_commands(
    command_file_path: Path,
    svanna_jar_file: Path,
    phenopacket_dir: Path,
    vcf_dir: Path,
    output_dir: Path,
    input_data: Path,
    output_format: list[str],
):
    phenopackets = all_files(phenopacket_dir)
    command_writer = CommandWriter(command_file_path)
    for phenopacket_path in phenopackets:
        write_command(
            svanna_jar_file=svanna_jar_file,
            command_writer=command_writer,
            phenopacket_path=phenopacket_path,
            vcf_path=get_vcf_path(phenopacket_path, vcf_dir),
            output_dir=output_dir,
            input_data=input_data,
            output_format=output_format,
        )
    command_writer.close()


def prepare_commands(
    svanna_jar_file: Path,
    output_dir: Path,
    file_prefix: str,
    phenopacket_dir: Path,
    results_dir: Path,
    vcf_dir: Path,
    output_format: list[str],
    input_data: Path,
):
    command_file_path = output_dir.joinpath(f"{file_prefix}-l4ci-batch.txt")
    write_commands(
        svanna_jar_file=svanna_jar_file,
        command_file_path=command_file_path,
        output_dir=results_dir,
        phenopacket_dir=phenopacket_dir,
        vcf_dir=vcf_dir,
        output_format=output_format,
        input_data=input_data,
    )


@click.command("prepare-commands")
@click.option(
    "--svanna-jar-file",
    "-s",
    required=True,
    metavar=Path,
    type=Path,
    help="Path to SvAnna jar executable.",
)
@click.option(
    "--output-dir",
    "-o",
    required=True,
    metavar="PATH",
    type=Path,
    help="Directory for batch file to be output.",
)
@click.option(
    "--results-dir",
    "-r",
    required=True,
    metavar="PATH",
    type=Path,
    help="Path for results to be output by SvAnna.",
)
@click.option(
    "--input-data",
    "-d",
    required=True,
    metavar="PATH",
    type=Path,
    help="Path to SvAnna data directory.",
)
@click.option(
    "--phenopacket-dir",
    "-p",
    required=True,
    metavar="PATH",
    type=Path,
    help="Path to phenopacket directory.",
)
@click.option(
    "--vcf-dir",
    "-v",
    required=True,
    metavar="PATH",
    type=Path,
    help="Path to vcf directory.",
)
@click.option(
    "--file-prefix",
    "-f",
    required=True,
    metavar="str",
    type=str,
    help="File prefix.",
)
@click.option(
    "--output-format",
    "-outf",
    required=True,
    help="Output formats for results.",
    multiple=True,
    default=["tsv"],
)
def prepare_commands_command(
    svanna_jar_file: Path,
    output_dir: Path,
    file_prefix: str,
    phenopacket_dir: Path,
    results_dir: Path,
    vcf_dir: Path,
    output_format: list[str],
    input_data: Path,
):
    output_dir.joinpath("tool_input_commands").mkdir(parents=True, exist_ok=True)
    prepare_commands(
        svanna_jar_file=svanna_jar_file,
        output_dir=output_dir.joinpath("tool_input_commands"),
        file_prefix=file_prefix,
        phenopacket_dir=phenopacket_dir,
        results_dir=results_dir,
        vcf_dir=vcf_dir,
        output_format=output_format,
        input_data=input_data,
    )
