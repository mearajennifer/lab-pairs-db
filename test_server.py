"""Balloonicorn's lab pair making machine tests."""

import server
import unittest

class MyAppTestCase(unittest.TestCase):
    """Integration testing."""

    def setUp(self):
        print("(setUp ran)")
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    def tearDown(self):
        # We don't need to do anything here; we could just
        # not define this method at all, but we have a stub
        # here as an example.
        print("(tearDown ran)")
        return

    def test_index(self):
        result = self.client.get("/")
        self.assertIn(b'<h2><a href="/view-cohorts" method="GET">View Cohorts & Students</a></h2>', result.data)

    def test_add_cohort_html(self):
        result = self.client.get("/add-cohort")
        self.assertIn(b'<h1>Add a Cohort</h1>', result.data)
    
    # def test_add_cohort_form(self):
    #     result = self.client.post("/manually-add-cohort", data={"cohort_id": "target01", "title": "Target Twin Cities 1"})
    #     self.assertIn(b'Cohort Target Twin Cities 1 added!', result.data)


if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()
