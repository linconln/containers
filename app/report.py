from minio import Minio
import redis
import io

cliente = Minio(
    endpoint="192.168.19.38:9000", 
    access_key="minioadmin", 
    secret_key="minioadmin",
    secure=False)

bucket_name = "bucket"
if cliente.bucket_exists(bucket_name):
    print("Bucket existe!")
else:
    cliente.make_bucket(bucket_name)

cache = redis.Redis(host='redis', port=6379, db=0)

chaves = cache.keys("report*")

for chave in chaves:
    str_chave = chave.decode("utf-8")
    str_chave = str_chave+".txt"
    reports = cache.lrange(chave, 0, 999999)
    value=""
    size=0
    for report in reports:
        str_report=report.decode("utf-8")
        value=value+str_report+"\n"

    size=len(value)
    value_as_bytes=value.encode("utf-8")
    str_reports=io.BytesIO(value_as_bytes)

    result = cliente.put_object(
        bucket_name=bucket_name,
        object_name=str_chave,
        data=str_reports,
        length=size
    )

    get_url = cliente.get_presigned_url(
        method='GET',
        bucket_name=bucket_name,
        object_name= str_chave, )

    print(f"Download URL: [GET] {get_url}")
