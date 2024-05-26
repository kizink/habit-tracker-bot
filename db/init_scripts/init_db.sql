CREATE TABLE IF NOT EXISTS "users" (
  "user_id" integer PRIMARY KEY,
  "name" varchar
);


CREATE TABLE IF NOT EXISTS "habits" (
  "habit_id" bigserial PRIMARY KEY,
  "user_id" integer,
  "name" varchar,
  "description" varchar,
  "notification_time" varchar
);


CREATE TABLE IF NOT EXISTS "history" (
  "habit_id" integer,
  "action_time" varchar,
  "is_complited" bool
);


ALTER TABLE "habits" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("user_id");


ALTER TABLE "history" ADD FOREIGN KEY ("habit_id") REFERENCES "habits" ("habit_id") ON DELETE CASCADE;