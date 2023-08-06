import sys
import unittest

from cloudshell.shell.standards.attribute_names import (
    BACKUP_LOCATION,
    BACKUP_PASSWORD,
    BACKUP_TYPE,
    BACKUP_USER,
    CLI_CONNECTION_TYPE,
    CLI_TCP_PORT,
    CONSOLE_PASSWORD,
    CONSOLE_PORT,
    CONSOLE_SERVER_IP_ADDRESS,
    CONSOLE_USER,
    DISABLE_SNMP,
    ENABLE_SNMP,
    PASSWORD,
    SESSION_CONCURRENCY_LIMIT,
    SNMP_READ_COMMUNITY,
    SNMP_V3_AUTH_PROTOCOL,
    SNMP_V3_PASSWORD,
    SNMP_V3_PRIVACY_PROTOCOL,
    SNMP_V3_PRIVATE_KEY,
    SNMP_V3_USER,
    SNMP_VERSION,
    SNMP_WRITE_COMMUNITY,
    VRF_MANAGEMENT_NAME,
)

from cloudshell.shell.standards.load_balancer.resource_config import (
    LoadBalancerResourceConfig,
)

if sys.version_info >= (3, 0):
    from unittest.mock import MagicMock
else:
    from mock import MagicMock


class TestLoadBalancerResourceConfig(unittest.TestCase):
    def test_snmp_config(self):
        shell_name = "Shell name"
        api = MagicMock(DecryptPassword=lambda password: MagicMock(Value=password))

        attributes = {
            SNMP_READ_COMMUNITY: "community",
            SNMP_WRITE_COMMUNITY: "write community",
            SNMP_V3_USER: "snmp user",
            SNMP_V3_PASSWORD: "snmp password",
            SNMP_V3_PRIVATE_KEY: "snmp private key",
            SNMP_V3_AUTH_PROTOCOL: "snmp auth protocol",
            SNMP_V3_PRIVACY_PROTOCOL: "snmp priv protocol",
            SNMP_VERSION: "v2c",
            ENABLE_SNMP: "True",
            DISABLE_SNMP: "False",
            VRF_MANAGEMENT_NAME: "vrf",
            PASSWORD: "password",
            BACKUP_LOCATION: "backup location",
            BACKUP_PASSWORD: "backup password",
            BACKUP_TYPE: "backup type",
            BACKUP_USER: "backup user",
            CLI_CONNECTION_TYPE: "ssh",
            CLI_TCP_PORT: "22",
            SESSION_CONCURRENCY_LIMIT: "1",
            CONSOLE_PASSWORD: "console password",
            CONSOLE_PORT: "3322",
            CONSOLE_SERVER_IP_ADDRESS: "192.168.1.1",
            CONSOLE_USER: "console user",
        }
        shell_attributes = {
            "{}.{}".format(shell_name, key): value for key, value in attributes.items()
        }

        config = LoadBalancerResourceConfig(
            shell_name, attributes=shell_attributes, api=api
        )
        self.assertEqual(attributes[SNMP_READ_COMMUNITY], config.snmp_read_community)
        self.assertEqual(attributes[SNMP_WRITE_COMMUNITY], config.snmp_write_community)
        self.assertEqual(attributes[SNMP_V3_USER], config.snmp_v3_user)
        self.assertEqual(attributes[SNMP_V3_PASSWORD], config.snmp_v3_password)
        self.assertEqual(attributes[SNMP_V3_PRIVATE_KEY], config.snmp_v3_private_key)
        self.assertEqual(
            attributes[SNMP_V3_AUTH_PROTOCOL], config.snmp_v3_auth_protocol
        )
        self.assertEqual(
            attributes[SNMP_V3_PRIVACY_PROTOCOL], config.snmp_v3_priv_protocol
        )
        self.assertEqual(attributes[SNMP_VERSION], config.snmp_version)
        self.assertEqual(attributes[ENABLE_SNMP], config.enable_snmp)
        self.assertEqual(attributes[DISABLE_SNMP], config.disable_snmp)
        self.assertEqual(attributes[VRF_MANAGEMENT_NAME], config.vrf_management_name)
        self.assertEqual(attributes[PASSWORD], config.password)
        self.assertEqual(attributes[BACKUP_LOCATION], config.backup_location)
        self.assertEqual(attributes[BACKUP_PASSWORD], config.backup_password)
        self.assertEqual(attributes[BACKUP_TYPE], config.backup_type)
        self.assertEqual(attributes[BACKUP_USER], config.backup_user)
        self.assertEqual(attributes[CLI_CONNECTION_TYPE], config.cli_connection_type)
        self.assertEqual(attributes[CLI_TCP_PORT], config.cli_tcp_port)
        self.assertEqual(
            attributes[SESSION_CONCURRENCY_LIMIT], config.sessions_concurrency_limit
        )
        self.assertEqual(attributes[CONSOLE_PASSWORD], config.console_password)
        self.assertEqual(attributes[CONSOLE_PORT], config.console_port)
        self.assertEqual(
            attributes[CONSOLE_SERVER_IP_ADDRESS], config.console_server_ip_address
        )
        self.assertEqual(attributes[CONSOLE_USER], config.console_user)
