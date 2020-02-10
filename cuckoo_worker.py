import requests


class CuckooWorker(object):
    def __init__(self, ip_addr: str, port: str, auth_token: str):
        self.__net_addr = 'http://' + ip_addr + ':' + port + '/'
        self.__auth_header = {"Authorization": "Bearer " + auth_token}

    def analyze_file(self, path_to_file: str, filename: str) -> str:
        url = self.__net_addr + 'tasks/create/file'

        with open(path_to_file, "rb") as sample:
            files = {"file": (filename, sample)}
            r = requests.post(url, headers=self.__auth_header, files=files)
        return r.json()["task_id"]

    def view_task_result(self, task_id: str) -> dict:
        url = self.__net_addr + 'tasks/view/' + str(task_id)

        r = requests.get(url, headers=self.__auth_header)
        return r.json()

    def view_task_result_by_sha256(self, file_sha256: str) -> dict:
        url = self.__net_addr + 'tasks/view/sha256/' + file_sha256

        r = requests.get(url, headers=self.__auth_header)
        return r.json()

    def get_task_report(self, task_id: str) -> dict:
        url = self.__net_addr + 'tasks/report/' + str(task_id)

        r = requests.get(url, headers=self.__auth_header)
        return r.json()
