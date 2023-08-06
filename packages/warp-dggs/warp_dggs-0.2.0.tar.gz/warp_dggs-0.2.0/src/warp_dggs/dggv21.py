# Copyright (c) 2017, Vienna University of Technology (TU Wien), Department
# of Geodesy and Geoinformation (GEO).
# All rights reserved.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL VIENNA UNIVERSITY OF TECHNOLOGY,
# DEPARTMENT OF GEODESY AND GEOINFORMATION BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os

import pygeogrids.netcdf as ncgrids

def get_grid_definition_filename():
    grid_info_path = os.path.join(os.path.dirname(__file__), 'definition_files')
    return os.path.join(grid_info_path, 'DGGv02.1_CPv02.nc')


def DGGv21CPv20(gridfilename=None):
    """
    All relevant information of DGG version 02.1 with cell partitioning
    (CP) version 02

    Parameters
    ----------
    gridfilename : string, optional
        Path to the grid file.

    Returns
    -------
    grid : CellGrid instance
        grid instance initialized with the loaded data
    """

    if gridfilename is None:
        gridfilename = get_grid_definition_filename()

    return ncgrids.load_grid(filename=gridfilename)


def DGGv21CPv20_ind_l(gridfilename=None):
    """
    Subset of DGG version 02.1 CP version 02 containing points on land and
    within a buffer zone (~50km) around the coast.

    Parameters
    ----------
    gridfilename : string, optional
        Path to the grid file.

    Returns
    -------
    grid : CellGrid instance
        grid instance initialized with the loaded data
    """

    if gridfilename is None:
        gridfilename = get_grid_definition_filename()

    return ncgrids.load_grid(filename=gridfilename, subset_flag='ind_l')


def DGGv21CPv20_ind_ld(gridfilename=None):
    """
    Subset of DGG version 02.1 CP version 02 containing only land points.

    Parameters
    ----------
    gridfilename : string, optional
        Path to the grid file.

    Returns
    -------
    grid : CellGrid instance
        grid instance initialized with the loaded data
    """

    if gridfilename is None:
        gridfilename = get_grid_definition_filename()

    return ncgrids.load_grid(filename=gridfilename, subset_flag='ind_ld')
