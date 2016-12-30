create database listmanagement;
	\connect listmanagement;
create schema listmanagement;

create table listmanagement.lists(
	list_name text,
	list_id text,
	list_type text,
	list_owner text
);