import asyncio

from hid_functions import *

RAW_EPSIZE = 32 # All data reports have 33 bytes: 0th byte is for the Report ID, leaving 32 bytes of payload data.
RGB_MATRIX_LED_COUNT = 87 # The Keychron Q3 has 87 RGB keys in its RGB Matrix (the encoder knob counts as a keycode but NOT an RGB light)



(                                                                                           
    KC_ESC,   KC_F1,    KC_F2,    KC_F3,    KC_F4,    KC_F5,    KC_F6,    KC_F7,    KC_F8,    KC_F9,    KC_F10,   KC_F11,   KC_F12,               KC_PSCR,  KC_NO,    RGB_MOD,
    KC_GRV,   KC_1,     KC_2,     KC_3,     KC_4,     KC_5,     KC_6,     KC_7,     KC_8,     KC_9,     KC_0,     KC_MINS,  KC_EQL,     KC_BSPC,  KC_INS,   KC_HOME,  KC_PGUP,
    KC_TAB,   KC_Q,     KC_W,     KC_E,     KC_R,     KC_T,     KC_Y,     KC_U,     KC_I,     KC_O,     KC_P,     KC_LBRC,  KC_RBRC,    KC_BSLS,  KC_DEL,   KC_END,   KC_PGDN,
    KC_CAPS,  KC_A,     KC_S,     KC_D,     KC_F,     KC_G,     KC_H,     KC_J,     KC_K,     KC_L,     KC_SCLN,  KC_QUOT,              KC_ENT,
    KC_LSFT,            KC_Z,     KC_X,     KC_C,     KC_V,     KC_B,     KC_N,     KC_M,     KC_COMM,  KC_DOT,   KC_SLSH,              KC_RSFT,            KC_UP,
    KC_LCTL,  KC_LWIN,  KC_LALT,                                KC_SPC,                                 KC_RALT,  KC_RWIN,  KC_FN,      KC_RCTL,  KC_LEFT,  KC_DOWN,  KC_RGHT
) = range(RGB_MATRIX_LED_COUNT)


def generate_keymap(regions: list[set[int]]):
    keymap = [0x00] * RGB_MATRIX_LED_COUNT
    for region, keys in enumerate(regions):
        for key in keys:
            keymap[key] = region
    
    return keymap


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

    keymap = [0x00] * RGB_MATRIX_LED_COUNT

    for i in range(RGB_MATRIX_LED_COUNT):
        keymap[i] = i % 3

    colors = [
        [0, 255, 000, 000],
        [1, 255, 50, 000],
        [2, 255, 100, 000]
    ]

    write_keymap(keymap)

    set_region_colors(colors)


if __name__ == '__main__':
    asyncio.run(main())
    