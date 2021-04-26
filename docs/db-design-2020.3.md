# Database Design

## Table user

| name                    | type        |
| ----------------------- | ----------- |
| uid (key, not null)     | int         |
| uname (not null)        | varchar(25) |
| passwd (not null)       | varchar(20) |

## Table admin

| name                      | type        |
| ------------------------- | ----------- |
| admin_id (key, not null) | int         |
| admin_name (not null)     | varchar(25) |
| passwd (not null)         | varchar(20) |


## Table question

| name                                          | type           |
| --------------------------------------------- | -------------- |
| qid (key, not null)                           | int            |
| qtitel(not null)                              | varchar(128)   |
| uid(提问人学号, references)                    | int            |
| plate_1 (板块名称, 限制问题隶属于最多3个板块)   | varchar(20)    |
| plate_2                                       | varchar(20)    |
| plate_3                                       | varchar(20)    |
| q_detail (问题描述)                            | varchar(512)   |

## Table article

| name                           | type |
| ------------------------------ | ---- |
| aid (key, not null)            | int  |
| atitle (not null)              | varchar(128) |
| uid (作者学号, references)      | int |
| plate_1 (板块名称, 限制问题隶属于最多3个板块)   | varchar(20)    |
| plate_2                                       | varchar(20)    |
| plate_3                                       | varchar(20)    |
| context (not null)             | mediumtext |