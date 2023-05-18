import unittest

import pandas as pd
from pheval.post_processing.post_processing import PhEvalVariantResult

from pheval_svanna.post_process.post_process_results_format import PhEvalVariantResultFromSvAnna

svanna_results = pd.DataFrame(
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

svanna_result = svanna_results.iloc[0]


class TestPhEvalVariantResultFromSvAnna(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.variant_result = PhEvalVariantResultFromSvAnna(svanna_results)

    def test_obtain_score(self):
        self.assertEqual(self.variant_result.obtain_score(svanna_result), 4.7851300482957155)

    def test_obtain_chromosome(self):
        self.assertEqual(self.variant_result.obtain_chromosome(svanna_result), "19")

    def test_obtain_start(self):
        self.assertEqual(self.variant_result.obtain_start(svanna_result), 55158139)

    def test_obtain_end(self):
        self.assertEqual(self.variant_result.obtain_end(svanna_result), 55158175)

    def test_obtain_ref(self):
        self.assertEqual(self.variant_result.obtain_ref(), "N")

    def test_obtain_alt(self):
        self.assertEqual(self.variant_result.obtain_alt(svanna_result), "DEL")

    def test_extract_pheval_requirements(self):
        self.assertEqual(
            self.variant_result.extract_pheval_requirements(),
            [
                PhEvalVariantResult(
                    chromosome="19",
                    start=55158139,
                    end=55158175,
                    ref="N",
                    alt="DEL",
                    score=4.7851300482957155,
                ),
                PhEvalVariantResult(
                    chromosome="2",
                    start=219469370,
                    end=219469406,
                    ref="N",
                    alt="DEL",
                    score=4.695487573142047,
                ),
                PhEvalVariantResult(
                    chromosome="1",
                    start=156106617,
                    end=156106639,
                    ref="N",
                    alt="DEL",
                    score=4.265903696888752,
                ),
            ],
        )
