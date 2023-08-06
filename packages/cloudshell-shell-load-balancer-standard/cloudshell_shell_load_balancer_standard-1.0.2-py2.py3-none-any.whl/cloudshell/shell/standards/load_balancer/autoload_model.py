from cloudshell.shell.standards.autoload_generic_models import (
    GenericChassis,
    GenericModule,
    GenericPort,
    GenericPortChannel,
    GenericPowerPort,
    GenericResourceModel,
    GenericSubModule,
)

__all__ = [
    "LoadBalancerResourceModel",
    "GenericResourceModel",
    "GenericChassis",
    "GenericModule",
    "GenericSubModule",
    "GenericPortChannel",
    "GenericPowerPort",
    "GenericPort",
]


class LoadBalancerResourceModel(GenericResourceModel):
    SUPPORTED_FAMILY_NAMES = ["CS_LoadBalancer"]

    @property
    def entities(self):
        class _LoadBalancerEntities:
            Chassis = GenericChassis
            Module = GenericModule
            SubModule = GenericSubModule
            Port = GenericPort
            PortChannel = GenericPortChannel
            PowerPort = GenericPowerPort

        return _LoadBalancerEntities
