FROM knowengdev/base_image:09_19_2017
MAINTAINER Dan Lanier <lanier4@illinois.edu>

ENV SRC_LOC /home

# Install the latest knpackage
RUN pip3 install -I knpackage dispy 

# Clone from github
RUN git clone https://dlanier:black396Bean!@github.com/KnowEnG-Research/Spreadsheets_Transformation.git ${SRC_LOC} 

# Set up working directory
WORKDIR ${SRC_LOC}
