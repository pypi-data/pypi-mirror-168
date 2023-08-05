from __future__ import annotations

from typing import Callable
from pathlib import Path
import numpy as np
import retworkx
import scipy.sparse as sp

from snapatac2.genome import Genome
from snapatac2._snapatac2 import (
    AnnData, AnnDataSet, link_region_to_gene, NodeData, LinkData
)

def init_network_from_annotation(
    regions: list[str],
    anno_file: Path | Genome,
    upstream: int = 250000,
    downstream: int = 250000,
    id_type: str = "gene_name",
    coding_gene_only: bool = True,
) -> retworkx.PyDiGraph:
    """
    Build CRE-gene network from gene annotations.

    Link CREs to genes if they are close to genes' promoter regions.

    Parameters
    ----------
    regions:
        A list of peaks/regions, e.g., `["chr1:100-1000", "chr2:55-222"]`.
    anno_file
        The GFF file containing the transcript level annotations.
    upstream
        Upstream extension to the transcription start site.
    downstream
        Downstream extension to the transcription start site.
    id_type
        "gene_name", "gene_id" or "transcript_id".
    coding_gene_only
        Retain only coding genes in the network.

    Returns
    -------
    A network where peaks/regions point towards genes if they are within genes'
    regulatory domains.
    """
    if isinstance(anno_file, Genome):
        anno_file = anno_file.fetch_annotations()
        
    region_added = {}
    graph = retworkx.PyDiGraph()
    links = link_region_to_gene(
        regions,
        str(anno_file),
        upstream,
        downstream,
        id_type,
        coding_gene_only,
    )
    for gene, regions in links.items():
        to = graph.add_node(gene)
        for region, data in regions:
            if region in region_added:
                graph.add_edge(region_added[region], to, data)
            else:
                region_added[region] = graph.add_parent(to, region, data)
    return graph

def add_cor_scores(
    network: retworkx.PyDiGraph,
    peak_mat: AnnData | AnnDataSet,
    gene_mat: AnnData | AnnDataSet,
):
    """
    Compute correlation scores between genes and CREs.

    Parameters
    ----------
    network
        network
    peak_mat
        AnnData or AnnDataSet object storing the cell by peak count matrix,
        where the `.var_names` contains peaks.
    gene_mat
        AnnData or AnnDataSet object storing the cell by gene count matrix,
        where the `.var_names` contains genes.
    """
    from tqdm import tqdm
    from scipy.stats import spearmanr

    if peak_mat.obs_names != gene_mat.obs_names:
        raise NameError("gene matrix and peak matrix should have the same obs_names")

    gene_set = set(gene_mat.var_names)
    prune_network(
        network, 
        node_filter = lambda x: x.id in gene_set or x.type == "region",
    )
    if network.num_edges() == 0:
        return network

    for (nd_X, X), (nd_y, y) in tqdm(_get_data_iter(network, peak_mat, gene_mat)):
        if sp.issparse(X):
            X = X.todense()
        if sp.issparse(y):
            y = y.todense()
        scores = np.apply_along_axis(lambda x: spearmanr(y, x)[0], 0, X)
        for nd, sc in zip(nd_X, scores):
            network.get_edge_data(nd, nd_y).correlation_score = sc

def add_regr_scores(
    network: retworkx.PyDiGraph,
    peak_mat: AnnData | AnnDataSet,
    gene_mat: AnnData | AnnDataSet,
    use_gpu: bool = False,
):
    """
    Perform regression analysis between genes and CREs.

    Parameters
    ----------
    network
        network
    peak_mat
        AnnData or AnnDataSet object storing the cell by peak count matrix,
        where the `.var_names` contains peaks.
    gene_mat
        AnnData or AnnDataSet object storing the cell by gene count matrix,
        where the `.var_names` contains genes.
    use_gpu
        Whether to use gpu
    """
    from tqdm import tqdm

    if peak_mat.obs_names != gene_mat.obs_names:
        raise NameError("gene matrix and peak matrix should have the same obs_names")

    gene_set = set(gene_mat.var_names)
    prune_network(
        network, 
        node_filter = lambda x: x.id in gene_set or x.type == "region",
    )
    if network.num_edges() == 0:
        return network

    tree_method = "gpu_hist" if use_gpu else "hist"

    for (nd_X, X), (nd_y, y) in tqdm(_get_data_iter(network, peak_mat, gene_mat)):
        y = y.todense() if sp.issparse(y) else y
        scores = gbTree(X, y, tree_method=tree_method)
        for nd, sc in zip(nd_X, scores):
            network.get_edge_data(nd, nd_y).regr_score = sc

def prune_network(
    network: retworkx.PyDiGraph,
    node_filter: Callable[[NodeData], bool] | None = None,
    edge_filter: Callable[[LinkData], bool] | None = None,
    remove_isolates: bool = True,
) -> None:
    """
    Prune the network.

    Parameters
    ----------
    network
        network
    node_filter
        Node filter function.
    edge_filter
        Edge filter function.
    """
    if edge_filter is not None:
        for eid in network.edge_indices():
            if not edge_filter(network.get_edge_data_by_index(eid)):
                network.remove_edge_from_index(eid)

    if node_filter is not None:
        for nid in network.node_indices():
            if not node_filter(network.get_node_data(nid)):
                network.remove_node(nid)

    if remove_isolates:
        for nid in network.node_indices():
            if network.in_degree(nid) + network.out_degree(nid) == 0:
                network.remove_node(nid)

class RegionGenePairIter:
    def __init__(
        self,
        network,
        peak_mat,
        gene_mat,
        region_idx_map,
        gene_ids
    ) -> None:
        self.network = network
        self.gene_ids = gene_ids
        self.peak_mat = peak_mat
        self.gene_mat = gene_mat
        self.region_idx_map = region_idx_map
        self.index = 0

    def __len__(self):
        return self.gene_mat.shape[1]

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= self.__len__():
            raise StopIteration

        nd_y = self.gene_ids[self.index]
        nd_X = self.network.predecessor_indices(nd_y)
        y = self.gene_mat[:, self.index]
        X = self.peak_mat[:, [self.region_idx_map[nd] for nd in nd_X]]

        self.index += 1
        return (nd_X, X), (nd_y, y)

def _get_data_iter(
    network: retworkx.PyDiGraph,
    peak_mat: AnnData | AnnDataSet,
    gene_mat: AnnData | AnnDataSet,
) -> RegionGenePairIter:
    genes = []
    regions = set()
    for nd in network.node_indices():
        parents = network.predecessor_indices(nd)
        if len(parents) > 0:
            genes.append(nd)
            for x in parents:
                regions.add(x)
    regions = list(regions)

    gene_idx = gene_mat.var_ix([network[x].id for x in genes])
    gene_mat = gene_mat.X[:, gene_idx]
    region_idx = peak_mat.var_ix([network[x].id for x in regions])
    peak_mat = peak_mat.X[:, region_idx]
    region_idx_map = dict(zip(regions, range(len(regions))))

    return RegionGenePairIter(
        network,
        peak_mat,
        gene_mat,
        region_idx_map,
        genes,
    )

def elastic_net(X, y):
    from sklearn.linear_model import ElasticNet
    regr = ElasticNet(random_state=0).fit(np.asarray(X.todense()), np.asarray(y.todense()))
    return regr.coef_

def gbTree(X, y, tree_method = "hist"):
    import xgboost as xgb
    model = xgb.XGBRegressor(tree_method = tree_method)
    return model.fit(X, y).feature_importances_