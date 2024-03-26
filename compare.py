# compare.py

class Compare():
    def __init__(self, profile1, profile2):
        self.profile1 = profile1
        self.profile2 = profile2

    def compare_profiles(self):
        common_plugins = {}
        not_shared_plugins = {}
        p1 = self.profile1
        p2 = self.profile2

        for plugin, formats in p1.items():
            if plugin in p2:
                common_formats = set(formats) & set(p2[plugin])
                if common_formats:
                    common_plugins[plugin] = list(common_formats)
                not_shared_formats = set(formats) - set(p2[plugin])
                if not_shared_formats:
                    not_shared_plugins[plugin] = list(not_shared_formats)
            else:
                not_shared_plugins[plugin] = formats

        for plugin, formats in p2.items():
            if plugin not in p1:
                not_shared_plugins[plugin] = formats

        return common_plugins, not_shared_plugins

    def output_common_plugins(self, report_output, user1_name, user2_name):
        common_plugins, not_shared_plugins = self.compare_profiles()
        output_path = report_output

        with open(output_path, "w") as file:
            file.write(f"{user1_name} and {user2_name} common plugins profile\n\n")
            file.write("Plugins shared:\n")
            for plugin, formats in common_plugins.items():
                file.write(f"{plugin}: {', '.join(formats)}\n")

            file.write("\nPlugins not shared:\n")
            for plugin, formats in not_shared_plugins.items():
                file.write(f"{plugin}: {', '.join(formats)}\n")