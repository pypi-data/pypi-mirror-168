import unittest

from cloudshell.shell.standards.autoload_generic_models import (
    GenericChassis,
    GenericModule,
    GenericPort,
    GenericPortChannel,
    GenericPowerPort,
    GenericSubModule,
)

from cloudshell.shell.standards.load_balancer.autoload_model import (
    LoadBalancerResourceModel,
)


class TestGenericResourceModel(unittest.TestCase):
    def test_resource_model(self):
        resource_name = "resource name"
        shell_name = "shell name"
        family_name = "CS_LoadBalancer"

        resource = LoadBalancerResourceModel(resource_name, shell_name, family_name)

        self.assertEqual(family_name, resource.family_name)
        self.assertEqual(shell_name, resource.shell_name)
        self.assertEqual(resource_name, resource.name)
        self.assertEqual("", resource.relative_address.__repr__())
        self.assertEqual("GenericResource", resource.resource_model)
        self.assertEqual(
            "{}.{}".format(shell_name, resource.resource_model),
            resource.cloudshell_model_name,
        )

        self.assertEqual(GenericChassis, resource.entities.Chassis)
        self.assertEqual(GenericModule, resource.entities.Module)
        self.assertEqual(GenericSubModule, resource.entities.SubModule)
        self.assertEqual(GenericPort, resource.entities.Port)
        self.assertEqual(GenericPortChannel, resource.entities.PortChannel)
        self.assertEqual(GenericPowerPort, resource.entities.PowerPort)

        self.assertIsInstance(resource.unique_identifier, str)
        self.assertTrue(resource.unique_identifier)
