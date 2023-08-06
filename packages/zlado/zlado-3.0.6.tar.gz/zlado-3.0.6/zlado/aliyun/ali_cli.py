# -*-coding=utf-8-*-

import logging
import json
import logging
from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526.DescribeRegionsRequest import DescribeRegionsRequest

class AliCli:

    def __init__(self, accessKeyId=None, accessKeySecret=None, regionIds=['cn-shenzhen']) :
        self.accessKeyId = accessKeyId
        self.accessKeySecret = accessKeySecret
        self.regionIds = regionIds
        self.clts = [client.AcsClient(accessKeyId, accessKeySecret, i) for i in regionIds]

    def list_aliyun_regions(self):
        request = DescribeRegionsRequest()
        response = self._send_request('cn-shenzhen',request)
        if response is not None:
            region_list = response.get('Regions').get('Region')
            assert response is not None
            assert region_list is not None
            result = map(self._map_region, region_list)
        return list(result)
    def _map_region(self,item):
        region_id = item.get('RegionId')
        return region_id

    def ecses_iterator(self):
        for regionId in self.regionIds:
            request = DescribeInstancesRequest()
            request.set_accept_format('json')
            # 设置请求参数的示例代码如下，表示进行分页查询，set_PageNumber指定查询第1页的内容，set_PageSize指定当前页显示2条数据。
            request.set_PageNumber(1)
            request.set_PageSize(100)
            response = self._send_request(regionId,request)
            if response is not None:
                instance_list = response.get('Instances').get('Instance')
                result = map(self._mapEcs, instance_list)
                for _ecs in result:
                    _ecs.regionId=regionId
                    yield _ecs

    # 	'Tags': {
    # 		'Tag': [{
    # 			'TagKey': '中间件',
    # 			'TagValue': ''
    # 		}]
    # 	},
    def _mapEcs(self, item):
        # instance_id = item
        # instance_id = item.get('NetworkInterfaces')
        # instance_id = item.get('NetworkInterfaces').get('NetworkInterface')[0].get('PrimaryIpAddress')
        return Ecs(hostname=item.get('HostName'),
                   privateIpAddress=item.get('VpcAttributes').get('PrivateIpAddress').get('IpAddress')[0],
                   description=item.get('Description'),createTime=item.get('CreationTime'))

    def _send_request(self, regionId,request):
        clt=client.AcsClient(self.accessKeyId, self.accessKeySecret, regionId)
        request.set_accept_format('json')
        try:
            response_str = clt.do_action_with_exception(request)
            logging.info(response_str)
            response_detail = json.loads(response_str)
            return response_detail
        except Exception as e:
            logging.error(e)

    def __str__(self) :
        return ','.join([self.accessKeyId,self.accessKeySecret,','.join(self.regionIds)])



class Ecs:

    def __init__(self, regionId=None,hostname=None, tags=[], privateIpAddress=None, description=None,createTime=None) :
        self.regionId=regionId
        self.hostname = hostname
        self.tags = tags
        self.ip = privateIpAddress
        self.description = description
        self.createTime=createTime



    def __str__(self) :
        return self.ip + '(' + self.hostname +'@'+self.regionId+ '#' + self.description + ')'



if __name__ == '__main__':
    ecsClient = AliCli(accessKeyId='LTAI4G8ckHBUv3aFWTJDupaS', accessKeySecret='ApsdTQS7lWXjASbgiXM2zbG5bk1ljM',
                       regionIds=['cn-shenzhen'])
    # print(ecsClient.list_aliyun_regions())
    ecses = [ecs for ecs in ecsClient.ecses_iterator()]
    ecses = sorted(ecses, key=lambda x: x.createTime,reverse=False)
    ecsips=[ecs.ip for ecs in ecses]
    print(ecsips)
    pass
