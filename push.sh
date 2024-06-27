docker build . -t registry.cn-hangzhou.aliyuncs.com/vswork/mymaxkb:$1 -f ./installer/Dockerfile-my
docker push registry.cn-hangzhou.aliyuncs.com/vswork/mymaxkb:$1
docker rmi registry.cn-hangzhou.aliyuncs.com/vswork/mymaxkb:$1