drop table l_temp;

create table if not exists l_temp(
no int,
content string,
mor string,
cnt string
)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile;

drop table l_temp2;

create table if not exists l_temp2(
content string,
mor string,
cnt int
)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile;

load data inpath 'hdfs:///user/maria_dev/projectData/londonPostResult.csv'
into table l_temp;

insert overwrite table l_temp2
select content, mor, cast(cnt as int) cnt
from l_temp
where mor in ( "Noun", "Modifier" );

insert overwrite table l_temp2
select content, mor, cnt
from l_temp2
order by cnt desc;

add jar hdfs:///user/maria_dev/hive/lib/hive-contrib-3.1.2.jar;

create temporary function row_sequence as 'org.apache.hadoop.hive.contrib.udf.UDFRowSequence';

drop table l_wordCnt;

create table if not exists l_wordCnt(
no int,
content string,
mor string,
cnt int
)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile;

insert overwrite table l_wordCnt
select row_sequence(), content, mor, cnt
from l_temp2;

select * from l_wordcnt;