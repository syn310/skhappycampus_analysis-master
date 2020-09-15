FROM necronia/flask-restful-mysql
 
#COPY ./requirements.txt /tmp/
#RUN pip install -r /tmp/requirements.txt && \
#    rm /tmp/requirements.txt

COPY . /app

# Install MeCab-ko
WORKDIR /app
RUN tar zxfv mecab-0.996-ko-0.9.2.tar.gz

WORKDIR /app/mecab-0.996-ko-0.9.2
RUN ./configure
RUN make
RUN make check
RUN make install

RUN echo /usr/local/lib >> /etc/ld.so.conf

RUN cat /etc/ld.so.conf
RUN ldconfig

# Install MeCab-ko-DIC
WORKDIR /app
RUN tar -xvzf mecab-ko-dic-2.1.1-20180720.tar.gz

WORKDIR /app/mecab-ko-dic-2.1.1-20180720
RUN /bin/bash -c "source /app/mecab-ko-dic-2.1.1-20180720/autogen.sh"
RUN ./configure
RUN make
RUN make install

# Install MeCab-ko-Python(seunjeon)
WORKDIR /app
RUN tar zxfv eunjeon-mecab-python-0.996.tar.gz

WORKDIR /app/eunjeon-mecab-python-0.996
RUN python setup.py build
RUN python setup.py install

WORKDIR /app