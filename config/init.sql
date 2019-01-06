create database IF NOT EXISTS appDB ;
create table IF NOT EXISTS appDB.user 
(
    id int(11),
    name varchar(200),
    primary key(id)
);

insert into appDB.user(id, name)
values
(1, "mamun"),
(2, "tutun");