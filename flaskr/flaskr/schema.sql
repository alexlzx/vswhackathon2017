drop table if exists entries;

create table entries (
	id integer primary key autoincrement,
	title text not null,
	'text' text not null
);

create table routes (
	id integer primary key autoincrement,
	address text not null
);

