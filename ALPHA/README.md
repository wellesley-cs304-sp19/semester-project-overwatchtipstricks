# Overwatch Tips and Trick
### by Hershel, Anna, and Emma

## Setting Up 

After ensuring venv is activated, perfrom the following steps: 

```
$ cd semester-project-overwatchtipstrick/ALPHA
$ mysql-ctl start 
$ mysql --local-infile 
mysql> source ovw.sql;
mysql> source insert_starter_data.sql; 
mysql> exit
$ python app.py
```