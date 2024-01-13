'''
    Litle thing for sideloading, for instance, you can specify yt link or local path to the audio (so it uses it instead of yt search)
'''

import spoton.structs as structs

def load(filename: str, playlist: list[structs.Track]):
    to_update = {}
    with open(filename, 'r') as f:
        data = f.readlines()
        for i in data:
            name, type, whr = i.strip().split(";")

            if not (name and type and whr):
                continue
            print("sideloaded!")
            name = name.replace(",", "").replace(".", "").replace("/", "-").replace("\\", "-")
            if type in {"link", "l", "url", "u"}:
                type = "link"
            elif type in {"path", "p"}:
                type = "path"
            else:
                continue

            to_update[name] = (type, whr)

    for i in playlist:
        if i.track_name in to_update:
            i.content_type = to_update[i.track_name][0]
            i.content_path = to_update[i.track_name][1]
            