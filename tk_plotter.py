import sys
import os
import json
import multiprocessing

import line_plotter
import load_csv

kColors = ('red', 'green', 'blue', 'cyan', 'yellow', 'magenta')

kDefaultConfig = {'share_coordinate': True}


def plot(plot_config: dict):
    plotter = line_plotter.LinePlotter()
    data = load_csv.load(filename=plot_config['file'],
                         index=plot_config['index'])
    data = tuple(zip(*data))
    for i, y in enumerate(data[1:]):
        plotter.add_line(ys=y, xs=data[0], color=kColors[i % len(kColors)])
    plotter.draw(title=plot_config['title'],
                 share_coordinate=plot_config['share_coordinate'])


def main():
    assert len(sys.argv) == 2, 'no parameter, it should be one json config'
    path_config = sys.argv[1]
    assert os.path.isfile(path_config), 'config not found'
    assert path_config.endswith('.json'), 'run tk_plotter.py CONFIG.json'
    with open(path_config) as fi:
        config = json.loads(fi.read())
    assert type(config) == type([]), 'config must contain a list'
    assert all(type(e) == type(dict())
               for e in config), 'each element must be dict'
    assert all(i in e for e in config
               for i in ('file', 'index', 'title')), 'config not complete'
    assert all(len(pc['index']) >= 2
               for pc in config), 'index not enough, must be at least [x,y1]'
    if any(len(pc['index']) >= len(kColors) for pc in config):
        print('too many lines, will reuse color')

    processes = []
    for plot_config in config:
        for config in kDefaultConfig:
            if config not in plot_config:
                plot_config[config] = kDefaultConfig[config]
        processes.append(
            multiprocessing.Process(target=plot, args=(plot_config, )))
        processes[-1].start()
    for p in processes:
        p.join()


if __name__ == '__main__':
    main()
