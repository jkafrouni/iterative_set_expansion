# this script should be run from the top-level iterative_set_expansion folder


sudo apt-get update

# prepare python:
sudo apt-get install python3-pip unzip
sudo pip3 install --upgrade pip
sudo pip install -r iterative_set_expansion/requirements.txt

# install java:
sudo apt-get install default-jdk

# install Stanford CoreNLP:
wget http://nlp.stanford.edu/software/stanford-corenlp-full-2017-06-09.zip 
sudo unzip stanford-corenlp-full-2017-06-09.zip
mv stanford-corenlp-full-2017-06-09 resources # moves the CoreNLP folder to resources/
