# AuthorGraph

This directory stores the code for challenge problem 1 of the Data Challenge.

## Dependencies

* Neo4j (v3.4.4 used in development)
* Py2Neo (v4.0.0b from Anaconda's `conda-forge` channel used in development)
* Python 3 (v3.6.5 used in development)

## Notes

* To start Neo4j using the "neo4j" user (default for local use) on Linux, use the following command to start the service: `sudo systemctl start neo4j`
  * Do __NOT__ use `neo4j start` for the "neo4j" user. This is because, when the service is started, it creates a `/var/run` tmpfs. If you use the default config (which includes the "neo4j" user), it creates this run directory in your local directory, which causes privilege issues.
