from gitlab2pandas.core import Core
from gitlab2pandas.extractions import Extractions

class GitLab2Pandas(Core):

    def extract_data(self, extract_parallel:bool = False, feature_blacklist:list = [], feature_whitelist:list = [], update:bool = True) -> None:
        """    
        Extracts GitLab data based on the feature black- or whitelist
        Parallel extraction might fail for some GitLab Server because of server settings.

        Parameters
        ----------
        extract_parallel : bool, default=False
            Extracting the data parallel.
        feature_blacklist : list, default=[]
            Features which will be ignored.
        feature_whitelist : list, default=[]
            Features which will be extracted. If its empty then all features are extracted which are not in the blacklist.
        update: bool, default=True
            Extract only new items after last extration.
            
        """
        extractions = Extractions(self.data_root_dir, 
                                    project=self.project,
                                    extract_parallel=extract_parallel)
        extractions.start(feature_blacklist, feature_whitelist, update)