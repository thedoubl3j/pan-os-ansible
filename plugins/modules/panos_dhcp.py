#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2022 Palo Alto Networks, Inc
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
module: panos_dhcp
short_description: Configure DHCP for an interface.
description:
    - Configure DHCP on PAN-OS firewall.
    - This module is really only useful if you intend to gather or delete any
      and all DHCP configuration for a given interface.  Otherwise, you can use
      M(panos_dhcp_relay) without ever having to use this module.
author:
    - Garfield Lee Freeman (@shinmog)
version_added: '2.10.0'
requirements:
    - pan-python >= 0.17
    - pan-os-python >= 1.7.3
notes:
    - Check mode is supported.
    - Panorama is not supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.network_resource_module_state
options:
    name:
        description:
            - The interface name.
        type: str
        required: true
"""

EXAMPLES = """
# Gather all DHCP configuration for an interface
- panos_dhcp:
    provider: '{{ provider }}'
    name: 'ethernet1/1'
    state: 'gathered'

# Delete any and all DHCP configuration
- panos_dhcp:
    provider: '{{ provider }}'
    name: 'ethernet1/1'
    state: absent
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
        with_network_resource_module_state=True,
        with_classic_provider_spec=True,
        panorama_error="This is a firewall only module",
        min_pandevice_version=(1, 7, 3),
        sdk_cls=("network", "Dhcp"),
        sdk_params=dict(
            name=dict(required=True),
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