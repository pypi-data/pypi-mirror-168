import os
import requests
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

class ManageFiles():
    def __init__(self):

        FMS_HOST = os.getenv('FMS_HOST') or '10.1.0.5'
        FMS_PORT = os.getenv('FMS_PORT') or '8007'
        self.fms_host = FMS_HOST
        self.fms_port = FMS_PORT
        self.fms_url = f"{self.fms_host}:{self.fms_port}"
        self.base_location = os.getcwd()
        
    def download_file(self, file_key, location):
        url = f"http://{self.fms_url}/{file_key}"
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            ext = response.headers['x-ext'].replace('.','')
            file_location = os.path.join(self.base_location, f"{location}/{file_key}.{ext}")
            with open(file_location, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024): 
                    file.write(chunk)
            response.close()
        logging.info(f"File Downloaded Successfully {file_key}.{ext}")
        return f"File Donwloaded Successfully {file_key}.{ext}"

    def upload_file(self, file_key, ext, location, group, created_by):
        url = f"http://{self.fms_url}/{file_key}"
        file_location = os.path.join(self.base_location, f"{location}/{file_key}.{ext}")
        headers = {'content-type': 'application/octet-stream',
                    'x-ext': ext, 'x-group': group, 'x-createdBy': created_by}
        file_request = requests.Session()
        with open(file_location, 'rb') as file:
            with file_request.post(url, file, headers=headers, stream=True) as req:
                req.raise_for_status()
        file_request.close()
        logging.info(f"File Uploaded Successfully {file_key}.{ext}")
        return f"File Uploaded Successfully {file_key}.{ext}"

    def delete_file(self, file_key, ext, location): 
        os.remove(os.path.join(self.base_location, f"{location}/{file_key}.{ext}"))
        logging.info(f"File Deleted Successfully {file_key}.{ext}")
        return f"File Deleted Successfully {file_key}.{ext}"




