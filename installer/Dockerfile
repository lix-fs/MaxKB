# 第一阶段：从已有的vector-model基础镜像构建
FROM ghcr.io/1panel-dev/maxkb-vector-model:v1.0.1 as vector-model

# 第二阶段：提取前端应用
FROM maxkb_ui as web-build

# 第三阶段：安装Python依赖并准备应用程序
FROM ghcr.io/1panel-dev/maxkb-python-pg:python3.11-pg15.6 as stage-build

# 安装必要的依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 复制应用代码
COPY . /opt/maxkb/app
RUN mkdir -p /opt/maxkb/model /opt/maxkb/conf && \
    rm -rf /opt/maxkb/app/ui

# 复制前端构建结果
COPY --from=web-build /ui /opt/maxkb/app/ui

WORKDIR /opt/maxkb/app

# 创建Python虚拟环境并安装依赖
RUN python3 -m venv /opt/py3 && \
    . /opt/py3/bin/activate && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    if [ "$(uname -m)" = "x86_64" ]; then sed -i 's/^torch.*/torch = {version = "^2.2.1+cpu", source = "pytorch"}/g' pyproject.toml; fi && \
    poetry install

# 最终阶段：准备运行时环境
FROM ghcr.io/1panel-dev/maxkb-python-pg:python3.11-pg15.6

# 设置构建和版本信息
ARG DOCKER_IMAGE_TAG=dev
ARG BUILD_AT
ARG GITHUB_COMMIT

# 环境变量设置
ENV MAXKB_VERSION="${DOCKER_IMAGE_TAG} (build at ${BUILD_AT}, commit: ${GITHUB_COMMIT})" \
    MAXKB_CONFIG_TYPE=ENV \
    MAXKB_DB_NAME=maxkb \
    MAXKB_DB_HOST=127.0.0.1 \
    MAXKB_DB_PORT=5432 \
    MAXKB_DB_USER=root \
    MAXKB_DB_PASSWORD=Password123@postgres \
    MAXKB_EMBEDDING_MODEL_NAME=/opt/maxkb/model/embedding/shibing624_text2vec-base-chinese \
    MAXKB_EMBEDDING_MODEL_PATH=/opt/maxkb/model/embedding \
    LANG=en_US.UTF-8 \
    PATH=/opt/py3/bin:$PATH \
    POSTGRES_USER=root \
    POSTGRES_PASSWORD=Password123@postgres

WORKDIR /opt/maxkb/app

# 复制构建阶段的成果
COPY --from=stage-build /opt/maxkb /opt/maxkb
COPY --from=stage-build /opt/py3 /opt/py3
COPY --from=vector-model /opt/maxkb/app/model /opt/maxkb/model

# 将run-maxkb.sh文件的换行符转换为LF
RUN sed -i 's/\r$//' /opt/maxkb/app/installer/run-maxkb.sh

# 设置权限和复制运行脚本,
RUN chmod 755 /opt/maxkb/app/installer/run-maxkb.sh && \
    cp -r /opt/maxkb/model/base/hub /opt/maxkb/model/tokenizer && \
    cp -f /opt/maxkb/app/installer/run-maxkb.sh /usr/bin/run-maxkb.sh && \
    cp -f /opt/maxkb/app/installer/init.sql /docker-entrypoint-initdb.d


# 暴露端口
EXPOSE 8080

ENTRYPOINT ["bash", "-c"]
CMD [ "/usr/bin/run-maxkb.sh" ]