FROM knowengdev/base_image:09_19_2017
MAINTAINER Dan Lanier <lanier4@illinois.edu>

ENV SRC_LOC /home
RUN apt-get install -y python3-tk

# Install the latest knpackage
RUN pip3 install --upgrade pip
RUN pip3 install -I knpackage dispy 
RUN pip3 install matplotlib
RUN pip3 install lifelines

# Clone from github
RUN git clone https://github.com/KnowEnG/Spreadsheets_Transformation.git ${SRC_LOC} 

# Set up working directory
WORKDIR ${SRC_LOC}
