import numpy as np
import networkx as nx
from typing import Optional
import matplotlib.pyplot as plt
from .plotting import _plot_template, \
    _plot_edges, _plot_nodes, _plot_spheres,\
    _scale_nodes, _add_axis_arrows, _plot_parcels,\
    _select_single_hemisphere_nodes, _add_subplot_title, get_frame_input,\
    _setup_legend, _process_edge_input, _process_node_input,\
    _add_nodesize_legend, _add_nodecolor_legend, _init_figure, _check_axinput, \
    _plot_gif, _process_highlightedge_input, _plot_springlayout, _add_title
from .utils import _highlight_nodes, _get_colorby_colors, _set_axes_equal, _get_view, \
    _load_profile, _nrows_in_fig, _highlight_edges, _from_networkx_input, _get_presetviews

def plot(nodes=None, fig: Optional[plt.Figure] = None, ax=None, view: str = 'L', edgeweights=None, frames=None, edges=None, template=None, network=None,
         edgecolor='k', nodesize=1, nodecolor='salmon', nodetype='circles', hemisphere='both', highlightnodes=None, highlightedges=None, **kwargs):
    """
    Plot a network on a brain

    Arguments:
    ------------------
    fig: matplotlib figure
    view : str, list, or tuple. If string: alternatives are 'A' (anterior), 'P' (posteiror), 'L' (left), 'R' (right), 'I' (inferior), 'S' (superior), 's' (spring layout), '360' (full rotation)
        or any combination of these (e.g 'LR', 'AP').
        The string can contain multiple combinations (e.g. LSR)
        if list: multiple strings (as above) which will create new rows of subplots.
        if tuple: (azim, elev) where azim rotates along xy, and elev rotates along xz.
        If LR or AP view combinations only, you can specify i.e. 'AP-' to rotate in the opposite direction
    nodes : dataframe, string, dict, or nii
        The dataframe must include x, y, z columns that correspond to coordinates of nodes (see nodecolumnnames to change this).
        Can include additional infomation for node size and color.
        If string, can load a csv file, tsv file (tab seperator), assumes index column is the 0th column.
        If nodes points to a nifti image, a string to filename or nibabel object that contains nodes as int.
        Or additionally can point to an atlas on templateflow.
    edges : dataframe, numpy array, or string
        If dataframe, must include i, j columns (and weight, for weighted).
        i and j specify indices in nodes.
        See edgecolumnames if you want to change the default column names.
        if numpy array, square adjacency array.
        If string, can load a tsv file (tab seperator), assumes index column is the 0th column.
    network : nx.Graph
        NetworkX input. Note the nodecolumnnames for coordinates (by default x, y, z) must be node attributes for nodes.
        If providing network input, than you cannot specify nodes or edges input.
        These should be included within the networkx object as nodes and edges attributes.
    template : str, dict or nibabel nifti
        Path to nifti image, or templateflow template name (see templateflow.org) in order to automatically download T1 template.
        If dict, specify keyword - value pairs for templateflow.api.get().
        If specifying templateflow string, and there are multiple cohorts (e.g. MNIInfant) add "_cohort-X" to the string.
        For example, for MNIInfant, cohort 3, write: "MNIInfant_cohort-3"
    frames : int
        If specifying 2 views (e.g. LR or AP) and would like to rotates a between them.
        This value will indicate the number of rotations to get from L to R.
        For any other view specification, (e.g. specifying string such as 'LSR')
        then this value is not needed.
    highlightnodes : int, list, dict, str
        List or int point out which nodes you want to be highlighted.
        If dict, should be a single column-value pair.
        Example: highlight all nodes of that, in the node dataframe, have a community
        value of 1, the input will be {'community': 1}.
        If string, should point to a column in the nodes dataframe and all non-zero values will be plotted.
    highlightedges : array, dict, str
        List or int point out which nodes you want to be highlighted.
        If dict, should be a single column-value pair.
        Example: highlight all nodes of that, in the edge dataframe, have a community
        value of 1, the input will be {'community': 1}.
        If string, should point to a column in the nodes dataframe and all non-zero values will be plotted.
    nodecolor : str or RGB value.
        If string, named matplotlib color or name of column in dataframe
    nodesize : str, int, float
        If string, can plot a column in nodes
    subtitle : list
        Default auto, will describe the view settings.
        Otherwise string or list of for subplot titles

    For more key word arguments, see `netplotbrain.kwargs`

    Returns
    --------
    fig, ax - matplotlib figure and ax handles.
        Legend handles should not be included but there should be an empty row in the figure size for each legend needed.

    .. include:: ../docs/kwargs.rst

    """
    # Raise Errors for deprecated inputs from version 0.1.x
    if 'nodeimg' in kwargs:
        raise ValueError('DEPRECATED INPUT (from 0.2.0): Use nodes instead of nodeimg. If additional nodeinfo exists as a dataframe, use nodes_df.')
    if 'nodecolorby' in kwargs:
        raise ValueError('DEPRECATED INPUT (from 0.2.0): Use nodecolor instead of nodecolorby.')
    # Load default settings, then update with kwargs
    profile = _load_profile(**kwargs)
    if network is not None:
        if nodes is not None or edges is not None:
            raise ValueError('Network is specified with edges or nodes.')
        elif isinstance(network, nx.Graph):
            nodes, edges, = _from_networkx_input(network, **profile)
        else:
            raise ValueError('Unnown netowrk input')

    # Check and load the input of nodes and edges
    nodes, nodeimg, nodecolorby, profile['nodecolumnnames'] = _process_node_input(
        nodes, profile['nodes_df'], nodecolor, profile['nodecolumnnames'], template, profile['templatevoxelsize'])
    edges, edgeweights = _process_edge_input(edges, edgeweights, **profile)
    # Set up legend row
    # TODO compact code into subfunction
    legends = None
    legendrows = 0
    if isinstance(profile['showlegend'], list):
        legends = profile['showlegend']
        legendrows = len(legends)
    elif profile['showlegend'] is True:
        # Only plot size legend is sphere/circle and string or list input
        # TODO setup_legend is a little clunky and could be fixed
        if nodetype != 'parcel' and not isinstance(nodesize, (float, int)):
            nodesizelegend = profile['nodesizelegend']
            legends = _setup_legend(
                nodesize, nodesizelegend, 'nodesize', legends)
        # Only plot color legend if colorby
        if nodecolorby is not None:
            nodecolorlegend = profile['nodecolorlegend']
            legends = _setup_legend(
                nodecolorby, nodecolorlegend, 'nodecolor', legends)
        if legends is not None:
            legendrows = len(legends)

    # Figure setup
    # Get preset views 
    if isinstance(view, str):
        if view.startswith('preset'):
            view, hemisphere = _get_presetviews(view)
    # Get number of non-legend rowsnon
    nrows, view, frames = _nrows_in_fig(view, frames)
    #Set subtitles to None if title is set.
    if profile['subtitles'] == 'auto' and profile['title'] is not None:
        profile['subtitles'] = None
    
    # Init figure, if not given as input
    if ax is None:
        fig, gridspec = _init_figure(frames, nrows, legendrows)
    else:
        expected_ax_len = (nrows * frames)
        ax, gridspec = _check_axinput(ax, expected_ax_len)
        
    # Set nodecolor to colorby argument
    if nodecolorby is not None:
        nodecolor = _get_colorby_colors(nodes, nodecolorby, **profile)
    if isinstance(edgecolor, str) and edges is not None:
        if edgecolor in edges:
            edgecolor = _get_colorby_colors(edges, edgecolor, 'edge', **profile)
    if highlightnodes is not None and highlightedges is not None:
        raise ValueError('Cannot highlight based on edges and nodes at the same time.')
    if highlightnodes is not None:
        nodecolor, highlightnodes, profile['nodealpha'] = _highlight_nodes(
            nodes, nodecolor, highlightnodes, **profile)

    if highlightedges is not None:
        edges, highlightedges = _process_highlightedge_input(edges, highlightedges, **profile)
        edgecolor, highlightedges, profile['edgealpha'] = _highlight_edges(edges, edgecolor, highlightedges, **profile)
        # Get the nodes that are touched by highlighted edges
        nodes_to_highlight = edges[highlightedges == 1]
        nodes_to_highlight = np.unique(nodes_to_highlight[profile['edgecolumnnames']].values)
        nodecolor, highlightnodes, profile['nodealpha'] = _highlight_nodes(
            nodes, nodecolor, nodes_to_highlight, **profile)

    # Rename ax as ax_in and prespecfiy ax_out before forloop
    ax_in = ax
    ax_out = []
    # TODO remove double forloop and make single forloop by running over nrows and frames
    for ri in range(nrows):
        # Get the azim, elev and arrowaxis for each row
        azim, elev, arrowaxis_row, viewtype = _get_view(
            view[ri], frames, arrowaxis=profile['arrowaxis'])
        for fi in range(frames):
            axind = (ri * nrows) + fi
            # get_frame_input allows input arguments to be string or list of different arguments for different plots
            hemi_frame = get_frame_input(hemisphere, axind, ri, fi, nrows, frames)
            subtitle_frame = get_frame_input(profile['subtitles'], axind, ri, fi, nrows, frames)
            templatestyle_frame = get_frame_input(profile['templatestyle'], axind, ri, fi, nrows, frames)
            # Set up subplot
            if ax_in is None:
                ax = fig.add_subplot(gridspec[ri, fi], projection='3d')
            elif isinstance(ax_in, list):
                # here ax can only be a 1d list, not 2d list.
                ax = ax_in[axind]
            else:
                ax = ax_in
            affine = None
            if template is not None and viewtype[fi]=='b':
                affine = _plot_template(ax, templatestyle_frame, template,
                                        hemisphere=hemi_frame,
                                        azim=azim[fi], elev=elev[fi],
                                        **profile)
            
            # Template voxels will have origin at 0,0,0
            # It is easier to scale the nodes from the image affine
            # Then to rescale the ax.voxels function
            # So if affine is not None, nodes get scaled in relation to origin and voxelsize,
            # If node coords are derived from nodeimg, this has already been taken care of.
            if nodes is not None and nodeimg is None and axind == 0:
                nodes = _scale_nodes(nodes, profile['nodecolumnnames'], affine)
            # nodes and subplot may change for each frame/subplot
            # e.g. if hemisphere is specified
            nodes_frame = None
            if nodes is not None and viewtype[fi]=='b':
                nodes_frame = nodes.copy()
                nodes_frame = _select_single_hemisphere_nodes(
                    nodes_frame, profile['nodecolumnnames'][0], affine, hemi_frame)

                if nodetype == 'spheres':
                    _plot_spheres(ax, nodes_frame, nodecolor=nodecolor,
                                  nodesize=nodesize, **profile)
                elif nodetype == 'circles':
                    _plot_nodes(ax, nodes_frame, nodecolor=nodecolor,
                                nodesize=nodesize, **profile)
                elif nodetype == 'parcels':
                    _plot_parcels(ax, nodeimg, cmap=nodecolor,
                                  hemisphere=hemi_frame, **profile)
            if edges is not None and viewtype[fi]=='b':
                edges_frame = edges.copy()
                _plot_edges(ax, nodes_frame, edges_frame, edgewidth=edgeweights,
                            edgecolor=edgecolor, highlightnodes=highlightnodes, **profile)
            if arrowaxis_row is not None and viewtype[fi]=='b':
                _add_axis_arrows(ax, dims=arrowaxis_row,
                                 origin=profile['arroworigin'],
                                 azim=azim[fi], elev=elev[fi], **profile)
            if viewtype[fi] == 's' and nodes is not None and edges is not None:
                _plot_springlayout(ax, nodes=nodes, edges=edges, nodecolor=nodecolor, nodesize=nodesize,
                                   edgecolor=edgecolor, edgeweights=edgeweights, highlightnodes=highlightnodes, **profile)
            ax.view_init(azim=azim[fi], elev=elev[fi])
            
            _add_subplot_title(ax, azim[fi], elev[fi], subtitle_frame, hemi_frame, viewtype[fi], **profile)
            
            # Fix the aspect ratio
            ax.set_box_aspect([1, 1, 1])
            _set_axes_equal(ax)
            ax.axis('off')
            # Append ax to ax_out to store it.
            ax_out.append(ax)
            
    # Add legends to plot
    if legends is not None and profile['gif'] is False:
        for li, legend in enumerate(legends):
            # setup legend subplot. Goes in centre or centre2 subplots
            spind = gridspec.ncols
            if np.remainder(spind, 2) == 0:
                legend_subplotp_colind = [int((spind / 2) - 1), int(spind / 2)]
            else:
                legend_subplotp_colind = int(np.round(spind / 2) - 1)
            ax = fig.add_subplot(gridspec[nrows + li, legend_subplotp_colind])
            if legend == 'nodesize':
                ax = _add_nodesize_legend(ax, nodes, nodesize, **profile)
            if legend == 'nodecolor':
                ax = _add_nodecolor_legend(
                    ax, nodes, nodecolorby, nodecolor, **profile)
            ax.axis('off')
            #ax = _add_size_legend(ax, nodes, nodesize, nodescale)
            ax_out.append(ax)

    # Title on top of the figure
    if profile['title'] is not None: 
        _add_title(fig, **profile)
            
    fig.tight_layout()

    # If gif is requested, create the gif.
    if profile['gif'] is True:
        _plot_gif(fig, ax_out, profile['gifduration'], profile['savename'], profile['gifloop'])
    # Save figure if set
    elif profile['savename'] is not None:
        if profile['savename'].endswith('.png'):
            fig.savefig(profile['savename'], dpi=profile['fig_dpi'])
        elif profile['savename'].endswith('.svg'):
            fig.savefig(profile['savename'])
        else:
            fig.savefig(profile['savename'] + '.png', dpi=profile['fig_dpi'])
            fig.savefig(profile['savename'] + '.svg')

    return (fig, ax_out)
