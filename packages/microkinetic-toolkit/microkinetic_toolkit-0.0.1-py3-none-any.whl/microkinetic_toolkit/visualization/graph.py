from microkinetic_toolkit.reactions import Reactions
import pickle
import json
import numpy as np
import os
from typing import Tuple
from matplotlib.figure import Figure
from matplotlib.axes._axes import Axes


def change_to_vissym(chem_sym: str) -> str:
    """change_to_vissym.

    Args:
        chem_sym (str): chem_sym like CH3_surf, etc.

    Returns:
        str: chemical symbol like CH3* etc.
    """
    symbol = chem_sym.replace(
                        "_surf",
                        "*").replace("surf", "*")
    return symbol


class ReactionsVisualizer(Reactions):
    """
    Reaction visualizer.
    """
    def draw_network(self, plot_option: bool = True) -> Tuple[Figure, Axes]:
        """
        Draw reaction network.

        Args:
            plot_option:
        Returns:
            fig, axes: matplotlib figure and axes
        """
        import matplotlib.pyplot as plt
        import networkx as nx
        from math import log10
        import h5py

        label_rxn = False
        directed = True

        eps = 1.0e-10
        edge_scale = 0.02  # scaling for edge thickness
        edge_min = 1.0  # minimal size of edge
        # Threshold for rxn rate in log scale. Rxn with smaller than this value is droped.
        rate_thre = -15.0

        node_scale = 100.0
        node_min = 10.0
        surf_scale = 1.0

        rxn_num = len(self.reaction_list)
        if not os.path.exists("rate.pickle"):
            ems = "rate.pickle is needed for draw_network method."
            raise OSError(ems)
        with open("rate.pickle", "rb") as file:
            rate = pickle.load(file)

        value = np.zeros(rxn_num)
        for irxn, reaction in enumerate(self.reaction_list):
            if abs(rate[irxn]) >= rate_thre:
                value[irxn] = edge_scale * log10(abs(rate[irxn])) + edge_min
            else:
                value[irxn] = 1.0

        c_siz = 200
        c_col = "blue"
        r_siz = 10
        r_col = "black"

        coverage = True
        conc_h5 = "coverage.h5"
        if coverage:
            with h5py.File(conc_h5) as h5file:
                cov = h5file["concentration"][:]
        cov = cov[:, -1]  # last

        if directed:
            G = nx.DiGraph()
        else:
            G = nx.Graph()

        for irxn, reaction in enumerate(self.reaction_list):
            rxn = reaction._reaction_str
            rxn = change_to_vissym(rxn)
            G.add_node(rxn, size=r_siz,
                       color=r_col, typ='rxn')
            for direction in ["forward", "reverse"]:
                sequence = reaction.reactants if direction == "forward" else reaction.products
                for mol in sequence:
                    if coverage:
                        spe = mol[1]
                        spe_num = self.get_index_of_species(spe)
                        size = cov[spe_num] if cov[spe_num] > eps else eps
                        size = node_scale * (node_min + log10(size))
                        if "surf" in spe:
                            size = size * surf_scale
                        size = int(size)
                    else:
                        size = c_siz
                    spe = change_to_vissym(spe)
                    G.add_node(spe, size=size, color=c_col, typ='comp')

                    if directed:
                        if direction == "forward":
                            if value[irxn] > 0:
                                G.add_edge(spe, rxn, weight=abs(value[irxn]))
                            else:
                                G.add_edge(rxn, spe, weight=abs(value[irxn]))
                        else:  # reverse
                            if value[irxn] > 0:
                                G.add_edge(rxn, spe, weight=abs(value[irxn]))
                            else:
                                G.add_edge(spe, rxn, weight=abs(value[irxn]))
                    else:  # non-directed
                        # G.add_edge(reac[i][ireac], rxn, weight=abs(value[i]))
                        G.add_edge(spe, rxn, weight=abs(value[irxn]))

        # drawing
        siz = nx.get_node_attributes(G, 'size')
        col = nx.get_node_attributes(G, 'color')

        pos = nx.drawing.nx_pydot.graphviz_layout(G, prog='fdp')  # prog='neato' is also a good choice
        if os.path.exists("network_pos.json"):
            with open("network_pos.json") as read:
                pos = json.load(read)
            print("===============================================================")
            print("loaded graph's node and edge positions from networks_pos.json")
            print("===============================================================")
        else:
            print("================================================")
            print("skiped loading graph pos from networks_pos.json")
            print("================================================")
        with open("network_pos_dumped.json", "w") as write:
            json.dump(pos, write)
            print("dumped network_pos_dumped.json")
        nx.draw_networkx_nodes(G, pos, nodelist=list(siz.keys()),
                               node_size=list(siz.values()),
                               node_color=list(col.values()),
                               alpha=0.5)
        edges = G.edges()
        weights = [G[u][v]['weight'] for u, v in edges]

        nx.draw_networkx_edges(G, pos, edge_color='gray',
                               alpha=0.8, width=weights)

        # compound labels
        if directed:
            Gcomp = nx.DiGraph()
        else:
            Gcomp = nx.Graph()

        for n, typ in G.nodes.data('typ'):
            if typ == 'comp':
                Gcomp.add_node(n)

        nx.draw_networkx_labels(Gcomp, pos, font_size=10)
        # font_family='Gill Sans MT')

        # reaction labels
        if label_rxn:
            rxn_label_size = 10
        else:
            rxn_label_size = 0

        if directed:
            Grxn = nx.DiGraph()
        else:
            Grxn = nx.Graph()
        #
        for n, typ in G.nodes.data('typ'):
            if typ == 'rxn':
                Grxn.add_node(n)

        nx.draw_networkx_labels(Grxn, pos, font_size=rxn_label_size)
        # font_family='Gill Sans MT')

        plt.xticks([])
        plt.yticks([])
        if plot_option:
            plt.show()
        # plt.savefig("graph.eps", format="eps")
        nx.write_gexf(G, './test.gexf')
        current_axes = plt.gca()
        current_fig = plt.gcf()

        return current_fig, current_axes
