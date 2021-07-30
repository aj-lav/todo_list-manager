drop table if exists task_list;
drop table if exists task_status;
drop table if exists todo_user;

create table todo_user (
    u_id serial primary key,
    u_name text,
    pass text,
    created timestamp
);

create table task_status (
    s_id serial primary key,
    name text
);

insert into task_status (name) values  ('completed');
insert into task_status (name) values  ('newly created');
insert into task_status (name) values  ('overdue');

create table task_list (
    t_id serial primary key,
    auth_id serial references todo_user(u_id),
    title text,
    description text,
    schedule timestamp,
    created timestamp,
    updated timestamp,
    status serial references task_status(s_id)
);