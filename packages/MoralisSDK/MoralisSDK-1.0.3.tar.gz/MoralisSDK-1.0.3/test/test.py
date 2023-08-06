from MoralisSDK import api, ipfs
from time import sleep

if __name__ == '__main__':
    t = api.MoralisApi()
    # t.set_api_key('L1aTPccpZTZpCTcRCMyCinajCny6uIMKKYT7we5L9ReQ7cSd53jm4npzQoE0NgkW')
    # nft = t.get_nfts(address='0x260fCF88102fB038B2506dC60fc49270199e12fE')
    # print(nft)
    # ntf_trans = t.get_nfts_transfer(address='0x260fCF88102fB038B2506dC60fc49270199e12fE')
    # print(ntf_trans)
    # res = t.get_nfts_token(chain='eth', address='0x260fCF88102fB038B2506dC60fc49270199e12fE',
    #                        token_address='0xd07dc4262bcdbf85190c01c996b4c06a461d2430', limit=3)
    # print(res)
    # lowest = t.get_nft_lowest_price(address='0x73f1780cb2b5ce961601fdf6a9b002082bb82b4d', days=5)
    # print(lowest)
    # transfer = t.get_nfts_transfer_blocks(from_block='12895140')
    # print(transfer)
    # token = t.get_token_id(address='0x73f1780cb2b5ce961601fdf6a9b002082bb82b4d', total_range=2)
    # print(token)
    # owners = t.get_nft_owners(address='0x73f1780cb2b5ce961601fdf6a9b002082bb82b4d', limit=1)
    # print(owners)
    # contract_trasfers = t.get_contract_nft_transfers(address='0x73f1780cb2b5ce961601fdf6a9b002082bb82b4d')
    # print(contract_trasfers)
    # sleep(10)
    # resync = t.get_nft_metadata_resync(address='0x73f1780cb2b5ce961601fdf6a9b002082bb82b4d', token_id='430')
    # print(resync)
    # token_meta = t.get_token_id_metadata(address='0x73f1780cb2b5ce961601fdf6a9b002082bb82b4d', token_id='430')
    # print(token_meta)
    # token_owners = t.get_token_id_owners(address='0x73f1780cb2b5ce961601fdf6a9b002082bb82b4d', token_id='432')
    # print(token_owners)
    # token_trans = t.get_token_id_transfers(address='0x73f1780cb2b5ce961601fdf6a9b002082bb82b4d', token_id='430')
    # print(token_trans)
    # # ChainLink
    # chain = chainlink.Chainlink()
    # data = chain.active_feeds(limit=10)
    # print(data)
    # IPFS
    i = ipfs.IPFS()
    # key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDE0RkY4NTU4MzVGMDYwZDBCRTk0ZWQyOTBjNTdiODE1YTE5MjQxNUQiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY1NzU2OTU4ODQxOSwibmFtZSI6Ik1BTklESUxMUyJ9.idaK-qJVyOb8WKP1cD0yddE8UJX4zRpBKtX-QqN49fU'
    # upload_file_nft = i.upload_nft_storage(key,'Flowcharts.png')
    # print(upload_file_nft)
    # cid = upload_file_nft['value']['cid']
    # print('cid',cid)
    # status = i.status_nft_storage(key,cid)
    # print(status)

    # web3
    web3key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDkwN2FFNDMyZTk3ZmQ3MzNCQjY3OTMwYTk2MUJGN2NFMTMxNTk0MUMiLCJpc3MiOiJ3ZWIzLXN0b3JhZ2UiLCJpYXQiOjE2NjQwMDA3NjgwNjMsIm5hbWUiOiJmaXJzdCB0b2tlbiJ9.mBzrbI7-1YPaNVk1HlDNNmjC_VW27w01TGJOanofdAA'
    upload_file_web3 = i.upload_web3_storage(web3key,'Flowcharts.png')
    print(upload_file_web3)
    web3_cid = upload_file_web3['cid']
    s = i.web3_storage_download_link(web3_cid)
    print(s)
    s1 = i.nft_storage_download_link(web3_cid)
    print(s1)
    s2 = i.status_web3_storage(web3key,web3_cid)
    print(s2)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
