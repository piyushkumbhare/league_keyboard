import random
import sys
import asyncio

import hid
import numpy as np

# QMK Constants - used to identify device when enumerating devices.
USAGE_PAGE = 0xFF60
USAGE = 0x61
RAW_EPSIZE = 32 # All data reports have 33 bytes: 0th byte is for the Report ID, leaving 32 bytes of payload data.
RGB_MATRIX_LED_COUNT = 87

# ID Constants
VENDOR_ID     = 0x3434
PRODUCT_ID    = 0x0121


(
    KC_ESC,   KC_F1,    KC_F2,    KC_F3,    KC_F4,    KC_F5,    KC_F6,    KC_F7,    KC_F8,    KC_F9,    KC_F10,   KC_F11,   KC_F12,     KC_MUTE,  KC_PSCR,  KC_NO,    RGB_MOD,
    KC_GRV,   KC_1,     KC_2,     KC_3,     KC_4,     KC_5,     KC_6,     KC_7,     KC_8,     KC_9,     KC_0,     KC_MINS,  KC_EQL,     KC_BSPC,  KC_INS,   KC_HOME,  KC_PGUP,
    KC_TAB,   KC_Q,     KC_W,     KC_E,     KC_R,     KC_T,     KC_Y,     KC_U,     KC_I,     KC_O,     KC_P,     KC_LBRC,  KC_RBRC,    KC_BSLS,  KC_DEL,   KC_END,   KC_PGDN,
    KC_CAPS,  KC_A,     KC_S,     KC_D,     KC_F,     KC_G,     KC_H,     KC_J,     KC_K,     KC_L,     KC_SCLN,  KC_QUOT,              KC_ENT,
    KC_LSFT,            KC_Z,     KC_X,     KC_C,     KC_V,     KC_B,     KC_N,     KC_M,     KC_COMM,  KC_DOT,   KC_SLSH,              KC_RSFT,            KC_UP,
    KC_LCTL,  KC_LWIN,  KC_LALT,                                KC_SPC,                                 KC_RALT,  KC_RWIN,  KC_FN,      KC_RCTL,  KC_LEFT,  KC_DOWN,  KC_RGHT
) = range(0, 88)


def generate_keymap(regions: list[set[int]]):
    pass





def get_raw_hid_interface(vendor_id: int, product_id: int):
    device_interfaces = hid.enumerate(vendor_id, product_id)
    raw_hid_interfaces = [i for i in device_interfaces if i['usage_page'] == USAGE_PAGE and i['usage'] == USAGE]

    if len(raw_hid_interfaces) == 0:
        return None

    interface = hid.Device(path=raw_hid_interfaces[0]['path'])

    return interface





def send_raw_report(payload: list[int]):
    interface = get_raw_hid_interface(VENDOR_ID, PRODUCT_ID)

    if(interface is None):
        print("ERROR: No device found")
        sys.exit(1)

    report = [0x00, *payload]
    # print(report)


    try:
        report_bytes = bytes(report)
        interface.write(report_bytes)

    finally:
        interface.close()





def send_group_report(payloads: list[list[int]]):
    interface = get_raw_hid_interface(VENDOR_ID, PRODUCT_ID)

    if(interface is None):
        print("ERROR: No device found")
        sys.exit(1)
        
    try:
        for payload in payloads:
            report = [0x00, *payload]
            # print(report)
            
            report_bytes = bytes(report)
            interface.write(report_bytes)
    
    finally:
        interface.close()





def toggle_custom_colors(state: bool):
    
    payload = [0x00] * RAW_EPSIZE

    if(state):
        payload[0] = ord('Y')
    
    else:
        payload[0] = ord('N')

    send_raw_report(payload)


def reset_keymap_to_default():

    payload = [0x00] * RAW_EPSIZE

    payload[0] = ord('D')

    send_raw_report(payload)


def set_region_colors(queries: list[list[int]]):
    payloads = []
    for query in queries:
        if(len(query) != 4):
            print("ERROR: Each color query in set_region_colors should be of the form [region, r, g, b]")
            return
        
        valid = all(0 <= d and d <= 255 for d in query)

        if not valid:
            print("ERROR: Values region, r, g, & b must be between 0 & 255")
            return
        
        current_payload = [0x00] * RAW_EPSIZE
        for i, val in enumerate(query):
            current_payload[i] = val

        payloads.append(current_payload)

    send_group_report(payloads)        





def write_keymap(keymap: list[int]):
    payloads = []
    if(len(keymap) != RGB_MATRIX_LED_COUNT):
        print(f"ERROR: Keymap size {len(keymap)} doesn't match RGB_MATRIX_LED_COUNT ({RGB_MATRIX_LED_COUNT})")

    valid = all(0 <= d and d <= 255 for d in keymap)
    if not valid:
        print("ERROR: All values in keymap must be integers between 0 & 255")

    def split_list(original_list, sublist_size):
        return [original_list[i:i + sublist_size] for i in range(0, len(original_list), sublist_size)]

    split_keymap = split_list(keymap, 31)

    for segment, subset in enumerate(split_keymap):
        payload = [ord('A') + segment, *subset]
        
        payloads.append(payload)

    send_group_report(payloads)

async def main():
    generate_keymap(())

if __name__ == '__main__':
    asyncio.run(main())
    