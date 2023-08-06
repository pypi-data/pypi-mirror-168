#!/usr/bin/env python3

import sys
import logging

sys.path.insert(0, '/home/x/OneDrive/Projects/btsm/src')
import btsm
from btsm import *

sys.path.insert(0, '/home/x/OneDrive/Projects/pyclui/src')
from pyclui import Logger

logger = Logger(__name__, logging.DEBUG)

sys.path.insert(0, '/home/x/OneDrive/Projects/bthci/src')
from bthci import HCI, ControllerErrorCodes

sys.path.insert(0, '/home/x/OneDrive/Projects/btl2cap/src')
from btl2cap import CID_BR_EDR_SECURITY_MANAGER


from scapy.layers.bluetooth import HCI_Cmd_LE_Create_Connection, HCI_ACL_Hdr, L2CAP_Hdr, SM_Confirm, SM_Failed ,SM_Pairing_Request, SM_Random
from scapy.layers.bluetooth import BluetoothHCISocket, SM_Hdr

from pyclui import Logger, DEBUG

logger = Logger(__name__, DEBUG)

CID_SMP = 0x0006

NEXUS_5_BD_ADDR = '58:3F:54:47:9A:1D'

HUAWEI_MATE_X2_BD_ADDR = 'A0:DE:0F:89:68:93'


def test_smp_over_le():
    hci = HCI('hci0')

   
    event_params = hci.le_create_connection('78:24:01:A9:93:B6', 0x01)
    logger.debug(event_params)

    connhdl = event_params['Connection_Handle']
    
    logger.info("Sending SMP Pairing_Request")
    btsm.send_pairing_request(
        event_params['Connection_Handle'],
        pairing_req=SM_Hdr(sm_command=CmdCode.PAIRING_REQUEST) / \
            SM_Pairing_Request(iocap="NoInputNoOutput", oob='Not Present', 
                authentication=(0b00 << AUTHREQ_RFU_POS) | (0 << CT2_POS) | \
                    (0 << KEYPRESS_POS) | (0 << SC_POS) | (0 << MITM_POS) | \
                    (NO_BONDING << BONDING_FLAGS_POS), max_key_size=0x7,
                initiator_key_distribution=(0b0000 << INIT_RESP_KEY_DIST_RFU_POS) \
                    | (0 << LINKKEY_POS) | (0 << SIGNKEY_POS) | (0 << IDKEY_POS) \
                    | (0 << ENCKEY_POS),
                responder_key_distribution=(0b0000 << INIT_RESP_KEY_DIST_RFU_POS) \
                    | (0 << LINKKEY_POS) | (0 << SIGNKEY_POS) | (0 << IDKEY_POS) \
                    | (0 << ENCKEY_POS)), hci='hci0')

    # pairing_req_pkt = bytes(SM_Hdr(sm_command=0x01)/SM_Pairing_Request(
    #     iocap='KeyboardDisplay', oob=0, authentication=0b00000000,
    #     max_key_size=0x11,
    #     initiator_key_distribution=0b00000001,
    #     responder_key_distribution=0b00000001)) #+ b'\xff'*1000
    # acl_data = bytes(L2CAP_Hdr(len=len(pairing_req_pkt), cid=CID_SMP)) + pairing_req_pkt
    # recv_data = hci.send_acl_data(HCI_ACL_Hdr(handle=connhdl, len=len(acl_data)), acl_data)
    # logger.info("Recv: {}".format(recv_data))

    # time.sleep(5)
    # logger.info("Sending SMP Pairing_Confirm, Mconfirm")
    # # pairing_confirm_pkt = bytes(SM_Hdr(sm_command=0x03)/SM_Confirm(confirm=b'\x00'*160))
    # pairing_confirm_pkt = bytes(SM_Hdr(sm_command=0x03)/SM_Confirm(confirm=b'\x00'*16)) + b'\xff'*1000
    # acl_data = bytes(L2CAP_Hdr(len=len(pairing_confirm_pkt), cid=CID_SMP)) + pairing_confirm_pkt
    # recv_data = hci.send_acl_data(HCI_ACL_Hdr(handle=connhdl, len=len(acl_data)), acl_data)
    # logger.info("Recv: {}".format(recv_data))

    # time.sleep(5)
    # logger.info("Sending SMP Pairing_Random, Mrand")
    # pairing_random_pkt = bytes(SM_Hdr(sm_command=0x04)/SM_Random(random=b'\x01'*16)) + b'\xff'*1000
    # acl_data = bytes(L2CAP_Hdr(len=len(pairing_random_pkt), cid=CID_SMP)) + pairing_random_pkt
    # recv_data = hci.send_acl_data(HCI_ACL_Hdr(handle=connhdl, len=len(acl_data)), acl_data)
    # logger.info("Recv: {}".format(recv_data))

    # time.sleep(5)
    # logger.info("Sending SMP Pairing_Failed")
    # pairing_random_pkt = bytes(SM_Hdr(sm_command=0x04)/SM_Random(random=b'\x01'*16))
    # acl_data = bytes(L2CAP_Hdr(len=len(pairing_random_pkt), cid=CID_SMP)) + pairing_random_pkt
    # recv_data = hci.send_acl_data(HCI_ACL_Hdr(handle=connhdl, len=len(acl_data)), acl_data)
    # logger.info("Recv: {}".format(recv_data))
    
    # time.sleep(5)
    # logger.info("Sending SMP Pairing_Failed")
    # pairing_random_pkt = bytes(SM_Hdr(sm_command=0x04)/SM_Random(random=b'\x01'*16))
    # acl_data = bytes(L2CAP_Hdr(len=len(pairing_random_pkt), cid=CID_SMP)) + pairing_random_pkt
    # recv_data = hci.send_acl_data(HCI_ACL_Hdr(handle=connhdl, len=len(acl_data)), acl_data)
    # logger.info("Recv: {}".format(recv_data))
    
    # time.sleep(5)
    # logger.info("Sending SMP Pairing_Failed, Pairing Not Supported")
    # pairing_failed_pkt = bytes(SM_Hdr(sm_command=0x05)/SM_Failed(reason=0x05))
    # acl_data = bytes(L2CAP_Hdr(len=len(pairing_failed_pkt), cid=CID_SMP)) + pairing_failed_pkt
    # recv_data = hci.send_acl_data(HCI_ACL_Hdr(handle=connhdl, len=len(acl_data)), acl_data)
    # logger.info("Recv: {}".format(recv_data))

    input("disconnect? ")

    event_params = hci.disconnect(connhdl, ControllerErrorCodes.REMOTE_USER_TERM_CONN)


def test_smp_over_acl_u():
    hci = HCI('hci0')
    
    conn_complete = hci.create_connection(HUAWEI_MATE_X2_BD_ADDR)
    if conn_complete.status != ControllerErrorCodes.SUCCESS:
        logger.error("Failed to connect {} BR/EDR address.\n"
                     "    Connection Complete status: 0x{:02x} {}".format(
                         HUAWEI_MATE_X2_BD_ADDR,
                         conn_complete.status, ControllerErrorCodes[conn_complete.status].name))

    pairing_req = SM_Hdr(sm_command=CmdCode.PAIRING_REQUEST) / \
        SM_Pairing_Request(iocap="NoInputNoOutput", oob='Not Present', 
            authentication=(0b00 << AUTHREQ_RFU_POS) | (0 << CT2_POS) | \
                (0 << KEYPRESS_POS) | (0 << SC_POS) | (0 << MITM_POS) | \
                (NO_BONDING << BONDING_FLAGS_POS), max_key_size=0x7,
            initiator_key_distribution=(0b0000 << INIT_RESP_KEY_DIST_RFU_POS) \
                | (0 << LINKKEY_POS) | (0 << SIGNKEY_POS) | (0 << IDKEY_POS) \
                | (0 << ENCKEY_POS),
            responder_key_distribution=(0b0000 << INIT_RESP_KEY_DIST_RFU_POS) \
                | (0 << LINKKEY_POS) | (0 << SIGNKEY_POS) | (0 << IDKEY_POS) \
                | (0 << ENCKEY_POS))
    data = bytes(L2CAP_Hdr(len=len(pairing_req), cid=CID_BR_EDR_SECURITY_MANAGER)/pairing_req)
    
    result = hci.send_acl_data_pkt(conn_complete.conn_handle, data)
    print(btsm.recv_pairing_response(hci, timeout=10))


def main():
    test_smp_over_acl_u()


if __name__ == '__main__':
    main()
