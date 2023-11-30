"""
pyhedron: a mesh data structure implemented with half edges
"""

__author__  = 'Andreas Lehn'
from .version import __version__

import sys
import numpy as np

class Polyhedron:
    """ Polyhedron mesh realize with half edges """

    class Edge:
        def __init__(self, idx, target=None, previous=None, next=None, opposite=None, face=None):
            self.idx = idx
            self.target = target
            self.previous = previous
            self.next = next
            self.opposite = opposite
            self.face = face

        def update_neighbours(self):
            self.next.previous = self
            self.previous.next = self
            self.opposite.opposite = self

        def points(self):
            return [self.opposite.target, self.target]

        def __str__(self):
            return str(self.idx)

    class Face:
        def __init__(self, idx, edge=None):
            self.idx = idx
            self.start = edge

        class Iterator:
            def __init__(self, start):
                self.start = start
                self.iter = None

            def __next__(self):
                if self.iter == None:
                    self.iter = self.start
                else:
                    self.iter = self.iter.next
                    if self.iter == self.start:
                        raise StopIteration()
                return self.iter

        def __iter__(self):
            return self.Iterator(self.start)

        def points(self):
            result = []
            for edge in self:
                result.append(edge.target)
            return result

        def update_edges(self):
            for edge in self:
                edge.face = self

        def __str__(self):
            FACE_LETTERS = 'ABCDEFGHIJKLMMNOPQRSTUVWXYZ'
            N = len(FACE_LETTERS)
            name, i = '', self.idx
            while True:
                name = FACE_LETTERS[i % N] + name
                i = i // N
                if i == 0: break
            return name

    def __init__(self):
        """creates a double face ot the points in poly or an empty mesh"""
        self.edges = []
        self.points = []
        self.faces = []

    def point(self, vec):
        """create a point in the list of points and returns its index"""
        assert(len(vec) == 3)
        self.points.append(np.array(vec))
        return len(self.points) - 1

    def half_edge(self, target = None, previous=None, next=None, opposite=None, face=None):
        result = Polyhedron.Edge(len(self.edges), target, previous, next, opposite, face)
        self.edges.append(result)
        return result

    def face(self, start=None):
        result = Polyhedron.Face(len(self.faces), start)
        self.faces.append(result)
        return result

    def make_double_face(self, vec):
        """ creates a double side face with only one point """
        assert(len(vec) == 3)
        point = self.point(vec)
        edge = self.half_edge(point)
        mate = self.half_edge(point, opposite=edge)
        mate.next = mate
        mate.previous = mate
        edge.next = edge
        edge.previous = edge
        edge.opposite = mate
        face = self.face(edge)
        edge.face = face
        double = self.face(mate)
        mate.face = double
        return face, double
    
    def make_poly_double_face(self, polygon):
        """ creates a double sided face out of the points (vectors) in polygon"""
        face, double = self.make_double_face(polygon[0])
        edge = face.start
        for i in range(1, len(polygon)):
            edge = self.append_point(edge)
            self.points[edge.target] = np.array(polygon[i])
        return face, double

    def from_poly(polygon):
        """ creates a polyhedron from the point (vectors) in polygon """
        result = Polyhedron()
        result.make_poly_double_face(polygon)
        return result
    
    def from_extrude(polygon, vector):
        """ creates a polyhedron form an extrusion of polygon (list of vectors) wiht vector """
        result = Polyhedron()
        face, _ = result.make_poly_double_face(polygon)
        result.extrude(face, vector)
        return result
    
    def dup_point(self, index):
        """ duplicates a point in the list of points """
        return self.point(np.array(self.points[index], copy=True))
    
    def edge_to_face(self, edge):
        assert(isinstance(edge, Polyhedron.Edge))
        new_face = self.face()
        new_edge = self.half_edge(edge.target, None, None, edge.opposite, new_face)
        new_opposite = self.half_edge(edge.opposite.target, new_edge, new_edge, edge, new_face)
        new_opposite.update_neighbours()
        new_edge.update_neighbours()
        new_face.start = new_edge
        return new_edge

    def point_to_edge(self, edge):
        assert(isinstance(edge, Polyhedron.Edge))
        opposite = edge.opposite
        new_point = self.dup_point(edge.target)
        new_edge = self.half_edge(edge.target, edge.next.opposite, edge.next.opposite.next, None, edge.next.opposite.face)
        new_opposite = self.half_edge(new_point, edge.opposite.previous, opposite, new_edge, edge.opposite.face)
        new_edge.opposite = new_opposite
        edge.target = new_point
        edge.next.opposite.target = new_point

        new_edge.update_neighbours()
        new_opposite.update_neighbours()
        return new_edge

    def append_point(self, edge):
        assert(isinstance(edge, Polyhedron.Edge))
        opposite = edge.opposite
        new_point = self.dup_point(edge.target)
        new_edge = self.half_edge(new_point, edge, edge.next, None, edge.face)
        new_opposite = self.half_edge(edge.target, opposite.previous, opposite, new_edge, edge.opposite.face)
        new_edge.opposite = new_opposite
        opposite.previous.target = new_point

        new_edge.update_neighbours()
        new_opposite.update_neighbours()
        return new_edge

    def apply_to_points(self, f, points):
        if points == None:
            points = self.points
        elif isinstance(points, int):
            points = [ points ]
        for i in points:
            f(i)

    def translate(self, vec, points=None):
        assert(len(vec) == 3)
        def add(self, i, vec):
            self.points[i] += np.array(vec)

        self.apply_to_points(lambda i: add(self, i, vec), points)

    def scale(self, vec, points=None):
        assert(len(vec) == 3)
        def mul(self, i, vec):
            self.points[i] *= vec

        self.apply_to_points(lambda i: mul(self, i, vec), points)

    def loop_cut(self, face):
        assert(isinstance(face, Polyhedron.Face))
        for edge in face:
            self.edge_to_face(edge)
        
        for edge in face:
            self.point_to_edge(edge)
        return face.start.opposite

    def split_face(self, edge):
        assert(isinstance(edge, Polyhedron.Edge))
        result = self.edge_to_face(edge)
        self.point_to_edge(edge)
        self.point_to_edge(edge.previous)
        return edge
    
    def edge_cut(self, edge):
        assert(isinstance(edge, Polyhedron.Edge))
        result = self.edge_to_face(edge)
        self.edge_to_face(edge.previous)
        self.edge_to_face(edge.next)
        self.point_to_edge(edge.opposite)
        self.point_to_edge(edge.opposite.previous)
        return edge

    def vertex_cut(self, edge):
        assert(isinstance(edge, Polyhedron.Edge))
        result = self.edge_to_face(edge)
        self.edge_to_face(edge.next)
        self.point_to_edge(edge.next.opposite)

    def extrude(self, face, vec):
        assert(isinstance(face, Polyhedron.Face))
        assert(len(vec) == 3)
        self.loop_cut(face)
        self.translate(vec, face.points())

    def to_dot(self, file=sys.stdout):
        print('digraph {', file=file)
        for edge in self.edges:
            print(f'    {edge.previous.target} -> {edge.target} [label="{str(edge.face)}"]', file=file)
        print('}', file=file)
    
    def to_obj(self, object_name, file=sys.stdout):
        print('o', object_name, file=file)
        for p in self.points:
            x, y, z = p
            print('v', x, y, z, file=file)
        for f in self.faces:
            p = f.points()
            print('f', *map(lambda i: i+1, p), file=file)
    
    def to_usda(self, path, file=sys.stdout):
        pass

    def list_edges(self):
        for i in range(len(self.edges)):
            edge = self.edges[i]
            print(f'e{edge.idx} -> e{edge.next.idx} | e{edge.opposite.idx}: p{edge.target} {self.points[edge.target]} {str(edge.face)}')

    def check_consistency(self):
        for edge in self.edges:
            assert edge.next.previous == edge, f'Edge {edge.idx}: next/previous check failed.'
            assert edge.previous.next == edge, f'Edge {edge.idx}: previous/next check failed.'
            assert edge.opposite.opposite == edge, f'Edge {edge.idx}: opposite/opposite check failed.'
            assert edge.previous.face == edge.face, f'Edge {edge.idx}: previous face check failed.'
            assert edge.next.face == edge.face, f'Edge {edge.idx}: next face check failed.'
            assert edge.target == edge.opposite.previous.target, f'Edge {edge.idx}: opposite target check failed.'
            assert edge.previous.target == edge.opposite.target, f'Edge {edge.idx}: previous opposite target check failed.'

        for face in self.faces:
            assert face.start.face == face, f'Face {str(face)}: start face check failed.'

    def list_points(self):
        for i in range(len(self.points)):
            print(f'[{i}]: {self.points[i]}')
        print()
