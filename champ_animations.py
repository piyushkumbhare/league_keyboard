from hidmanager import *
import random
import requests
import sys


def check_valid(response: requests.Response):
    if(response.status_code < 200 or 299 < response.status_code):
        print("ERROR: Problem with request to Riot Server")
        print(f"URL: {response.url}\nStatus Code: {response.status_code}; {response.reason}")
        print("Aborting with exit code 1")
        sys.exit(1)


# The following code snippet generates a list of all champs and their data using Riot's Data Dragon API.

# version_request = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
# check_valid(version_request)
# version = version_request.json()[0]

# raw_champ_request = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json")
# check_valid(raw_champ_request)
# raw_champ_json = raw_champ_request.json()

# champs = raw_champ_json['data']
# champs_all = [data for data in champs.values()]




async def keyboard_animation(champion: str):

    toggle_custom_colors(True)

    match champion.upper():
        case "AATROX":
            reset_keymap_to_default()
            colors = [
                [0, 255, 000, 000],
                [1, 100, 000, 000]
            ]
            set_region_colors(colors)
        
        case "AHRI":
            reset_keymap_to_default()
            colors = [
                [0, 150, 150, 255],
                [1, 255, 000, 100]
            ]
            set_region_colors(colors)
            
        case "ZERI":
            keymap = generate_keymap(
                [
                    (),
                    (
                        KC_F3, KC_3, KC_W, KC_E, KC_R, KC_D, KC_X, KC_LALT,
                        KC_F6, KC_7, KC_U, KC_H, KC_N,
                        KC_F11, KC_MINS, KC_P, KC_LBRC, KC_RBRC, KC_QUOT, KC_SLSH
                    )
                ]
            )

            write_keymap(keymap)
            base = [
                [0, 50, 50, 000],
                [1, 50, 50, 000],
            ]
            set_region_colors(base)

            dark = [
                [0, 0, 0, 0],
                [1, 0, 0, 0]
            ]

            lightning = [
                [0, 0, 0, 0],
                [1, 255, 50, 0]
            ]

            half_dark = [
                [0, 0, 0, 0],
                [1, 125, 25, 0]
            ]

            for _ in range(10):
                await asyncio.sleep(5)

                set_region_colors(lightning)
                await asyncio.sleep(0.3)
                set_region_colors(half_dark)
                await asyncio.sleep(0.3)
                set_region_colors(lightning)
                await asyncio.sleep(0.3)
                set_region_colors(half_dark)
                await asyncio.sleep(0.3)
                set_region_colors(lightning)
                await asyncio.sleep(0.3)
                set_region_colors(half_dark)
                await asyncio.sleep(0.3)
                set_region_colors(lightning)

                await asyncio.sleep(2)



                set_region_colors(base)



        case _:
            toggle_custom_colors(False)

    
    return


async def main():
    name = ""
    
    while(name.upper() != "QUIT"):
        name = input("Enter Champion Name: ")
        await keyboard_animation(name)


if __name__ == '__main__':
    asyncio.run(main())