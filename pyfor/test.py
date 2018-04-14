import importlib.machinery
import matplotlib.pyplot as plt
pyfor = importlib.machinery.SourceFileLoader('pyfor','/home/bryce/Programming/PyFor/pyfor/__init__.py').load_module()
reload(pyfor)

import laspy

pc = pyfor.cloud.Cloud("/home/bryce/Programming/PyFor/pyfortest/data/test.las")

a = pc.clip((pc.las.header.min[0], pc.las.header.min[0]+5, pc.las.header.min[1], pc.las.header.min[1] + 5))

pc_grid = pc.grid(1)


metrics_df = {
    'z': [np.min, np.mean, np.max]
}

pc_grid.metrics(metrics_df)



interp = pc_grid._interpolate("max", "z")
interp = pc_grid.normalize(7, 2, 0.5)
interp = interp._interpolate("max", "z")

from skimage import feature
from scipy import ndimage

tops = feature.peak_local_max(interp, indices = False, min_distance= 2, threshold_abs=2)
tops = ndimage.label(tops)[0]



from skimage.morphology import watershed
labels = watershed(-interp, tops, mask = interp, watershed_line=True)
