drop table if exists hashes;
create table hashes (
  id integer primary key autoincrement,
  hash text not null,
  message text not null
);
