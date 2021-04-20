# SciVisProject

## Volcano Dataset

### Explanation and Source
* http://www.viscontest.rwth-aachen.de/

### Information
* Airs Folder
    * The data set is given as vtkPolyData and stored in legacy, binary vtk format. It containes the following data attributes:
        * (x,y,z) coordinates - This information is analogous to MIPAS, i.e. the x and y coordinates contain longitude and latitude, respectively, while z defaults to 0.
        * time - The time stamp for each measurement is also given in the same time frame as the MIPAS data. Data ranges from June to August 2011.
        * ash index - This scalar field indicates, per data point, the presence of ash particles at the respective sample location. Negative values indicate high concentration of ash. Positive values should be ignored.
        * SO2 index - Similarly to the ash index, this scalar field indicates the presence of SO2 in the atmosphere. However, in this field high positive numbers correspond to a high concentration of SO2.
* Support folder
    * Outline of Earths texture. Makes for a good background

### Experiments
* At low and mid latitudes there are small data gaps between successive tracks for which no AIRS data are available. This can explain the missing bands
* First Eruption
    * On June 4, 2011, a fissure opened in Chile’s Puyehue-Cordón Caulle Volcanic Complex, sending ash 45,000 feet (14,000 meters) into the air. As of the afternoon of June 6, the eruption had started to diminish in intensity, said SERNOGEOMIN, Chile’s geology and mineral agency.
    * Note detections over northern Africa are not from volcanic origin, but relate to dust clouds over the Sahara desert.
    * volcano_2011_000.vtk => June 1, 2011 AM
    * volcano_2011_001.vtk => June 1, 2011 PM
    * volcano_2011_002.vtk => June 2, 2011 AM
    * volcano_2011_003.vtk => June 2, 2011 PM
    * etc...
    * Ash can first visibly be seen on volcano_2011_012.vtk. Doesn't completely dissipate until volcano_2011_048.vtk.
