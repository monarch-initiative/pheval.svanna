import unittest

import polars as pl

from pheval_svanna.post_process.post_process_results_format import extract_variant_results

svanna_results = pl.DataFrame(
    [
        {
            "contig": "19",
            "start": "55158139",
            "end": "55158175",
            "id": "pbsv.DEL.46563",
            "vtype": "DEL",
            "failed_filters": "",
            "psv": "4.7851300482957155",
        },
        {
            "contig": "2",
            "start": "219469370",
            "end": "219469406",
            "id": ".",
            "vtype": "DEL",
            "failed_filters": "",
            "psv": "4.695487573142047",
        },
        {
            "contig": "1",
            "start": "156106617",
            "end": "156106639",
            "id": "pbsv.DEL.2251",
            "vtype": "DEL",
            "failed_filters": "",
            "psv": "4.265903696888752",
        },
    ]
)


class TestPostProcessResultsFromSvAnna(unittest.TestCase):
    def test_extract_variant_results(self):
        self.assertTrue(
            extract_variant_results(svanna_results).equals(
                pl.DataFrame(
                    [
                        {
                            "chrom": "19",
                            "start": 55158139,
                            "end": 55158175,
                            "ref": "N",
                            "alt": "DEL",
                            "score": 4.7851300482957155,
                        },
                        {
                            "chrom": "2",
                            "start": 219469370,
                            "end": 219469406,
                            "ref": "N",
                            "alt": "DEL",
                            "score": 4.695487573142047,
                        },
                        {
                            "chrom": "1",
                            "start": 156106617,
                            "end": 156106639,
                            "ref": "N",
                            "alt": "DEL",
                            "score": 4.265903696888752,
                        },
                    ]
                )
            )
        )
