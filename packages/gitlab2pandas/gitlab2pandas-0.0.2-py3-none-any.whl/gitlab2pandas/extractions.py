from typing import Union
import json
import sys
import threading
import queue
import pandas as pd
from gitlab2pandas.core import Core
from gitlab.exceptions import GitlabAuthenticationError

class Extractions(Core):
    """
    Initializes extractions object with general information.
    Decide wheather to initialize with a project object or with the project namespace and name.
    Extractions can only be done with a project object or after connecting to a server with the project namespace and name.

    Parameters
    ----------
    data_root_dir : str
        A existing top level directory for data extraction.
    project : Project, default=None
        Project object from gitlab.
    project_namespace : str, default=None
        Namespace of the project.
    project_name : str, default=None
        Name of the project.
    extract_parallel: bool, default=False
        Parallel extraction might fail for some GitLab Server because of server settings.

    """

    EXTRACTIONS_WITHOUT_UPDATE = [
        Core.Features.BRANCHES,
        Core.Features.ISSUE_BOARDS,
        Core.Features.LABELS,
        Core.Features.MILESTONES,
        Core.Features.PROJECTS,
        Core.Features.RELEASES,
        Core.Features.SNIPPETS,
        Core.Features.USERS,
        Core.Features.WIKIS,
        Core.Features.TRIGGERS
    ]
    
    def __init__(self, data_root_dir: str, project=None, project_namespace=None, project_name=None, extract_parallel=False) -> None:
        """
        Initializes a Extractions object with general information.
        Decide wheather to initialize with a project object or with the project namespace and name.
        Extractions can only be started with a project object.
        ToDo: log_level=logging.INFO

        Parameters
        ----------
        data_root_dir : str
            A existing top level directory for data extraction.
        project : Project, default=None
            Project object from gitlab.
        project_namespace : str, default=None
           Namespace of the project.
        project_name : str, default=None
            Name of the project.
        extract_parallel: bool, default=False
            Parallel extraction might fail for some GitLab Server because of server settings.

        """
        super().__init__(data_root_dir, project, project_namespace, project_name)
        self.extract_parallel = extract_parallel
        self.data_queue = queue.Queue()
        self.consumer_thread = threading.Thread(target=self.__gitlab_data_consumer)
        self.log_queue = queue.Queue()
        self.log_serial_thread = threading.Thread(target=self.__log_serial_consumer)
        self.log_parallel_thread = threading.Thread(target=self.__log_parallel_consumer)
        self.use_feature_whitelist = None
        self.feature_list = []
        self.update_date = None

    def start(self, feature_blacklist:list = [], feature_whitelist:list = [], update:bool = True) -> None:
        """
        Starts a extraction with a blacklist or whitelist for features.
        The extraction can start from the last commit date or the entire project.

        Parameters
        ----------
        feature_blacklist : list, default=[]
            Features which will be ignored.
        feature_whitelist : list, default=[]
            Features which will be extracted. If its empty then all features are extracted which are not in the blacklist.
        update: bool, default=True
            Extract only new items after last extration.

        """
        if self.project is None:
            raise Exception("Need a connection (project object)")
        if self.consumer_thread.is_alive():
            raise Exception("Can not extract Data. There is already one extraction running")
        if feature_whitelist != []:
            self.use_feature_whitelist = True
            self.feature_list = feature_whitelist
            if feature_blacklist != []:
                print("Whitelist is used and Blacklist is ignored!")
        elif feature_blacklist != []:
            self.use_feature_whitelist = False
            self.feature_list = feature_blacklist
        else:
            self.use_feature_whitelist = None
        if update:
            # ToDo: Check projects atributes
            projects_df = self.get_pandas_data_frame(self.Features.PROJECTS)
            if projects_df is not None and not projects_df.empty:
                project_df = projects_df.loc[projects_df["path_with_namespace"] == self.project.attributes["path_with_namespace"]]
                if len(project_df) == 1:
                    self.update_date = project_df.iloc[0]["last_activity_at"]
                else:
                    print("there is redundant information in projects pandas file")
        self.consumer_thread.start()
        method_list = [method for method in dir(Extractions) if method.startswith('extract') is True]
        if self.extract_parallel:
            ### parallel ###
            self.log_parallel_thread.start()
            threads = []
            for method in method_list:
                threads.append(threading.Thread(target=getattr(self,method), args=()))
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
        else:
            ### sequential ### 
            self.log_serial_thread.start()
            for method in method_list:
                getattr(self,method)()
        self.data_queue.put((None,None))
        self.consumer_thread.join()
        self.use_feature_whitelist = None
        self.feature_list = []

    def pass_white_black_list(self, feature) -> bool:
        """
        Checks if a feature passes the white- and blacklist.

        Parameters
        ----------
        feature : str
            Feature to be checked.

        Returns
        -------
        bool
            True if the feature can be extracted.
            False if the feature should be ignored.

        """
        if self.use_feature_whitelist is None:
            return True
        elif self.use_feature_whitelist and feature in self.feature_list:
            return True
        elif not self.use_feature_whitelist and feature not in self.feature_list:
            return True
        return False

    def extract_branches(self) -> None:
        """
        Extracts branches from GitLab.
        Check for update does not work.

        """
        if not self.pass_white_black_list(Core.Features.BRANCHES):
            return
        self.__gitlab_data_producer(self.project, Core.Features.BRANCHES, ["branches", "list"])
        
    def extract_commits(self) -> None:
        """
        Extracts commits and its sub features from GitLab.
        Check for update works.
        
        """
        functions = ["commits", "list"]
        sub_functions = {}
        if self.pass_white_black_list(Core.Features.COMMITS_COMMENTS):
            sub_functions[Core.Features.COMMITS_COMMENTS] = ["comments", "list"]
        if self.pass_white_black_list(Core.Features.COMMITS_REFS):
            sub_functions[Core.Features.COMMITS_REFS] = ["refs"]
        if self.pass_white_black_list(Core.Features.COMMITS_DIFFS):
            sub_functions[Core.Features.COMMITS_DIFFS] = ["diff"]
        if self.pass_white_black_list(Core.Features.COMMITS_STATUSES):
            sub_functions[Core.Features.COMMITS_STATUSES] = ["statuses", "list"]
        if not self.pass_white_black_list(Core.Features.COMMITS):
            if not self.use_feature_whitelist:
                # If the feature is on the blacklist then ignore the feature and its subfeatures
                return
            if sub_functions == {}:
                # If the feature is not on the whitelist then ignore the feature only if no subfeature is on the whitelist
                return
        if sub_functions != {}:
            functions = {
                "attr": functions,
                "sub_functions": sub_functions
            }
        self.__gitlab_data_producer(self.project, Core.Features.COMMITS, functions)

    def extract_events(self) -> None:
        """
        Extracts events from GitLab.
        Check for update works.
        
        """
        if not self.pass_white_black_list(Core.Features.EVENTS):
            return
        self.__gitlab_data_producer(self.project, Core.Features.EVENTS, ["events", "list"])

    def extract_issues(self) -> None:
        """
        Extracts issues and its sub features from GitLab.
        Check for update works.
        
        """
        functions = ["issues", "list"]
        sub_functions = {}
        # ignored ["time_stats"] --> already in issue
        # ignored ["participants"] --> already in issue
        if self.pass_white_black_list(Core.Features.ISSUES_NOTES_AWARD_EMOJIS):
            if not self.use_feature_whitelist is False or Core.Features.ISSUES_NOTES not in self.feature_list:
                # If there is not a blacklist or notes are not on the blacklist then add notes award emojis.
                sub_functions[Core.Features.ISSUES_NOTES] = {
                    "attr": ["notes", "list"], 
                    "sub_functions": {Core.Features.ISSUES_NOTES_AWARD_EMOJIS: ["awardemojis", "list"]}
                }
        elif self.pass_white_black_list(Core.Features.ISSUES_NOTES):
            sub_functions[Core.Features.ISSUES_NOTES] = ["notes", "list"]
        if self.pass_white_black_list(Core.Features.ISSUES_AWARD_EMOJIS):
            sub_functions[Core.Features.ISSUES_AWARD_EMOJIS] = ["awardemojis", "list"]
        if self.pass_white_black_list(Core.Features.ISSUES_RESOURCESTATEEVENTS):
            sub_functions[Core.Features.ISSUES_RESOURCESTATEEVENTS] = ["resourcestateevents", "list"]
        if self.pass_white_black_list(Core.Features.ISSUES_RESOURCELABELEVENTS):
            sub_functions[Core.Features.ISSUES_RESOURCELABELEVENTS] = ["resourcelabelevents", "list"]
        if self.pass_white_black_list(Core.Features.ISSUES_CLOSED_BY_MR):
            sub_functions[Core.Features.ISSUES_CLOSED_BY_MR] = ["closed_by"]
        if self.pass_white_black_list(Core.Features.ISSUES_RELATED_MR):
            sub_functions[Core.Features.ISSUES_RELATED_MR] = ["related_merge_requests"]
        if self.pass_white_black_list(Core.Features.ISSUES_LINKS):
            sub_functions[Core.Features.ISSUES_LINKS] = ["links", "list"]
        if self.pass_white_black_list(Core.Features.ISSUES_RESOURCEMILESTONESEVENTS):
            sub_functions[Core.Features.ISSUES_RESOURCEMILESTONESEVENTS] = ["resourcemilestoneevents", "list"]
        if not self.pass_white_black_list(Core.Features.ISSUES):
            if not self.use_feature_whitelist:
                # If the feature is on the blacklist then ignore the feature and its subfeatures
                return
            if sub_functions == {}:
                # If the feature is not on the whitelist then ignore the feature only if no subfeature is on the whitelist
                return
        if sub_functions != {}:
            functions = {
                "attr": functions,
                "sub_functions": sub_functions
            }
        self.__gitlab_data_producer(self.project, Core.Features.ISSUES, functions)

    def extract_issue_boards(self) -> None:
        """
        Extracts issue boards from GitLab.
        Check for update does not work.

        """
        functions = ["boards", "list"]
        sub_functions = {}
        if self.pass_white_black_list(Core.Features.ISSUE_BOARDS_LISTS):
            sub_functions[Core.Features.ISSUE_BOARDS_LISTS] = ["lists", "list"]
        if not self.pass_white_black_list(Core.Features.ISSUE_BOARDS):
            if not self.use_feature_whitelist:
                # If the feature is on the blacklist then ignore the feature and its subfeatures
                return
            if sub_functions == {}:
                # If the feature is not on the whitelist then ignore the feature only if no subfeature is on the whitelist
                return
        if sub_functions != {}:
            functions = {
                "attr": functions,
                "sub_functions": sub_functions
            }
        self.__gitlab_data_producer(self.project, Core.Features.ISSUE_BOARDS, functions)

    def extract_labels(self) -> None:
        """
        Extracts labels from GitLab.
        Check for update does not work.

        """
        if not self.pass_white_black_list(Core.Features.LABELS):
            return
        self.__gitlab_data_producer(self.project, Core.Features.LABELS, ["labels", "list"])

    def extract_merge_requests(self) -> None:
        """
        Extracts merge requests and its sub features from GitLab.
        Check for update works.
        
        """
        functions = ["mergerequests", "list"]
        sub_functions = {}
        # ignore ["pipelines", "list"] --> pipelines can be matched via commit sha
        # ignored ["time_stats"] --> already in mr
        if self.pass_white_black_list(Core.Features.MERGE_REQUESTS_NOTES_AWARD_EMOJIS):
            if not self.use_feature_whitelist is False or Core.Features.MERGE_REQUESTS_NOTES not in self.feature_list:
                # If there is not a blacklist or notes are not on the blacklist then add notes award emojis.
                sub_functions[Core.Features.MERGE_REQUESTS_NOTES] = {
                    "attr": ["notes", "list"], 
                    "sub_functions": {Core.Features.MERGE_REQUESTS_NOTES_AWARD_EMOJIS: ["awardemojis", "list"]}
                }
        elif self.pass_white_black_list(Core.Features.MERGE_REQUESTS_NOTES):
            sub_functions[Core.Features.MERGE_REQUESTS_NOTES] = ["notes", "list"]
        if self.pass_white_black_list(Core.Features.MERGE_REQUESTS_AWARD_EMOJIS):
            sub_functions[Core.Features.MERGE_REQUESTS_AWARD_EMOJIS] = ["awardemojis", "list"]
        if self.pass_white_black_list(Core.Features.MERGE_REQUESTS_COMMITS):
            sub_functions[Core.Features.MERGE_REQUESTS_COMMITS] = ["commits"]
        if self.pass_white_black_list(Core.Features.MERGE_REQUESTS_CHANGES):
            sub_functions[Core.Features.MERGE_REQUESTS_CHANGES] = ["changes"]
        if self.pass_white_black_list(Core.Features.MERGE_REQUESTS_DIFFS):
            sub_functions[Core.Features.MERGE_REQUESTS_DIFFS] = ["diffs", "list"]
        if self.pass_white_black_list(Core.Features.MERGE_REQUESTS_RESOURCESTATEEVENTS):
            sub_functions[Core.Features.MERGE_REQUESTS_RESOURCESTATEEVENTS] = ["resourcestateevents", "list"]
        if self.pass_white_black_list(Core.Features.MERGE_REQUESTS_RESOURCELABELEVENTS):
            sub_functions[Core.Features.MERGE_REQUESTS_RESOURCELABELEVENTS] = ["resourcelabelevents", "list"]
        if self.pass_white_black_list(Core.Features.MERGE_REQUESTS_RESOURCEMILESTONESEVENTS):
            sub_functions[Core.Features.MERGE_REQUESTS_RESOURCEMILESTONESEVENTS] = ["resourcemilestoneevents", "list"]
        if not self.pass_white_black_list(Core.Features.MERGE_REQUESTS):
            if not self.use_feature_whitelist:
                # If the feature is on the blacklist then ignore the feature and its subfeatures
                return
            if sub_functions == {}:
                # If the feature is not on the whitelist then ignore the feature only if no subfeature is on the whitelist
                return
        if sub_functions != {}:
            functions = {
                "attr": functions,
                "sub_functions": sub_functions
            }
        self.__gitlab_data_producer(self.project, Core.Features.MERGE_REQUESTS, functions)
    
    def extract_milestones(self) -> None:
        """
        Extracts milestones from GitLab.
        Check for update does not work.

        """
        if not self.pass_white_black_list(Core.Features.MILESTONES):
            return
        # milestone.issues() --> in issues
        # milestone.merge_requests() --> in merge requests
        self.__gitlab_data_producer(self.project, Core.Features.MILESTONES, ["milestones", "list"]  )

    def extract_pipelines(self) -> None:
        """
        Extracts pipelines and its sub features from GitLab.
        Check for update works.
        If updated, then it will extract jobs, too.

        """
        functions = ["pipelines", "list"]
        sub_functions = {}
        if self.pass_white_black_list(Core.Features.PIPELINES_REPORT):
            sub_functions[Core.Features.PIPELINES_REPORT] = ["test_report", "get"]
        if self.pass_white_black_list(Core.Features.PIPELINES_BRIDGES):
            sub_functions[Core.Features.PIPELINES_BRIDGES] = ["bridges", "list"]
        if self.update_date is not None:
            sub_functions[Core.Features.JOBS] = ["jobs", "list"]
        if not self.pass_white_black_list(Core.Features.PIPELINES):
            if not self.use_feature_whitelist:
                # If the feature is on the blacklist then ignore the feature and its subfeatures
                return
            if sub_functions == {}:
                # If the feature is not on the whitelist then ignore the feature only if no subfeature is on the whitelist
                return
        if sub_functions != {}:
            functions = {
                "attr": functions,
                "sub_functions": sub_functions
            }
        self.__gitlab_data_producer(self.project, Core.Features.PIPELINES, functions)
    
    def extract_triggers(self) -> None:
        """
        Extracts triggers for pipelines from GitLab.
        Check for update does not work.

        """
        if not self.pass_white_black_list(Core.Features.TRIGGERS):
            return
        self.__gitlab_data_producer(self.project, Core.Features.TRIGGERS, ["triggers", "list"])

    def extract_pipeline_schedules(self) -> None:
        """
        Extracts pipeline schedules for pipelines from GitLab.
        Check for update does not work.

        """
        if not self.pass_white_black_list(Core.Features.PIPELINE_SCHEDULES):
            return
        self.__gitlab_data_producer(self.project, Core.Features.PIPELINE_SCHEDULES, ["pipelineschedules", "list"])

    def extract_jobs(self) -> None:
        """
        Extracts jobs from GitLab.
        Check for update works.
        If updated, then jobs will be extract in pipelines.
        
        """
        if self.update_date is not None:
            return
        if not self.pass_white_black_list(Core.Features.JOBS):
            return
        self.__gitlab_data_producer(self.project, Core.Features.JOBS, ["jobs", "list"])

    def extract_project(self) -> None:
        """
        Extracts general project information from GitLab.
        Check for update does not work.

        """
        def try_len(function, **kwargs):
            try:
                obj = function(**kwargs)
            except GitlabAuthenticationError:
                print(f"Token can not access {function}")
                return None
            else:
                return len(obj)

        if not self.pass_white_black_list(Core.Features.PROJECTS):
            return
        try:
            commits = self.project.commits.list(all=True)
            last_commit_date = commits[0].attributes["created_at"]
            commit_count = len(commits)
        except GitlabAuthenticationError:
            print(f"Token can not access self.project.commits.list")
            last_commit_date = None
            commit_count = None
        project_data = self.__get_gitlab_attributes(self.project.attributes)
        project_data.update({
            "contributor_count": try_len(self.project.repository_contributors,all=True),
            "member_count": try_len(self.project.members_all.list,all=True),
            "branch_count": try_len(self.project.branches.list,all=True),
            "commit_count": commit_count,
            "last_commit_date": last_commit_date,
            "labels_count": try_len(self.project.labels.list,all=True),
            "milestone_count": try_len(self.project.milestones.list,all=True),
            "merge_requests_count": try_len(self.project.mergerequests.list,all=True),
            "release_count":  try_len(self.project.releases.list,all=True),
            "issues_count": try_len(self.project.issues.list,all=True)
        })
        projects_df = self.get_pandas_data_frame(Core.Features.PROJECTS)
        if projects_df is None or projects_df.empty:
            self.save_as_pandas(Core.Features.PROJECTS,pd.DataFrame([project_data]))
            return
        projects_df = projects_df[projects_df.id != project_data['id']]
        projects_df = pd.concat([projects_df, pd.DataFrame([project_data])], ignore_index=True, sort=False)
        self.save_as_pandas(Core.Features.PROJECTS,projects_df)

    def extract_releases(self) -> None:
        """
        Extracts releases from GitLab.
        Check for update does not work.

        """
        if not self.pass_white_black_list(Core.Features.RELEASES):
            return
        self.__gitlab_data_producer(self.project, Core.Features.RELEASES, ["releases", "list"])
        
    def extract_snippets(self) -> None:
        """
        Extracts snippets from GitLab.
        Check for update does not work.

        """
        if not self.pass_white_black_list(Core.Features.SNIPPETS):
            return
        self.__gitlab_data_producer(self.project, Core.Features.SNIPPETS, ["snippets", "list"])

    def extract_users(self) -> None:
        """
        Extracts users from GitLab.
        Check for update does not work.

        """
        if not self.pass_white_black_list(Core.Features.USERS):
            return
        self.__gitlab_data_producer(self.project, Core.Features.USERS, ["users", "list"])

    def extract_wikis(self) -> None:
        """
        Extracts wiki pages from GitLab.
        Check for update does not work.

        """
        if not self.pass_white_black_list(Core.Features.WIKIS):
            return
        self.__gitlab_data_producer(self.project, Core.Features.WIKIS, ["wikis", "list"])
 
    def __log_serial_consumer(self) -> None:
        """
        Method for a consumer thread to log the serial process of extracting data.

        """
        totals = {}
        counts = {}
        size = 60
        max_text_length = 30
        while self.consumer_thread.is_alive() or not self.log_queue.empty():
            if not self.log_queue.empty():
                feature, total = self.log_queue.get()
                if feature not in totals:
                    if totals != {}:
                        sys.stdout.write("\n")
                    totals[feature] = total
                    counts[feature] = 0
                else:
                    counts[feature] += 1
                x = int(size*counts[feature]/total)
                sys.stdout.flush()
                text = f" extracting {feature}:"
                while len(text) < max_text_length:
                    text += " "
                sys.stdout.write("%s[%s%s] %i/%i\r" % (text, "#"*x, "."*(size-x), counts[feature], total))
        sys.stdout.write("\n")
        sys.stdout.flush()
    
    def __log_parallel_consumer(self) -> None:
        """
        Method for a consumer thread to log the parallel process of extracting data.

        """
        features = []
        sum = 0
        count = 0
        size = 60
        while self.consumer_thread.is_alive() or not self.log_queue.empty():
            if not self.log_queue.empty():
                feature, total = self.log_queue.get()
                if feature not in features:
                    features.append(feature)
                    sum += total
                else:
                    count += 1
                x = int(size*count/sum)
                sys.stdout.flush()
                sys.stdout.write("%s[%s%s] %i/%i\r" % (f" extracting parallel:         ", "#"*x, "."*(size-x), count, sum))
        sys.stdout.write("\n")
        sys.stdout.flush()

    def __gitlab_data_consumer(self) -> None:
        """
        Method for a consumer thread to collect the extracted data.
        After everything is extracted the data will be saved to pandas files.

        """
        buffer = {}
        while True:
            if not self.data_queue.empty():
                feature_name, gitlab_data = self.data_queue.get()
                if feature_name is None:
                    break
                if feature_name in buffer:
                    buffer[feature_name].append(gitlab_data)
                else:
                    buffer[feature_name] = [gitlab_data]
        # updated on and after the last day of modification
        if self.update_date is None:
            for key, value in buffer.items():
                self.save_as_pandas(key,pd.DataFrame(value))  
        else:
            # ToDo: Check if there are redudant information
            for key, value in buffer.items():
                if key == self.Features.BRANCHES or key == self.Features.ISSUE_BOARDS or key == self.Features.ISSUE_BOARDS_LISTS or key == self.Features.LABELS or key == self.Features.USERS:
                    self.save_as_pandas(key,pd.DataFrame(value))
                else:
                    feature_df = self.get_pandas_data_frame(key)
                    new_df = pd.concat([feature_df,pd.DataFrame(value)], ignore_index=True, sort=False)
                    if "iid" in new_df:
                        new_df = new_df.drop_duplicates(subset=['iid'])
                    elif "id" in new_df:
                        new_df = new_df.drop_duplicates(subset=['id'])
                    else:
                        print(f"Ids not found in {key}. Might not drop duplicates")
                        new_df = new_df.drop_duplicates()
                    self.save_as_pandas(key,new_df)

    def __gitlab_data_producer(self, gitlab_obj, feature_name:str, value, is_sub_function:bool = False) -> None:
        """
        Method for a producer thread to extract data from GitLab.
        It can run mutiple producer loops in order to extract subfeatures
        After extracting the data is placed in a queue.

        Parameters
        ----------
        gitlab_obj : Any
            A GitLab object which can acquire information. 
            Top level object is the GitLab project object.
        feature_name : str
            The name of the feature which will be extracted.
        value : Any
            The value as dict defines if the feature has subfeatures to extract.
            The value as list defines a list of methods for the feature in order to extract data.
        is_sub_function : bool
            States if this feature is a subfeature and called by main feature.

        """
        if feature_name == Core.Features.ISSUES_CLOSED_BY_MR:
            x = 0
        obj = gitlab_obj
        has_sub_functions = False
        if isinstance(value, dict):
            attrs = value["attr"]
            has_sub_functions = True
        else:
            attrs = value
        for attr in attrs:
            obj = getattr(obj, attr)
        try:
            if self.update_date is None:
                gitlab_data_list = obj(all=True)
            else:
                gitlab_data_list = obj(all=True, since=self.update_date, updated_after=self.update_date, after=self.update_date)
        except GitlabAuthenticationError:
            print(f"Token can not access {feature_name}!")
            return

        threads = []
        if isinstance(gitlab_data_list, dict) or hasattr(gitlab_data_list, "attributes"):
            self.__producer_loop(gitlab_data_list, gitlab_obj, feature_name, value, has_sub_functions)
        else:
            if not is_sub_function and len(gitlab_data_list) > 0:
                self.log_queue.put((feature_name,len(gitlab_data_list)))
            for gitlab_data in gitlab_data_list:
                if has_sub_functions and self.extract_parallel:
                        loop_thread = threading.Thread(target=self.__producer_loop, args=(gitlab_data, gitlab_obj, feature_name, value, has_sub_functions,))
                        loop_thread.start()
                        threads.append(loop_thread)
                else:
                    self.__producer_loop(gitlab_data, gitlab_obj, feature_name, value, has_sub_functions)
                if not is_sub_function:
                    self.log_queue.put((feature_name,len(gitlab_data_list)))
        for thread in threads:
            thread.join()
    
    def __producer_loop(self, gitlab_data, gitlab_obj, feature_name:str, value, has_sub_functions:bool) -> None:
        """
        Method for a thread to start a new data producer or to extact the data from the attributes.

        Parameters
        ----------
        gitlab_data : Any
            Includes the extracted data of the gitlab object.
        gitlab_obj : Any
            A GitLab object which can acquire information. 
            Top level object is the GitLab project object.
        feature_name : str
            The name of the feature which will be extracted.
        value : Any
            The value as dict defines if the feature has subfeatures to extract.
            The value as list defines a list of methods for the feature in order to extract data.
        has_sub_function : bool
            States if this feature has a subfeature and need to be called by current feature.
            
        """
        if feature_name == Core.Features.ISSUES_CLOSED_BY_MR or feature_name == Core.Features.ISSUES_RELATED_MR:
            data = {}
            data["issue_iid"] = gitlab_obj.attributes["iid"]
            data["mr_iid"] = gitlab_data["iid"]
            data["project_id"] = gitlab_data["project_id"]
            self.data_queue.put((feature_name,data))
            return
        if feature_name == Core.Features.MERGE_REQUESTS_COMMITS:
            data = {}
            data["mr_iid"] = gitlab_obj.attributes["iid"]
            data["commit_id"] = gitlab_data.attributes["id"]
            data["project_id"] = gitlab_data.attributes["project_id"]
            self.data_queue.put((feature_name,data))
            return
        if isinstance(gitlab_data, dict):
            if "iid" in gitlab_obj.attributes:
                self.__get_gitlab_attributes(gitlab_data, feature_name, gitlab_obj.attributes["iid"])
            elif "id" in gitlab_obj.attributes:
                self.__get_gitlab_attributes(gitlab_data, feature_name, gitlab_obj.attributes["id"])
        else:
            parent_id = None
            if feature_name == Core.Features.MERGE_REQUESTS_COMMITS:
                parent_id = gitlab_obj.attributes["iid"]
            ## ad mr changes
            self.__get_gitlab_attributes(gitlab_data.attributes, feature_name, parent_id)
            if has_sub_functions:
                for feature_name2, value2 in value["sub_functions"].items():
                    self.__gitlab_data_producer(gitlab_data,feature_name2,value2,True)

    def __get_gitlab_attributes(self, gitlab_data, feature_name:str = None, parent_id = None) -> Union[dict,None]:
        """
        Extract the data from a GitLab feature object and apply special information.

        Parameters
        ----------
        gitlab_data : Any
            Includes the extracted data of the gitlab object
        feature_name : str, default=None
            The name of the feature which will be extracted. 
            Only if the feature is defined then it will place the data in the data_queue or otherwise it will return the data.
        parent_id : Any, default=None
            If the festure has a parent then the parent_id will be added to the data.
            
        Returns
        -------
        dict
            The extracted data will be returned because no feature is defined.
        None
            The extracted data will be passed in the data_queue because a feature is defined.

        """
        data = {}
        if parent_id is not None:
            if "MRs" in feature_name:
                data["mr_iid"] = parent_id
            else:
                data["parent_id"] = parent_id
        for key, value in gitlab_data.items():
            if isinstance(value, dict):
                if key == "commit" and "id" in value:
                    data["commit_id"] = value["id"]
                elif key == "author" and "id" in value:
                    data["author_id"] = value["id"]
                elif key == "user" and "id" in value:
                    data["user_id"] = value["id"]
                elif key == "owner" and "id" in value:
                    data["owner_id"] = value["id"]
                elif key == "assignee" and "id" in value:
                    data["assignee_id"] = value["id"]
                elif key == "closed_by" and "id" in value:
                    data["closed_by_id"] = value["id"]
                elif key == "merged_by" and "id" in value:
                    # deprecated --> merge_user
                    pass
                elif key == "merge_user" and "id" in value:
                    data["merge_user_id"] = value["id"]
                elif key == "resolved_by" and "id" in value:
                    data["resolved_by_id"] = value["id"]
                elif key == "milestone" and "id" in value:
                    data["milestone_id"] = value["id"]
                elif key == "label" and "id" in value:
                    data["label_id"] = value["id"]
                elif key == "pipeline" and "id" in value:
                    data["pipeline_id"] = value["id"]
                elif key == "namespace":
                    for key2, value2 in value.items():
                        data[f"{key}_{key2}"] = value2
                else:
                    data[key] = json.dumps(value)
            elif isinstance(value, list):
                if key == "labels":
                    data[key] = value
                elif key == "assignees":
                    data["assignees_ids"] = []
                    for assignee in value:
                        data["assignees_ids"].append(assignee["id"])
                elif key == "reviewers":
                    data["reviewers_ids"] = []
                    for reviewer in value:
                        data["reviewers_ids"].append(reviewer["id"])
                elif key == "parent_ids":
                    data["parent_ids"] = []
                    for parent_id in value:
                        data["parent_ids"].append(parent_id)
                elif key == "tag_list":
                    # deprecated --> topics
                    pass
                elif key == "topics":
                    data["topics"] = []
                    for topic in value:
                        data["topics"].append(topic)
                else:
                    data[key] = json.dumps(value)
            else:
                data[key] = value
        if feature_name is None:
            return data
        self.data_queue.put((feature_name,data))

