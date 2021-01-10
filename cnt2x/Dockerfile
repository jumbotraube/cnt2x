FROM ubuntu:21.04

WORKDIR /builddir
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y cmake python-dev build-essential
ADD libeep-3.3.177 libeep
RUN cd libeep && mkdir build && cd build && cmake .. && make && make install
RUN apt-get install -y wget && wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
RUN pip install numpy scipy

WORKDIR /workdir
ADD convert_antcnt.py convert_antcnt.py
RUN mkdir libeep && cp /builddir/libeep/python/__init__.py libeep && cp /builddir/libeep/build/pyeep.so libeep

ENTRYPOINT [ "python",  "convert_antcnt.py" ]
