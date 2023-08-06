# plotID for Python

This is the python plotID project.  
plotID is a program connected to Research Data Management (RDM). It has two main functionalities:
1. Tag your plot with an identifier.
2. Export the resulting file to a specified directory along the corresponding research data, the plot is based on. Additionally, the script that created the plot will also be copied to the directory.

**Note:** To run plotID python version &ge; 3.10 is required.

## Installation
Currently there are two options to run plotID. Either install it via pip from the Python Package Index (PyPi) or install plotID from the source code.

1. [Optional] Create a virtual environment and activate it:  
```bash
pip install venv
mkdir venv  
python3 -m venv venv

source venv/bin/activate  # Unix
```
```cmd
venv\Scripts\activate.bat # Windows Command Prompt
venv\Scripts\Activate.ps1 # Windows PowerShell
```

### From PyPi with pip
2. Install plotID  
`pip install plotid --extra-index-url=https://test.pypi.org/simple/`  
If you also want to run the unittests use `plotid[test]` instead of `plotid`.

### From source
2. Download the source code from [Gitlab](https://git.rwth-aachen.de/plotid/plotid_python):  
`git clone https://git.rwth-aachen.de/plotid/plotid_python.git`  
`cd plotid_python`  
3. Install dependencies  
`pip install -r requirements.txt`  
4. Install plotID  
`pip install .`  

## Usage
plotID has two main functionalities:
1. Tag your plot with an identifier.
2. Export the resulting file to a specified directory along the corresponding research data, the plot is based on. Additionally, the script that created the plot will also be copied to the directory.

### tagplot()
Tag your figure/plot with an ID. It is possible to tag multiple figures at once.  
`tagplot(figures, plot_engine)`  
The variable "figures" can be a single figure or a list of multiple figures.  
The argument "plot_engine" defines which plot engine was used to create the figures. It also determines which plot engine plotID uses to place the ID on the plot. Currently supported plot engines are:
- 'matplotlib', which processes figures created by matplotlib.
- 'image', which processes pictures with common extensions (jpg, png, etc.).

tagplot returns a PlotIDTransfer object that contains the tagged figures and the corresponding IDs as strings.

Optional parameters can be used to customize the tag process.
- prefix : str, optional
        Will be added as prefix to the ID.
- id_method : str, optional
        id_method for creating the ID. Create an ID by Unix time is referenced as 'time', create a random ID with id_method='random'. The default is 'time'.
- location : string, optional
        Location for ID to be displayed on the plot. Default is 'east'.
- qrcode : boolean, optional
        Experimental support for encoding the ID in a QR Code.

Example:  
```python
FIG1 = plt.figure()  
FIG2 = plt.figure()   
FIGS_AS_LIST = [FIG1, FIG2]  
FIGS_AND_IDS = tagplot(FIGS_AS_LIST, 'matplotlib', prefix='XY23_', id_method='random', location='west')
```


### publish()
Save plot, data and measuring script. It is possible to export multiple figures at once.
`publish(figs_and_ids, src_datapath, dst_path, plot_name)`  
  
- "figs_and_ids" must be a PlotIDTransfer object. Therefore, it can be directly passed from tagplot() to publish().  
- "src_datapath" specifies the path to (raw) data that should be published. It can be a string or a list of strings that specifies all files and directories which will be published.  
- "dst_path" is the path to the destination directory, where all the data should be copied/exported to.  
- "plot_names" will be the file names for the exported plots. If you give only one plot name but several figures, plotID will name the exported plots with an appended number, e.g. example_fig1.png, example_fig2.png, ...  

Optional parameters can be used to customize the publish process.
- data_storage: str, optional  
        Method how the data should be stored. Available options:  
  - centralized: The raw data will copied only once. All other plots will reference this data via sym link.
  - individual: The complete raw data will be copied to a folder for every plot, respectively.
Example:
`publish(figs_and_ids, '/home/user/Documents/research_data', '/home/user/Documents/exported_data', 'EnergyOverTime-Plot')`  

## Build
If you want to build plotID yourself, follow these steps:  
1. Download the source code from [Gitlab](https://git.rwth-aachen.de/plotid/plotid_python):  
`git clone https://git.rwth-aachen.de/plotid/plotid_python.git`  
`cd plotid_python`  
2. [Optional] Create a virtual environment (see Installation).  
3. [Optional] Run unittests and coverage:  
`python3 tests/runner_tests.py`
4. Build the package
`python3 -m build`


## Documentation
If you have more questions about plotID, please have a look at the [documentation](https://plotid.pages.rwth-aachen.de/plotid_python).  
Also have a look at the [examples](./examples) that are shipped with plotID.
