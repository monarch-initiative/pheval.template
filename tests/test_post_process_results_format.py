import unittest

import polars as pl
from pheval.utils.phenopacket_utils import GeneIdentifierUpdater, create_gene_identifier_map

from pheval_template.post_process.post_process_results_format import extract_gene_results

result = pl.DataFrame(
    [
        {"gene_symbol": "GCDH", "score": 0.6415226418151174},
        {"gene_symbol": "RBP5", "score": 0.9544966959822396},
        {"gene_symbol": "ANKRD27", "score": 0.010339408049069188},
        {"gene_symbol": "HNRNPCP10", "score": 0.9341396532637285},
        {"gene_symbol": "FXYD6P2", "score": 0.5754332215873432},
        {"gene_symbol": "RPL7AP9", "score": 0.7019868839537887},
        {"gene_symbol": "RNA5SP232", "score": 0.8323299063014772},
        {"gene_symbol": "TMEM63A", "score": 0.14946381720965796},
        {"gene_symbol": "CCNT2-AS1", "score": 0.5782537824662363},
    ]
)


class TestPostProcessResultsFormat(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gene_identifier = GeneIdentifierUpdater("ensembl_id", create_gene_identifier_map())

    def test_extract_gene_results(self):
        self.assertTrue(
            extract_gene_results(result, self.gene_identifier).equals(
                pl.DataFrame(
                    [
                        {
                            "gene_symbol": "GCDH",
                            "gene_identifier": "ENSG00000105607",
                            "score": 0.6415226418151174,
                        },
                        {
                            "gene_symbol": "RBP5",
                            "gene_identifier": "ENSG00000139194",
                            "score": 0.9544966959822396,
                        },
                        {
                            "gene_symbol": "ANKRD27",
                            "gene_identifier": "ENSG00000105186",
                            "score": 0.010339408049069188,
                        },
                        {
                            "gene_symbol": "HNRNPCP10",
                            "gene_identifier": "ENSG00000215054",
                            "score": 0.9341396532637285,
                        },
                        {
                            "gene_symbol": "FXYD6P2",
                            "gene_identifier": "ENSG00000235964",
                            "score": 0.5754332215873432,
                        },
                        {
                            "gene_symbol": "RPL7AP9",
                            "gene_identifier": "ENSG00000213272",
                            "score": 0.7019868839537887,
                        },
                        {
                            "gene_symbol": "RNA5SP232",
                            "gene_identifier": "ENSG00000201014",
                            "score": 0.8323299063014772,
                        },
                        {
                            "gene_symbol": "TMEM63A",
                            "gene_identifier": "ENSG00000196187",
                            "score": 0.14946381720965796,
                        },
                        {
                            "gene_symbol": "CCNT2-AS1",
                            "gene_identifier": "ENSG00000224043",
                            "score": 0.5782537824662363,
                        },
                    ]
                )
            )
        )
