#  -*- coding: utf-8 -*-
# *****************************************************************************
# ufit, a universal scattering fitting suite
#
# Copyright (c) 2013-2022, Georg Brandl and contributors.  All rights reserved.
# Licensed under a 2-clause BSD license, see LICENSE.
# *****************************************************************************

"""Load routine for PSI ZEBRA data files."""

import io

from numpy import loadtxt, array, concatenate, zeros


def guess_cols(colnames, coldata, meta):
    if 'hkle_vary' in meta:
        xcol = {'h': 'H', 'k': 'K', 'l': 'L', 'E': 'NP'}[meta['hkle_vary']]
    else:
        xcol = colnames[1]
    return xcol, 'Counts', None, 'Monitor1'


def check_data(fp):
    line = fp.readline()
    fp.seek(0, 0)
    # on the first line is always name of the raw file
    return line.startswith(b'##SICS ASCII at ZEBRA')


def read_data(filename, fp):
    fp = io.TextIOWrapper(fp, 'ascii', 'ignore')

    meta = {}
    try:
        meta['filenumber'] = int(filename.split('n')[-1].split('.')[0])
    except Exception:
        meta['filenumber'] = 0
    meta['instrument'] = 'ZEBRA'
    remark = ''
    title = ''

    # parse headers
    lines = iter(fp)
    for line in lines:
        line = line.strip()
        if line == '#data':
            break
        if not line or line.startswith('#'):
            continue
        key, val = line.split('=', 1)
        key = key.strip()
        oval = val.strip()
        try:
            val = float(oval)
        except ValueError:
            val = oval
        if key == 'title':
            title = oval
        elif key == 'ProposalID':
            meta['experiment'] = oval
        elif key == 'sample':
            remark = oval
        elif key == 'comment':
            meta['subtitle'] = oval
        elif key == 'original_filename':
            if meta['filenumber'] == 0:
                try:
                    meta['filenumber'] = \
                        int(filename.split('n')[-1].split('.')[0])
                except Exception:
                    pass
        else:
            meta[key] = val

    if remark:
        title += ', ' + remark
    meta['title'] = title

    # parse data table
    next(lines)   # Scanning variables
    parts = next(lines).split()   # npoints, mease. mode
    meta['mode'] = parts[3].strip(',').lower()
    meta['preset'] = float(parts[5])
    colnames = next(lines).split()
    arr = loadtxt(lines, comments='E')  # E as in END-OF-DATA

    # if number of colnames is not correct, discard them
    if len(colnames) != arr.shape[1]:
        colnames = ['Column %d' % i for i in range(1, arr.shape[1]+1)]

    cols = dict((name, arr[:, i]) for (i, name) in enumerate(colnames))
    meta['environment'] = []
    if 'H' in colnames:
        npoints = arr.shape[0]
        hkle = concatenate([arr[:, (1, 2, 3)], zeros((npoints, 1))], axis=1)
        meta['hkle'] = hkle
        deviations = array([(cs.max()-cs.min()) for cs in meta['hkle'].T])
        meta['hkle_vary'] = ['h', 'k', 'l', 'E'][deviations.argmax()]
    for col in cols:
        meta[col] = cols[col].mean()
    if 'temp' in cols:
        if meta['temp'] > 0:
            meta['environment'].append('T = %.3f K' % meta['temp'])
    if 'mf' in cols:
        if meta['mf'] > 0:
            meta['environment'].append('B = %.3f T' % meta['mf'])

    return colnames, arr, meta
