
import human_id
import pandas as pd
from gitlab2pandas.core import Core

class Processing(Core):

    def name_parent_ids(self):
        """
        Rename all parent_id column names to a suitable id name.

        """
        self.name_parent_id("parent_id", "commit_id", self.Features.COMMITS_REFS)
        self.name_parent_id("parent_id", "commit_id", self.Features.COMMITS_DIFFS)

    def name_parent_id(self, old_column, new_column, filename):
        """
        Rename a column name for a pandas file.
        
        """
        df = self.get_pandas_data_frame(filename)
        if df is not None and not df.empty and old_column in df:
            if new_column in df:
                df[new_column] = df[[old_column,new_column]].sum(1)
                df.drop([old_column],1)
            else:
                df.rename(columns = {old_column:new_column}, inplace = True)
            self.save_as_pandas(filename,df)
    
    def replace_user_id(self):
        """
        Replace user_ids with a pseudonym geneerated by human-id.
        There might be some user_ids in commits that are not connected to a User.

        """
        users_df = self.get_pandas_data_frame(Core.Features.USERS)
        if users_df is None or users_df.empty:
            return
        uuids = []
        users = {}
        for index, row in users_df.iterrows():
            uuid = human_id.generate_id(seed=row["web_url"])
            uuids.append(uuid)
            users[row["id"]] = uuid
        users_df = users_df.assign(uuid=uuids)
        self.save_as_pandas(self.Features.USERS,users_df)
        for filename in self.Features.to_list():
            if filename != "Users":
                self.__try_replace_id_with_uuid(filename, users, "user_id")
                self.__try_replace_id_with_uuid(filename, users, "author_id")
                self.__try_replace_id_with_uuid(filename, users, "owner_id")
                self.__try_replace_id_with_uuid(filename, users, "assignee_id")
                self.__try_replace_id_with_uuid(filename, users, "closed_by_id")
                self.__try_replace_id_with_uuid(filename, users, "merge_user_id")
                self.__try_replace_id_with_uuid(filename, users, "resolved_by_id")
                self.__try_replace_list_id_with_uuid(filename, users, "assignees_ids")
                self.__try_replace_list_id_with_uuid(filename, users, "reviewers_ids")
    
    def __try_replace_id_with_uuid(self, filename, users, column):
        """
        Replaces all user_ids for a standard column in a pandas file with a human-id.
        
        """
        df = self.get_pandas_data_frame(filename)
        if df is None:
            return
        if column in df:
            for user_id, user_uuid in users.items():
                df.loc[df[column] == user_id, column] = user_uuid
        self.save_as_pandas(filename,df)
        
    def __try_replace_list_id_with_uuid(self, filename, users, column):
        """
        Replaces all user_ids for a list column in a pandas file with a human-id.
        
        """
        df = self.get_pandas_data_frame(filename)
        if df is None:
            return
        data_list = []
        if column in df:
            for index, row in df.iterrows():
                uuids = []
                for id in row[column]:
                    if id in users:
                        uuids.append(users[id])
                data = row
                data[column] = uuids
                data_list.append(data)
            self.save_as_pandas(filename,pd.DataFrame(data_list))

    