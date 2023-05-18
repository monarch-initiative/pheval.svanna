from pathlib import Path

import click
import pandas as pd
from pheval.post_processing.post_processing import PhEvalVariantResult, generate_pheval_result
from pheval.utils.file_utils import files_with_suffix


def read_svanna_result(svanna_result_path: Path) -> pd.DataFrame:
    """Read SvAnna tsv output and return a dataframe."""
    return pd.read_csv(svanna_result_path, delimiter="\t")


def trim_svanna_result(svanna_result_path: Path) -> Path:
    """Trim .SVANNA from results filename."""
    return Path(str(svanna_result_path.name.replace(".SVANNA", "")))


class PhEvalVariantResultFromSvAnna:
    def __init__(self, svanna_result: pd.DataFrame):
        self.svanna_result = svanna_result

    @staticmethod
    def obtain_score(svanna_result_entry: pd.Series) -> float:
        """Obtain score from result."""
        return float(svanna_result_entry["psv"])

    @staticmethod
    def obtain_chromosome(svanna_result_entry: pd.Series) -> str:
        """Obtain chromosome from result."""
        return svanna_result_entry["contig"]

    @staticmethod
    def obtain_start(svanna_result_entry: pd.Series) -> int:
        """Obtain start position from result."""
        return int(svanna_result_entry["start"])

    @staticmethod
    def obtain_end(svanna_result_entry: pd.Series) -> int:
        """Obtain end position from result."""
        return int(svanna_result_entry["end"])

    @staticmethod
    def obtain_ref() -> str:
        """Obtain reference allele from result."""
        return "N"

    @staticmethod
    def obtain_alt(svanna_result_entry: pd.Series) -> str:
        """Obtain alternate allele from result."""
        return svanna_result_entry["vtype"]

    def extract_pheval_requirements(self) -> PhEvalVariantResult:
        """Extract data required to produce PhEval variant output."""
        simplified_variant_results = []
        for _index, result in self.svanna_result.iterrows():
            simplified_variant_results.append(
                PhEvalVariantResult(
                    chromosome=self.obtain_chromosome(result),
                    start=self.obtain_start(result),
                    end=self.obtain_end(result),
                    ref=self.obtain_ref(),
                    alt=self.obtain_alt(result),
                    score=self.obtain_score(result),
                )
            )
        return simplified_variant_results


def create_standardised_results(raw_results_dir: Path, output_dir: Path, sort_order: str) -> None:
    """Write standardised variant results from SvAnna tsv output."""
    for result in files_with_suffix(raw_results_dir, ".tsv"):
        svanna_result = read_svanna_result(result)
        pheval_variant_result = PhEvalVariantResultFromSvAnna(
            svanna_result
        ).extract_pheval_requirements()
        generate_pheval_result(
            pheval_variant_result, sort_order, output_dir, trim_svanna_result(result)
        )


@click.command("post-process")
@click.option(
    "--results-dir", "-r", required=True, help="Path to SvAnna results directory.", type=Path
)
@click.option("--output-dir", "-o", required=True, help="Path to output directory.", type=Path)
@click.option(
    "--sort-order",
    "-s",
    required=True,
    help="sort order.",
    type=click.Choice(["ascending", "descending"]),
    default="descending",
    show_default=True,
)
def post_process(results_dir: Path, output_dir: Path, sort_order: str):
    """Post-process SvAnna .tsv results to PhEval variant result format."""
    output_dir.joinpath("pheval_variant_results/").mkdir(exist_ok=True, parents=True)
    create_standardised_results(results_dir, output_dir, sort_order)
