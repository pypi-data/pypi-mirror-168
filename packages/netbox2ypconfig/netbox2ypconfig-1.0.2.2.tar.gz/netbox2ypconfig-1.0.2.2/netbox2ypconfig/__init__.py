"""Program to construct ypconfig YAML configuration file from NetBox."""

import sys
from typing import Dict, List, Optional

import pynetbox
import yaml

from netbox2ypconfig.ypconfig import Attributes


def get(
    device_name: str,
    default_routes: List[str],
    netbox_host: str,
    netbox_token: str,
) -> str:
    """Construct and return configuration."""
    output: Dict[str, Dict] = {}

    # Get API object

    nb = pynetbox.api(
        netbox_host,
        token=netbox_token,
    )

    # Get device ID by device name

    device_id = nb.dcim.devices.get(name=device_name)["id"]

    # Get interfaces by device ID

    for interface in nb.dcim.interfaces.filter(device_id=device_id):
        # Set empty variables

        adminstate: Optional[str] = None
        description: Optional[str] = None
        mtu: Optional[int] = None
        name: Optional[str] = None
        parent: Optional[str] = None
        type_: Optional[str] = None
        vlanid: Optional[int] = None
        autoconfigure: Optional[str] = None
        vaddresses: list = []
        addresses: list = []

        # Set admin state

        if interface.enabled:
            adminstate = "UP"
        else:
            adminstate = "DOWN"

        # Set description

        if interface.description:
            description = interface.description
        else:
            description = interface.name

        # Set MTU

        if interface.mtu:
            mtu = interface.mtu
        else:
            mtu = 1500

        # Set name

        name = interface.name

        # Set vLAN attributes

        if (
            interface.parent
        ):  # Maybe someone wants to add bond, slave, loopback
            type_ = "vlan"

            if len(interface.tagged_vlans) > 1:
                raise Exception("Too many vLANs")

            vlanid = interface.tagged_vlans[0].vid
            parent = interface.parent.name
            autoconfigure = "none"
        else:
            type_ = "default"

        # Set addresses and vaddresses

        addresses = []
        vaddresses = []

        for address in nb.ipam.ip_addresses.filter(interface_id=interface.id):
            if address.role:
                if str(address.role) == "VRRP":
                    vaddresses.append(address.address)
            else:
                addresses.append(address.address)

        # Add to configuration

        output[interface.name] = {}

        if adminstate:
            output[interface.name][Attributes.ADMINSTATE] = adminstate
        if description:
            output[interface.name][Attributes.DESCRIPTION] = description
        if mtu:
            output[interface.name][Attributes.MTU] = mtu
        if name:
            output[interface.name][Attributes.NAME] = name
        if type_:
            output[interface.name][Attributes.TYPE] = type_
        if vlanid:
            output[interface.name][Attributes.VLANID] = vlanid
        if parent:
            output[interface.name][Attributes.PARENT] = parent
        if autoconfigure:
            output[interface.name][Attributes.AUTOCONFIGURE] = autoconfigure
        if addresses:
            output[interface.name][Attributes.ADDRESSES] = addresses
        if vaddresses:
            output[interface.name][Attributes.VADDRESSES] = vaddresses

    # Always add loopback interface

    output["lo"] = {
        Attributes.ADDRESSES: ["127.0.0.1/8", "::1/128"],
        Attributes.ADMINSTATE: "UP",
        Attributes.DESCRIPTION: "lo",
        Attributes.MTU: 65536,
        Attributes.NAME: "lo",
        Attributes.TYPE: "loopback",
    }

    # Add default routes

    output[Attributes.ROUTES] = {"default": default_routes}

    # Return YAML

    return yaml.dump(output, sort_keys=False, explicit_start=True)


def main() -> None:
    """Call get function."""
    try:
        print(
            get(
                device_name=sys.argv[1],
                default_routes=sys.argv[2].split(","),
                netbox_host=sys.argv[3],
                netbox_token=sys.argv[4],
            )
        )
    except IndexError:
        print("Not enough arguments")
