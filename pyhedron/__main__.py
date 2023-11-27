"""
A Polyhedron implemented in Python

Polyhedron is a mesh data structure realized as half edge implementation
"""

__author__  = 'Andreas Lehn'
from .version import __version__
from . import Polyhedron

if __name__ == '__main__':
    base_plate = [
        (-1.0, -1.0, 0.0),
        ( 1.0, -1.0, 0.0),
        ( 1.0,  1.0, 0.0),
        (-1.0,  1.0, 0.0)]

    mesh = Polyhedron()
    face, _ = mesh.poly_to_double_face(base_plate)
    edge = mesh.edges[0]
    opposite = edge.opposite
    #mesh.loop_cut(face)
    mesh.extrude(face, (0.0, 0.0, 1.0))
    mesh.extrude(face, (0.0, 0.0, 0.5))
    mesh.scale((0.5, 0.5, 1.0), face.points())
    mesh.extrude(face, (0.0, 0.0, 0.5))
    #mesh.edge_cut(face.start)
    #mesh.translate((0.5, 0.0, 0.5), face.start.points())
    #mesh.list_edges()
    mesh.check_consistency()
    
    mesh.to_obj('pyhedron')
