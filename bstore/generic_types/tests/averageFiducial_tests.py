# © All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE,
# Switzerland, Laboratory of Experimental Biophysics, 2016
# See the LICENSE.txt file for more details.

"""Unit tests for the testType generic dataset type.

Notes
-----
nosetests should be run in the B-Store parent directory.

"""
 
__author__ = 'Kyle M. Douglass'
__email__ = 'kyle.m.douglass@gmail.com'

from nose.tools                    import *

# Register the type
from bstore  import config
config.__Registered_Generics__.append('averageFiducial')

from bstore.generic_types.averageFiducial import averageFiducial
from bstore                        import database as db
from pathlib                       import Path
from os                            import remove
from os.path                       import exists

import pandas as pd
import h5py

testDataRoot = Path(config.__Path_To_Test_Data__)

def test_averageFiducial_Instantiation():
    """testType is properly instantiated.
    
    """
    # Make up some dataset IDs
    prefix      = 'test_prefix'
    acqID       = 1
    datasetType = 'generic'
    data        = 42
    
    averageFiducial(prefix, acqID, datasetType, data)

def test_averageFiducial_Put_Data():
    """averageFiducial can put its own data and datasetIDs.
    
    """
    try:
        # Make up some dataset IDs and a dataset
        prefix      = 'test_prefix'
        acqID       = 1
        datasetType = 'generic'
        data        = pd.DataFrame({'A' : [1,2], 'B' : [3,4]})
        ds = averageFiducial(prefix, acqID, datasetType, data)
        
        pathToDB = testDataRoot
        # Remove database if it exists
        if exists(str(pathToDB / Path('test_db.h5'))):
            remove(str(pathToDB / Path('test_db.h5')))
        
        myDB = db.HDFDatabase(pathToDB / Path('test_db.h5'))
        myDB.put(ds)
        
        key = 'test_prefix/test_prefix_1/averageFiducial'
        with h5py.File(str(pathToDB / Path('test_db.h5')), 'r') as hdf:
            assert_equal(hdf[key].attrs['SMLM_datasetType'], 'generic')
            assert_equal(hdf[key].attrs['SMLM_genericTypeName'],
                         'averageFiducial')
        
        df = pd.read_hdf(str(pathToDB / Path('test_db.h5')), key = key)
        assert_equal(df.loc[0, 'A'], 1)
        assert_equal(df.loc[1, 'A'], 2)
        assert_equal(df.loc[0, 'B'], 3)
        assert_equal(df.loc[1, 'B'], 4)
    finally:
        # Remove the test database
        remove(str(pathToDB / Path('test_db.h5')))
        
def test_averageFiducial_Get_Data():
    """averageFiducial can get its own data and datasetIDs.
    
    """
    try:
        # Make up some dataset IDs and a dataset
        prefix      = 'test_prefix'
        acqID       = 1
        datasetType = 'generic'
        data        = pd.DataFrame({'A' : [1,2], 'B' : [3,4]})
        ds = averageFiducial(prefix, acqID, datasetType, data)
        
        pathToDB = testDataRoot
        # Remove database if it exists
        if exists(str(pathToDB / Path('test_db.h5'))):
            remove(str(pathToDB / Path('test_db.h5')))
        
        myDB = db.HDFDatabase(pathToDB / Path('test_db.h5'))
        myDB.put(ds)
        
        # Create a new dataset containing only IDs to test getting of the data
        myNewDS = myDB.get(averageFiducial(prefix, acqID, datasetType, None))
        ids     = myNewDS.getInfoDict()
        assert_equal(ids['prefix'],              'test_prefix')
        assert_equal(ids['acqID'],                           1)
        assert_equal(ids['datasetType'],             'generic')
        assert_equal(ids['channelID'],                    None)
        assert_equal(ids['dateID'],                       None)
        assert_equal(ids['posID'],                        None)
        assert_equal(ids['sliceID'],                      None)
        assert_equal(ids['genericTypeName'], 'averageFiducial')   
        assert_equal(myNewDS.data.loc[0, 'A'], 1)
        assert_equal(myNewDS.data.loc[1, 'A'], 2)
        assert_equal(myNewDS.data.loc[0, 'B'], 3)
        assert_equal(myNewDS.data.loc[1, 'B'], 4)
    finally:
        # Remove the test database
        remove(str(pathToDB / Path('test_db.h5')))