import json

def get_frames(fname, frame_count):
    frames = [[] for _ in range(frame_count)]
    with open(fname) as json_data:
        data = json.load(json_data)
        for _,item in data.iteritems():
            for fno,inst in item["boxes"].iteritems():
                inst['label'] = item['label']
                frames[int(fno)].append(inst)
    return frames