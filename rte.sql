CREATE TABLE October30 {
    id INT NOT NULL AUTO_INCREMENT,
    conso_date DECIMAL(12,10),
    heures INT NOT NULL,
    consommation INT NOT NULL,
    PRIMARY KEY (id)
};

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/RTE_data.csv'
INTO TABLE October30 
FIELDS TERMINATED BY ';' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
