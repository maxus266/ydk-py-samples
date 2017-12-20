#!/usr/bin/env python
#
# Copyright 2016 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Edit configuration for model Cisco-IOS-XE-native.

usage: nc-edit-config-xe-native-router-ospf-34-ydk.py [-h] [-v] device

positional arguments:
  device         NETCONF device (ssh://user:password@host:port)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import NetconfService, Datastore
from ydk.providers import NetconfServiceProvider
from ydk.models.cisco_ios_xe import Cisco_IOS_XE_native \
    as xe_native
from ydk.types import Empty
import logging


def config_native(native):
    """Add config data to native object."""
    # OSPF process
    ospf = native.router.Ospf()
    ospf.id = 172
    ospf.router_id = "172.16.255.1"

    ospf.passive_interface.interface = "Loopback0"

    network = ospf.Network()
    network.ip = "172.16.0.0"
    network.mask = "0.0.0.255"
    network.area = 0

    ospf.network.append(network)

    network = ospf.Network()
    network.ip = "172.16.1.0"
    network.mask = "0.0.0.255"
    network.area = 1

    ospf.network.append(network)

    # OSPF stub Area
    area = ospf.Area()
    area.id = 1
    stub = area.Stub()
    stub.no_summary = Empty()
    area.stub = stub
    ospf.area.append(area)

    native.router.ospf.append(ospf)


if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    parser.add_argument("device",
                        help="NETCONF device (ssh://user:password@host:port)")
    args = parser.parse_args()
    device = urlparse(args.device)

    # log debug messages if verbose argument specified
    if args.verbose:
        logger = logging.getLogger("ydk")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                      "%(levelname)s - %(message)s"))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # create NETCONF provider
    provider = NetconfServiceProvider(address=device.hostname,
                                      port=device.port,
                                      username=device.username,
                                      password=device.password,
                                      protocol=device.scheme)
    # create NETCONF service
    netconf = NetconfService()

    native = xe_native.Native()  # create object
    config_native(native)  # add object configuration

    # edit configuration on NETCONF device
    # netconf.lock(provider, Datastore.running)
    netconf.edit_config(provider, Datastore.running, native)
    # netconf.unlock(provider, Datastore.running)

    exit()
# End of script