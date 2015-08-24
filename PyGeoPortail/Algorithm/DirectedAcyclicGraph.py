####################################################################################################
#
# PyGeoPortail - A IGN GeoPortail Map Viewer
# Copyright (C) 2015 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

class DirectedAcyclicGraphNode(object):

    ##############################################

    def __init__(self, node_id, data=None):

        # self._ ?
        self._node_id = node_id
        self._data = data

        self.ancestors = set()
        self.descendants = set()

    ##############################################

    def __repr__(self):
        return str(self._node_id)

    ##############################################

    @property
    def node_id(self):
        return self._node_id

    ##############################################

    @property
    def data(self):
        return self._data

    ##############################################

    @property
    def is_root(self):
        return not self.ancestors

    ##############################################

    @property
    def is_leaf(self):
        return not self.descendants

    ##############################################

    def disconnect_ancestor(self, node):

        self.ancestors.remove(node)
        node.descendants.remove(self)

    ##############################################

    def connect_ancestor(self, node):

        self.ancestors.add(node)
        node.descendants.add(self)

    ##############################################

    def breadth_first_search(self):

        # Name

        queue = [self]
        visited = set((self,))
        while queue:
            node = queue.pop(0)
            yield node
            for descendant in node.descendants:
                if descendant not in visited:
                    queue.append(descendant)
                    visited.add(descendant)

####################################################################################################

class DirectedAcyclicGraph(object):

    ##############################################
    
    def __init__(self):

        self._nodes = {}

    ##############################################

    def __iter__(self):

        return iter(self._nodes.values())

    ##############################################

    def __getitem__(self, node_id):

        return self._nodes[node_id]

    ##############################################

    def add_node(self, node_id, **kwargs):

        if node_id not in self._nodes:
            self._nodes[node_id] = DirectedAcyclicGraphNode(node_id, **kwargs)
        else:
            raise NameError("Node {} is already registered".format(node_id))

    ##############################################

    def add_edge(self, ancestor, descendant):

        descendant.connect_ancestor(ancestor)

    ##############################################

    def roots(self):

        return [node for node in self if node.is_root]

    ##############################################

    def leafs(self):

        return [node for node in self if node.is_leaf]

    ##############################################

    def topological_sort(self):

        sorted_list = [] # reversed
        unmarked_nodes = set(self._nodes.values())
        marked_nodes = set()
        temporary_marked_nodes = set()

        def visit(node):
            if node in temporary_marked_nodes:
                raise NameError("Not a DAG")
            if node not in marked_nodes:
                temporary_marked_nodes.add(node)
                for descendant in node.descendants:
                    visit(descendant)
                marked_nodes.add(node)
                temporary_marked_nodes.remove(node)
                sorted_list.append(node)

        while unmarked_nodes:
            node = unmarked_nodes.pop()
            visit(node)

        sorted_list.reverse()

        return sorted_list

####################################################################################################
# 
# End
# 
####################################################################################################
