import os

from mock import patch

from test import HokusaiIntegrationTestCase, TEST_KUBE_CONTEXT
from test.utils import captured_output, mock_verbosity
from test.mocks.mock_ecr import MockECR

from hokusai import CWD
from hokusai.lib.common import shout
from hokusai.commands import kubernetes
from hokusai.services.kubectl import Kubectl


class TestKubernetes(HokusaiIntegrationTestCase):
    @classmethod
    def setUpClass(cls):
        kubernetes.ECR = MockECR
        kubernetes.HOKUSAI_CONFIG_DIR = os.path.join(CWD, 'test/fixtures/project/hokusai')
        cls.kubernetes_yml = os.path.abspath(os.path.join(kubernetes.HOKUSAI_CONFIG_DIR, 'minikube.yml'))
        cls.kctl = Kubectl(TEST_KUBE_CONTEXT)

    @classmethod
    def tearDownClass(cls):
        with captured_output() as (out, err):
            shout(cls.kctl.command("delete all --selector testFixture=true"), print_output=True)

    @patch('hokusai.lib.command.sys.exit')
    def test_00_k8s_create(self, mocked_sys_exit):
        with captured_output() as (out, err):
            kubernetes.k8s_create(TEST_KUBE_CONTEXT, yaml_file_name='minikube')
            mocked_sys_exit.assert_called_once_with(0)
            # self.assertIn('deployment.apps "hello-web" created', out.getvalue().strip())
            # self.assertIn('service "hello-web" created', out.getvalue().strip())
            self.assertIn('Created Kubernetes environment %s' % self.__class__.kubernetes_yml,
                            out.getvalue().strip())

    @patch('hokusai.lib.command.sys.exit')
    def test_01_k8s_update(self, mocked_sys_exit):
        with captured_output() as (out, err):
            kubernetes.k8s_update(TEST_KUBE_CONTEXT, yaml_file_name='minikube')
            mocked_sys_exit.assert_called_once_with(0)
            # self.assertIn('deployment.apps "hello-web" unchanged', out.getvalue().strip())
            # self.assertIn('service "hello-web" unchanged', out.getvalue().strip())
            self.assertIn('Updated Kubernetes environment %s' % self.__class__.kubernetes_yml,
                            out.getvalue().strip())

    @patch('hokusai.lib.command.sys.exit')
    def test_02_k8s_status(self, mocked_sys_exit):
        with captured_output() as (out, err):
            kubernetes.k8s_status(TEST_KUBE_CONTEXT, True, False, False, False, yaml_file_name='minikube')
            mocked_sys_exit.assert_called_once_with(0)
            self.assertIn('Resources', out.getvalue().strip())
            # self.assertIn('deployment.apps/hello-web', out.getvalue().strip())
            # self.assertIn('service/hello-web', out.getvalue().strip())
            mocked_sys_exit.reset_mock()

            kubernetes.k8s_status(TEST_KUBE_CONTEXT, True, False, True, False, yaml_file_name='minikube')
            mocked_sys_exit.assert_called_once_with(0)
            self.assertIn('Resources', out.getvalue().strip())
            # self.assertIn('Name:                   hello-web', out.getvalue().strip())
            # self.assertIn('Selector:               app=hello', out.getvalue().strip())
            mocked_sys_exit.reset_mock()

            kubernetes.k8s_status(TEST_KUBE_CONTEXT, False, True, False, False, yaml_file_name='minikube')
            mocked_sys_exit.assert_called_once_with(0)
            self.assertIn('Pods', out.getvalue().strip())
            # self.assertIn('hello-web', out.getvalue().strip())
            # self.assertTrue('ContainerCreating' in out.getvalue().strip() or 'Running' in out.getvalue().strip())
            mocked_sys_exit.reset_mock()

            kubernetes.k8s_status(TEST_KUBE_CONTEXT, False, True, True, False, yaml_file_name='minikube')
            mocked_sys_exit.assert_called_once_with(0)
            # self.assertIn('Name:           hello-web', out.getvalue().strip())
            mocked_sys_exit.reset_mock()

            # TODO enable heapster in minikube to get top pods
            # kubernetes.k8s_status(TEST_KUBE_CONTEXT, False, False, False, True, yaml_file_name='minikube')


    @patch('hokusai.lib.command.sys.exit')
    def test_03_k8s_delete(self, mocked_sys_exit):
        with captured_output() as (out, err):
            kubernetes.k8s_delete(TEST_KUBE_CONTEXT, yaml_file_name='minikube')
            mocked_sys_exit.assert_called_once_with(0)
            self.assertIn('Deleted Kubernetes environment %s' % self.__class__.kubernetes_yml,
                            out.getvalue().strip())
