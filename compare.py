# compare.py

class Compare():
    def __init__(self, profile1, profile2):
        self.profile1 = profile1
        self.profile2 = profile2

    def compare_profiles(self):
        common_plugins = [] # or {}
        p1 = self.profile1
        p2 = self.profile2
        # if item in profile 1 matches item in profile 2, add it to the union list
            # if plugin format matches add format to list of common formats for that plugin
        # return dict or list for output report
        
    def output_common_plugins(self, report_output):
        self.compare_profiles()
        output_path = report_output
        # output common profile