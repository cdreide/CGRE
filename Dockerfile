FROM ubuntu:20.04

# Set entrypoint
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Linux Dependencies Installation
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends mercurial \
    git \
    curl \
    make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    llvm \
    libncurses5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
    libx11-xcb-dev \
    libgtk2.0-dev \
    libgtkglext1-dev \
    libxtst6 \
    libasound2 \
    libxss-dev\
    libx11-dev\
    python3 \
    python3-dev \
    python3-pip \
    libopencv-dev \
    libtesseract-dev \
    xvfb \
    g++ \
    cmake

# PyEnv Installation
ENV PYENV_ROOT="/root/.pyenv" \
    PATH="/root/.pyenv/shims:/root/.pyenv/bin:${PATH}" \
    PIPENV_YES=1 \
    PIPENV_DONT_LOAD_ENV=1 \
    LC_ALL="C.UTF-8" \
    LANG="en_US.UTF-8"
    # PYTHON_CONFIGURE_OPTS="--enable-shared"
RUN curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash && \
    env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.7.2 && \
    pyenv global 3.7.2 && \
    pyenv rehash

# Pipenv Installation
RUN pip install --upgrade pip \
    setuptools \
    pipenv

# Pipenv Setup
COPY Pipfile Pipfile.lock /app/
WORKDIR /app
RUN pipenv install --deploy --ignore-pipfile

# Download Chromium for cefpython
RUN pipenv run python -c 'import pyppeteer; pyppeteer.chromium_downloader.download_chromium()'

# Recognition
# Get language data
RUN wget https://github.com/tesseract-ocr/tessdata/raw/master/eng.traineddata
RUN mkdir -p /usr/share/tessdata/
RUN mv -v eng.traineddata /usr/share/tessdata/
ENV TESSDATA_PREFIX /usr/share/tessdata/

# Compile C++ Code
COPY recognition /app/recognition
RUN cd /app/recognition/determination/ && ./setup.sh && \
    cd /app/recognition/localisation/ && ./setup.sh

# Remove unneeded
RUN apt-get purge -y curl \
    python3-pip \
    cmake \
    make \
    build-essential \
    make \
    wget \
    ca-certificates && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY complete_pipeline_docker.sh /app/complete_pipeline_docker.sh
COPY dataset /app/dataset
COPY evaluation /app/evaluation

ENV DISPLAY :99
ADD docker_start.sh /docker_start.sh
RUN chmod a+x /docker_start.sh
CMD /docker_start.sh
