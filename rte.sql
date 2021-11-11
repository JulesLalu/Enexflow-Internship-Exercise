CREATE DATABASE IF NOT EXISTS rte;

CREATE TABLE October30 {
    time_stamp INT
    consommation INT NOT NULL,
    PRIMARY KEY (time_stamp)
};

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/RTE_data.csv'
INTO TABLE October30 
FIELDS TERMINATED BY ';' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
