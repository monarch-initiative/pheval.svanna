import shutil
import tempfile
import unittest
from pathlib import Path

from pheval_svanna.prepare.prepare_commands import CommandWriter, SvAnnaCommandLineArguments


class TestCommandWriter(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()
        self.command_file_path = Path(self.test_dir).joinpath("test-commands.txt")
        self.command_writer = CommandWriter(output_file=self.command_file_path)
        self.command_arguments = SvAnnaCommandLineArguments(
            svanna_jar_file=Path("/path/to/svanna.jar"),
            phenopacket_path=Path("/path/to/phenopacket.json"),
            vcf_path=Path("/path/to/sample.vcf"),
            output_dir=Path("/path/to/results_dir"),
            input_data=Path("/path/to/input_data"),
            output_format=["tsv"],
        )

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_write_java_command(self):
        self.command_writer.write_java_command(self.command_arguments)
        self.command_writer.file.close()
        with open(self.command_file_path) as f:
            content = f.readlines()
        f.close()
        self.assertEqual(content, ["java -jar /path/to/svanna.jar prioritize "])

    def test_write_phenopacket(self):
        self.command_writer.write_phenopacket(self.command_arguments)
        self.command_writer.file.close()
        with open(self.command_file_path) as f:
            content = f.readlines()
        f.close()
        self.assertEqual(content, ["--phenopacket /path/to/phenopacket.json"])

    def test_write_vcf(self):
        self.command_writer.write_vcf(self.command_arguments)
        self.command_writer.file.close()
        with open(self.command_file_path) as f:
            content = f.readlines()
        f.close()
        self.assertEqual(content, [" --vcf /path/to/sample.vcf"])

    def test_write_output_directory(self):
        self.command_writer.write_output_directory(self.command_arguments)
        self.command_writer.file.close()
        with open(self.command_file_path) as f:
            content = f.readlines()
        f.close()
        self.assertEqual(content, [" --out-dir /path/to/results_dir"])

    def test_write_data_directory(self):
        self.command_writer.write_data_directory(self.command_arguments)
        self.command_writer.file.close()
        with open(self.command_file_path) as f:
            content = f.readlines()
        f.close()
        self.assertEqual(content, [" --data-directory /path/to/input_data"])

    def test_write_output_format(self):
        self.command_writer.write_output_format(self.command_arguments)
        self.command_writer.file.close()
        with open(self.command_file_path) as f:
            content = f.readlines()
        f.close()
        self.assertEqual(content, [" --output-format tsv"])

    def test_write_uncompressed(self):
        self.command_writer.write_uncompressed()
        self.command_writer.file.close()
        with open(self.command_file_path) as f:
            content = f.readlines()
        f.close()
        self.assertEqual(content, [" --uncompressed-output"])

    def test_write_command(self):
        self.command_writer.write_command(self.command_arguments)
        self.command_writer.file.close()
        with open(self.command_file_path) as f:
            content = f.readlines()
        f.close()
        self.assertEqual(
            content,
            [
                "java -jar /path/to/svanna.jar prioritize --phenopacket "
                "/path/to/phenopacket.json --vcf /path/to/sample.vcf --out-dir "
                "/path/to/results_dir --data-directory /path/to/input_data --output-format "
                "tsv --uncompressed-output\n"
            ],
        )

    def test_close(self):
        self.command_writer.close()
        self.assertTrue(self.command_writer.file.closed)
