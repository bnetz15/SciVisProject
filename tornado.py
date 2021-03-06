import vtk
from vtk.numpy_interface import algorithms as algs
import vtk.util.numpy_support as nps
import math
import random

class KeyboardInterface(object):
    def __init__(self, point1, point2, sphere1, sphere2, seeds, resolution, bounds):
        self.point1 = point1
        self.point2 = point2
        self.sphere1 = sphere1
        self.sphere2 = sphere2
        self.seeds = seeds
        self.resolution = resolution
        self.xmin = bounds[0]
        self.xmax = bounds[1]
        self.ymin = bounds[2]
        self.ymax = bounds[3]
        self.zmin = bounds[4]
        self.zmax = bounds[5]

    def check_bounds(self, point):
        if point[0] > self.xmax:
            point[0] = self.xmax
        elif point[0] < self.xmin:
            point[0] = self.xmin
        elif point[1] > self.ymax:
            point[1] = self.ymax
        elif point[1] < self.ymin:
            point[1] = self.ymin
        elif point[2] > self.zmax:
            point[2] = self.zmax
        elif point[2] < self.zmin:
            point[2] = self.zmin
        return point

    def keypress(self, obj, event):
        key = obj.GetKeySym().upper()

        point1_dir = {
            'Z': {'direction': [1, 0, 0], 'description': 'Positive in the X axis'},
            'X': {'direction': [-1, 0, 0], 'description': 'Negative in the X axis'},
            'C': {'direction': [0, 1, 0], 'description': 'Positive in the Y axis'},
            'V': {'direction': [0, -1, 0], 'description': 'Negative in the Y axis'},
            'B': {'direction': [0, 0, 1], 'description': 'Positive in the Z axis'},
            'N': {'direction': [0, 0, -1], 'description': 'Negative in the Z axis'},
        }

        point2_dir = {
            'M': {'direction': [1, 0, 0], 'description': 'Positive in the X axis'},
            'G': {'direction': [-1, 0, 0], 'description': 'Negative in the X axis'},
            'H': {'direction': [0, 1, 0], 'description': 'Positive in the Y axis'},
            'J': {'direction': [0, -1, 0], 'description': 'Negative in the Y axis'},
            'K': {'direction': [0, 0, 1], 'description': 'Positive in the Z axis'},
            'L': {'direction': [0, 0, -1], 'description': 'Negative in the Z axis'},
        }

        if key in point1_dir:
            self.point1 = [
                self.point1[i] + point1_dir[key]['direction'][i] for i in range(len(self.point1))]
            self.point1 = self.check_bounds(self.point1)
            self.sphere1.SetCenter(self.point1)
            self.seeds.SetPoint1(self.point1)
            streamline.Update()
            streamline.GetOutput().GetPointData().SetActiveScalars("Vorticity")
            render_window.Render()
        elif key in point2_dir:
            self.point2 = [
                self.point2[i] + point2_dir[key]['direction'][i] for i in range(len(self.point2))]
            self.point2 = self.check_bounds(self.point2)
            self.sphere2.SetCenter(self.point2)
            self.seeds.SetPoint2(self.point2)
            streamline.Update()
            streamline.GetOutput().GetPointData().SetActiveScalars("Vorticity")
            render_window.Render()
        elif key == 'UP':
            self.resolution += 1
            self.seeds.SetXResolution(self.resolution)
            # cap at 3 for that aesthetic
            if self.resolution > 3:
                self.seeds.SetYResolution(3)
            else:
                self.seeds.SetYResolution(math.ceil(self.resolution / 2))
            streamline.Update()
            streamline.GetOutput().GetPointData().SetActiveScalars("Vorticity")
            render_window.Render()
        elif key == 'DOWN':
            self.resolution -= 1
            if self.resolution <= 1:
                self.resolution = 1
            self.seeds.SetXResolution(self.resolution)
            if self.resolution > 3:
                self.seeds.SetYResolution(3)
            else:
                self.seeds.SetYResolution(math.ceil(self.resolution / 2))
            streamline.Update()
            streamline.GetOutput().GetPointData().SetActiveScalars("Vorticity")
            render_window.Render()
        elif key == "SPACE":
            self.point1 = (
                random.randint(int(self.xmin), int(self.xmax) + 1),
                random.randint(int(self.ymin), int(self.ymax) + 1),
                random.randint(int(self.zmin), int(self.zmax) + 1)
            )
            self.sphere1.SetCenter(self.point1)
            self.seeds.SetPoint1(self.point1)

            self.point2 = (
                random.randint(int(self.xmin), int(self.xmax) + 1),
                random.randint(int(self.ymin), int(self.ymax) + 1),
                random.randint(int(self.zmin), int(self.zmax) + 1)
            )
            self.sphere2.SetCenter(self.point2)
            self.seeds.SetPoint2(self.point2)
            render_window.Render()

def main():
    # read the data and
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName("tornado3d.vti")
    reader.Update()

    ds = reader.GetOutput()
    pd = ds.GetPointData()
    u = nps.vtk_to_numpy(pd.GetArray("u"))
    v = nps.vtk_to_numpy(pd.GetArray("v"))
    w = nps.vtk_to_numpy(pd.GetArray("w"))
    vectors = algs.make_vector(u, v, w)
    vtk_vectors = nps.numpy_to_vtk(num_array=vectors, deep=True, array_type=vtk.VTK_FLOAT)
    vtk_vectors.SetName("result")
    reader.GetOutput().GetPointData().SetScalars(vtk_vectors)
    reader.GetOutput().GetPointData().SetActiveVectors('result')

    # color map
    colors = vtk.vtkNamedColors()
    colorSeries = vtk.vtkColorSeries()
    colorSeries.SetColorScheme(vtk.vtkColorSeries.BREWER_SEQUENTIAL_YELLOW_ORANGE_BROWN_9)
    lut = vtk.vtkLookupTable()
    colorSeries.BuildLookupTable(lut, vtk.vtkColorSeries.ORDINAL)

    resolution = 4
    seeds = vtk.vtkPlaneSource()
    seeds.SetXResolution(resolution)
    seeds.SetYResolution(resolution // 2)

    xmin, xmax, ymin, ymax, zmin, zmax = reader.GetOutput().GetBounds()
    seedpoint1_location = [xmin, ymin, zmin]
    seedpoint2_location = [xmax, ymax, zmax]

    seeds.SetOrigin((xmax - xmin) / 2, (ymax - ymin) / 2, zmin)
    seeds.SetPoint1(seedpoint1_location)
    seeds.SetPoint2(seedpoint2_location)

    # Stream Tracer
    global streamline
    streamline = vtk.vtkStreamTracer()
    streamline.SetInputData(reader.GetOutput())
    streamline.SetSourceConnection(seeds.GetOutputPort())
    streamline.SetMaximumPropagation(500)
    streamline.SetIntegratorTypeToRungeKutta45()
    streamline.SetInitialIntegrationStep(.2)
    streamline.SetIntegrationDirectionToBoth()
    streamline.Update()

    streamline.GetOutput().GetPointData().SetActiveScalars("Vorticity")

    streamlineMapper = vtk.vtkPolyDataMapper()
    streamlineMapper.SetInputConnection(streamline.GetOutputPort())
    streamlineActor = vtk.vtkActor()
    streamlineActor.SetMapper(streamlineMapper)
    streamlineActor.GetProperty().SetLineWidth(1.0)
    streamlineActor.VisibilityOn()

    # tube filter
    tubeFilter = vtk.vtkTubeFilter()
    tubeFilter.SetInputConnection(streamline.GetOutputPort())
    tubeFilter.SetRadius(0.15)
    tubeFilter.SetNumberOfSides(50)
    tubeFilter.Update()

    tubeMapper = vtk.vtkPolyDataMapper()
    tubeMapper.SetLookupTable(lut)
    #tubeMapper.SetScalarRange(streamline.GetOutput().GetScalarRange())
    tubeMapper.SetScalarRange(0, 6)
    tubeMapper.SetInputConnection(tubeFilter.GetOutputPort())

    tubeActor = vtk.vtkActor()
    tubeActor.SetMapper(tubeMapper)

    # Draw seed points
    sphere1 = vtk.vtkSphereSource()
    sphere1.SetCenter(seedpoint1_location)
    sphere1.SetRadius(0.5)
    sphere1.SetPhiResolution(100)
    sphere1.SetThetaResolution(100)

    pointMapper1 = vtk.vtkPolyDataMapper()
    pointMapper1.SetInputConnection(sphere1.GetOutputPort())
    pointActor1 = vtk.vtkActor()
    pointActor1.SetMapper(pointMapper1)
    pointActor1.GetProperty().SetColor(colors.GetColor3d("Red"))

    sphere2 = vtk.vtkSphereSource()
    sphere2.SetCenter(seedpoint2_location)
    sphere2.SetRadius(0.5)
    sphere2.SetPhiResolution(100)
    sphere2.SetThetaResolution(100)

    pointMapper2 = vtk.vtkPolyDataMapper()
    pointMapper2.SetInputConnection(sphere2.GetOutputPort())
    pointActor2 = vtk.vtkActor()
    pointActor2.SetMapper(pointMapper2)
    pointActor2.GetProperty().SetColor(colors.GetColor3d("Blue"))

    # outline
    outline = vtk.vtkOutlineFilter()
    outline.SetInputData(reader.GetOutput())
    outline.Update()
    outlineMapper = vtk.vtkPolyDataMapper()
    outlineMapper.SetInputData(outline.GetOutput())
    outlineActor = vtk.vtkActor()
    outlineActor.SetMapper(outlineMapper)
    outlineActor.GetProperty().SetColor(0.8, 0.8, 0.8)
    outlineActor.GetProperty().SetLineWidth(3.0)

    # color bar
    scalar_bar = vtk.vtkScalarBarActor()
    scalar_bar.SetOrientationToHorizontal()
    scalar_bar.SetLookupTable(lut)
    scalar_bar.SetTitle("Vorticity")

    # Text
    txt = vtk.vtkTextActor()
    txt.SetInput(
        "Press UP arrow to increase streamlines\n"
        "Press DOWN arrow to decrease streamlines\n\n"
        "Press Z, X, C, V, B, N to modify the position of the red seed point\n"
        "Press M, G, H, J, K, L to modify the position of the blue seed point\n\n"
        "Press Space Bar for random seed positions"
    )
    txtprop = txt.GetTextProperty()
    txtprop.SetFontFamilyToArial()
    txtprop.SetFontSize(18)
    txtprop.SetColor(1, 1, 1)
    txt.SetDisplayPosition(10, 10)

    # Create a renderer and add the actors to it
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.2, 0.2, 0.2)

    # add actors
    renderer.AddActor(outlineActor)
    #renderer.AddActor(streamlineActor)
    renderer.AddActor(tubeActor)
    renderer.AddActor(pointActor1)
    renderer.AddActor(pointActor2)
    renderer.AddActor(txt)

    # Create a render window
    global render_window
    render_window = vtk.vtkRenderWindow()
    render_window.SetWindowName("Tornado")
    render_window.SetSize(1800, 1600)
    render_window.AddRenderer(renderer)

    # Create an interactor
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    # create the scalar_bar_widget
    scalar_bar_widget = vtk.vtkScalarBarWidget()
    scalar_bar_widget.SetInteractor(interactor)
    scalar_bar_widget.SetScalarBarActor(scalar_bar)
    scalar_bar_widget.On()

    # Create a window-to-image filter and a PNG writer that can be used
    # to take screenshots
    window2image_filter = vtk.vtkWindowToImageFilter()
    window2image_filter.SetInput(render_window)
    png_writer = vtk.vtkPNGWriter()
    png_writer.SetInputConnection(window2image_filter.GetOutputPort())

    # Set up the keyboard interface
    bounds = reader.GetOutput().GetBounds()
    keyboard_interface = KeyboardInterface(seedpoint1_location, seedpoint2_location, sphere1, sphere2, seeds, resolution, bounds)
    keyboard_interface.render_window = render_window
    keyboard_interface.window2image_filter = window2image_filter
    keyboard_interface.png_writer = png_writer

    # Connect the keyboard interface to the interactor
    interactor.AddObserver("KeyPressEvent", keyboard_interface.keypress)

    # Initialize the interactor and start the rendering loop
    interactor.Initialize()
    render_window.Render()
    interactor.Start()


if __name__ == '__main__':
    main()
