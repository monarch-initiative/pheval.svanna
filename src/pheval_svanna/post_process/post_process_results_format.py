from pathlib import Path

import polars as pl
from pheval.post_processing.post_processing import SortOrder, generate_variant_result
from pheval.utils.file_utils import files_with_suffix


def read_svanna_result(svanna_result_path: Path) -> pl.DataFrame:
    """Read SvAnna tsv output and return a dataframe."""
    return pl.read_csv(svanna_result_path, separator="\t")


def trim_svanna_result(svanna_result_path: Path) -> Path:
    """Trim .SVANNA from results filename."""
    return Path(str(svanna_result_path.name.replace(".SVANNA", "")))


def extract_variant_results(raw_results: pl.DataFrame) -> pl.DataFrame:
    """
    Extract variant results from SvAnna output.
    Args:
        raw_results (pl.DataFrame): Raw results from SvAnna.
    Returns:
        pl.DataFrame: Variant results from SvAnna.
    """
    return raw_results.select(
        [
            pl.col("contig").alias("chrom").cast(pl.String),
            pl.col("start").alias("start").cast(pl.Int64),
            pl.col("end").alias("end").cast(pl.Int64),
            pl.lit("N").alias("ref"),
            pl.col("vtype").alias("alt"),
            pl.col("psv").alias("score").cast(pl.Float64),
        ]
    )


def create_standardised_results(
    raw_results_dir: Path, output_dir: Path, phenopacket_dir: Path, sort_order: str
) -> None:
    """Write standardised variant results from SvAnna tsv output."""
    sort_order = SortOrder.ASCENDING if sort_order.lower() == "ascending" else SortOrder.DESCENDING
    for result in files_with_suffix(raw_results_dir, ".tsv"):
        svanna_result = read_svanna_result(result)
        pheval_variant_result = extract_variant_results(svanna_result)
        generate_variant_result(
            results=pheval_variant_result,
            output_dir=output_dir,
            sort_order=sort_order,
            result_path=trim_svanna_result(result),
            phenopacket_dir=phenopacket_dir,
        )
