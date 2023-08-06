import tifffile
import zarr


def open_ndpi(path, level=0):
    with tifffile.imread(path, aszarr=True) as store:
        group = zarr.open(store, mode='r')
        group_keys = [int(r) for r in group.keys()]
        level = min(level, max(group_keys))
        level = max(level, min(group_keys))
        assert isinstance(group, zarr.Group)
        return group[str(level)]
