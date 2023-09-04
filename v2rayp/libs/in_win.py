import os
import platform

# Define the local filename to save data
import requests

if os.name == "nt":
    import winsound


class pass_by_ref:
    value = None


class temp:
    def update(self, a):
        pass


class FactorySetting:
    @staticmethod
    def check_file_or_folder_exists(path):
        return os.path.exists(path)

    @staticmethod
    def delete_config_folder():
        path = f"{config_path()}"
        cmd = f"rmdir /s /q {path}"
        if not inside_windows():
            path = path.replace("\\", "/")
            cmd = f"rm -rf {path}"
        os.popen(cmd).read()

    @staticmethod
    def make_config_folder_ready(folder_path):
        ################################temporary remove all subscriptions

        if not inside_windows():
            folder_path = folder_path.replace("\\", "/")
        cmd = f"mkdir {folder_path}"
        if not inside_windows():
            cmd = f"mkdir -p {folder_path}"
        os.popen(cmd).read()

    gui_config = """
{
    "local_port": "8080",
    "selected_profile_name": "",
    "selected_profile_number": 0,
    "use_fragmentation": false,
    "keep_top": false,
    "close_to_tray": false,
    "auto_connect": false,
    "start_minimized": false,
    "cloudflare_address": "bruce.ns.cloudflare.com",
    "segmentation_timeout": "5",
    "num_of_fragments": "77",
    "subscription": "",
    "beep": true
}"""


tmp = temp()


def download_xray_gost(window, enable_download: pass_by_ref, filename):
    if filename == "xray":
        if platform.system() == "Windows":
            url = "https://github.com/iblockchaincyberchain/v2rayp_bin/raw/main/win/xray.exe"
            filename = "xray.exe"

        elif platform.system() == "Linux":
            url = "https://github.com/iblockchaincyberchain/v2rayp_bin/raw/main/linux/xray"

        elif platform.system() == "Darwin":
            url = (
                "https://github.com/iblockchaincyberchain/v2rayp_bin/raw/main/mac/xray"
            )
    elif filename == "gost":
        if platform.system() == "Windows":
            url = "https://github.com/iblockchaincyberchain/v2rayp_bin/raw/main/win/gost.exe"
            filename = "gost.exe"

        elif platform.system() == "Linux":
            url = "https://github.com/iblockchaincyberchain/v2rayp_bin/raw/main/linux/gost"

        elif platform.system() == "Darwin":
            url = (
                "https://github.com/iblockchaincyberchain/v2rayp_bin/raw/main/mac/gost"
            )

    download_binary(url, filename, window, enable_download)


def download_binary(url, filename, window, enable_download: pass_by_ref):
    cwd = os.getcwd()
    path = f"{config_path()}/bin"
    try:
        os.mkdir(path)
    except:
        pass

    chunk_size = 2048
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get("content-length", 0))

    fname_temp = f"{filename}.tmp"
    sum = 0
    perc = 0

    pbar = window["progressbar2"]
    percentage = window["percentage"]

    with open(f"{path}/{fname_temp}", "wb") as file:
        for data in resp.iter_content(chunk_size=chunk_size):
            if not enable_download.value:
                return
                break
            size = file.write(data)
            sum = sum + size
            # print(
            #     f"downloading: {int(100 * sum / total)}%, downloaded {int(sum/1024)} from {int(total/1024)} KBytes."
            # )
            perc = int(100 * sum / total)
            pbar.update(perc)
            percentage.update(f"Total Percentage is: {perc}%")
    # window.close()
    os.chdir(path)
    if not inside_windows():
        os.popen(f"mv {path}/{filename}.tmp {path}/{filename}").read()
        os.popen(f"chmod +x {path}/{filename}").read()
    else:
        path = path.replace("\\", "/")
        os.popen(f"move {path}\\{filename}.tmp {path}\\{filename}")
    os.chdir(cwd)


def beep():
    if os.name == "nt":
        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)


def inside_windows():
    inside_window = False
    if os.name == "nt":
        inside_window = True
    return inside_window


def config_path():
    inside_window = False
    if os.name == "nt":
        inside_window = True

    if inside_window:
        config_path = f"{os.getenv('USERPROFILE')}\\appdata\\roaming\\v2rayp\\configs"
    else:
        config_path = f'{os.popen("cd ~;pwd").read().strip()}/Documents/v2rayp/configs'
    return config_path


if __name__ == "__main__":
    print(config_path())
    # download_xray()
    # a = pass_by_ref()
    # a.value = True

    # def temp(b: pass_by_ref):
    #     b.value = False

    # temp(a)
    # print(a.value)
