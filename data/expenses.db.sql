BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "categories" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL UNIQUE,
	"is_custom"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "expenses" (
	"id"	INTEGER,
	"date"	TEXT NOT NULL,
	"amount"	REAL NOT NULL,
	"category_id"	INTEGER NOT NULL,
	"description"	TEXT,
	"is_recurring"	INTEGER NOT NULL DEFAULT 0,
	"attachment_path"	TEXT,
	"attachment_type"	TEXT,
	"analysis_data"	TEXT,
	"analysis_summary"	TEXT,
	"created_at"	TEXT NOT NULL,
	"recurring_expense_id"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("category_id") REFERENCES "categories"("id"),
	FOREIGN KEY("recurring_expense_id") REFERENCES "recurring_expenses"("id")
);
CREATE TABLE IF NOT EXISTS "recurring_expenses" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"amount"	REAL NOT NULL,
	"category_id"	INTEGER NOT NULL,
	"frequency"	TEXT NOT NULL,
	"start_date"	TEXT NOT NULL,
	"end_date"	TEXT,
	"description"	TEXT,
	"attachment_path"	TEXT,
	"attachment_type"	TEXT,
	"last_generated_date"	TEXT,
	"created_at"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("category_id") REFERENCES "categories"("id")
);
CREATE INDEX IF NOT EXISTS "idx_expenses_recurring_id" ON "expenses" (
	"recurring_expense_id"
);
COMMIT;
