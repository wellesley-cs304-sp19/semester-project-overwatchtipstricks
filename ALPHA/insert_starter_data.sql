use ovw;


load data local infile 'user.tsv' 
into table user
fields terminated by '\t'
lines terminated by '\n'
IGNORE 1 ROWS;

load data local infile 'tips.tsv' 
into table tips
fields terminated by '\t'
lines terminated by '\n'
IGNORE 1 ROWS;
(@var_datePosted)
SET datePosted = STR_TO_DATE(@var_col1,'%c/%e/%Y %h:%i %p');
-- date posted isn't working 

