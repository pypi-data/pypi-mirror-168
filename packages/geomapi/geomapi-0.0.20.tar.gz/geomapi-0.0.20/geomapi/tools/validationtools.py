"""
validationtools - a Python library for validating objects.
"""
#IMPORT PACKAGES
from lib2to3.pytree import Node
import numpy as np 
import cv2 
import open3d as o3d 
import json  
import os 
import re
import matplotlib.pyplot as plt #conda install -c conda-forge matplotlib
#import torch #conda install -c pytorch pytorch
# import pye57 #conda install xerces-c  =>  pip install pye57
import xml.etree.ElementTree as ET 
# from pathlib import Path
import math
import xlsxwriter
import csv
import copy
from PIL import Image, ImageDraw
import time 
import ifcopenshell.geom as geom
import math
from scipy.spatial.transform import Rotation as R
from PIL import Image, ImageDraw
import shutil
from rdflib import Graph, URIRef, RDF
import os.path
import importlib
import numpy as np
import xml.etree.ElementTree as ET
import open3d as o3d
import uuid    
import copy
import pye57 
import ifcopenshell
import multiprocessing as mp
import time
from pathlib import Path
from typing import List
import matplotlib.pyplot as plt
import csv
import xlsxwriter

# import ifcopenshell.util
# import ifcopenshell.geom as geom
# from ifcopenshell.util.selector import Selector
# from ifcopenshell.ifcopenshell_wrapper import file

# import APIs
import rdflib
from rdflib import Graph, plugin
from rdflib.serializer import Serializer #pip install rdflib-jsonld https://pypi.org/project/rdflib-jsonld/
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
                           PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
                           VOID, XMLNS, XSD


import geomapi.utils.geometryutils as gt

#IMPORT MODULES 
from geomapi.nodes import *
from geomapi.nodes.sessionnode import create_node 
import geomapi.utils as ut
import geomapi.utils.geometryutils as gt

def get_boundingbox_of_list_of_geometries(geometries:List[Node]) -> np.array:
    """Determines the global boundingbox of a group of Node containing geometries.

    Args:
        geometries (List[Nodes]):  list of Nodes containing a resource of which the boundingbox must be determined"
            
    Returns:
        np.array[3x1]
    """
    pcd = o3d.geometry.PointCloud()
    for n in geometries:
        n.get_resource()
        if n.resource is not None:
            pcd.__iadd__(o3d.geometry.PointCloud(gt.get_oriented_bounds(gt.get_cartesian_bounds(n.resource))))
    cartesianBounds = gt.get_cartesian_bounds(pcd.get_oriented_bounding_box())
    return cartesianBounds

def optimize_camera_for_overview(geometries:List[Node]):
    """Determines the camera position to create an overview image of a group of Nodes containing geometries.

    Args:
        geometries (List[Nodes]):  list of Nodes containing a resource "
            
    Returns:
        c center of the objects np.array[1x3]
        c_i the camera position np.array[1x3]
        up defines which direction is up [0,0,1] for z
    """

    cartesianBounds = get_boundingbox_of_list_of_geometries(geometries=geometries)
    bbbox = gt.get_oriented_bounding_box(cartesianBounds)

    fov = np.pi / 3 #60 #degrees
            
    #determine extrinsic camera parameters
    extrinsic = np.empty((1,3), dtype=float)
    
    c = bbbox.get_center()
    u = bbbox.extent[0]
    d_w = math.cos(fov/2)*u

    #determine c_i
    rotation_matrix = bbbox.R
    pcd2 = o3d.geometry.PointCloud()
    array = np.array([[c[0],c[1],c[2]+d_w]])
    pcd2.points = o3d.utility.Vector3dVector(array)
    c_i = np.asarray(pcd2.points[0])

    up = [0, 0, 1]  # camera orientation

    
    return c,c_i,up

def create_croppedpcd(pointcloud: PointCloudNode, element: BIMNode, bb: o3d.geometry.OrientedBoundingBox, sn : SessionNode) -> PointCloudNode:
    """Crops a part of a point cloud around a BIM object.

    Args:
        pointcloud (PointCloudNode): Pointcloud from which the zone needs to be cropped
        element (BIMNode): The BIMNode that the cropped region represents
        bb (o3d.geometry.OrientedBoundingBox): The boundingbox that needs to be cropped from the pointcloud
        samplesize (Optional float): When the results needs to be downsampled.
            
    Returns:
        PointCloudNode containing the pointcloud of the cropped region
    """
    myCroppedPCD=pointcloud.resource.crop(bb)
    if len(np.asarray(myCroppedPCD.points)) > 0:
        if sn.resolution and len(np.asarray(myCroppedPCD.points)) >= 1000:
            myCroppedPCD = myCroppedPCD.voxel_down_sample(sn.resolution)
        
        try:
            myCroppedPCDNode=PointCloudNode(resource=myCroppedPCD,
                                        name = element.get_name().split("-")[0] + "-CROPPEDPCD",
                                        subject=element.get_name().split("-")[0] + "-CROPPEDPCD",
                                        isDerivedFromGeometry=pointcloud.subject,
                                        processed = False)
            myCroppedPCDNode.save_resource(sn.projectProcessingPath)
            return myCroppedPCDNode
        
        except:
            return None
    else:
        return None

def add_to_croppedpcd(pointcloud: PointCloudNode, element: BIMNode, target: PointCloudNode ,bb: o3d.geometry.OrientedBoundingBox, sn: SessionNode) -> PointCloudNode:
    """adds a part to a point cloud.

    Args:
        
            
    Returns:
        PointCloudNode containing the pointcloud of the cropped region
    """
    myCroppedPCD=pointcloud.resource.crop(bb)
    if len(np.asarray(myCroppedPCD.points)) > 0:
        if sn.resolution and len(np.asarray(myCroppedPCD.points)) >= 1000:
            myCroppedPCD = myCroppedPCD.voxel_down_sample(sn.resolution)
        target.resource.__iadd__(myCroppedPCD)
        target.save_resource(sn.projectProcessingPath)

def get_BIMNode(subject, sn : SessionNode):
    """Gets the BIMNode  from which it is derived.

    Args:
        subject: the subject from which it was derived
        BIMNodeList (List[BIMNodes]): list of all the BIMNodes in the project
            
    Returns:
        PointCloudNode containing the pointcloud of the cropped region
    """
    for n in sn.bimNodes:
        if n.subject is subject:
            return n

def get_cropped_pcdNode(subject, sn : SessionNode):
    for n in sn.meshpcdNodes:
        if n.subject.split("-")[0] in subject:
            return n

def get_referenceCloudNode(subject, sn : SessionNode):
    for n in sn.meshpcdNodes:
        if n.subject.split("-")[0] in subject:
            return n

def distance_filtering(target: PointCloudNode, reference: PointCloudNode, sn : SessionNode):
    
    d = target.resource.compute_point_cloud_distance(reference.resource)
    
    i = 0
    indeces = []

    while i < len(d):
        if d[i] < sn.Td:
            indeces.append(i)
        i += 1
    
    BIMNode = get_BIMNode(reference.isDerivedFromGeometry, sn=sn)
    
    if len(indeces) > 50:
        filteredpcdNode = PointCloudNode(resource = target.resource.select_by_index(indeces),
                                        subject=BIMNode.get_name().split("-")[0] + "-FILTEREDPCD",
                                        name = BIMNode.get_name().split("-")[0] + "-FILTEREDPCD",
                                        isDerivedFromGeometry=target.subject,
                                        processingType = 'DISTANCE',
                                        processed = False)
        filteredpcdNode.path = os.path.join(sn.projectProcessingPath, filteredpcdNode.get_name() + ".pcd")
        if os.path.exists(filteredpcdNode.path):
            print("Path already exisits")
            filteredpcdNode.path = os.path.join(sn.projectProcessingPath, filteredpcdNode.get_name() + time.strftime("%Y%m%d%H%M%S") +".pcd")
        filteredpcdNode.save_resource(sn.projectProcessingPath)
       
        return filteredpcdNode
    else:
        return None

def normal_filtering(target: PointCloudNode, reference: PointCloudNode, sn : SessionNode ):
    if not target.resource.has_normals():
        target.resource.estimate_normals()
    if not reference.resource.has_normals():
        reference.resource.estimate_normals()

    d = target.resource.compute_point_cloud_distance(reference.resource)

    i = 0
    indeces_d = []

    while i < len(d):
        if d[i] < sn.Td:
            indeces_d.append(i)
        i += 1
    
    BIMNode = get_BIMNode(reference.isDerivedFromGeometry, sn=sn)
    
    if len(indeces_d) > 50:
        indeces_n = []
        kdtree = o3d.geometry.KDTreeFlann(reference.resource)
        for id in indeces_d:
            [k, idx, d] = kdtree.search_radius_vector_3d(target.resource.points[id], 0.1)
            matched = False
            i = 0
            while not matched and i < len(idx) and len(idx) > 0:
                if np.abs(np.dot(np.asarray(target.resource.normals[id]), np.asarray(reference.resource.normals[idx[i]]))) > sn.Tdot:
                    indeces_n.append(id)
                    matched = True
                i += 1
        if len(indeces_n) > 50:
            filteredpcdNode = PointCloudNode(resource = target.resource.select_by_index(indeces_n),
                                        subject=BIMNode.get_name().split("-")[0] + "-FILTEREDPCD",
                                        name = BIMNode.get_name().split("-")[0] + "-FILTEREDPCD",
                                        isDerivedFromGeometry=target.subject,
                                        processingType = 'NORMALS',
                                        processed = False)
            filteredpcdNode.path = os.path.join(sn.projectProcessingPath, filteredpcdNode.get_name() + ".pcd")
            if os.path.exists(filteredpcdNode.path):
                print("Path already exisits")
                filteredpcdNode.path = os.path.join(sn.projectProcessingPath, filteredpcdNode.get_name() + time.strftime("%Y%m%d%H%M%S") +".pcd")
            filteredpcdNode.save_resource(sn.projectProcessingPath)
        
            return filteredpcdNode
        else: 
            return None
    else:
        return None

def color_by_LOA(target: PointCloudNode, distances: o3d.utility.DoubleVector, sn : SessionNode):
    i=0
    target.resource.paint_uniform_color([1,1,1])
    # print(len(np.asarray(target.resource.points)))
    # print(len(np.asarray(target.resource.colors)))
    # print(len(np.asarray(distances)))
    while i < len(distances):
        distance = distances[i]
        
        if distance < sn.t00:
            np.asarray(target.resource.colors)[i] = [1,0,0]
        if distance < sn.t10:
            np.asarray(target.resource.colors)[i] = [1,0.76,0]
        if distance < sn.t20:
            np.asarray(target.resource.colors)[i] = [1,1,0]
        if distance < sn.t30:
            np.asarray(target.resource.colors)[i] = [0,1,0]
        i += 1
    
    pcdResultDirectory = os.path.join(sn.resultsPath, "PCD")
    if not os.path.isdir(pcdResultDirectory): #check if the folder exists
        os.mkdir(pcdResultDirectory)

    target.save_resource(pcdResultDirectory)

def compute_LOA(target: PointCloudNode, reference: PointCloudNode,sn : SessionNode):
    d = target.resource.compute_point_cloud_distance(reference.resource)
    
    LOA10Inliers = 0
    LOA20Inliers = 0
    LOA30Inliers = 0
    LOA00Inliers = 0
    totalPoints = len(d)

    for dis in np.asarray(d):
        if dis < sn.t00:
            LOA00Inliers += 1
        if dis < sn.t10:
            LOA10Inliers += 1
        if dis < sn.t20:
            LOA20Inliers += 1
        if dis < sn.t30: 
            LOA30Inliers += 1
    if LOA00Inliers < totalPoints:
        prct = LOA00Inliers/totalPoints *100
    
    if LOA00Inliers > 0:
        LOA10 = LOA10Inliers/LOA00Inliers
        LOA20 = LOA20Inliers/LOA00Inliers
        LOA30 = LOA30Inliers/LOA00Inliers

        color_by_LOA(target = target, distances=d, sn = sn)

        return [LOA10, LOA20, LOA30]
    else:
        return None

def LOA_to_csv(element : BIMNode, sn : SessionNode):
    data = [element.name, element.globalId, element.key, element.accuracy, element.LOA10, element.LOA20, element.LOA30]
    sn.csvWriter.writerow(data)

def LOA_to_xlsx(element : BIMNode, sn : SessionNode):

    sn.worksheet.write(sn.xlsxRow, 0, element.name)
    sn.worksheet.write(sn.xlsxRow, 1, element.globalId)
    sn.worksheet.write(sn.xlsxRow, 2, element.key)
    sn.worksheet.write(sn.xlsxRow, 3, element.accuracy)
    sn.worksheet.write(sn.xlsxRow, 4, element.LOA10)
    sn.worksheet.write(sn.xlsxRow, 5, element.LOA20)
    sn.worksheet.write(sn.xlsxRow, 6, element.LOA30)

    sn.xlsxRow +=1


def LOA_to_mesh(element : BIMNode, sn : SessionNode):
    
    meshResultDirectory = os.path.join(sn.resultsPath, "PLY")
    if not os.path.isdir(meshResultDirectory): #check if the folder exists
        os.mkdir(meshResultDirectory)
    
    meshResultName = element.name
    meshResultFileName = meshResultName + ".ply"
    meshResultPath = os.path.join(meshResultDirectory, meshResultFileName)

    if not element.accuracy == "NO LOA":
        if element.resource or os.path.exists(element.path):
            loaded = False
            if not element.resource and element.path:
                #Load the meshobject from disk
                element.resource = o3d.io.read_triangle_mesh(element.path)
                loaded = True
        result = element.resource
        if element.accuracy == "LOA30":
            result.paint_uniform_color([0,1,0])
        elif element.accuracy == "LOA20":
            result.paint_uniform_color([1,1,0])
        elif element.accuracy == "LOA10":
            result.paint_uniform_color([1,0.76,0])
        elif element.accuracy == "LOA00":
            result.paint_uniform_color([1,0,0])
        else:
            result.paint_uniform_color([1,1,1])
        
        if loaded:
            element.resource = None
        
        o3d.io.write_triangle_mesh(meshResultPath,result)
        # print("OBJ file saved in %s" %meshResultPath)

    else: 
        print("ERROR no LOAs where computed in previous steps") 

def optimize_camera(node: Node):
    
    fov = np.pi / 3 #60 #degrees
    
    #determine extrinsic camera parameters
    extrinsic = np.empty((1,3), dtype=float)
    
    if node.resource is not None:
        box=node.resource.get_oriented_bounding_box()
        c = box.get_center()
        u= box.extent[0]

        d_w=math.cos(fov/2)*u
        #determine c_i
        rotation_matrix=box.R
        pcd = o3d.geometry.PointCloud()
        array=np.array([[c[0],c[1],c[2]+d_w]])
        pcd.points = o3d.utility.Vector3dVector(array)
        pcd.rotate(rotation_matrix, center =c)
        c_i=np.asarray(pcd.points[0])

        up = [0, 0, 1]  # camera orientation

    return c,c_i,up

def create_detail_image(resultpcd : PointCloudNode, sn : SessionNode, width = 640, height = 480):

    referenceNode = get_referenceCloudNode(subject = resultpcd.subject, sn = sn)
    bimnode = get_BIMNode(subject = referenceNode.isDerivedFromGeometry, sn = sn)
    
    #generate scene
    render = o3d.visualization.rendering.OffscreenRenderer(width,height)

    #Determine the materials for visualization 
    mtl=o3d.visualization.rendering.MaterialRecord()
    mtl.base_color = [1.0, 1.0, 1.0, 1.0]  # RGBA
    mtl.shader = "defaultUnlit"
    
    mtlline=o3d.visualization.rendering.MaterialRecord()
    mtlline.base_color = [0.0, 0.0, 0.0, 0.0]  # RGBA
    mtlline.shader = "defaultUnlit"
    
    #set camera
    # # Look at the origin from the front (along the -Z direction, into the screen), with Y as Up.
    center, eye, up = optimize_camera(bimnode)
    render.scene.camera.look_at(center, eye, up)
    
    #add geometries
    if not bimnode.resource:
        bimnode.get_resource()
    #Add the BIM elements wireframe to the scene to have a bether understanding of the object
    wireframe = o3d.geometry.LineSet.create_from_triangle_mesh(bimnode.resource)
    wireframe.paint_uniform_color([0,0,0])
    
    render.scene.add_geometry("test",resultpcd.resource,mtl)
    render.scene.add_geometry("lines", wireframe, mtlline)

    #render the image
    img = render.render_to_image()
    imageResultDirectory = os.path.join(sn.resultsPath, "IMAGES")
    if not os.path.isdir(imageResultDirectory):
        os.mkdir(imageResultDirectory)
    detailImageResultName = bimnode.name
    detailImageResultFileName = detailImageResultName + ".png"
    detailImageResultPath = os.path.join(imageResultDirectory, detailImageResultFileName)

    o3d.io.write_image(detailImageResultPath, img)
    bimnode.detailImagePath = detailImageResultPath

def create_report(resultpcd : PointCloudNode, sn : SessionNode):

    referenceNode = get_referenceCloudNode(subject = resultpcd.subject, sn = sn)
    bimnode = get_BIMNode(subject = referenceNode.isDerivedFromGeometry, sn = sn)

    #Load both the detail and overview image of the object
    detail = Image.open(bimnode.detailImagePath)
    overview = Image.open(bimnode.overviewImagePath)

    info = Image.new('RGB', (int(overview.width/2), int(overview.height/2)), color = (255,255,255))
    d = ImageDraw.Draw(info)
    d.text((10,10),bimnode.name, fill=(0,0,0))
    d.text((10,20), time.strftime("%Y%m%d-%H%M%S"), fill=(0,0,0))
    
    d.text((10,70),"LOA10  (%sm - %sm)" %(sn.t20,sn.t10), fill=(0,0,0))
    if np.round(bimnode.LOA10, decimals = 2) < sn.p10:
        d.text((200,70), str(np.round(bimnode.LOA10*100, decimals = 2)) + "%", fill=(255,0,0))
    else:
        d.text((200,70), str(np.round(bimnode.LOA10*100, decimals = 2))+ "%", fill=(0,255,0))
    
    d.text((10,80), "LOA20  (%sm - %sm)" %(sn.t30, sn.t20), fill=(0,0,0))
    if np.round(bimnode.LOA20, decimals = 2) < sn.p20:
        d.text((200,80), str(np.round(bimnode.LOA20*100, decimals = 2))+ "%", fill=(255,0,0))
    else:
        d.text((200,80), str(np.round(bimnode.LOA20*100, decimals = 2))+ "%", fill=(0,255,0))

    d.text((10,90), "LOA30  (%sm - %sm)" %(0, sn.t30), fill=(0,0,0))
    if np.round(bimnode.LOA30, decimals = 2) < sn.p30:
        d.text((200,90), str(np.round(bimnode.LOA30*100, decimals = 2))+ "%", fill=(255,0,0))
    else:
        d.text((200,90), str(np.round(bimnode.LOA30*100, decimals = 2))+ "%", fill=(0,255,0))
    

    resizedInfo= info.resize((overview.width,overview.height), Image.ANTIALIAS)
    info_overview = Image.new('RGB', (overview.width, overview.height*2))
    info_overview.paste(resizedInfo, (0,0))
    info_overview.paste(overview, (0,overview.height))

    newHeigth = 2*overview.height
    hpercent = (newHeigth/float(detail.height))
    wsize = int((float(detail.width)*float(hpercent)))
    resizedImage = detail.resize((wsize, newHeigth), Image.ANTIALIAS)

    report = Image.new('RGB', (overview.width + wsize, overview.height*2))
    report.paste(info_overview,(0,0))
    report.paste(resizedImage, (info_overview.width, 0))

    reportsResultDirectory = os.path.join(sn.resultsPath, "Reports")
    if not os.path.isdir(reportsResultDirectory):
        os.mkdir(reportsResultDirectory)
    reportName = bimnode.name
    reportFileName = reportName + ".png"
    reportPath = os.path.join(reportsResultDirectory, reportFileName)

    report.save(reportPath)