# Copyright (c) 2017, Vienna University of Technology (TU Wien),
# Department of Geodesy and Geoinformation (GEO).
# All rights reserved.
#
# All information contained herein is, and remains the property of Vienna
# University of Technology (TU Wien), Department of Geodesy and Geoinformation
# (GEO). The intellectual and technical concepts contained herein are
# proprietary to Vienna University of Technology (TU Wien), Department of
# Geodesy and Geoinformation (GEO). Dissemination of this information or
# reproduction of this material is forbidden unless prior written permission
# is obtained from Vienna University of Technology (TU Wien), Department of
# Geodesy and Geoinformation (GEO).

import numpy.testing as nptest

from warp_dggs.dggv21 import DGGv21CPv20
from warp_dggs.dggv21 import DGGv21CPv20_ind_l
from warp_dggs.dggv21 import DGGv21CPv20_ind_ld

def test_warp5_DGGv21CPv20():

    dgg = DGGv21CPv20()
    assert dgg.activegpis.size == 3264391
    assert dgg.activegpis[514534] == 514534
    assert dgg.activearrcell[514534] == 1171
    nptest.assert_almost_equal(dgg.activearrlat[514534], 9.155969, 6)
    nptest.assert_almost_equal(dgg.activearrlon[514534], -15.239660, 6)


def test_warp5_DGGv21CPv20_ind_l():

    dgg_ind_l = DGGv21CPv20_ind_l()
    assert dgg_ind_l.activegpis.size == 1035365
    assert dgg_ind_l.activegpis[165388] == 558788
    assert dgg_ind_l.activearrcell[165388] == 1207
    nptest.assert_almost_equal(dgg_ind_l.activearrlat[165388], 9.947075, 6)
    nptest.assert_almost_equal(dgg_ind_l.activearrlon[165388], -14.704920, 6)


def test_warp5_DGGv21CPv20_ind_ld():

    dgg_ind_ld = DGGv21CPv20_ind_ld()
    assert dgg_ind_ld.activegpis.size == 839826
    assert dgg_ind_ld.activegpis[143041] == 621828
    assert dgg_ind_ld.activearrcell[143041] == 1208
    nptest.assert_almost_equal(dgg_ind_ld.activearrlat[143041], 11.077161, 6)
    nptest.assert_almost_equal(dgg_ind_ld.activearrlon[143041], -14.186455, 6)
