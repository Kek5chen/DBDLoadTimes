import numpy as np
import pyscreenshot as ps
import pygetwindow as gw
import time
import json


def takeDbdScreenshot():
    # get window size of window "Dead by Daylight"
    wnd_result_list = gw.getWindowsWithTitle("DeadByDaylight")
    if len(wnd_result_list) == 0:
        print("Could not find window")
        exit(1)
    window = wnd_result_list[0]
    window_size = window.size
    # get window position
    window_position = [window.left, window.top]
    # calculate the offset
    window = (window_position[0], window_position[1],
              window_position[0] + window_size[0],
              window_position[1] + window_size[1])
    # take screenshot
    return ps.grab(bbox=window)


def detectMap(mapLoadImg):
    if mapLoadImg.getpixel(156, 955) == (108, 111, 114):
        return "ormond"


loadingTimes = json.load(open("loadingTimes.json"))

possibleMaps = json.load(open("possibleMaps.json"))

if __name__ == "__main__":
    # take and show a screenshot every second
    loading_since = 0
    while True:
        img = takeDbdScreenshot()

        pixel = img.getpixel((128, 128))

        if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0:
            if loading_since == 0:
                loading_since = time.time()
        elif loading_since != 0:
            totalLoad = time.time() - loading_since
            print("Total loading time: " + str(totalLoad))
            if time.time() - loading_since > 10:
                print("Loading took too long")
                foundMap = ""
                mapId = 0
                for curMap in possibleMaps:
                    mapId += 1
                    print(str(mapId) + ". " + possibleMaps[curMap])
                while not foundMap.isdigit():
                    mapId = input("Enter map number: ")
                    if mapId.isdigit():
                        mapId = int(mapId)
                        if 0 < mapId <= len(possibleMaps):
                            foundMap = list(possibleMaps.keys())[mapId - 1]
                            break

                # append totalLoad to dict loading_times with foundMap as key
                if foundMap in loadingTimes:
                    loadingTimes[foundMap].append(totalLoad)
                else:
                    loadingTimes[foundMap] = [totalLoad]

                # save dict loading_times to json file
                with open("loadingTimes.json", "w") as outfile:
                    json.dump(loadingTimes, outfile, indent=2)
                print("Average loading time for " + possibleMaps[foundMap] + ": " +
                      str(np.average(loadingTimes[foundMap])))
            else:
                print("Loading time too short")

            loading_since = 0

        time.sleep(.2)
