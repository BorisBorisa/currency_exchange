CREATE TABLE "users" (
	"id" INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	"email" VARCHAR(255) NOT NULL,
	"password_hash" VARCHAR(60) NOT NULL,
	"disabled" BOOLEAN NOT NULL DEFAULT FALSE,
	"created_at" TIMESTAMP NOT NULL DEFAULT current_timestamp
);

CREATE TABLE "user_profiles" (
	"id" INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
	"first_name" VARCHAR(50) NOT NULL,
	"last_name" VARCHAR(50) NOT NULL,
	"avatar_url" VARCHAR(255),
	"phone" VARCHAR(20),
	"date_of_birth" DATE NOT NULL, 
	"gender" VARCHAR(10) NOT NULL
);