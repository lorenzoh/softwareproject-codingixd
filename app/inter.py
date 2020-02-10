from detector import Detector
from app import REGIONS

d = Detector(REGIONS, 1)

d.setup()

print(d.process_frame())

d.cleanup()



def main(args):
    ledclient = LEDClient(args.controllerurl)
    detector = Detector(args.cameraid)


    try:
        while True:
            print("---")
            frame, markers = detector.get_markers()
            print(len(markers))
            markerregions, markertimeouts = update_regions(
                markers, REGIONS, markerregions, markertimeouts
            )
            print(json.dumps(dict(markerregions), indent=2))
            
            # count markers for every region
            region_counts = {region: 0 for region in REGIONS}
            for markerid, regionname in markerregions.items():
                if regionname is None:
                    continue
                region_counts[regionname] += 1
            
            for regionname, count in region_counts.items():
                light_region(regionname, count, ledclient)

            draw_debug(frame, markers, REGIONS)
            lh, lw = int(frame.shape[0]*2), int(frame.shape[1]*2)
            frame = cv2.resize(frame, (lw, lh))
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        detector.cleanup()