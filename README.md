# enhanceNextBus

NextBus is a feed service that provides information about trains and buses in the United States. The information they 
serve includes agencies, routes, schedules, stops, vehicle location and more in XML format.


This code implements a little NextBus service JSON converter in python Tornado. The web-server, once running, creates a 
tunnel which redirects all RESTful queries to NextBus service (http://webservices.nextbus.com). Upon reception, the code
 translates the resulting query information into JSON format and presents it to the user via web interface.
 
### Web server deployment
 In order to run the web-server, several libraries have to be present in the destination computer.
1.  Clone repository.

    First, install **git** in order to clone repository files.
    ```
    sudo apt-get install git
    ```
    
    To clone the repository, execute the following command in the directory of your choice.
    ```
    git clone https://github.com/eloiGarrido/enhanceNextBus.git
    ```
    This will download the web-server within the directory `enhanceNextBus`.
    

2.  Install **python3**, and git if not already present in your computer.

    Validate if python is already installed.
    ```
    sudo apt-get update
    sudo apt-get -y upgrade
    python3 -V
    ```
    Output should be similar to:
    ```
    Python 3.5.2
    ```
    To install python packages pip library or similar is required. Install **pip**
    ```
    sudo apt-get install -y python3-pip
    ```
    These few previous steps can be executed using the `setup.sh` script located in `/setup/setup.sh`. Which will first install the 
    system requirements and then attempt to install all required python libraries. 
    
3.  Manually install python libraries (Optional)
    
    If you have not run the installation script or you have encountered a problem you could try
    to install the python packages manually. To that end, run the following command:
    ```
    sudo pip3 install appdirs==1.4.3 packaging==16.8 pyparsing==2.2.0 six==1.10.0 tornado==4.4.3 xmljson==0.1.7 xmltodict==0.10.2
    ```
    Validate the correct installation with the command:
    ```
    pip3 freeze
    ```
    
4.  Use Docker image (Optional)
    
    Optionally, one can download the docker image with the system set from:
    ```
    docker pull jesther21/nextbus_ubuntu
    ```
    

    
### Run web server
    
Once the system has been deployed one can run the unittests to validate that the installation has 
been successful.

1.  Go to `enhancedNextBus/handlers` and run the `run_unittests.sh` script.
    ```
    cd enhancedNextBus/handlers
    ./run_unittests.sh
    ```
    (optional) If permissions have not been set for the script one can modify with:
    ```
    chmod 777 run_unittests.sh
    ```
    This script should return OK after running a few unittest. Those test check a few system functions,
    like information caching and proper performance of custom endpoints as well as a few comparisons between expected
     regular nextBus API use against this web-server tunnel.
     
2.  Launch web-server
    
    To launch the web server go to the root folder and execute the `run.sh` script in the same fashion as the unittest script.
    The terminal will show the message: `Starting server on port 8888` when the server is ready to receive requests.
    
### Web server use cases

This web-server accepts the same commands as NextBus Public XML Feed. However, in order to differentiate ourselves the access
  end point has been modified and two more endpoints have been added.
  
1.  General nextBus tunnel queries:
    
    NextBus service uses query commands with the format:
    ```
    http://webservices.nextbus.com/service/publicXMLFeed?command=commandName&a=agency_tag&additionParams...
    ```
    
    Our system uses the same general format except that changes the endpoint link. Instead of using
     `http://webservices.nextbus.com/service/publicXMLFeed` the web-server uses `http://localhost:8888/publicJSONFeed`
     
    Therefore, an example query would look like: 
    ```
    http://localhost:8888/publicJSONFeed?command=agencyList
    ```
    
    All the queries allowed by NextBus can be found in: `https://www.nextbus.com/xmlFeedDocs/NextBusXMLFeed.pdf​`. 
    
    Apart from the common endpoints, this web-server provides two more endpoints:
    ```
    http://localhost:8888/queryCounter
    http://localhost:8888/slowestQueries
    ```
    The first will return the number of times a certain query has been called to a specific web-server instance.
    
    The second query will return a list of the 5 slowest queries performed by a specific instance of the web-server.


    

