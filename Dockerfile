FROM ubuntu:24.04

# Update package lists and upgrade packages
RUN apt-get update && apt-get upgrade -y

# Install required packages
RUN apt-get install -y \
    python3 \
    python3-pip \
    wget \
    dos2unix

# Add i386 architecture
RUN dpkg --add-architecture i386

# Add WineHQ repository key and APT source
RUN mkdir -pm755 /etc/apt/keyrings && \
    wget -O /etc/apt/keyrings/winehq-archive.key https://dl.winehq.org/wine-builds/winehq.key && \
    wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/noble/winehq-noble.sources

# Install WineHQ stable package and dependencies
RUN apt-get install --install-recommends -y \
    winehq-stable

# Setup working directory
WORKDIR /app

COPY . /app

RUN dos2unix scripts/*.sh && \
    chmod +x scripts/*.sh

EXPOSE 3000