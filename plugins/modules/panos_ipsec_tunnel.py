#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2017 Palo Alto Networks, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: panos_ipsec_tunnel
short_description: Configures IPSec Tunnels on the firewall with subset of settings.
description:
    - Use IPSec Tunnels to establish and manage IPSec VPN tunnels between firewalls. This is the Phase 2 portion of the
    - IKE/IPSec VPN setup.
author: "Ivan Bojer (@ivanbojer)"
version_added: '1.0.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
    - paloaltonetworks.panos.fragments.full_template_support
    - paloaltonetworks.panos.fragments.deprecated_commit
options:
    name:
        description:
            - Name for the IPSec tunnel.
        type: str
    tunnel_interface:
        description:
            - Specify existing tunnel interface that will be used.
        type: str
        default: 'tunnel.1'
    anti_replay:
        description:
            - Enable anti-replay check on this tunnel.
        type: bool
        default: True
    ipv6:
        description:
            - Use IPv6 for the IPsec tunnel (7.0+)
        type: bool
        default: False
    type:
        description:
            - Type of IPsec tunnel.
        type: str
        choices: ['auto-key', 'manual-key', 'global-protect-satellite']
        default: 'auto-key'
    ak_ike_gateway:
        description:
            - Name of the existing IKE gateway (auto-key).
        type: str
        default: 'default'
        aliases:
            - ike_gtw_name
    ak_ipsec_crypto_profile:
        description:
            - Name of the existing IPsec profile or use default (auto-key).
        type: str
        default: 'default'
        aliases:
            - ipsec_profile
    mk_local_spi:
        description:
            - Outbound SPI in hex (manual-key).
        type: str
    mk_interface:
        description:
            - Interface to terminate tunnel (manual-key).
        type: str
    mk_remote_spi:
        description:
            - Inbound SPI in hex (manual-key).
        type: str
    mk_remote_address:
        description:
            - Tunnel peer IP address (manual-key).
        type: str
    mk_local_address_ip:
        description:
            - Exact IP address if interface has multiple IP addresses (manual-key).
        type: str
    mk_local_address_floating_ip:
        description:
            - Floating IP address in HA Active-Active configuration (manual-key).
        type: str
    mk_protocol:
        description:
            - Protocol for traffic through the tunnel (manual-key).
        type: str
        choices: ['esp', 'ah']
    mk_auth_type:
        description:
            - Authentication type for tunnel access (manual-key).
        type: str
        choices: ['md5', 'sha1', 'sha256', 'sha384', 'sha512']
    mk_auth_key:
        description:
            - Authentication key (manual-key).
        type: str
    mk_esp_encryption:
        description:
            - Encryption algorithm for tunnel traffic (manual-key).
        type: str
        choices: ['des', '3des', 'aes-128-cbc', 'aes-192-cbc', 'aes-256-cbc', 'null']
    mk_esp_encryption_key:
        description:
            - Encryption key (manual-key).
        type: str
    gps_portal_address:
        description:
            - GlobalProtect portal address (global-protect-satellite).
        type: str
    gps_prefer_ipv6:
        description:
            - Prefer to register portal in IPv6 (8.0+) (global-protect-satellite).
        type: bool
        default: False
    gps_interface:
        description:
            - Interface to communicate with portal (global-protect-satellite).
        type: str
    gps_interface_ipv4_ip:
        description:
            - Exact IPv4 IP address if interface has multiple IP addresses (global-protect-satellite).
        type: str
    gps_interface_ipv6_ip:
        description:
            - Exact IPv6 IP address if interface has multiple IP addresses (8.0+) (global-protect-satellite).
        type: str
    gps_interface_ipv4_floating_ip:
        description:
            - Floating IPv4 IP address in HA Active-Active configuration (7.0+) (global-protect-satellite).
        type: str
    gps_interface_ipv6_floating_ip:
        description:
            - Floating IPv6 IP address in HA Active-Active configuration (8.0+) (global-protect-satellite).
        type: str
    gps_publish_connected_routes:
        description:
            - Enable publishing of connected and static routes (global-protect-satellite).
        type: bool
        default: False
    gps_publish_routes:
        description:
            - Specify list of routes to publish to GlobalProtect gateway (global-protect-satellite).
        type: list
        elements: str
    gps_local_certificate:
        description:
            - GlobalProtect satellite certificate file name (global-protect-satellite).
        type: str
    gps_certificate_profile:
        description:
            - Profile for authenticating GlobalProtect gateway certificates (global-protect-satellite).
        type: str
    copy_tos:
        description:
            - Copy IP TOS bits from inner packet to IPSec packet (not recommended).
        type: bool
        default: False
    copy_flow_label:
        description:
            - Copy IPv6 flow label for 6in6 tunnel from inner packet to IPSec packet (not recommended) (7.0+).
        type: bool
        default: False
    enable_tunnel_monitor:
        description:
            - Enable tunnel monitoring on this tunnel.
        type: bool
        default: False
    tunnel_monitor_dest_ip:
        description:
            - Destination IP to send ICMP probe.
        type: str
    tunnel_monitor_proxy_id:
        description:
            - Which proxy-id (or proxy-id-v6) the monitoring traffic will use.
        type: str
    tunnel_monitor_profile:
        description:
            - Monitoring action.
        type: str
    disabled:
        description:
            - Disable the IPsec tunnel.
        type: bool
        default: False
"""

EXAMPLES = """
- name: Add IPSec tunnel to IKE gateway profile
  panos_ipsec_tunnel:
    provider: '{{ provider }}'
    name: 'IPSecTunnel-Ansible'
    tunnel_interface: 'tunnel.2'
    ak_ike_gateway: 'IKEGW-Ansible'
    ak_ipsec_crypto_profile: 'IPSec-Ansible'
"""

RETURN = """
# Default return values
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import (
    get_connection,
)


def main():
    helper = get_connection(
        template=True,
        template_stack=True,
        with_classic_provider_spec=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        with_commit=True,
        sdk_cls=("network", "IpsecTunnel"),
        sdk_params=dict(
            name=dict(required=True),
            tunnel_interface=dict(default="tunnel.1"),
            anti_replay=dict(type="bool", default=True),
            ipv6=dict(type="bool", default=False),
            type=dict(
                type="str",
                choices=["auto-key", "manual-key", "global-protect-satellite"],
                default="auto-key",
            ),
            ak_ike_gateway=dict(default="default", aliases=["ike_gtw_name"]),
            ak_ipsec_crypto_profile=dict(default="default", aliases=["ipsec_profile"]),
            mk_local_spi=dict(type="str", default=None),
            mk_interface=dict(type="str", default=None),
            mk_remote_spi=dict(type="str", default=None),
            mk_remote_address=dict(type="str", default=None),
            mk_local_address_ip=dict(type="str", default=None),
            mk_local_address_floating_ip=dict(type="str", default=None),
            mk_protocol=dict(type="str", default=None, choices=["esp", "ah"]),
            mk_auth_type=dict(
                type="str",
                default=None,
                choices=["md5", "sha1", "sha256", "sha384", "sha512"],
            ),
            mk_auth_key=dict(type="str", default=None, no_log=True),
            mk_esp_encryption=dict(
                type="str",
                default=None,
                choices=[
                    "des",
                    "3des",
                    "aes-128-cbc",
                    "aes-192-cbc",
                    "aes-256-cbc",
                    "null",
                ],
            ),
            mk_esp_encryption_key=dict(type="str", default=None, no_log=True),
            gps_portal_address=dict(type="str", default=None),
            gps_prefer_ipv6=dict(type="bool", default=False),
            gps_interface=dict(type="str", default=None),
            gps_interface_ipv4_ip=dict(type="str", default=None),
            gps_interface_ipv6_ip=dict(type="str", default=None),
            gps_interface_ipv4_floating_ip=dict(type="str", default=None),
            gps_interface_ipv6_floating_ip=dict(type="str", default=None),
            gps_publish_connected_routes=dict(type="bool", default=False),
            gps_publish_routes=dict(type="list", elements="str", default=None),
            gps_local_certificate=dict(type="str", default=None),
            gps_certificate_profile=dict(type="str", default=None),
            copy_tos=dict(type="bool", default=False),
            copy_flow_label=dict(type="bool", default=False),
            enable_tunnel_monitor=dict(type="bool", default=False),
            tunnel_monitor_dest_ip=dict(type="str", default=None),
            tunnel_monitor_proxy_id=dict(type="str", default=None),
            tunnel_monitor_profile=dict(type="str", default=None),
            disabled=dict(type="bool", default=False),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    helper.process(module)


if __name__ == "__main__":
    main()
