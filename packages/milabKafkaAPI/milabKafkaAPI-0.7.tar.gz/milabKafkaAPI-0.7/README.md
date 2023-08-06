# Kafka-API
An API to communicate with the Kafka server (on the Raspberry Pi).

## Packages Needed For The API:

### For Python:
pip - kafka-python, lxml, butter.mas-api (for the listener example)

## Kafka Server Setup

### Initial Install On RaspPi:
1. Run on Raspberry OS (password: !milabspirit).
2. install Java: sudo apt update => sudo apt install default-jdk
3. Download Kafka from official website: https://www.kafka.apache.org/
4. Extract file: tar -xzf kafka_(Scala version)-(kafka-version).tgz => cd kafka_(Scala version)-(kafka-version)

### Start Kafka Server:
From the kafka folder (extracted in the installation process step 4):
1. On a terminal, run Zookeeper: bin/zookeeper-server-start.sh config/zookeeper.properties
2. On a seperate terminal, run Kafka: bin/kafka-server-start.sh config/server.properties

source: https://codetober.com/apache-kafka-on-raspberry-pi-4/



