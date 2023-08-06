
import os
import sys
from utils import log


class FirmwareBinPath(object):

    def __init__(self):
        self.linux_path = "/home/share/release/redtail"
        self.windows_path = r"\\172.29.190.4\share\release\redtail"
        self.auto_build_folder = "nightly"

    def get_default_base_path(self):
        if "win" in sys.platform.lower():
            base_path = self.windows_path
        else:
            base_path = self.linux_path
        return base_path

    def get_image_path(self, base_path, volume, commit_id, nand):
        commit_6bit = commit_id[0:6]
        nand = "ALL" if volume.lower() == "all" else nand
        _files = os.listdir(base_path)
        if os.path.exists(base_path):
            for item in _files:
                item_path = os.path.join(base_path, item)
                if os.path.isdir(item_path) and commit_6bit in item:
                    ret = self.get_image_path(item_path, volume, commit_id, nand)
                    if ret is not None:
                        return ret
                elif ("_{}_".format(volume) in item) and ("preBootloader" not in item) and \
                        item.endswith(".bin") and ("_{}_".format(nand) in item):
                    return os.path.join(base_path, item)

    def get_win_fw_path(self, parameters):
        volume = parameters.get("volume", "ALL")
        nand = parameters.get("nand", "BICS4")
        commit = parameters.get("commit", "")
        fw_path = parameters.get("fw_path", "")    # this is windows path format for perses
        if os.path.isfile(fw_path):
            win_fw_bin = fw_path
        else:
            win_fw_bin = self.get_image_path(fw_path, volume, commit, nand)
        log.INFO("Get windows path: {}".format(win_fw_bin))
        return win_fw_bin

    @staticmethod
    def change_path_win_2_linux(win_path):
        path_temp = win_path.replace("\\\\172.29.190.4", "/home")
        linux_path = path_temp.replace("\\", "/")
        log.INFO("Get linux path: {}".format(linux_path))
        return linux_path

    def get_default_base_path_enhance(self, parameters):
        if "base_path" in parameters.keys():  # for oakgate
            return parameters["base_path"]
        if "fw_path" in parameters.keys():   # for perses
            temp_path = parameters["fw_path"]
            if "172.29.190.4" in temp_path:
                if "win" in sys.platform.lower():
                    base_path = temp_path
                else:
                    base_path = self.change_path_win_2_linux(temp_path)
            else:
                base_path = temp_path
        else:
            base_path = self.get_default_base_path()
        log.INFO("Get base path: {}".format(base_path))
        return base_path

    def generate_oakgate_images(self, parameters):
        output_parm = dict()
        volume = parameters.get("volume", "ALL")
        nand = parameters.get("nand", "BICS4")
        base_path = self.get_default_base_path_enhance(parameters)
        if "image1" not in parameters.keys() and "base_version" in parameters.keys():
            ret = self.get_image_path(base_path, volume, parameters["base_version"], nand)
            if ret is not None:
                output_parm["image1"] = ret
                output_parm["base_version"] = parameters["base_version"]
        if "image2" not in parameters.keys():
            if "target_version" in parameters.keys():
                ret = self.get_image_path(base_path, volume, parameters["target_version"], nand)
                if ret is not None:
                    output_parm["image2"] = ret
                    output_parm["target_version"] = parameters["target_version"]
            else:
                if "image1" in output_parm.keys():
                    output_parm["image2"] = output_parm["image1"]
                    output_parm["target_version"] = output_parm["base_version"]
        return output_parm

    def update_perses_fw_path(self, parameters):
        if "fw_path" in parameters.keys():
            if os.path.exists(parameters["fw_path"]) is True and os.path.isfile(parameters["fw_path"]):
                return parameters  # when user send a bin file fw path skip update fw_path parameters
        if "commit" in parameters.keys():
            commit = parameters["commit"]
            volume = parameters.get("volume", "ALL")
            nand = parameters.get("nand", "BICS4")
            base_path = self.get_default_base_path_enhance(parameters)
            fw_path = self.get_image_path(base_path, volume, commit, nand)
            if fw_path is not None:
                parameters["fw_path"] = fw_path
        return parameters
