import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ..plotting import _npedges2dfedges, _get_nodes_from_nii

def get_frame_input(inputvar, axind, ri, fi, nrows, frames):
    """
    Gets subplot variable.

    The variable depends on whether the
    input is a string, array or 2d array.
    """
    # First sett if input is a singular string, int or None.
    if isinstance(inputvar, int):
        var_frame = inputvar
    elif isinstance(inputvar, str):
        var_frame = inputvar
    elif inputvar is None:
        var_frame = inputvar
    # Then check if first input of list is also a list (e.g. format ['LR', 'SP'])
    elif len(inputvar) == nrows and isinstance(inputvar[0], str) and len(inputvar[0]) == frames:
        var_frame = inputvar[ri][fi]
    # If a 2x2 figure input is ['LRSP']
    elif len(inputvar) == (nrows * frames):
        var_frame = inputvar[axind]
    else:
        var_frame = inputvar[ri][fi]
    return var_frame


def _process_node_input(nodes, nodes_df, nodecolor, nodecolumnnames, template, templatevoxelsize):
    """
    Takes node input (nodes, nodesdf and nodecolumnnames) and processes them.
    Loads pandas dataframe if nodes is string.
    Gets the nodes from the nifti file if nodes is an img is set.
    Sets defult columns for nodecolumnnames.
    If nodes is an img, then nodes_df passes additional info if wanted.
    """
    # Preset nodeimg to None
    nodeimg=None
    # Load nodes if string is provided
    if isinstance(nodes, pd.DataFrame) or nodes is None:
        pass
    elif isinstance(nodes, str):
        if nodes.endswith('.tsv'):
            nodes = pd.read_csv(nodes, sep='\t', index_col=0)
        elif nodes.endswith('.csv'):
            nodes = pd.read_csv(nodes, index_col=0)
        elif nodes.endswith('.nii') or  nodes.endswith('.nii.gz'):
            nodes, nodeimg = _get_nodes_from_nii(
                nodes, voxsize=templatevoxelsize, template=template, nodes=nodes_df)
        else:
            raise ValueError('nodes as str must be a .csv, .tsv, .nii, or .nii.gz')
    else:
        nodes, nodeimg = _get_nodes_from_nii(
            nodes, voxsize=templatevoxelsize, template=template, nodes=nodes_df)
    # set nodecolumnnames if no explicit input
    if nodecolumnnames == 'auto':
        nodecolumnnames = ['x', 'y', 'z']
    # Check if nodecolor is a string in nodes, if yes, set to nodecolorby to nodecolor
    # Note: this may not be the most effective way to do this.
    nodecolorby = None
    if isinstance(nodecolor, str) and nodes is not None:
        if nodecolor in nodes:
            nodecolorby = str(nodecolor)
    return nodes, nodeimg, nodecolorby, nodecolumnnames


def _process_edge_input(edges, edgeweights, **kwargs):
    """
    Takes the input edges and edgeweight.
    Loads pandas dataframe if edges is string.
    Creates pandas dataframe if edges is numpy array.
    Sets default edgeweight to "weight" if not given.
    """
    edgethreshold = kwargs.get('edgethreshold')
    edgethresholddirection = kwargs.get('edgethresholddirection')
    edges_df = kwargs.get('edges_df')
    if isinstance(edges, str):
        edges = pd.read_csv(edges, sep='\t', index_col=0)
    # Check input, if numpy array, make dataframe
    if isinstance(edges, np.ndarray):
        edges = _npedges2dfedges(edges)
        edgeweights = 'weight'
    # Merge edges_df if it exists.
    if edges_df is not None:
        edges = edges.merge(edges_df, how='left')
    # Set default behaviour of edgeweights
    if isinstance(edges, pd.DataFrame):
        if edgeweights is None or edgeweights is True:
            edgeweights = 'weight'
        if 'weight' not in edges:
            edgeweights = None
        if edgeweights is not None and edgeweights not in edges:
            raise ValueError('Edgeweights is specified and not in edges')
        # If edgeweight and edgethreshold have been set
        if edgeweights is not None and edgethreshold is not None:
            if edgethresholddirection == 'absabove':
                edges = edges[np.abs(edges[edgeweights]) > edgethreshold]
            if edgethresholddirection == 'above' or edgethresholddirection == '>':
                edges = edges[edges[edgeweights] > edgethreshold]
            if edgethresholddirection == 'below' or edgethresholddirection == '<':
                edges = edges[edges[edgeweights] < edgethreshold]

    return edges, edgeweights


def _init_figure(frames, nrows, legendrow):
    widths = [6] * frames
    heights = [6] * nrows
    if legendrow > 0:
        heights += [1] * legendrow
    fig = plt.figure(figsize=(frames * 3, (3 * nrows) + (0.5 * legendrow)))
    gridspec = fig.add_gridspec(ncols=frames,
                                nrows=nrows+legendrow,
                                width_ratios=widths,
                                height_ratios=heights)
    return fig, gridspec

def _check_axinput(ax, expected_ax_len):
    if not isinstance(ax, list) and expected_ax_len > 1:
        raise ValueError(
            'Ax input must be a list when requesting multiple frames')
    if isinstance(ax, list):
        if len(ax) != expected_ax_len:
            raise ValueError('Ax list, must equal number of frames requested')
    if not isinstance(ax, list):
        ax = [ax]
    gridspec = ax[0].get_gridspec()
    return ax, gridspec


def _process_highlightedge_input(edges, highlightedges, **profile):
    # if highlight edges is array, convert to pandas.
    if isinstance(highlightedges, np.ndarray):
        # Convert np input to pd
        highlightedges = _npedges2dfedges(highlightedges)
        ecols = profile['edgecolumnnames']
        # Make sure that the i and j column are the same name
        # Also rename weight to edge_to_highlight
        highlightedges.rename(columns = {'weight': 'edge_to_highlight',
                                         'i': ecols[0],
                                         'j': ecols[1]}, inplace = True)
        # Merge dataframes with edges
        edges = edges.merge(highlightedges, how='left')
        # Make nans 0s
        edges['edge_to_highlight'] = edges['edge_to_highlight'].fillna(0)
        # Rename highlightedges to new column
        highlightedges = 'edge_to_highlight'
    return edges, highlightedges