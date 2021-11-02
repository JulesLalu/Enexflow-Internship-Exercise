# Enexflow-Internship-Exercise
A little exercise that fetches data from RTE.

## Steps to run the code

1. Copy the file RTE_data.csv into the following path : 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/RTE_data.csv'
2. Run the SQL queries after connecting to your SQL Server
3. In app.py, line 9, enter your own password instead of 'your_password'
4. Type docker-compose up in the terminal
5. Open the link http://localhost:5000/electricity_consumption/?n=1

## Ways of upgrading the program

- Implement a SQL instance on Docker, so that it runs with "docker-compose up" only. This will help us get rid of manually entering the password in the code, too.
- Query only the n last hours instead of all the data in the SQL command, for performance purposes
- 
