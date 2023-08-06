import sys
import unittest
from functools import partial

from cloudshell.shell.standards.load_balancer.driver_interface import (
    LoadBalancerResourceDriverInterface,
)

if sys.version_info >= (3, 0):
    from unittest.mock import MagicMock
else:
    from mock import MagicMock


class TestDriverInterface(unittest.TestCase):
    def test_interface_is_abstract(self):
        with self.assertRaisesRegexp(TypeError, "abstract"):
            LoadBalancerResourceDriverInterface()

    def test_interface_have_all_methods(self):
        intr_has_attr = partial(hasattr, LoadBalancerResourceDriverInterface)
        self.assertTrue(intr_has_attr("run_custom_command"))
        self.assertTrue(intr_has_attr("run_custom_config_command"))
        self.assertTrue(intr_has_attr("save"))
        self.assertTrue(intr_has_attr("restore"))
        self.assertTrue(intr_has_attr("get_inventory"))
        self.assertTrue(intr_has_attr("orchestration_restore"))
        self.assertTrue(intr_has_attr("orchestration_save"))
        self.assertTrue(intr_has_attr("health_check"))
        self.assertTrue(intr_has_attr("shutdown"))

    def test_abstract_methods_return_none(self):
        class TestedClass(LoadBalancerResourceDriverInterface):
            def run_custom_command(self, context, custom_command):
                return super(TestedClass, self).run_custom_command(
                    context, custom_command
                )

            def run_custom_config_command(self, context, custom_command):
                return super(TestedClass, self).run_custom_config_command(
                    context, custom_command
                )

            def save(
                self, context, folder_path, configuration_type, vrf_management_name
            ):
                return super(TestedClass, self).save(
                    context, folder_path, configuration_type, vrf_management_name
                )

            def restore(
                self,
                context,
                path,
                configuration_type,
                restore_method,
                vrf_management_name,
            ):
                return super(TestedClass, self).restore(
                    context,
                    path,
                    configuration_type,
                    restore_method,
                    vrf_management_name,
                )

            def get_inventory(self, context):
                return super(TestedClass, self).get_inventory(context)

            def orchestration_restore(
                self, context, saved_artifact_info, custom_params
            ):
                return super(TestedClass, self).orchestration_restore(
                    context, saved_artifact_info, custom_params
                )

            def orchestration_save(self, context, mode, custom_params):
                return super(TestedClass, self).orchestration_save(
                    context, mode, custom_params
                )

            def health_check(self, context):
                return super(TestedClass, self).health_check(context)

            def shutdown(self, context):
                return super(TestedClass, self).shutdown(context)

        inst = TestedClass()
        arg = MagicMock()
        self.assertIsNone(inst.run_custom_command(arg, arg))
        self.assertIsNone(inst.run_custom_config_command(arg, arg))
        self.assertIsNone(inst.save(arg, arg, arg, arg))
        self.assertIsNone(inst.restore(arg, arg, arg, arg, arg))
        self.assertIsNone(inst.get_inventory(arg))
        self.assertIsNone(inst.orchestration_restore(arg, arg, arg))
        self.assertIsNone(inst.orchestration_save(arg, arg, arg))
        self.assertIsNone(inst.health_check(arg))
        self.assertIsNone(inst.shutdown(arg))
