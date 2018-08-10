#!/bin/bash

help()
{
    echo "Usage: $0 [Options]" >&2
    echo
    echo "    Options:"
    echo "      -h | --help  Prints the usage info to the screen"
    echo "      -id          Signifies that the remaining command-line arguments will"
    echo "                   specify specific tests to run. The valid arguments are:"
    echo "         * 0       Runs the code in the AuthGraph directory."
    echo "                   This code solves Challenge Problem 1."
    echo "         * 1       Runs the code in the DataQuest2 directory."
    echo "                   This code helps solve Challenge Problem 2."
    echo "         * 2       Runs the code in the ResearchEngine directory"
    echo "                   This code helps solve Challenge Problem 2."
    echo "         * 3       Runs the code in webScrape.Geocode directory"
    echo "                   This code solves Challenge Problem 3."
}

runAuthGraph()
{
    echo "Starting the code from AuthGraph"
    echo "\n"
    cd AuthorGraph
    python driver.py
    cd ..
}

runDataQuest2()
{
    echo "Starting the code from DataQuest2"
    echo "\n"
    cd DataQuest2
    python Data_Quest_2.py
    cd ..
}

runResearchEngine()
{
    echo "Starting the code from ResearchEngine"
    echo "\n"
    cd ResearchEngine
    python researchEngine.py
    cd ..
}

runGeocode()
{
    echo "Sample outputs for the scripts in the webScrape.Geocode directory already exist."
    echo "Also, running all the code can take a very long time (4-6 hours)."
    echo "This code also uses the Google Maps API. As a result, it works best with an API key to run and produce results."
    echo "If you haven't already, it is recommended (but not required) that you add your key to the hcoffey1.geocode.py file."
    echo "Do you want to run this code anyway? (yes/no)"
    printf ">>> "
    read runCode
    if [ ${runCode:0:1} == "y" ]; then
        echo "\nStarting the code from webScrape.Geocode"
	echo "\n"
	cd webScrape.Geocode
	python hcoffey1.webScrape.py
	python hcoffey1.geocode.py
	cd ..
    fi
}

if [ $# -eq 0 ]; then
    help
    echo
    echo "Would you like to run all code in succession? (yes/no)"
    printf ">>> "
    read cont
    if [ ${cont:0:1} == "y" ]; then
        runAuthGraph
	runDataQuest2
	runResearchEngine
	runGeocode
    fi
    exit 0
fi

idflag=false

for CLA in $@; do
    if [ ${CLA} == $0 ]; then
        continue
    fi
    case "${CLA}" in
        -h|--help) help
	           ;;
        -id) idflag=true
	     ;;
	0) if ${idflag}; then runAuthGraph; fi
           ;;
	1) if ${idflag}; then runDataQuest2; fi
	   ;;
	2) if ${idflag}; then runResearchEngine; fi
	   ;;
	3) if ${idflag}; then runGeocode; fi
	   ;;
        *) ;;
    esac
done