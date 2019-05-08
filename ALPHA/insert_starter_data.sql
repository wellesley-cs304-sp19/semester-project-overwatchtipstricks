use ovw;


load data local infile 'user.tsv' 
into table user
fields terminated by '\t'
lines terminated by '\n'
IGNORE 1 ROWS;

load data local infile 'tips_2.tsv' 
into table tips
fields terminated by '\t'
lines terminated by '\n'
IGNORE 1 ROWS


