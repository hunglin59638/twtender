FROM alpine:3.20.3

LABEL base.image="alpine"
LABEL software="twtender"
LABEL software.version="0.1.0"
LABEL description="API to get tenders from Taiwan"
LABEL website="https://github.com/hunglin59638/twtender"
LABEL maintainer="Hung-Lin, Chen"
LABEL maintainer.email="hunglin59638@gmail.com"

RUN apk update && apk add --no-cache \
    python3 \
    py3-pip

RUN pip install toml --break-system-packages

RUN mkdir -p /opt/twtender 
WORKDIR /opt/twtender
ADD . .
RUN python3 setup.py install
ENTRYPOINT [ "twtender" ]
EXPOSE 8000