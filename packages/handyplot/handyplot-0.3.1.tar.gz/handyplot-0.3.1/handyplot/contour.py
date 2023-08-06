import vtkmodules.all as vtk


class VtkWindow:
    def __init__(self):
        self._render_window = vtk.vtkRenderWindow()
        self._render_window.SetSize(800, 800)

        self._interactor = vtk.vtkRenderWindowInteractor()
        self._interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        self._interactor.SetRenderWindow(self._render_window)

        self._renderer = vtk.vtkRenderer()
        self._renderer.SetBackground((1, 1, 1))
        self._render_window.AddRenderer(self._renderer)


class Contour(VtkWindow):
    def __init__(self):
        """
        :param mesh:
        """
        VtkWindow.__init__(self)

        self._scalar_bar_actor = vtk.vtkScalarBarActor()
        self._scalar_bar_actor.UnconstrainedFontSizeOn()
        self._scalar_bar_actor.GetLabelTextProperty().SetColor(0, 0, 0)
        self._scalar_bar_actor.GetLabelTextProperty().SetColor(124 / 255, 124 / 255, 124 / 255)
        self._scalar_bar_actor.GetLabelTextProperty().SetFontSize(13)
        self._scalar_bar_actor.GetLabelTextProperty().SetBold(False)
        self._scalar_bar_actor.GetLabelTextProperty().SetShadow(False)
        self._scalar_bar_actor.SetTitle("")
        self._scalar_bar_actor.SetWidth(0.05)
        self._scalar_bar_actor.SetHeight(0.6)
        self._scalar_bar_actor.SetNumberOfLabels(8)
        self._scalar_bar_actor.SetOrientationToVertical()
        self._scalar_bar_actor.GetPositionCoordinate().SetValue(0.9, 0.2)

    def show_vtk_file(self, filename):
        """

        :param filename: Should add vtk.
        :return:
        """
        reader = vtk.vtkUnstructuredGridReader()
        reader.SetFileName(filename)
        reader.Update()

        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        mapper.SetScalarRange(2000, 4000)

        contour_actor = vtk.vtkActor()
        contour_actor.SetMapper(mapper)
        self._renderer.AddActor(contour_actor)

        self._scalar_bar_actor.SetLookupTable(mapper.GetLookupTable())
        self._renderer.AddActor(self._scalar_bar_actor)

        # Show.
        self._interactor.Start()


if __name__ == "__main__":
    contour = Contour()
    contour.show_vtk_file("test_resource/theis_contour.vtk")
