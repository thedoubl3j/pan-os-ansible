#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2020 Palo Alto Networks, Inc
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

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
module: panos_dynamic_user_group
short_description: Create dynamic user groups on PAN-OS devices.
description:
    - Create dynamic user groups on PAN-OS devices.
author: "Michael Richardson (@mrichardson03)"
version_added: '2.1.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.vsys
    - paloaltonetworks.panos.fragments.device_group
    - paloaltonetworks.panos.fragments.network_resource_module_state
    - paloaltonetworks.panos.fragments.gathered_filter
options:
    name:
        description:
            - Name of the object.
        type: str
    description:
        description:
            - Description of this object
        type: str
    filter:
        description:
            - Tag-based filter
        type: str
    tag:
        description:
            - Administrative tags
        type: list
        elements: str
"""

EXAMPLES = """
- name: Create dynamic user group
  panos_dynamic_user_group:
    provider: '{{ provider }}'
    name: 'Questionable-Users'
    description: 'Questionable Users'
    filter: 'questionable-activity'
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
        vsys=True,
        device_group=True,
        min_panos_version=(9, 1, 0),
        with_classic_provider_spec=True,
        with_network_resource_module_state=True,
        with_gathered_filter=True,
        sdk_cls=("objects", "DynamicUserGroup"),
        sdk_params=dict(
            name=dict(required=True),
            description=dict(),
            filter=dict(),
            tag=dict(type="list", elements="str"),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        required_one_of=helper.required_one_of,
        supports_check_mode=True,
    )

    helper.process(module)


if __name__ == "__main__":
    main()
