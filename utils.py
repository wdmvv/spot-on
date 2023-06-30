def parse(link):
    parts = link.split('/')
    return parts[-1] if parts[-1] != '' else parts[-2]

def ms_to_s(time_ms):
    time_s = time_ms // 1000 + 60 #offset since some yt track may have intro, outro, etc. 
    return time_s