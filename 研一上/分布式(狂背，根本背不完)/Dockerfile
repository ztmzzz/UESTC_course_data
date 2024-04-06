FROM ubuntu:20.04
WORKDIR /root
#ENV TZ Asia/Shanghai
#RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y wget ca-certificates && apt-get clean
RUN wget https://go.dev/dl/go1.21.1.linux-amd64.tar.gz && tar -C /usr/local -xzf go1.21.1.linux-amd64.tar.gz && rm go1.21.1.linux-amd64.tar.gz
ENV PATH /usr/local/go/bin:$PATH
COPY . .
ENTRYPOINT ["go", "run", "main.go"]