import crud
import unittest

class FormatCohortIdTestCase(unittest.TestCase):
    """Test format_cohort_id(cohort_id) function"""

    def test_format_cohort_id(self):
        # assert crud.format_cohort_id('SERFT7') == 'serft7'
        self.assertEqual(crud.format_cohort_id('SERFT7'), 'serft7')
        

if __name__ == "__main__":
    unittest.main()