drop table temp;

create table if not exists temp(
no int,
content string,
mor string,
cnt string
)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile;

drop table temp2;

create table if not exists temp2(
content string,
mor string,
cnt int
)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile;

load data inpath 'hdfs:///user/maria_dev/projectData/countryPostResult.csv'
into table temp;

insert overwrite table temp2
select content, mor, cast(cnt as int) cnt
from temp
where mor in ( "Noun", "Verb", "Adverb", "Adjective" );

insert overwrite table temp2
select content, mor, cnt
from temp2
order by cnt desc;

add jar hdfs:///user/maria_dev/hive/lib/hive-contrib-3.1.2.jar;
create temporary function row_sequence as 'org.apache.hadoop.hive.contrib.udf.UDFRowSequence';

drop table wordCnt;

create table if not exists wordCnt(
no int,
content string,
mor string,
cnt int
)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile;

insert overwrite table wordCnt
select row_sequence(), content, mor, cnt
from temp2;