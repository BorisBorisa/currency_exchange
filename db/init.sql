CREATE TABLE "users" (
	"id" INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	"username" VARCHAR(50) NOT NULL UNIQUE,
	"email" VARCHAR(255) NOT NULL UNIQUE,
	"password_hash" VARCHAR(60) NOT NULL,
	"disabled" BOOLEAN NOT NULL DEFAULT FALSE,
	"created_at" TIMESTAMP NOT NULL DEFAULT current_timestamp
);

CREATE TABLE "user_profiles" (
	"id" INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    "birth_date" DATE,
	"avatar_url" VARCHAR(255),
	"phone" VARCHAR(20),
	"gender" VARCHAR(10)
);


CREATE TABLE "currencies" (
    "id" INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "currency_code" VARCHAR(3) NOT NULL,
    "currency_name" VARCHAR(50) NOT NULL
);
