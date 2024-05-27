CREATE TABLE IF NOT EXISTS "user" (
  "id" integer PRIMARY KEY,
  "name" varchar
);


CREATE TABLE IF NOT EXISTS "habit" (
  "id" bigserial PRIMARY KEY,
  "user_id" integer,
  "name" varchar,
  "description" varchar,
  "notification_time" time
);


CREATE TABLE IF NOT EXISTS "action" (
  "habit_id" integer,
  "action_time" timestamp,
  "is_complited" bool
);


ALTER TABLE "habit" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("id") ON DELETE CASCADE;


ALTER TABLE "action" ADD FOREIGN KEY ("habit_id") REFERENCES "habit" ("id") ON DELETE CASCADE;
