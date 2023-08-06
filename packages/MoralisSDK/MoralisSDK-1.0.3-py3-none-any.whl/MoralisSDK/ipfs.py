import binascii
import os
import time
from urllib3 import encode_multipart_formdata
from pinatapy import PinataPy
import nft_storage
from nft_storage.api import nft_storage_api
from nft_storage.model.error_response import ErrorResponse
from nft_storage.model.upload_response import UploadResponse
from nft_storage.model.unauthorized_error_response import UnauthorizedErrorResponse
from nft_storage.model.forbidden_error_response import ForbiddenErrorResponse
from pprint import pprint
import requests


class IPFS:
    def __init__(self):
        self.nft_base_uri = 'https://api.nft.storage'

    def upload_nft_storage(self, apikey, file):
        # See configuration.py for a list of all supported configuration parameters.
        configuration = nft_storage.Configuration(
            host="https://api.nft.storage"
        )

        configuration = nft_storage.Configuration(
            access_token=apikey
        )
        with nft_storage.ApiClient(configuration) as api_client:
            # Create an instance of the API class
            api_instance = nft_storage_api.NFTStorageAPI(api_client)
            body = open(file, 'rb')  # file_type |

            # example passing only required values which don't have defaults set
            try:
                # Store a file
                api_response = api_instance.store(body, _check_return_type=False)
                return (api_response)
            except nft_storage.ApiException as e:
                return ("Exception when calling NFTStorageAPI->store: %s\n" % e)

    # def upload_nft_storage_test(self, apikey, file, file_type):
    #     try:
    #         print('in')
    #         store_uri = f'{self.nft_base_uri}/store'
    #         print(store_uri)
    #         body = ''
    #         # with open(file,'rb') as f:
    #         #     body = f.read()\
    #         f = open(file,'rb')
    #         data = {
    #             'name': '{} data'.format(file.split('.')[0]),
    #             'file_type': file_type,
    #             'file_content': f
    #         }
    #         # body, head = encode_multipart_formdata(data)
    #         # print(data)
    #         boundary = binascii.hexlify(os.urandom(16)).decode('ascii')
    #         header = {
    #             'accept': 'application/json',
    #             'Authorization': f'Bearer {apikey}'
    #         }
    #         response = requests.request(url=store_uri, method='POST', headers=header, data=f'meta = {data}')
    #         print(response.request.__dict__)
    #         print(response.content.decode())
    #         print(response.headers)
    #         if response.status_code == 200:
    #             response_object = response.json()
    #             # response_object['status_code'] = 200
    #             return response_object
    #
    #     except Exception as e:
    #         print(f'Got exception while upload file to nft {e}')

    def status_nft_storage(self, apikey, cid_):
        configuration = nft_storage.Configuration(
            host="https://api.nft.storage"
        )
        configuration = nft_storage.Configuration(
            access_token=apikey
        )

        with nft_storage.ApiClient(configuration) as api_client:
            # Create an instance of the API class
            api_instance = nft_storage_api.NFTStorageAPI(api_client)
            cid = cid_  # str | CID for the NFT

            # example passing only required values which don't have defaults set
            try:
                # Get information for the stored file CID
                api_response = api_instance.status(cid, _check_return_type=False)
                return (api_response)
            except nft_storage.ApiException as e:
                return ("Exception when calling NFTStorageAPI->status: %s\n" % e)

    def upload_web3_storage(self, apikey, file):

        body = open(file, 'rb')
        response = requests.post(
            "https://api.web3.storage/upload",
            headers={"Authorization": f'Bearer {apikey}'},
            files={"file": body}
        )

        return (response.json())

    def status_web3_storage(self, apikey, cid_):

        response = requests.get(f'https://api.web3.storage/status/{cid_}')
        return response.json()

    def nft_storage_download_link(self, cid_):
        data = f'https://nftstorage.link/ipfs/{cid_}'
        return data

    def web3_storage_download_link(self, cid_):
        data = f'https://{cid_}.ipfs.w3s.link/'
        return data

    def upload_pinata(self, pinata_api_key, pinata_secret_api_key, file):
        body = open(file, 'rb')
        pinata = PinataPy(pinata_api_key, pinata_secret_api_key)
        result = pinata.pin_file_to_ipfs(body)
        return result.json()
