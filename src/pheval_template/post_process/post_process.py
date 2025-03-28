from pathlib import Path

from pheval_template.post_process.post_process_results_format import create_standardised_results


def post_process(raw_results_dir: Path, output_dir: Path, phenopacket_dir: Path) -> None:
    """
    Post-process the raw results output to standardised PhEval TSV format.

    Args:
        raw_results_dir (Path): Path to the raw result directory.
        output_dir (Path): Path to the output directory.
        phenopacket_dir (Path): Path to the directory containing the phenopackets.
    """
    create_standardised_results(
        raw_results_dir=raw_results_dir, output_dir=output_dir, phenopacket_dir=phenopacket_dir
    )
