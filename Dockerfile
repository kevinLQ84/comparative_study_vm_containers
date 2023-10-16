# Dockerfile, Image, Container
# pull image
FROM python:3.8.10

# add dot, the current folder
# destination is the dot, current folder
ADD . .
# import non-standard libraries
RUN python -m pip install matplotlib
# specify entry command when container is started
CMD ["python", "./run.py"]


# docker image must be built in terminal
# -t is pseudo terminal. after it is name of docker image with dot as location
# docker build -t python-imdb .
