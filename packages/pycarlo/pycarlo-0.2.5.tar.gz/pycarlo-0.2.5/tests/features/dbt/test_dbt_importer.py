import json
import os
import pathlib
from unittest import TestCase
from unittest.mock import Mock

import requests
from box import Box
from requests import HTTPError, Response

from pycarlo.features.dbt import DbtImporter
from pycarlo.features.dbt.queries import (
    IMPORT_DBT_MANIFEST,
    IMPORT_DBT_RUN_RESULTS,
    UPLOAD_DBT_MANIFEST,
    UPLOAD_DBT_RUN_RESULTS,
)


class DbtImportServiceTest(TestCase):

    def test_import_dbt_manifest(self):
        self._client_mock = Mock(return_value=Box({
            'import_dbt_manifest': {
                'response': {
                    'node_ids_imported': [
                        "model.analytics.metric_types",
                        "model.analytics.recent_metrics",
                        "model.analytics.lineage_nodes"
                    ]
                }
            }
        }))

        service = DbtImporter(
            mc_client=self._client_mock
        )

        manifest_file = os.path.join(pathlib.Path(__file__).parent.resolve(), 'sample_manifest.json')
        node_ids_imported = service.import_dbt_manifest(manifest_file, default_resource='snowflake')

        with open(manifest_file, 'r') as f:
            dbt_manifest = Box(json.load(f))

        self._client_mock.assert_called_once_with(
            query=IMPORT_DBT_MANIFEST,
            variables=dict(
                dbtSchemaVersion='https://schemas.getdbt.com/dbt/manifest/v2.json',
                manifestNodesJson=json.dumps(dbt_manifest.nodes.to_dict()),
                projectName=None,
                defaultResource='snowflake'
            )
        )

        self.assertEqual(
            node_ids_imported,
            ['model.analytics.metric_types', 'model.analytics.recent_metrics', 'model.analytics.lineage_nodes']
        )

    def test_import_dbt_manifest_retry(self):
        def create_responses(*args, **kwargs):
            nodes = json.loads(kwargs['variables']['manifestNodesJson'])

            if len(list(nodes.items())) == 1:
                return Box({
                    'import_dbt_manifest': {
                        'response': {
                            'node_ids_imported': [list(nodes.keys())[0]]
                        }
                    }
                })

            response = Response()
            response.status_code = requests.codes.gateway_timeout

            raise HTTPError(response=response)

        self._client_mock = Mock(side_effect=create_responses)

        importer = DbtImporter(
            mc_client=self._client_mock
        )

        manifest_file = os.path.join(pathlib.Path(__file__).parent.resolve(), 'sample_manifest.json')
        node_ids_imported = importer.import_dbt_manifest(manifest_file)

        # client call will timeout, then will send each one-by-one
        # client will be called a total of 4 times
        self.assertEqual(4, self._client_mock.call_count)

        self.assertEqual(
            node_ids_imported,
            ['model.analytics.metric_types', 'model.analytics.recent_metrics', 'model.analytics.lineage_nodes']
        )

    def test_import_dbt_manifest_retry_bail_out(self):
        def create_responses(*args, **kwargs):
            response = Response()
            response.status_code = requests.codes.gateway_timeout

            raise HTTPError(response=response)

        self._client_mock = Mock(side_effect=create_responses)

        importer = DbtImporter(
            mc_client=self._client_mock
        )

        manifest_file = os.path.join(pathlib.Path(__file__).parent.resolve(), 'sample_manifest.json')

        with self.assertRaises(RuntimeError):
            node_ids_imported = importer.import_dbt_manifest(manifest_file)

        # make_request_v2() will always timeout
        # First request will time out
        # Then the next will time out, which has a batch size of 1, at which point it bails out
        self.assertEqual(2, self._client_mock.call_count)

    def test_import_dbt_run_results(self):
        self._client_mock = Mock(return_value=Box({
            'import_dbt_run_results': {
                'response': {
                    'num_results_imported': 4
                }
            }
        }))

        service = DbtImporter(
            mc_client=self._client_mock
        )

        run_results_file = os.path.join(pathlib.Path(__file__).parent.resolve(), 'sample_run_results.json')
        with open(run_results_file, 'r') as f:
            run_results = Box(json.load(f))

        node_ids_imported = service.import_run_results(run_results_file)

        self._client_mock.assert_called_once_with(
            query=IMPORT_DBT_RUN_RESULTS,
            variables=dict(
                dbtSchemaVersion='https://schemas.getdbt.com/dbt/run-results/v2.json',
                runResultsJson=json.dumps(run_results),
                projectName=None,
                runId=None,
                runLogs=None
            )
        )

        self.assertEqual(node_ids_imported, 4)

    def test_upload_dbt_manifest(self):
        # given
        project_name = 'mydb'
        resource_name = 'mywarehouse'
        batch_size = 2

        logs = []

        self._client_mock = Mock()
        service = DbtImporter(
            mc_client=self._client_mock,
            print_func=lambda m: logs.append(m)
        )

        manifest_file = os.path.join(pathlib.Path(__file__).parent.resolve(), 'sample_manifest.json')
        with open(manifest_file, 'r') as f:
            dbt_manifest = Box(json.load(f))

        all_nodes = dbt_manifest.nodes.to_dict()
        batch_1_nodes = dict(list(all_nodes.items())[:batch_size])
        batch_2_nodes = dict(list(all_nodes.items())[batch_size:])

        # when
        service.upload_dbt_manifest(
            dbt_manifest=manifest_file,
            project_name=project_name,
            default_resource=resource_name,
            batch_size=batch_size)

        # verify expected calls to MC client
        calls = self._client_mock.call_args_list
        self.assertEqual(2, len(calls))

        self.assertDictEqual(dict(
            query=UPLOAD_DBT_MANIFEST,
            variables=dict(
                invocationId='3b44f6e7-0a4a-4c81-8859-468b2d15075e',
                batch=1,
                dbtSchemaVersion='https://schemas.getdbt.com/dbt/manifest/v2.json',
                manifestNodesJson=json.dumps(batch_1_nodes),
                projectName='mydb',
                defaultResource='mywarehouse'
            )
        ), calls[0][1])

        self.assertDictEqual(dict(
            query=UPLOAD_DBT_MANIFEST,
            variables=dict(
                invocationId='3b44f6e7-0a4a-4c81-8859-468b2d15075e',
                batch=2,
                dbtSchemaVersion='https://schemas.getdbt.com/dbt/manifest/v2.json',
                manifestNodesJson=json.dumps(batch_2_nodes),
                projectName='mydb',
                defaultResource='mywarehouse'
            )
        ), calls[1][1])

        # verify expected logging
        self.assertEqual(3, len(logs))
        self.assertListEqual([
            'Uploading 3 DBT objects to Monte Carlo for processing. Please wait...',
            'Uploaded 2 objects',
            'Uploaded 3 objects'
        ], logs)

    def test_upload_dbt_run_results(self):
        self._client_mock = Mock()
        service = DbtImporter(mc_client=self._client_mock)

        run_results_file = os.path.join(pathlib.Path(__file__).parent.resolve(), 'sample_run_results.json')
        with open(run_results_file, 'r') as f:
            run_results = Box(json.load(f))

        service.upload_run_results(run_results_file)

        self._client_mock.assert_called_once_with(
            query=UPLOAD_DBT_RUN_RESULTS,
            variables=dict(
                dbtSchemaVersion='https://schemas.getdbt.com/dbt/run-results/v2.json',
                runResultsJson=json.dumps(run_results),
                invocationId='6e265bb1-a782-4063-a9b5-c06738be25ea',
                projectName=None,
                runId=None,
                runLogs=None
            )
        )
