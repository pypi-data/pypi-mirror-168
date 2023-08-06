#!/usr/bin/env python3
import json

from .utils import join as utils_join
from os.path import isfile
from re import sub


def episode_search(library, episode, base_dir):
    """
    First perform a simple search for the episode by checking if it is
    listed in the user's library. This may not be 100% accurate if your library
    is not up-to-date, for that reason if the simple search does not return
    anything we do a deeper search to see if the file exists in your base_dir
    in a tracked show. If all of this fails we return None
    """
    # Perform simple search for the episode
    for key in library.keys():
        episodes = library[key]["episodes"]
        for ep in episodes:
            if ep == episode:
                return key
    # If the simple seach does not return anything we do a more involved search
    for dir in library.keys():
        try_dir = utils_join(base_dir, dir)
        try_episode = utils_join(try_dir, episode)
        if isfile(try_episode):
            return dir
    return None


def main_search(user, episode, track=False):
    """The main search loop"""
    with open(user.files["library_file"], "r") as data:
        library = json.load(data)
    episode = sub(r"^.*/", "", episode)
    dir = episode_search(library, episode, base_dir=user.settings["base_dir"])
    if dir is None:
        return 1
    if track:
        library = track_episode(dir, episode, library, user)
        with open(user.files["library_file"], "w+") as data:
            json.dump(library, data, indent=4)
    return 0


def track_episode(dir, episode, library, user):
    """
    Track an episode in user's library by updating
    thier library and log file
    """
    log_file = user.files["log_file"]
    max = int(user.settings["max_history"])
    # Update library
    library[dir]["watching"] = episode
    log = {}
    log[dir] = library[dir]
    if isfile(log_file):
        with open(log_file, "r") as data:
            old_log = json.load(data)
            if dir in old_log:
                old_log.pop(dir)
            if len(old_log) >= max:
                old_log.popitem()
            log.update(old_log)
    with open(log_file, "w+") as data:
        json.dump(log, data, indent=4)
    return library
