import os

from PySide2.QtCore import QSize, qDebug
from PySide2.QtGui import QOpenGLFramebufferObject, QOpenGLFramebufferObjectFormat, QOpenGLFunctions
from PySide2.QtQuick import QQuickFramebufferObject

import vtk
from vtk.util.colors import tomato

from example import constants as const


class QmlVTKOpenGLRenderWindowInteractor(QQuickFramebufferObject.Renderer):
    def __init__(self):
        super(QmlVTKOpenGLRenderWindowInteractor, self).__init__()

        self._glFunc = QOpenGLFunctions()

        self._RenderWindow = vtk.vtkGenericOpenGLRenderWindow()
        self._Iren = vtk.vtkGenericRenderWindowInteractor()
        self._ren = vtk.vtkRenderer()
        self._RenderWindow.AddRenderer(self._ren)
        self._Iren.SetRenderWindow(self._RenderWindow)
        self._RenderWindow.OpenGLInitContext()

    def createFramebufferObject(self, size:QSize) -> QOpenGLFramebufferObject:
        print("createFramebufferobj")
        gl_format = QOpenGLFramebufferObjectFormat()
        gl_format.setAttachment(QOpenGLFramebufferObject.Depth)
        frame_buffer_object = QOpenGLFramebufferObject(size, gl_format)
        self.__fbo = frame_buffer_object
        return self.__fbo

    def synchronize(self, item:QQuickFramebufferObject):
        print("synchronize")
        pass

    def render(self):
        self.openGLInitState()

        # cylinderActor = self.__get_polydata_actor()
        # self._ren.AddActor(cylinderActor)
        # self._ren.SetBackground(0.1, 0.2, 0.4)
        ironPortVolume = self.__get_volumedata_actor()
        self._ren.AddVolume(ironPortVolume)
        self._ren.SetBackground(1, 1, 1)
        self._RenderWindow.SetSize(150, 150)

        self._Iren.Initialize()
        self._ren.ResetCamera()
        self._ren.GetActiveCamera().Zoom(1.5)
        self._RenderWindow.Render()
        print("Start rendering")
        self._Iren.Start()

    def __get_polydata_actor(self):
        cylinder = vtk.vtkCylinderSource()
        cylinder.SetResolution(8)
        cylinderMapper = vtk.vtkPolyDataMapper()
        cylinderMapper.SetInputConnection(cylinder.GetOutputPort())
        cylinderActor = vtk.vtkActor()
        cylinderActor.SetMapper(cylinderMapper)
        cylinderActor.GetProperty().SetColor(tomato)
        cylinderActor.RotateX(30.0)
        cylinderActor.RotateY(-45.0)
        return cylinderActor

    def __get_volumedata_actor(self):
        # Create the reader for the data
        reader = vtk.vtkStructuredPointsReader()
        file_path = os.path.join(const.RC_FILE_DIR, "ironProt.vtk")
        reader.SetFileName(file_path)

        # Create transfer mapping scalar value to opacity
        opacityTransferFunction = vtk.vtkPiecewiseFunction()
        opacityTransferFunction.AddPoint(20, 0.0)
        opacityTransferFunction.AddPoint(255, 0.2)

        # Create transfer mapping scalar value to color
        colorTransferFunction = vtk.vtkColorTransferFunction()
        colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
        colorTransferFunction.AddRGBPoint(64.0, 1.0, 0.0, 0.0)
        colorTransferFunction.AddRGBPoint(128.0, 0.0, 0.0, 1.0)
        colorTransferFunction.AddRGBPoint(192.0, 0.0, 1.0, 0.0)
        colorTransferFunction.AddRGBPoint(255.0, 0.0, 0.2, 0.0)

        # The property describes how the data will look
        volumeProperty = vtk.vtkVolumeProperty()
        volumeProperty.SetColor(colorTransferFunction)
        volumeProperty.SetScalarOpacity(opacityTransferFunction)
        volumeProperty.ShadeOn()
        volumeProperty.SetInterpolationTypeToLinear()

        # The mapper / ray cast function know how to render the data
        volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
        # volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
        volumeMapper.SetBlendModeToComposite()
        volumeMapper.SetInputConnection(reader.GetOutputPort())

        # The volume holds the mapper and the property and
        # can be used to position/orient the volume
        volume = vtk.vtkVolume()
        volume.SetMapper(volumeMapper)
        volume.SetProperty(volumeProperty)
        return volume

    def openGLInitState(self):
        self._RenderWindow.OpenGLInitState()
        self._RenderWindow.MakeCurrent()
        self._glFunc.initializeOpenGLFunctions()
        self._glFunc.glUseProgram(0)
