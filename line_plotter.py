import functools
import tkinter
import math


class LinePlotter(tkinter.Frame):
    def __init__(self):
        self.root = tkinter.Tk()
        super().__init__()
        self._xs = []
        self._ys = []
        self._colors = []
        self._size = (800, 600)
        self._margin = 30
        self._canvas_range = {
            'x': {
                'min': self._margin,
                'max': self._size[0] - self._margin
            },
            'y': {
                'min': self._margin,
                'max': self._size[1] - self._margin
            }
        }

    def add_line(self, ys: list, xs: list = None, color: str = 'blue'):
        if xs is None:
            xs = tuple(range(len(ys)))
        assert len(xs) == len(ys), 'length not matched'
        assert len(xs) > 0, 'line is empty'
        self._xs.append(xs)
        self._ys.append(ys)
        self._colors.append(color)

    def _resolve_canvas(self, xs: list, ys: list):
        assert len(xs) == len(ys), 'data length not matched'

        def dim_resolve(data: list):
            max_val = max(max(val) for val in data)
            min_val = min(min(val) for val in data)
            diff = max(max_val - min_val, 1e-8)
            resolution = 10**(math.floor(math.log10(diff)) - 1)
            max_val = math.ceil(max_val / resolution) * resolution
            min_val = math.floor(min_val / resolution) * resolution
            return {'min': min_val, 'max': max_val, 'resolution': resolution}

        return {'x': dim_resolve(xs), 'y': dim_resolve(ys)}

    @staticmethod
    def _map_array(src_range, dst_range, data):
        scale = (dst_range['max'] - dst_range['min']) / (src_range['max'] -
                                                         src_range['min'])
        src_base = src_range['min']
        dst_base = dst_range['min']
        return tuple(int((s - src_base) * scale + dst_base) for s in data)

    def _map_line(self, xs: list, ys: list, line_range: dict):
        xs_px = self._map_array(line_range['x'], self._canvas_range['x'], xs)
        ys_px = self._map_array(line_range['y'], self._canvas_range['y'], ys)
        ys_px = tuple(self._size[1] - 1 - y_px for y_px in ys_px)
        return xs_px, ys_px

    @classmethod
    def _sparsify(cls, array: list, num: int):
        return array[::max(len(array) // num, 1)]

    @classmethod
    def _label_values(cls, xs: list, ys: list, xs_px: list, ys_px: list,
                      color: str, canvas: tkinter.Canvas):
        # selected = set(cls._sparsify(tuple(range(len(xs))), 6))
        selected = set([ys.index(max(ys)), ys.index(min(ys))])
        num_labels = 6
        half_interval = len(xs) // (num_labels * 2)
        selected = selected.union(
            set(i for i in cls._sparsify(tuple(range(len(xs))), 6) if all(
                abs(i - m) > half_interval for m in selected)))

        offset = 10
        for i in selected:
            canvas.create_text(xs_px[i],
                               ys_px[i] - offset,
                               text='{:.1E}'.format(ys[i]),
                               fill=color)

    def _ticks(self, line_range: dict, canvas: tkinter.Canvas):
        def linspace(start: float, end: float, interval: float):
            ret = [start]
            while ret[-1] <= end:
                ret.append(interval + ret[-1])
            return ret

        xs = linspace(line_range['x']['min'], line_range['x']['max'],
                      line_range['x']['resolution'])
        xs = self._sparsify(xs, 10)
        xs_px = self._map_array(line_range['x'], self._canvas_range['x'], xs)
        for val, pos in zip(xs, xs_px):
            canvas.create_text(pos,
                               self._size[1] - self._margin // 2,
                               text='{:.1E}'.format(val))
            canvas.create_line(pos,
                               0,
                               pos,
                               self._size[1] - self._margin,
                               fill='grey')
        ys = linspace(line_range['y']['min'], line_range['y']['max'],
                      line_range['y']['resolution'])
        ys = self._sparsify(ys, 6)
        ys_px = self._map_array(line_range['y'], self._canvas_range['y'], ys)
        for val, pos in zip(ys, ys_px):
            pos = self._size[1] - 1 - pos
            canvas.create_text(self._margin, pos, text='{:.1E}'.format(val))
            canvas.create_line(self._margin,
                               pos,
                               self._size[0],
                               pos,
                               fill='grey')

    def draw(self, title: str = 'plot', share_coordinate: bool = False):
        assert len(self._xs) > 0, 'empty plot'
        assert len(self._xs) == len(self._ys) == len(
            self._colors), 'lines not matched'
        self.master.title(title)
        self.pack(fill=tkinter.BOTH, expand=1)

        canvas = tkinter.Canvas(self)
        if share_coordinate:
            line_range = self._resolve_canvas(xs=self._xs, ys=self._ys)
            self._ticks(line_range=line_range, canvas=canvas)

        for i in range(len(self._ys)):
            xs_px, ys_px = self._map_line(
                self._xs[i], self._ys[i], line_range if share_coordinate else
                self._resolve_canvas(xs=(self._xs[i], ), ys=(self._ys[i], )))
            self._label_values(xs=self._xs[i],
                               ys=self._ys[i],
                               xs_px=xs_px,
                               ys_px=ys_px,
                               color=self._colors[i],
                               canvas=canvas)
            canvas.create_line(*functools.reduce(
                lambda x_px, y_px: x_px + y_px, zip(xs_px, ys_px)),
                               fill=self._colors[i])

        canvas.pack(fill=tkinter.BOTH, expand=1)
        self.root.geometry(f'{self._size[0]}x{self._size[1]}')
        self.root.mainloop()


if __name__ == '__main__':
    plotter = LinePlotter()
    xs, ys = zip(*[[i / 100, math.sin(i / 100)] for i in range(660)])
    plotter.add_line(ys=ys, xs=xs, color='red')
    xs, ys = zip(*[[i / 100, math.cos(i / 100)] for i in range(660)])
    plotter.add_line(ys=ys, xs=xs, color='blue')
    plotter.draw(title='test')
    # 'red', 'green', 'blue', 'cyan', 'yellow', 'magenta'
