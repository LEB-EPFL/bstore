# © All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE,
# Switzerland, Laboratory of Experimental Biophysics, 2016
# See the LICENSE.txt file for more details.

import bstore.config
__version__ = bstore.config.__bstore_Version__

# Be sure not to use the from ... import syntax to avoid cyclical imports!
import bstore.database
import h5py
from numpy import array

class TestType(bstore.database.Dataset):
    """A class for testing B-Store Datasets.
    
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @property
    def attributeOf(self):
        """The other DatasetType that this DatasetType describes.
        
        If the DatasetType is an attribute of another type, return the name of
        this other DatasetType. An attribute means that it simply contains
        metadata and attributes that more fully describe another datasetType.
        If this DatasetType is not an attribute, return None.

        Returns
        -------
        None
        
        """
        return None  
   
    @property
    def datasetType(self):
        """This should be set to the same name as the class.
        
        """
        return 'TestType'
    
    def get(self, database, key, **kwargs):
        """Returns a testType dataset from the database.
        
        Parameters
        ----------
        database : str
            String containing the path to a B-Store HDF database.
        key      : str
            The HDF key pointing to the dataset locationin the HDF database.
        
        Returns
        -------
        data : NumPy array
            The data retrieved from the HDF file.
            
        """
        with h5py.File(database, 'r') as hdf:
            data = array(hdf.get(key))
            
        return data
    
    def put(self, database, key, **kwargs):
        """Puts the data into the database.
        
        Parameters
        ----------
        database : str
            String containing the path to a B-Store HDF database.
        key      : str
            The HDF key pointing to the dataset locationin the HDF database.
            
        """
        # Writes the data in the dataset to the HDF file.
        with h5py.File(database, 'a') as hdf:
            hdf.create_dataset(key, self.data.shape,
                               dtype = 'float64', data = self.data)
                               
    def readFromFile(self, **kwargs):
        """Required by the GenericDatasetType metaclass.
        
        """
        return None