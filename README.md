# SciVisProject

## Volcano Dataset

### Explanation and Source
* http://www.viscontest.rwth-aachen.de/

### Information
* Airs Folder
    * The data set is given as vtkPolyData and stored in legacy, binary vtk format. It containes the following data attributes:
        * (x,y,z) coordinates - This information is analogous to MIPAS, i.e. the x and y coordinates contain longitude and latitude, respectively, while z defaults to 0.
        * time - The time stamp for each measurement is also given in the same time frame as the MIPAS data.
        * ash index - This scalar field indicates, per data point, the presence of ash particles at the respective sample location. Negative values indicate high concentration of ash. Positive values should be ignored.
        * SO2 index - Similarly to the ash index, this scalar field indicates the presence of SO2 in the atmosphere. However, in this field high positive numbers correspond to a high concentration of SO2.
* Support folder
    * Outline of Earths texture. Makes for a good background