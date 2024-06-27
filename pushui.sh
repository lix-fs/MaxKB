docker build . -t registry.cn-hangzhou.aliyuncs.com/vswork/maxkb_ui:$1 -f ./installer/Dockerfile-ui
docker push registry.cn-hangzhou.aliyuncs.com/vswork/maxkb_ui:$1
docker rmi registry.cn-hangzhou.aliyuncs.com/vswork/maxkb_ui:$1