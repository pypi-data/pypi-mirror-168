import os
import unittest
import boto3

from aws import cluster, factsheet
from test import test_cluster

CLUSTER_NAME = test_cluster.CONFIG_FILE['clusterName']


class TestFactsheet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        vpc = cluster.get_vpc(CLUSTER_NAME)
        cp = cluster.get_cp(CLUSTER_NAME)
        workers = cluster.get_eks_workers(CLUSTER_NAME)
        if not vpc or not cp or not workers:
            raise RuntimeError('must call test_cluster.create_test_cluster() prior to this test')

    @classmethod
    def tearDownClass(cls):
        None

    def test_generate_cluster_factsheet_missing_clustername(self):
        with self.assertRaisesRegex(AssertionError, 'requires cluster_name'):
            factsheet.generate_cluster_factsheet(cluster_name='', base_domain='')
    
    def test_generate_cluster_factsheet_missing_basedomain(self):
        with self.assertRaisesRegex(AssertionError, 'requires base_domain'):
            factsheet.generate_cluster_factsheet(cluster_name='ac-unit', base_domain='')
    
    def test_generate_cluster_factsheet_invalid_directory(self):
        with self.assertRaisesRegex(AssertionError, 'requires a valid output_dir'):
            factsheet.generate_cluster_factsheet(cluster_name='ac-unit', base_domain='base.domain.com', is_cicd=False, output_dir='bogus')

    def test_generate_cluster_factsheet_nonexistant(self):
        self.assertIsNone(factsheet.generate_cluster_factsheet(cluster_name='ac-unit', base_domain='base.domain.com'))    

    def test_generate_cluster_factsheet(self):
        cluster_name = CLUSTER_NAME + '-cluster'
        filename = factsheet.generate_cluster_factsheet(cluster_name=cluster_name, base_domain='basedomain.com', is_cicd=True)
        self.assertTrue(os.path.isfile(filename))

    def test_get_nodegroups(self):
        results = factsheet._get_nodegroups(CLUSTER_NAME + '-cluster')
        self.assertTrue(results)

        for ng in results:
            self.assertTrue(ng['name'])
            self.assertTrue(ng['type'])
            self.assertTrue(ng['min'])
            self.assertTrue(ng['max'])
            self.assertTrue(ng['desired'])
            self.assertTrue(ng['nodeRoleArn'])
            self.assertTrue(ng['nodeRoleName'])

    def test_get_nodes(self):
        results = factsheet._get_nodes(CLUSTER_NAME + '-cluster')
        self.assertTrue(results)

        for node in results:
            self.assertTrue(node['name'])
            self.assertTrue(node['nodeGroup'])
            self.assertTrue(node['instanceId'])
            self.assertTrue(node['instanceType'])

    def test_extract_role_name(self):
        result = factsheet._extract_role_name('arn:aws:iam::123456789:role/something-role')
        self.assertEqual('something-role', result)

    def test_get_template_params(self):
        eks_cluster = boto3.client('eks').describe_cluster(name=CLUSTER_NAME+'-cluster').get('cluster', {})
        self.assertTrue(eks_cluster)
        params = factsheet._get_template_params(eks_cluster=eks_cluster, base_domain='basedomain.com', is_cicd=False)
        self.assertTrue(params)