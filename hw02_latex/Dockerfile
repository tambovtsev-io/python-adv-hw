# FROM debian:bookworm
FROM python:3.12

# Latex installation copied from here: https://github.com/theredfish/docker-pdflatex
RUN apt-get update && \
    apt-get install -y --no-install-recommends texlive-latex-recommended texlive-fonts-recommended dvipng && \
    rm -rf /var/lib/apt/lists/*

# Set home to the user's home directory
ENV WORKDIR="/workdir"
ENV PATH="$WORKDIR/.venv/bin:$PATH"
ENV PYTHONPATH="$WORKDIR:$PYTHONPATH"
WORKDIR $WORKDIR

# Load image
RUN curl --create-dirs -o images/cat_ballet.png https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/78a499bf-97f5-4a29-b2b2-e917e40a0959/original=true,quality=90/00061-1394326287.jpeg

# Build python package
COPY . .
RUN pip3 install -e .
