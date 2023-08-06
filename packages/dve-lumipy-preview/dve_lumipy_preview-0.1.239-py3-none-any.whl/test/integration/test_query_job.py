import time

import pandas as pd

from test.integration.base_intergration_test import BaseIntegrationTest


class TestQueryJob(BaseIntegrationTest):

    """Integration tests for async usage of QueryJob class

    """

    def test_query_job_status_progress_and_result(self):

        pf = self.atlas.lusid_portfolio()

        job = pf.select('*').limit(10).go_async()

        status = job.get_status()
        self.assertNotEqual(status, '')
        while status == 'WaitingForActivation':
            status = job.get_status()
            self.assertNotEqual(status, '')
            time.sleep(1)

        df = job.get_result()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 10)

        log = job.get_progress()
        self.assertIsInstance(log, str)
        self.assertGreater(len(log), 0)
