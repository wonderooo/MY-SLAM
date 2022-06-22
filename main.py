from display import FeaturesPreview, Map3d
import multiprocessing as mp

processes = []
if __name__ == '__main__':
    queue = mp.Queue()

    processes.append(mp.Process(target=FeaturesPreview, args=("videos/0.hevc", queue,)))
    processes.append(mp.Process(target=Map3d, args=(queue,)))
    for proc in processes:
        proc.start()
    for proc in processes:
        proc.join()
    
