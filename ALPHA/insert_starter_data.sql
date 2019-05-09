use ovw;


load data local infile 'starterdata/user.tsv' 
into table user
fields terminated by '\t'
lines terminated by '\n'
IGNORE 1 ROWS;

load data local infile 'starterdata/tips.tsv' 
into table tips
fields terminated by '\t'
lines terminated by '\n'
IGNORE 1 ROWS;

load data local infile 'starterdata/comments.tsv' 
into table comments
fields terminated by '\t'
lines terminated by '\n'
IGNORE 1 ROWS

