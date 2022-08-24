# Using Python Slim-Buster
FROM biansepang/weebproject:buster

# Clone repo and prepare working directory
RUN git clone -b master https://github.com/Ajibcdefgh/DarkProject /home/darkproject/ \
    && chmod 777 /home/darkproject \
    && mkdir /home/darkproject/bin/

# Copies config.env (if exists)
COPY ./sample_config.env ./config.env* /home/darkproject/

# Setup Working Directory
WORKDIR /home/darkproject/

# Finalization
CMD ["python3","-m","userbot"]
