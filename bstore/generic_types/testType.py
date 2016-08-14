# © All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE,
# Switzerland, Laboratory of Experimental Biophysics, 2016
# See the LICENSE.txt file for more details.

from bstore import database as db
import h5py

class testType(db.Dataset, db.GenericDatasetType):
    """A class for testing B-Store generic datasetTypes.
    
    """
    def __init__(self, prefix, acqID, datasetType, data,
                 channelID = None, dateID = None,
                 posID = None, sliceID = None):
        super(testType, self).__init__(prefix, acqID, datasetType, data,
                                       channelID = channelID,
                                       dateID    = dateID,
                                       posID     = posID,
                                       sliceID   = sliceID)
    
    @property
    def genericTypeName(self):
        """This should be set to the same name as the class.
        
        """
        return 'testType'
    
    def get(self, database, key):
        """Returns a testType dataset from the database.
        
        Parameters
        ----------
        database : str
            String containing the path to a B-Store HDF database.
        key      : str
            The HDF key pointing to the dataset locationin the HDF database.
        
        """
        pass
    
    def put(self, database, key):
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
                               dtype = 'i', data = self.data)