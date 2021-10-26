
import os
import oss2
from oss2.models import ReplicationRule

# 首先初始化AccessKeyId、AccessKeySecret、Endpoint等信息。
# 通过环境变量获取，或者把诸如“<你的AccessKeyId>”替换成真实的AccessKeyId等。
#
# 以杭州区域为例，Endpoint可以是：
#   http://oss-cn-hangzhou.aliyuncs.com
#   https://oss-cn-hangzhou.aliyuncs.com


access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', '<你的AccessKeyId>')
access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', '<你的AccessKeySecret>')
bucket_name = os.getenv('OSS_TEST_BUCKET', '<你的Bucket>')
endpoint = os.getenv('OSS_TEST_ENDPOINT', '<你的访问域名>')


# 确认上面的参数都填写正确了
for param in (access_key_id, access_key_secret, bucket_name, endpoint):
    assert '<' not in param, '请设置参数：' + param


# 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

# 依次填写复制规则ID、目标Bucket名称、目标Bucket所在地域和是否同步历史数据。
# 如果未设置rule_id或者设置rule_id为空，则OSS会为该复制规则生成唯一值。
# 目标Bucket所在地域以华北2（北京）为例，target_bucket_location填写为oss-cn-beijing。
# OSS默认会同步历史数据。如果设置is_enable_historical_object_replication为False，表示禁止同步历史数据。
replica_config = ReplicationRule(rule_id='test_replication_1',
                                 target_bucket_name='dstexamplebucket',
                                 target_bucket_location='oss-cn-beijing',
                                 is_enable_historical_object_replication=False
                                 )
# 开启跨区域复制。
bucket.put_bucket_replication(replica_config)

# 查看跨区域复制信息。
result = bucket.get_bucket_replication()
# 打印返回的信息。
for rule in result.rule_list:
    print(rule.rule_id)
    print(rule.target_bucket_name)
    print(rule.target_bucket_location)

# 查看跨区域复制进度。
# 填写复制规则ID，例如test_replication_1。
result = bucket.get_bucket_replication_progress('test_replication_1')
print(result.progress.rule_id)
# 是否开启了历史数据同步。
print(result.progress.is_enable_historical_object_replication)
# 历史数据同步进度。
print(result.progress.historical_object_progress)
# 实时数据同步进度。
print(result.progress.new_object_progress)

# 查看可同步的目标地域。
result = bucket.get_bucket_replication_location()
for location in result.location_list:
    print(location)

# 关闭跨区域复制。
# 填写复制规则ID，例如test_replication_1。
result = bucket.delete_bucket_replication('test_replication_1')