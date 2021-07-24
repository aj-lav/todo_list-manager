drop table if exists todo_user;
drop table if exists task_list;
drop table if exists task_status;


create table todo_user (
    u_id serial primary key,
    name text,
    u_name text,
    pass text,
    first_login timestamp,
    last_login timestamp
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
    t_name text,
    t_desc text,
    created_info timestamp,
    up_info timestamp,
    status serial references task_status(s_id)
);