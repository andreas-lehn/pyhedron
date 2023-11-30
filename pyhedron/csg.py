"""Constructive Solid Geometry bridge from pyhedron to pycsg"""

__author__ = "Andreas Lehn"
from .version import __version__
from . import Polyhedron
import numpy as np
from csg.core import CSG
from csg.geom import Vertex, Polygon

def deg2rad(alpha):
    return np.pi * alpha / 180

def yaw_matrix(gamma):
    a = deg2rad(gamma)
    yaw = np.array([
        [np.cos(a), -np.sin(a), 0],
        [np.sin(a),  np.cos(a), 0],
        [        0,          0, 1]
    ])
    return yaw

def pitch_matrix(alpha):
    b = deg2rad(alpha)
    pitch = np.array([
        [np.cos(b), 0, -np.sin(b)],
        [        0, 1,          0],
        [np.sin(b), 0,  np.cos(b)]
    ])
    return pitch

def roll_matrix(beta):
    c = deg2rad(beta)
    roll = np.array([
        [ 1,         0,          0],
        [ 0, np.cos(c), -np.sin(c)],
        [ 0, np.sin(c),  np.cos(c)]
    ])
    return roll

def rot_matrix(vec):
    """ rotates in XYZ-Euler """
    alpha, beta, gamma = vec
    return yaw_matrix(gamma).dot(roll_matrix(beta)).dot(pitch_matrix(alpha))

def from_polyhedron(polyhedron, rotate=(0.,0.,0.), scale=(1.,1.,1.), translate=(0.,0.,0.)):
    """ constructs a CSG object from a Polyhedron

    The polyhedron can be transformed with rotate, scale and translate in this order.
    """
    assert isinstance(polyhedron, Polyhedron)
    translate, scale = np.array(translate), np.array(scale)
    polygons = []
    for face in polyhedron.faces:
        vertices = []
        for edge in face:
            point = polyhedron.points[edge.target]
            point = rot_matrix(rotate).dot(point) * scale + translate
            vertices.append(Vertex(point))
        polygons.append(Polygon(vertices))
    return CSG.fromPolygons(polygons)
