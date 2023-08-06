from pathlib import Path
from typing import *
import numpy as np
import pandas as pd
from caiman import load_memmap
from caiman.source_extraction.cnmf import CNMF
from caiman.source_extraction.cnmf.cnmf import load_CNMF
from caiman.utils.visualization import get_contours as caiman_get_contours
from functools import wraps
import os
from copy import deepcopy

from ._utils import validate
from .cache import Cache

cnmf_cache = Cache()


# this decorator MUST be called BEFORE caching decorators!
def _component_indices_parser(func):
    @wraps(func)
    def _parser(instance, *args, **kwargs) -> Any:
        if "component_indices" in kwargs.keys():
            component_indices: Union[np.ndarray, str, None] = kwargs["component_indices"]
        elif len(args) > 0:
            component_indices = args[0]  # always first positional arg in the extensions
        else:
            component_indices = None  # default

        cnmf_obj = instance.get_output()

        # TODO: finally time to learn Python's new switch case
        accepted = (np.ndarray, str, type(None))
        if not isinstance(component_indices, accepted):
            raise TypeError(f"`component_indices` must be one of type: {accepted}")

        if isinstance(component_indices, np.ndarray):
            pass

        elif component_indices is None:
            component_indices = np.arange(cnmf_obj.estimates.A.shape[1])

        if isinstance(component_indices, str):
            accepted = ["all", "good", "bad"]
            if component_indices not in accepted:
                raise ValueError(f"Accepted `str` values for `component_indices` are: {accepted}")

            if component_indices == "all":
                component_indices = np.arange(cnmf_obj.estimates.A.shape[1])

            elif component_indices == "good":
                component_indices = cnmf_obj.estimates.idx_components

            elif component_indices == "bad":
                component_indices = cnmf_obj.estimates.idx_components_bad
        if "component_indices" in kwargs.keys():
            kwargs["component_indices"] = component_indices
        else:
            args = (component_indices, *args[1:])

        return func(instance, *args, **kwargs)
    return _parser


def _check_permissions(func):
    @wraps(func)
    def __check(instance, *args, **kwargs):
        cnmf_obj_path = instance.get_output_path()

        if not os.access(cnmf_obj_path, os.W_OK):
            raise PermissionError(
                "You do not have write access to the hdf5 output file for this batch item"
            )

        return func(instance, *args, **kwargs)
    return __check


@pd.api.extensions.register_series_accessor("cnmf")
class CNMFExtensions:
    """
    Extensions for managing CNMF output data
    """

    def __init__(self, s: pd.Series):
        self._series = s

    @validate("cnmf")
    def get_cnmf_memmap(self) -> np.ndarray:
        """
        Get the CNMF C-order memmap

        Returns
        -------
        np.ndarray
            numpy memmap array used for CNMF
        """
        path = self._series.paths.resolve(self._series["outputs"]["cnmf-memmap-path"])
        # Get order f images
        Yr, dims, T = load_memmap(str(path))
        images = np.reshape(Yr.T, [T] + list(dims), order="F")
        return images

    def get_input_memmap(self) -> np.ndarray:
        """
        Return the F-order memmap if the input to this
        CNMF batch item was a mcorr output memmap

        Returns
        -------
        np.ndarray
            numpy memmap array of the input

        Examples
        --------

        Get the input memmap and view it with random access scrolling

        .. code-block:: python

            from mesmerize_core import load_batch
            from matplotlib import pyplot as plt

            # needs fastplotlib and must be run in a notebook
            from fastplotlib import Plot
            from ipywidgets import IntSlider, VBox

            df = load_batch("/path/to/batch_dataframe_file.pickle")

            # assuming the 0th index is a cnmf item
            movie = df.iloc[0].cnmf.get_input_memmap()

            # plot a frame
            plt.imshow(movie[0])
            plt.show()

            # the following requires fastplotlib and must be run in a new notebook cell
            slider = IntSlider(value=0, min=0, max=movie.shape[0] - 1, step=1)
            plot = Plot()

            image_graphic = plot.image(movie[0], cmap="gnuplot2")

            previous_slider_value = 0
            def update_frame():  # runs on each rendering cycle
                if slider.value == previous_slider_value:
                    return
                image_graphic.update_data(data=movie[slider.value])

            plot.add_animations([update_frame])

            VBox([plot.show(), slider])

        """
        movie_path = str(self._series.caiman.get_input_movie_path())
        if movie_path.endswith("mmap"):
            Yr, dims, T = load_memmap(movie_path)
            images = np.reshape(Yr.T, [T] + list(dims), order="F")
            return images
        else:
            raise TypeError(
                f"Input movie for CNMF was not a memmap, path to input movie is:\n"
                f"{movie_path}"
            )

    @validate("cnmf")
    def get_output_path(self) -> Path:
        """
        Get the path to the cnmf hdf5 output file.

        **Note:** You generally want to work with the other extensions instead of directly using the hdf5 file.

        Returns
        -------
        Path
            full path to the caiman-format CNMF hdf5 output file

        """
        return self._series.paths.resolve(self._series["outputs"]["cnmf-hdf5-path"])

    @validate("cnmf")
    @cnmf_cache.use_cache
    def get_output(self, return_copy=True) -> CNMF:
        """
        Parameters
        ----------
        return_copy: bool
            | if ``True`` returns a copy of the cached value in memory.
            | if ``False`` returns the same object as the cached value in memory, not recommend this could result in strange unexpected behavior.
            | In general you want a copy of the cached value.

        Returns
        -------
        CNMF
            Returns the Caiman CNMF object

        Examples
        --------

        Load the CNMF model with estimates from the hdf5 file.

        .. code-block:: python

            from mesmerize_core import load_batch

            df = load_batch("/path/to/batch_dataframe_file.pickle")

            # assume the 0th index is a cnmf item
            cnmf_obj = df.iloc[0].cnmf.get_output()

            # see some estimates
            print(cnmf_obj.estimates.C)
            print(cnmf_obj.estimates.f)

        """
        # Need to create a cache object that takes the item's UUID and returns based on that
        # collective global cache
        return load_CNMF(self.get_output_path())

    @validate("cnmf")
    @_component_indices_parser
    @cnmf_cache.use_cache
    def get_masks(
        self, component_indices: Union[np.ndarray, str] = None, threshold: float = 0.01, return_copy=True
    ) -> np.ndarray:
        """
        | Get binary masks of the spatial components at the given ``component_indices``.
        | Created from ``CNMF.estimates.A``

        Parameters
        ----------
        component_indices: optional, Union[np.ndarray, str]
            | indices of the components to include
            | if ``np.ndarray``, uses these indices in the provided array
            | if ``"good"`` uses good components, i.e. cnmf.estimates.idx_components
            | if ``"bad"`` uses bad components, i.e. cnmf.estimates.idx_components_bad
            | if not provided, ``None``, or ``"all"`` uses all components


        threshold: float
            threshold

        return_copy: bool
            | if ``True`` returns a copy of the cached value in memory.
            | if ``False`` returns the same object as the cached value in memory, not recommend this could result in strange unexpected behavior.
            | In general you want a copy of the cached value.

        Returns
        -------
        np.ndarray
            shape is [dim_0, dim_1, n_components]

        """
        cnmf_obj = self.get_output()

        dims = cnmf_obj.dims
        if dims is None:
            dims = cnmf_obj.estimates.dims

        masks = np.zeros(shape=(dims[0], dims[1], len(component_indices)), dtype=bool)

        for n, ix in enumerate(component_indices):
            s = cnmf_obj.estimates.A[:, ix].toarray().reshape(cnmf_obj.dims)
            s[s >= threshold] = 1
            s[s < threshold] = 0

            masks[:, :, n] = s.astype(bool)

        return masks

    @staticmethod
    def _get_spatial_contours(
        cnmf_obj: CNMF, component_indices, swap_dim
    ):

        dims = cnmf_obj.dims
        if dims is None:
            # I think that one of these is `None` if loaded from an hdf5 file
            dims = cnmf_obj.estimates.dims

        # need to transpose these
        if swap_dim:
            dims = dims[1], dims[0]
        else:
            dims = dims[0], dims[1]

        contours = caiman_get_contours(
            cnmf_obj.estimates.A[:, component_indices], dims, swap_dim=swap_dim
        )

        return contours

    @validate("cnmf")
    @_component_indices_parser
    @cnmf_cache.use_cache
    def get_contours(
            self,
            component_indices: Union[np.ndarray, str] = None,
            swap_dim: bool = True,
            return_copy=True
    ) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        """
        Get the contour and center of mass for each spatial footprint

        Parameters
        ----------
        component_indices: optional, Union[np.ndarray, str]
            | indices of the components to include
            | if ``np.ndarray``, uses these indices in the provided array
            | if ``"good"`` uses good components, i.e. cnmf.estimates.idx_components
            | if ``"bad"`` uses bad components, i.e. cnmf.estimates.idx_components_bad
            | if not provided, ``None``, or ``"all"`` uses all components

        swap_dim: bool
            swap the x and y coordinates, use if the contours don't align with the cells in your image

        return_copy: bool
            | if ``True`` returns a copy of the cached value in memory.
            | if ``False`` returns the same object as the cached value in memory, not recommend this could result in strange unexpected behavior.
            | In general you want a copy of the cached value.

        Returns
        -------
        Tuple[List[np.ndarray], List[np.ndarray]]
            | (List[coordinates array], List[centers of masses array])
            | each array of coordinates is 2D, [xs, ys]
            | each center of mass is [x, y]

        Examples
        --------

        This example loads the input movie and contours, and plots them with fastplotlib

        .. code-block:: python

            from mesmerize_core import load_batch
            from matplotlib import pyplot as plt

            # needs fastplotlib and must be run in a notebook
            from fastplotlib import Plot
            from ipywidgets import IntSlider, VBox

            df = load_batch("/path/to/batch_dataframe_file.pickle")

            # assuming the 0th index is a cnmf item
            movie = df.iloc[0].cnmf.get_input_memmap()
            contours, coms = df.iloc[0].cnmf.get_contours()

            # plot a corr img and contours using matplotlib
            plt.imshow(df.iloc[0].caiman.get_corr_image().T)
            for coor in contours:
                plt.scatter(coor[:, 0], coor[:, 1])
            plt.show()

            # the following requires fastplotlib and must be run in a new notebook cell
            slider = IntSlider(value=0, min=0, max=movie.shape[0] - 1, step=1)
            plot = Plot()

            image_graphic = plot.image(movie[0].T, cmap="gnuplot2")
            # note the movie frame is transposed, this is sometimes requires to get the contours to align

            for coor in contours:
                # line data has to be 3D
                zs = np.ones(coor.shape[0])  # this will place it above the image graphic
                c3d = [coor[:, 0], coor[:, 1], zs]
                coors_3d = np.dstack(c3d)[0]

                # make all the lines red, [R, G, B, A] array
                colors = np.vstack([[1., 0., 0., 0.7]] * coors_3d.shape[0])
                plot.line(data=coors_3d, colors=colors)

            previous_slider_value = 0
            def update_frame():  # runs on each rendering cycle
                if slider.value == previous_slider_value:
                    return
                image_graphic.update_data(data=movie[slider.value].T)

            plot.add_animations([update_frame])

            VBox([plot.show(), slider])
        """
        cnmf_obj = self.get_output()
        contours = self._get_spatial_contours(cnmf_obj, component_indices, swap_dim)

        coordinates = list()
        coms = list()

        for contour in contours:
            coors = contour["coordinates"]
            coors = coors[~np.isnan(coors).any(axis=1)]
            coordinates.append(coors)

            com = coors.mean(axis=0)
            coms.append(com)

        return coordinates, coms

    @validate("cnmf")
    @_component_indices_parser
    @cnmf_cache.use_cache
    def get_temporal(
        self, component_indices: Union[np.ndarray, str] = None, add_background: bool = False, return_copy=True
    ) -> np.ndarray:
        """
        Get the temporal components for this CNMF item, basically ``CNMF.estimates.C``

        Parameters
        ----------
        component_indices: optional, Union[np.ndarray, str]
            | indices of the components to include
            | if ``np.ndarray``, uses these indices in the provided array
            | if ``"good"`` uses good components, i.e. cnmf.estimates.idx_components
            | if ``"bad"`` uses bad components, i.e. cnmf.estimates.idx_components_bad
            | if not provided, ``None``, or ``"all"`` uses all components

        add_background: bool
            if ``True``, add the temporal background, ``cnmf.estimates.C + cnmf.estimates.f``

        return_copy: bool
            | if ``True`` returns a copy of the cached value in memory.
            | if ``False`` returns the same object as the cached value in memory, not recommend this could result in strange unexpected behavior.
            | In general you want a copy of the cached value.

        Returns
        -------
        np.ndarray
            shape is [n_components, n_frames]

        Examples
        --------

        Plot the temporal components as a heatmap

        .. code-block:: python

            from mesmerize_core import load_batch
            from seaborn import heatmap

            df = load_batch("/path/to/batch_dataframe_file.pickle")

            # assumes 0th index is a cnmf batch item
            temporal = df.iloc[0].cnmf.get_temporal()

            heatmap(temporal)
        """
        cnmf_obj = self.get_output()

        C = cnmf_obj.estimates.C[component_indices]
        f = cnmf_obj.estimates.f

        if add_background:
            return C + f
        else:
            return C

    @validate("cnmf")
    @_component_indices_parser
    def get_rcm(
            self,
            component_indices: Union[np.ndarray, str] = None,
            frame_indices: Union[Tuple[int, int], int] = None,
            temporal_components: np.ndarray = None
    ) -> np.ndarray:
        """
        Return the reconstructed movie with no background, (A * C)

        Parameters
        ----------
        component_indices: optional, Union[np.ndarray, str]
            | indices of the components to include
            | if ``np.ndarray``, uses these indices in the provided array
            | if ``"good"`` uses good components, i.e. cnmf.estimates.idx_components
            | if ``"bad"`` uses bad components, i.e. cnmf.estimates.idx_components_bad
            | if not provided, ``None``, or ``"all"`` uses all components

        frame_indices: optional, Union[Tuple[int, int], int]
            (start_frame, stop_frame), return frames in this range including
            the ``start_frame`` upto and not including the ``stop_frame``

            | if single int, return only for single frame indicated
            | if ``None`` or not provided returns all frames, **not recommended**

        temporal_components: optional, np.ndarray
            temporal components to use as ``C`` for computing reconstructed movie.

            | uses ``cnmf.estimates.C`` if not provided
            | useful if you want to create the reconstructed movie using dF/Fo, z-scored data, etc.

        Returns
        -------
        np.ndarray
            shape is [n_frames, x_pixels, y_pixels]

        Examples
        --------

        This example uses fastplotlib to display the reconstructed movie from a CNMF item that has already been run.

        | **fastplotlib code must be run in a notebook**

        | See the demo notebooks for more detailed examples.

        .. code-block:: python

            from mesmerize_core import *
            from fastplotlib import Plot
            from ipywidgets import VBox, IntSlider

            # load existing batch
            df = load_batch("/path/to/batch.pickle")

            # get the first reconstructed frame using only "good" components
            # assumes the last index, `-1`, is a cnmf item
            frame0 = df.iloc[-1].cnmf.get_rcm(component_indices="good", frame_indices=0)[0]

            plot = Plot()

            # add an image graphic to the plot
            # we set some contrast limits with `vmin` and `vmax`, adjust these if the video doesn't look right
            graphic = plot.image(frame0, cmap="gnuplot2", vmin=0, vmax=100)

            # we need the number of frames in this movie, we can just get the length of the temporal components
            n_frames = df.iloc[-1].cnmf.get_temporal().shape[1]

            # make a frame slider
            frame_slider = IntSlider(value=0, min=0, max=n_frames - 1, step=1)

            # update the image graphic when the slider moves
            previous_index = 0
            def update_frame():
                if previous_index == frame_slider.value:
                    return

                new_frame = df.iloc[-1].cnmf.get_rcm(component_indices="good", frame_indices=frame_slider.value)[0]
                graphic.update_data(new_frame)

                previous_index = frame_slider.value

            plot.add_animations([update_frame])

            VBox([plot.show(), frame_slider])

        """
        cnmf_obj = self.get_output()

        if temporal_components is None:
            temporal_components = cnmf_obj.estimates.C

        else:  # number of spatial components must equal number of temporal components
            if cnmf_obj.estimates.A.shape[1] != temporal_components.shape[0]:
                raise ValueError(
                    f"Number of temporal components provided: `{temporal_components.shape[0]}` "
                    f"does not equal number of spatial components provided: `{cnmf_obj.estimates.A.shape[1]}`"
                )

        if frame_indices is None:
            frame_indices = (0, temporal_components.shape[1])

        if isinstance(frame_indices, int):
            frame_indices = (frame_indices, frame_indices + 1)

        dn = cnmf_obj.estimates.A[:, component_indices].dot(
            temporal_components[component_indices, frame_indices[0]: frame_indices[1]]
        )

        return dn.reshape(cnmf_obj.dims + (-1,), order="F").transpose([2, 0, 1])

    @validate("cnmf")
    def get_rcb(
            self,
            frame_indices: Union[Tuple[int, int], int] = None,
    ) -> np.ndarray:
        """
        Return the reconstructed background, ``(b * f)``

        Parameters
        ----------
        frame_indices: optional, Union[Tuple[int, int], int]
            (start_frame, stop_frame), return frames in this range including
            the ``start_frame`` upto and not including the ``stop_frame``

            | if single int, return only for single frame indicated
            | if ``None`` or not provided returns all frames, **not recommended**

        Returns
        -------
        np.ndarray
            shape is [n_frames, x_pixels, y_pixels]
        """
        cnmf_obj = self.get_output()

        if frame_indices is None:
            frame_indices = (0, cnmf_obj.estimates.C.shape[1])

        if isinstance(frame_indices, int):
            frame_indices = (frame_indices, frame_indices + 1)

        dn = cnmf_obj.estimates.b.dot(
            cnmf_obj.estimates.f[:, frame_indices[0]: frame_indices[1]]
        )
        return dn.reshape(cnmf_obj.dims + (-1,), order="F").transpose([2, 0, 1])

    @validate("cnmf")
    def get_residuals(
            self,
            frame_indices: Union[Tuple[int, int], int] = None,
    ) -> np.ndarray:
        """
        Return residuals, ``raw movie - (A * C) - (b * f)``

        Parameters
        ----------
        frame_indices: optional, Union[Tuple[int, int], int]
            (start_frame, stop_frame), return frames in this range including
            the ``start_frame`` upto and not including the ``stop_frame``
            | if single int, return only for single frame indicated
            | if ``None`` or not provided returns all frames, **not recommended**

        Returns
        -------
        np.ndarray
            shape is [n_frames, x_pixels, y_pixels]

        Examples
        --------

        This example uses fastplotlib to display the residuals movie from a CNMF item that has already been run.

        | **fastplotlib code must be run in a notebook**

        | See the demo notebooks for more detailed examples.

        .. code-block:: python

            from mesmerize_core import *
            from fastplotlib import Plot
            from ipywidgets import VBox, IntSlider

            # load existing batch
            df = load_batch("/path/to/batch.pickle")

            # get the residuals for the first frame
            # assumes the last index, `-1`, is a cnmf item
            frame0 = df.iloc[-1].cnmf.get_residuals(frame_indices=0)[0]

            plot = Plot()

            # add an image graphic to the plot
            graphic = plot.image(frame0, cmap="gnuplot2")

            # we need the number of frames in this movie, we can just get the length of the temporal components
            n_frames = df.iloc[-1].cnmf.get_temporal().shape[1]

            # make a frame slider
            frame_slider = IntSlider(value=0, min=0, max=n_frames - 1, step=1)

            # update the image graphic when the slider moves
            previous_index = 0
            def update_frame():
                if previous_index == frame_slider.value:
                    return

                graphic.update_data(df.iloc[-1].cnmf.get_residuals(frame_indices=frame_slider.value)[0])
                previous_index = frame_slider.value

            plot.add_animations([update_frame])

            VBox([plot.show(), frame_slider])
        """

        cnmf_obj = self.get_output()

        if frame_indices is None:
            frame_indices = (0, cnmf_obj.estimates.C.shape[1])

        if isinstance(frame_indices, int):
            frame_indices = (frame_indices, frame_indices + 1)

        raw_movie = self.get_input_memmap()

        reconstructed_movie = self.get_rcm(component_indices="all", frame_indices=frame_indices)

        background = self.get_rcb(frame_indices)

        residuals = raw_movie[np.arange(*frame_indices)] - reconstructed_movie - background

        return residuals.reshape(cnmf_obj.dims + (-1,), order="F").transpose([2, 0, 1])

    @validate("cnmf")
    @_check_permissions
    @cnmf_cache.invalidate()
    def run_detrend_dfof(
            self,
            quantileMin: float = 8,
            frames_window: int = 500,
            flag_auto: bool = True,
            use_fast: bool = False,
            use_residuals: bool = True,
            detrend_only: bool = False
    ) -> None:
        """
        | Uses caiman's detrend_df_f.
        | call ``cnmf.get_detrend_dfof()`` to get the values.
        | Sets ``CNMF.estimates.F_dff``

        Warnings
        --------
        Overwrites the existing cnmf hdf5 output file for this batch item

        Parameters
        ----------
        quantileMin: float
            quantile used to estimate the baseline (values in [0,100])
            used only if 'flag_auto' is False, i.e. ignored by default

        frames_window: int
            number of frames for computing running quantile

        flag_auto: bool
            flag for determining quantile automatically

        use_fast: bool
            flag for using approximate fast percentile filtering

        detrend_only: bool
            flag for only subtracting baseline and not normalizing by it.
            Used in 1p data processing where baseline fluorescence cannot be
            determined.

        Returns
        -------
        None

        Notes
        ------
        invalidates the cache for this batch item.

        """

        cnmf_obj: CNMF = self.get_output()
        cnmf_obj.estimates.detrend_df_f(
            quantileMin=quantileMin,
            frames_window=frames_window,
            flag_auto=flag_auto,
            use_fast=use_fast,
            use_residuals=use_residuals,
            detrend_only=detrend_only
        )

        # remove current hdf5 file
        cnmf_obj_path = self.get_output_path()
        cnmf_obj_path.unlink()

        # save new hdf5 file with new F_dff vals
        cnmf_obj.save(str(cnmf_obj_path))

    @validate("cnmf")
    @_component_indices_parser
    @cnmf_cache.use_cache
    def get_detrend_dfof(
            self,
            component_indices: Union[np.ndarray, str] = None,
            return_copy: bool = True
    ):
        """
        Get the detrended dF/F0 curves after calling ``run_detrend_dfof``.
        Basically ``CNMF.estimates.F_dff``.

        Parameters
        ----------
        component_indices: optional, Union[np.ndarray, str]
            | indices of the components to include
            | if ``np.ndarray``, uses these indices in the provided array
            | if ``"good"`` uses good components, i.e. cnmf.estimates.idx_components
            | if ``"bad"`` uses bad components, i.e. cnmf.estimates.idx_components_bad
            | if not provided, ``None``, or ``"all"`` uses all components

        return_copy: bool
            | if ``True`` returns a copy of the cached value in memory.
            | if ``False`` returns the same object as the cached value in memory, not recommend this could result in strange unexpected behavior.
            | In general you want a copy of the cached value.

        Returns
        -------
        np.ndarray
            shape is [n_components, n_frames]

        """
        cnmf_obj = self.get_output()
        if cnmf_obj.estimates.F_dff is None:
            raise AttributeError("You must run ``cnmf.run_detrend_dfof()`` first")

        return cnmf_obj.estimates.F_dff[component_indices]

    @validate("cnmf")
    @_check_permissions
    @cnmf_cache.invalidate()
    def run_eval(self, params: dict) -> None:
        """
        Run component evaluation. This basically changes the indices for good and bad components.

        Warnings
        --------
        Overwrites the existing cnmf hdf5 output file for this batch item

        Parameters
        ----------
        params: dict
            dict of parameters for component evaluation

            ==============  =================
            parameter       details
            ==============  =================
            SNR_lowest      ``float``, minimum accepted SNR value
            cnn_lowest      ``float``, minimum accepted value for CNN classifier
            gSig_range      ``List[int, int]`` or ``None``, range for gSig scale for CNN classifier
            min_SNR         ``float``, transient SNR threshold
            min_cnn_thr     ``float``, threshold for CNN classifier
            rval_lowest     ``float``, minimum accepted space correlation
            rval_thr        ``float``, space correlation threshold
            use_cnn         ``bool``, use CNN based classifier
            use_ecc         ``bool``, flag for eccentricity based filtering
            max_ecc         ``float``, max eccentricity
            ==============  =================

        Returns
        -------
        None

        Notes
        ------
        invalidates the cache for this batch item.

        """

        cnmf_obj = self.get_output()

        valid = list(cnmf_obj.params.quality.keys())
        for k in params.keys():
            if k not in valid:
                raise KeyError(
                    f"passed params dict key `{k}` is not a valid parameter for quality evaluation\n"
                    f"valid param keys are: {valid}"
                )

        cnmf_obj.params.quality.update(params)
        cnmf_obj.estimates.filter_components(
            imgs=self.get_input_memmap(),
            params=cnmf_obj.params
        )

        cnmf_obj_path = self.get_output_path()
        cnmf_obj_path.unlink()

        cnmf_obj.save(str(cnmf_obj_path))
        self._series["params"]["eval"] = deepcopy(params)

    @validate("cnmf")
    def get_good_components(self) -> np.ndarray:
        """
        get the good component indices, ``CNMF.estimates.idx_components``

        Returns
        -------
        np.ndarray
            array of ints, indices of good components

        """

        cnmf_obj = self.get_output()
        return cnmf_obj.estimates.idx_components

    @validate("cnmf")
    def get_bad_components(self) -> np.ndarray:
        """
        get the bad component indices, ``CNMF.estimates.idx_components_bad``

        Returns
        -------
        np.ndarray
            array of ints, indices of bad components

        """
        cnmf_obj = self.get_output()
        return cnmf_obj.estimates.idx_components_bad
