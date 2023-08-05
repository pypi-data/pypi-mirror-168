# Copyright (c) 2015, Ecole Polytechnique Federale de Lausanne, Blue Brain Project
# All rights reserved.
#
# This file is part of NeuroM <https://github.com/BlueBrain/NeuroM>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     1. Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#     2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#     3. Neither the name of the copyright holder nor the names of
#        its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 501ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""visualize morphologies"""

import matplotlib.pyplot as plt
import matplotlib.offsetbox as offsetbox
from matplotlib.collections import LineCollection, PatchCollection
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle
from mpl_toolkits.mplot3d.art3d import Line3DCollection

import numpy as np
from patchview.neurom import NeuriteType, geom
from patchview.neurom._compat import zip
from patchview.neurom.core import iter_neurites, iter_segments, iter_sections
from patchview.neurom.core._soma import SomaCylinders
from patchview.neurom.core.dataformat import COLS
from patchview.neurom.core.types import tree_type_checker
from patchview.neurom.morphmath import segment_radius
from patchview.neurom.view.dendrogram import (
    Dendrogram,
    layout_dendrogram,
    get_size,
    move_positions,
)

from . import common

_LINEWIDTH = 1.2
_ALPHA = 0.8
_DIAMETER_SCALE = 1.0
TREE_COLOR = {
    NeuriteType.basal_dendrite: "blue",
    NeuriteType.apical_dendrite: "purple",
    NeuriteType.axon: "red",
    NeuriteType.soma: "black",
    NeuriteType.undefined: "green",
}


class AnchoredHScaleBar(offsetbox.AnchoredOffsetbox):
    """size: length of bar in data units
    extent : height of bar ends in axes units"""

    def __init__(
        self,
        size=1,
        extent=0.03,
        label="",
        loc=2,
        ax=None,
        pad=0.4,
        borderpad=0.5,
        ppad=0,
        sep=2,
        prop=None,
        frameon=True,
        linekw={},
        **kwargs
    ):
        if not ax:
            ax = plt.gca()
        trans = ax.get_xaxis_transform()
        size_bar = offsetbox.AuxTransformBox(trans)
        line = Line2D([0, size], [0, 0], **linekw)
        vline1 = Line2D([0, 0], [-extent / 2.0, extent / 2.0], **linekw)
        vline2 = Line2D([size, size], [-extent / 2.0, extent / 2.0], **linekw)
        size_bar.add_artist(line)
        size_bar.add_artist(vline1)
        size_bar.add_artist(vline2)
        txt = offsetbox.TextArea(label)
        self.vpac = offsetbox.VPacker(
            children=[size_bar, txt], align="center", pad=ppad, sep=sep
        )
        offsetbox.AnchoredOffsetbox.__init__(
            self,
            loc,
            pad=pad,
            borderpad=borderpad,
            child=self.vpac,
            prop=prop,
            frameon=frameon,
            **kwargs
        )


def _plane2col(plane):
    """take a string like 'xy', and return the indices from COLS.*"""
    planes = ("xy", "yx", "xz", "zx", "yz", "zy")
    assert plane in planes, "No such plane found! Please select one of: " + str(planes)
    return (
        getattr(COLS, plane[0].capitalize()),
        getattr(COLS, plane[1].capitalize()),
    )


def _get_linewidth(tree, linewidth, diameter_scale):
    """calculate the desired linewidth based on tree contents

    If diameter_scale exists, it is used to scale the diameter of each of the segments
    in the tree
    If diameter_scale is None, the linewidth is used.
    """
    if diameter_scale is not None and tree:
        linewidth = [
            2 * segment_radius(s) * diameter_scale for s in iter_segments(tree)
        ]
    return linewidth


def _get_color(treecolor, tree_type):
    """if treecolor set, it's returned, otherwise tree_type is used to return set colors"""
    if treecolor is not None:
        return treecolor
    return TREE_COLOR.get(tree_type, "green")


def plot_tree(
    ax,
    tree,
    plane="xy",
    diameter_scale=_DIAMETER_SCALE,
    linewidth=_LINEWIDTH,
    color=None,
    alpha=_ALPHA,
    realistic_diameters=False,
):
    from itertools import chain

    plane0, plane1 = _plane2col(plane)
    section_segment_list = [
        (section, segment)
        for section in iter_sections(tree)
        for segment in iter_segments(section)
    ]
    colors = [_get_color(color, section.type) for section, _ in section_segment_list]
    if realistic_diameters:
        segs = [(s[0][COLS.XYZ], s[1][COLS.XYZ]) for _, s in section_segment_list]

        coords = [
            list(chain.from_iterable((p1[0], p2[0], None) for p1, p2 in segs)),
            list(chain.from_iterable((p1[1], p2[1], None) for p1, p2 in segs)),
        ]
        points = np.array(coords).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        lwidths = [
            2 * segment_radius(seg) * diameter_scale for _, seg in section_segment_list
        ]
        lwidths.append(lwidths[-1])
        collection = LineCollection(segments, linewidths=lwidths, color=colors[0])

    else:
        segs = [
            ((seg[0][plane0], seg[0][plane1]), (seg[1][plane0], seg[1][plane1]))
            for _, seg in section_segment_list
        ]

        colors = [
            _get_color(color, section.type) for section, _ in section_segment_list
        ]

        linewidth = _get_linewidth(
            tree, diameter_scale=diameter_scale, linewidth=linewidth
        )

        collection = LineCollection(
            segs, colors=colors, linewidth=linewidth, alpha=alpha
        )
    ax.add_collection(collection)


def plot_tree2(
    ax,
    tree,
    plane="xy",
    diameter_scale=_DIAMETER_SCALE,
    linewidth=_LINEWIDTH,
    color=None,
    alpha=_ALPHA,
    realistic_diameters=False,
):
    """Plots a 2d figure of the tree's segments

    Args:
        ax(matplotlib axes): on what to plot
        tree(neurom.core.Tree or neurom.core.Neurite): plotted tree
        plane(str): Any pair of 'xyz'
        diameter_scale(float): Scale factor multiplied with segment diameters before plotting
        linewidth(float): all segments are plotted with this width, but only if diameter_scale=None
        color(str or None): Color of plotted values, None corresponds to default choice
        alpha(float): Transparency of plotted values

    Note:
        If the tree contains one single point the plot will be empty
        since no segments can be constructed.
    """
    print("plot trees")
    plane0, plane1 = _plane2col(plane)
    section_segment_list = [
        (section, segment)
        for section in iter_sections(tree)
        for segment in iter_segments(section)
    ]
    colors = [_get_color(color, section.type) for section, _ in section_segment_list]
    if realistic_diameters:

        def _get_rectangle(x, y, linewidth):
            """Draw  a rectangle to represent a secgment."""
            x, y = np.array(x), np.array(y)
            diff = y - x
            angle = np.arctan2(diff[1], diff[0]) % (2 * np.pi)
            return Rectangle(
                x - linewidth / 2.0 * np.array([-np.sin(angle), np.cos(angle)]),
                np.linalg.norm(diff),
                linewidth,
                np.rad2deg(angle),
            )

        segs = [
            _get_rectangle(
                (seg[0][plane0], seg[0][plane1]),
                (seg[1][plane0], seg[1][plane1]),
                2 * segment_radius(seg) * diameter_scale,
            )
            for _, seg in section_segment_list
        ]

        collection = PatchCollection(
            segs, match_original=False, linewidths=0, alpha=alpha, facecolors=colors
        )
        # collection.set_zorder(zorders)
    else:
        segs = [
            ((seg[0][plane0], seg[0][plane1]), (seg[1][plane0], seg[1][plane1]))
            for _, seg in section_segment_list
        ]

        colors = [
            _get_color(color, section.type) for section, _ in section_segment_list
        ]

        linewidth = _get_linewidth(
            tree, diameter_scale=diameter_scale, linewidth=linewidth
        )

        collection = LineCollection(
            segs, colors=colors, linewidth=linewidth, alpha=alpha
        )
    ax.add_collection(collection)


def plot_soma(
    ax,
    soma,
    plane="xy",
    soma_outline=True,
    linewidth=_LINEWIDTH,
    color=None,
    alpha=_ALPHA,
    label="",
):
    """Generates a 2d figure of the soma.

    Args:
        ax(matplotlib axes): on what to plot
        soma(neurom.core.Soma): plotted soma
        plane(str): Any pair of 'xyz'
        diameter_scale(float): Scale factor multiplied with segment diameters before plotting
        linewidth(float): all segments are plotted with this width, but only if diameter_scale=None
        color(str or None): Color of plotted values, None corresponds to default choice
        alpha(float): Transparency of plotted values
    """
    plane0, plane1 = _plane2col(plane)
    color = _get_color(color, tree_type=NeuriteType.soma)

    if isinstance(soma, SomaCylinders):
        plane0, plane1 = _plane2col(plane)
        # for start, end in zip(soma.points, soma.points[1:]):
        #     common.project_cylinder_onto_2d(ax, (plane0, plane1),
        #                                     start=start[COLS.XYZ], end=end[COLS.XYZ],
        #                                     start_radius=start[COLS.R], end_radius=end[COLS.R],
        #                                     color=color, alpha=alpha)

        # points = common.generate_cylindrical_points(start[COLS.XYZ], end[COLS.XYZ],\
        #                                     start[COLS.R], end[COLS.R], 10)
        from scipy.spatial import ConvexHull

        points = np.vstack(
            [soma.points[:, plane0].ravel(), soma.points[:, plane1].ravel()]
        )
        points = points.T
        hull = ConvexHull(points)
        ax.add_patch(
            Polygon(
                points[hull.vertices], fill=True, color=color, alpha=alpha, zorder=-1
            )
        )

    else:
        if soma_outline:
            ax.add_artist(
                Circle(
                    soma.center[[plane0, plane1]], soma.radius, color=color, alpha=alpha
                )
            )
        else:
            plane0, plane1 = _plane2col(plane)
            points = [(p[plane0], p[plane1]) for p in soma.iter()]

            if points:
                points.append(points[0])  # close the loop
                ax.plot(points, color=color, alpha=alpha, linewidth=linewidth)

    if label != "":
        ax.axes.text(
            soma.center[plane0],
            soma.center[plane1],
            label,
            horizontalalignment="center",
            verticalalignment="center",
            color="r",
            fontsize=11,
        )

    ax.set_xlabel(plane[0])
    ax.set_ylabel(plane[1])

    bounding_box = geom.bounding_box(soma)
    ax.dataLim.update_from_data_xy(
        np.vstack(
            (
                [bounding_box[0][plane0], bounding_box[0][plane1]],
                [bounding_box[1][plane0], bounding_box[1][plane1]],
            )
        ),
        ignore=False,
    )
    return ax


# pylint: disable=too-many-arguments
def plot_neuron(
    ax,
    nrn,
    neurite_type=NeuriteType.all,
    plane="xy",
    soma_outline=True,
    diameter_scale=_DIAMETER_SCALE,
    linewidth=_LINEWIDTH,
    color=None,
    alpha=_ALPHA,
    realistic_diameters=False,
    label="",
):
    """Plots a 2D figure of the neuron, that contains a soma and the neurites

    Args:
        ax(matplotlib axes): on what to plot
        neurite_type(NeuriteType): an optional filter on the neurite type
        nrn(neuron): neuron to be plotted
        soma_outline(bool): should the soma be drawn as an outline
        plane(str): Any pair of 'xyz'
        diameter_scale(float): Scale factor multiplied with segment diameters before plotting
        linewidth(float): all segments are plotted with this width, but only if diameter_scale=None
        color(str or None): Color of plotted values, None corresponds to default choice
        alpha(float): Transparency of plotted values
    """
    plot_soma(
        ax,
        nrn.soma,
        plane=plane,
        soma_outline=soma_outline,
        linewidth=linewidth,
        color=color,
        alpha=alpha,
        label=label,
    )

    for neurite in iter_neurites(nrn, filt=tree_type_checker(neurite_type)):
        plot_tree(
            ax,
            neurite,
            plane=plane,
            diameter_scale=diameter_scale,
            linewidth=linewidth,
            color=color,
            alpha=alpha,
            realistic_diameters=realistic_diameters,
        )
    ob = AnchoredHScaleBar(
        size=50,
        extent=0.01,
        label="50 um",
        loc=4,
        frameon=False,
        pad=0.6,
        sep=4,
        linekw=dict(color="black"),
        ax=ax,
    )
    ax.add_artist(ob)
    ax.set_title(nrn.name)
    ax.set_xlabel(plane[0])
    ax.set_ylabel(plane[1])
    return ax


def _update_3d_datalim(ax, obj):
    """unlike w/ 2d Axes, the dataLim isn't set by collections, so it has to be updated manually"""
    min_bounding_box, max_bounding_box = geom.bounding_box(obj)
    xy_bounds = np.vstack((min_bounding_box[: COLS.Z], max_bounding_box[: COLS.Z]))
    ax.xy_dataLim.update_from_data_xy(xy_bounds, ignore=False)

    z_bounds = np.vstack(
        (
            (min_bounding_box[COLS.Z], min_bounding_box[COLS.Z]),
            (max_bounding_box[COLS.Z], max_bounding_box[COLS.Z]),
        )
    )
    ax.zz_dataLim.update_from_data_xy(z_bounds, ignore=False)


def plot_tree3d(
    ax,
    tree,
    diameter_scale=_DIAMETER_SCALE,
    linewidth=_LINEWIDTH,
    color=None,
    alpha=_ALPHA,
):
    """Generates a figure of the tree in 3d.

    If the tree contains one single point the plot will be empty \
    since no segments can be constructed.

    Args:
        ax(matplotlib axes): on what to plot
        tree(neurom.core.Tree or neurom.core.Neurite): plotted tree
        diameter_scale(float): Scale factor multiplied with segment diameters before plotting
        linewidth(float): all segments are plotted with this width, but only if diameter_scale=None
        color(str or None): Color of plotted values, None corresponds to default choice
        alpha(float): Transparency of plotted values
    """
    section_segment_list = [
        (section, segment)
        for section in iter_sections(tree)
        for segment in iter_segments(section)
    ]
    segs = [(seg[0][COLS.XYZ], seg[1][COLS.XYZ]) for _, seg in section_segment_list]
    colors = [_get_color(color, section.type) for section, _ in section_segment_list]

    linewidth = _get_linewidth(tree, diameter_scale=diameter_scale, linewidth=linewidth)

    collection = Line3DCollection(segs, colors=colors, linewidth=linewidth, alpha=alpha)
    ax.add_collection3d(collection)

    _update_3d_datalim(ax, tree)


def plot_soma3d(ax, soma, color=None, alpha=_ALPHA):
    """Generates a 3d figure of the soma.

    Args:
        ax(matplotlib axes): on what to plot
        soma(neurom.core.Soma): plotted soma
        color(str or None): Color of plotted values, None corresponds to default choice
        alpha(float): Transparency of plotted values
    """
    color = _get_color(color, tree_type=NeuriteType.soma)

    if isinstance(soma, SomaCylinders):
        for start, end in zip(soma.points, soma.points[1:]):
            common.plot_cylinder(
                ax,
                start=start[COLS.XYZ],
                end=end[COLS.XYZ],
                start_radius=start[COLS.R],
                end_radius=end[COLS.R],
                color=color,
                alpha=alpha,
            )
    else:
        common.plot_sphere(
            ax,
            center=soma.center[COLS.XYZ],
            radius=soma.radius,
            color=color,
            alpha=alpha,
        )

    # unlike w/ 2d Axes, the dataLim isn't set by collections, so it has to be updated manually
    _update_3d_datalim(ax, soma)


def plot_neuron3d(
    ax,
    nrn,
    neurite_type=NeuriteType.all,
    diameter_scale=_DIAMETER_SCALE,
    linewidth=_LINEWIDTH,
    color=None,
    alpha=_ALPHA,
):
    """
    Generates a figure of the neuron,
    that contains a soma and a list of trees.

    Args:
        ax(matplotlib axes): on what to plot
        nrn(neuron): neuron to be plotted
        neurite_type(NeuriteType): an optional filter on the neurite type
        diameter_scale(float): Scale factor multiplied with segment diameters before plotting
        linewidth(float): all segments are plotted with this width, but only if diameter_scale=None
        color(str or None): Color of plotted values, None corresponds to default choice
        alpha(float): Transparency of plotted values
    """
    plot_soma3d(ax, nrn.soma, color=color, alpha=alpha)

    for neurite in iter_neurites(nrn, filt=tree_type_checker(neurite_type)):
        plot_tree3d(
            ax,
            neurite,
            diameter_scale=diameter_scale,
            linewidth=linewidth,
            color=color,
            alpha=alpha,
        )

    ax.set_title(nrn.name)


def _get_dendrogram_legend(dendrogram):
    """Generates labels legend for dendrogram.

    Because dendrogram is rendered as patches, we need to manually label it.
    Args:
        dendrogram (Dendrogram): dendrogram

    Returns:
        List of legend handles.
    """

    def neurite_legend(neurite_type):
        return Line2D(
            [0], [0], color=TREE_COLOR[neurite_type], lw=2, label=neurite_type.name
        )

    if dendrogram.neurite_type == NeuriteType.soma:
        handles = {
            d.neurite_type: neurite_legend(d.neurite_type)
            for d in [dendrogram] + dendrogram.children
        }
        return handles.values()
    return [neurite_legend(dendrogram.neurite_type)]


def _as_dendrogram_polygon(coords, color):
    return Polygon(coords, color=color, fill=True)


def _as_dendrogram_line(start, end, color):
    return FancyArrowPatch(
        start, end, arrowstyle="-", color=color, lw=2, shrinkA=0, shrinkB=0
    )


def _get_dendrogram_shapes(dendrogram, positions, show_diameters):
    """Generates drawable patches for dendrogram.

    Args:
        dendrogram (Dendrogram): dendrogram
        positions (dict of Dendrogram: np.array): positions xy coordinates of dendrograms
        show_diameter (bool): whether to draw shapes with diameter or as plain lines

    Returns:
        List of matplotlib.patches.
    """
    color = TREE_COLOR[dendrogram.neurite_type]
    start_point = positions[dendrogram]
    end_point = start_point + [0, dendrogram.height]
    if show_diameters:
        shapes = [_as_dendrogram_polygon(dendrogram.coords + start_point, color)]
    else:
        shapes = [_as_dendrogram_line(start_point, end_point, color)]
    for child in dendrogram.children:
        shapes.append(_as_dendrogram_line(end_point, positions[child], color))
        shapes += _get_dendrogram_shapes(child, positions, show_diameters)
    return shapes


def plot_dendrogram(ax, obj, show_diameters=True):
    """Plots Dendrogram of `obj`.

    Args:
        ax: matplotlib axes
        obj (neurom.Neuron, neurom.Tree): neuron or tree
        show_diameters (bool): whether to show node diameters or not
    """
    dendrogram = Dendrogram(obj)
    positions = layout_dendrogram(dendrogram, np.array([0, 0]))
    w, h = get_size(positions)
    positions = move_positions(positions, np.array([0.5 * w, 0]))
    ax.set_xlim([-0.05 * w, 1.05 * w])
    ax.set_ylim([-0.05 * h, 1.05 * h])
    ax.set_title("Morphology Dendrogram")
    ax.set_xlabel("micrometers (um)")
    ax.set_ylabel("micrometers (um)")
    shapes = _get_dendrogram_shapes(dendrogram, positions, show_diameters)
    ax.add_collection(PatchCollection(shapes, match_original=True))

    ax.set_aspect("auto")
    ax.legend(handles=_get_dendrogram_legend(dendrogram))
