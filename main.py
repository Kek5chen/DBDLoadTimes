import atexit
import numpy as np
import pandas as pd
import pyscreenshot as ps
import pygetwindow as gw
import time
import json
import plotly.express as px


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
    else:
        return ""


loadingTimes = json.load(open("loadingTimes.json"))
possibleMaps = json.load(open("possibleMaps.json"))


def drawLoadingTimesBarChart():
    average_loading_times = list()
    map_translations = list()
    for cur_map in loadingTimes.keys():
        average_loading_times.append(np.average(loadingTimes[cur_map]))
        map_translations.append(possibleMaps[cur_map])
    data_frame = pd.DataFrame(dict(
        map=map_translations,
        average_load=average_loading_times
    ))
    fig = px.bar(data_frame, x="map", y="average_load")
    fig.show()


def shutdown():
    drawLoadingTimesBarChart()


def isPixelBlack(pixel):
    return pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0


if __name__ == "__main__":
    atexit.register(shutdown)
    # take and show a screenshot every second
    loading_since = 0
    while True:
        time.sleep(.2)
        img = takeDbdScreenshot()
        pixel = img.getpixel((128, 128))

        if isPixelBlack(pixel):
            if loading_since == 0:
                loading_since = time.time()
            continue
        elif loading_since == 0:
            continue

        totalLoad = time.time() - loading_since
        print("Total loading time: " + str(totalLoad))

        if totalLoad < 10:
            print("Loading time too short")
            loading_since = 0
            continue

        # find the map
        foundMap = ""
        mapId = 0
        for curMap in possibleMaps:
            mapId += 1
            print(str(mapId) + ". " + possibleMaps[curMap])
        mapId = ""
        while not mapId.isdigit() or int(mapId) < 1 or int(mapId) > len(possibleMaps):
            mapId = input("Enter map number: ")
        mapId = int(mapId)
        foundMap = list(possibleMaps.keys())[mapId - 1]

        if foundMap in loadingTimes:
            loadingTimes[foundMap].append(totalLoad)
        else:
            loadingTimes[foundMap] = [totalLoad]

        # save dict loading_times to json file
        with open("loadingTimes.json", "w") as outfile:
            json.dump(loadingTimes, outfile, indent=2)
        print("Average loading time for " + possibleMaps[foundMap] + ": " +
              str(np.average(loadingTimes[foundMap])))
        loading_since = 0
