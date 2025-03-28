from pathlib import Path

import polars as pl
from pheval.post_processing.post_processing import SortOrder, generate_gene_result
from pheval.utils.file_utils import all_files
from pheval.utils.phenopacket_utils import GeneIdentifierUpdater, create_gene_identifier_map


def read_raw_result(raw_result_path: Path) -> pl.DataFrame:
    """
    Read the raw result file.

    Args:
        raw_result_path(Path): Path to the raw result file.

    Returns:
        pl.DataFrame: Contents of the raw result file.
    """
    return pl.read_json(raw_result_path)


def extract_gene_results(
    raw_results: pl.DataFrame, gene_identifier_updater: GeneIdentifierUpdater
) -> pl.DataFrame:
    """
    Extract gene results from raw results.
    Args:
        raw_results (pl.DataFrame): Raw results.
        gene_identifier_updater (GeneIdentifierUpdater): GeneIdentifierUpdater.

    Returns:
        pl.DataFrame: Extracted gene results.
    """
    return raw_results.select(
        [
            pl.col("gene_symbol").cast(pl.String),
            pl.col("gene_symbol")
            .map_elements(gene_identifier_updater.find_identifier, return_dtype=pl.String)
            .alias("gene_identifier")
            .cast(pl.String),
            pl.col("score").cast(pl.Float64),
        ]
    )


def create_standardised_results(
    raw_results_dir: Path, output_dir: Path, phenopacket_dir: Path
) -> None:
    """
    Create PhEval gene tsv output from raw results.

    Args:
        raw_results_dir (Path): Path to the raw result directory.
        output_dir (Path): Path to the output directory.
        phenopacket_dir (Path): Path to the phenopackets directory.
    """
    gene_identifier_updater = GeneIdentifierUpdater(
        gene_identifier="ensembl_id", identifier_map=create_gene_identifier_map()
    )
    for raw_result_path in all_files(raw_results_dir):
        raw_result = read_raw_result(raw_result_path)
        pheval_result = extract_gene_results(raw_result, gene_identifier_updater)
        generate_gene_result(
            results=pheval_result,
            output_dir=output_dir,
            sort_order=SortOrder.DESCENDING,
            result_path=raw_result_path,
            phenopacket_dir=phenopacket_dir,
        )
