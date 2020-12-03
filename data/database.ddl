BEGIN;
--
-- Create model CustomUser
--
CREATE TABLE "customer" ("password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "first_name" varchar(150) NOT NULL, "last_name" varchar(150) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "cid" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "email" varchar(254) NOT NULL UNIQUE, "friendly_name" varchar(40) NOT NULL, "address" varchar(40) NOT NULL, "phone" varchar(40) NOT NULL);
CREATE TABLE "customer_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "customuser_id" integer NOT NULL REFERENCES "customer" ("cid") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "customer_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "customuser_id" integer NOT NULL REFERENCES "customer" ("cid") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX "customer_groups_customuser_id_group_id_02648757_uniq" ON "customer_groups" ("customuser_id", "group_id");
CREATE INDEX "customer_groups_customuser_id_74ad332c" ON "customer_groups" ("customuser_id");
CREATE INDEX "customer_groups_group_id_902232a5" ON "customer_groups" ("group_id");
CREATE UNIQUE INDEX "customer_user_permissions_customuser_id_permission_id_c4999290_uniq" ON "customer_user_permissions" ("customuser_id", "permission_id");
CREATE INDEX "customer_user_permissions_customuser_id_af62db96" ON "customer_user_permissions" ("customuser_id");
CREATE INDEX "customer_user_permissions_permission_id_2c3e834e" ON "customer_user_permissions" ("permission_id");
COMMIT;
BEGIN;
--
-- Create model Breakfast
--
CREATE TABLE "breakfast" ("bid" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "b_type" varchar(20) NOT NULL, "b_price" real NOT NULL, "description" varchar(40) NOT NULL);
--
-- Create model BreakfastReview
--
CREATE TABLE "breakfast_review" ("rid" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "review_date" date NOT NULL, "rating" integer unsigned NOT NULL CHECK ("rating" >= 0), "text" varchar(40) NOT NULL);
--
-- Create model CreditCard
--
CREATE TABLE "credit_card" ("ccid" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "cc_number" varchar(20) NOT NULL, "cc_type" varchar(20) NOT NULL, "address" varchar(40) NOT NULL, "cv_code" varchar(4) NOT NULL, "exp_date" date NOT NULL, "name" varchar(40) NOT NULL);
--
-- Create model Hotel
--
CREATE TABLE "hotel" ("hotel_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "hotel_name" varchar(20) NOT NULL, "street" varchar(40) NOT NULL, "country" varchar(40) NOT NULL, "state" varchar(20) NOT NULL, "zip" varchar(5) NOT NULL);
--
-- Create model Reservation
--
CREATE TABLE "reservation" ("invoice_number" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "r_date" date NOT NULL, "cc_number" integer NOT NULL REFERENCES "credit_card" ("ccid") DEFERRABLE INITIALLY DEFERRED, "cid" integer NOT NULL REFERENCES "customer" ("cid") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model ReservationService
--
CREATE TABLE "rresv_service" ("rs_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "sprice" real NOT NULL, "rr_id" integer NOT NULL REFERENCES "reservation" ("invoice_number") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Room
--
CREATE TABLE "room" ("room_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "room_no" varchar(10) NOT NULL, "room_type" varchar(20) NOT NULL, "price" real NOT NULL, "description" varchar(40) NOT NULL, "floor" integer unsigned NOT NULL CHECK ("floor" >= 0), "capacity" integer unsigned NOT NULL CHECK ("capacity" >= 0), "hotel_id" integer NOT NULL REFERENCES "hotel" ("hotel_id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model ServiceReview
--
CREATE TABLE "service_review" ("rid" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "review_date" date NOT NULL, "rating" integer unsigned NOT NULL CHECK ("rating" >= 0), "text" varchar(40) NOT NULL, "cid" integer NOT NULL REFERENCES "customer" ("cid") DEFERRABLE INITIALLY DEFERRED, "sid" integer NOT NULL REFERENCES "rresv_service" ("rs_id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Service
--
CREATE TABLE "service" ("sid" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "s_type" varchar(20) NOT NULL, "s_price" real NOT NULL, "hotel_id" integer NOT NULL REFERENCES "hotel" ("hotel_id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model RoomReview
--
CREATE TABLE "room_review" ("rid" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "review_date" date NULL, "rating" integer unsigned NOT NULL CHECK ("rating" >= 0), "text" varchar(40) NOT NULL, "cid" integer NOT NULL REFERENCES "customer" ("cid") DEFERRABLE INITIALLY DEFERRED, "room_id" integer NOT NULL REFERENCES "room" ("room_id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model RoomReservation
--
CREATE TABLE "room_reservation" ("rr_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "check_in_date" date NOT NULL, "check_out_date" date NOT NULL, "hotel_id" integer NOT NULL REFERENCES "hotel" ("hotel_id") DEFERRABLE INITIALLY DEFERRED, "invoice_number" integer NOT NULL REFERENCES "reservation" ("invoice_number") DEFERRABLE INITIALLY DEFERRED, "room_no" integer NOT NULL REFERENCES "room" ("room_id") DEFERRABLE INITIALLY DEFERRED);
--
-- Add field sid to reservationservice
--
CREATE TABLE "new__rresv_service" ("rs_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "sprice" real NOT NULL, "rr_id" integer NOT NULL REFERENCES "reservation" ("invoice_number") DEFERRABLE INITIALLY DEFERRED, "sid" integer NOT NULL REFERENCES "service" ("sid") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__rresv_service" ("rs_id", "sprice", "rr_id", "sid") SELECT "rs_id", "sprice", "rr_id", NULL FROM "rresv_service";
DROP TABLE "rresv_service";
ALTER TABLE "new__rresv_service" RENAME TO "rresv_service";
CREATE INDEX "reservation_cc_number_d939d41c" ON "reservation" ("cc_number");
CREATE INDEX "reservation_cid_582e16c2" ON "reservation" ("cid");
CREATE INDEX "room_hotel_id_9bc4d861" ON "room" ("hotel_id");
CREATE INDEX "service_review_cid_12575593" ON "service_review" ("cid");
CREATE INDEX "service_review_sid_fe847c50" ON "service_review" ("sid");
CREATE INDEX "service_hotel_id_5a184fee" ON "service" ("hotel_id");
CREATE INDEX "room_review_cid_657c5f74" ON "room_review" ("cid");
CREATE INDEX "room_review_room_id_aca2e2fc" ON "room_review" ("room_id");
CREATE INDEX "room_reservation_hotel_id_1e997af2" ON "room_reservation" ("hotel_id");
CREATE INDEX "room_reservation_invoice_number_9ed5b516" ON "room_reservation" ("invoice_number");
CREATE INDEX "room_reservation_room_no_c5f42443" ON "room_reservation" ("room_no");
CREATE INDEX "rresv_service_rr_id_84b453f1" ON "rresv_service" ("rr_id");
CREATE INDEX "rresv_service_sid_6035fdd5" ON "rresv_service" ("sid");
--
-- Create model ReservationBreakfast
--
CREATE TABLE "rresv_breakfast" ("rb_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nooforders" integer unsigned NOT NULL CHECK ("nooforders" >= 0), "bid" integer NOT NULL REFERENCES "breakfast" ("bid") DEFERRABLE INITIALLY DEFERRED, "rr_id" integer NOT NULL REFERENCES "reservation" ("invoice_number") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model DiscountedRoom
--
CREATE TABLE "discounted_room" ("dr_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "discount" real NOT NULL, "start_date" date NOT NULL, "end_date" date NOT NULL, "room_id" integer NOT NULL REFERENCES "room" ("room_id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create constraint unique creditcard on model creditcard
--
CREATE TABLE "new__credit_card" ("ccid" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "cc_number" varchar(20) NOT NULL, "cc_type" varchar(20) NOT NULL, "address" varchar(40) NOT NULL, "cv_code" varchar(4) NOT NULL, "exp_date" date NOT NULL, "name" varchar(40) NOT NULL, CONSTRAINT "unique creditcard" UNIQUE ("cc_number"));
INSERT INTO "new__credit_card" ("ccid", "cc_number", "cc_type", "address", "cv_code", "exp_date", "name") SELECT "ccid", "cc_number", "cc_type", "address", "cv_code", "exp_date", "name" FROM "credit_card";
DROP TABLE "credit_card";
ALTER TABLE "new__credit_card" RENAME TO "credit_card";
CREATE INDEX "rresv_breakfast_bid_c76a73f5" ON "rresv_breakfast" ("bid");
CREATE INDEX "rresv_breakfast_rr_id_471482c8" ON "rresv_breakfast" ("rr_id");
CREATE INDEX "discounted_room_room_id_df002d73" ON "discounted_room" ("room_id");
--
-- Add field bid to breakfastreview
--
CREATE TABLE "new__breakfast_review" ("rid" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "review_date" date NOT NULL, "rating" integer unsigned NOT NULL CHECK ("rating" >= 0), "text" varchar(40) NOT NULL, "bid" integer NOT NULL REFERENCES "rresv_breakfast" ("rb_id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__breakfast_review" ("rid", "review_date", "rating", "text", "bid") SELECT "rid", "review_date", "rating", "text", NULL FROM "breakfast_review";
DROP TABLE "breakfast_review";
ALTER TABLE "new__breakfast_review" RENAME TO "breakfast_review";
CREATE INDEX "breakfast_review_bid_85ce83af" ON "breakfast_review" ("bid");
--
-- Add field cid to breakfastreview
--
CREATE TABLE "new__breakfast_review" ("rid" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "review_date" date NOT NULL, "rating" integer unsigned NOT NULL CHECK ("rating" >= 0), "text" varchar(40) NOT NULL, "bid" integer NOT NULL REFERENCES "rresv_breakfast" ("rb_id") DEFERRABLE INITIALLY DEFERRED, "cid" integer NOT NULL REFERENCES "customer" ("cid") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__breakfast_review" ("rid", "review_date", "rating", "text", "bid", "cid") SELECT "rid", "review_date", "rating", "text", "bid", NULL FROM "breakfast_review";
DROP TABLE "breakfast_review";
ALTER TABLE "new__breakfast_review" RENAME TO "breakfast_review";
CREATE INDEX "breakfast_review_bid_85ce83af" ON "breakfast_review" ("bid");
CREATE INDEX "breakfast_review_cid_376cf138" ON "breakfast_review" ("cid");
--
-- Add field hotel_id to breakfast
--
CREATE TABLE "new__breakfast" ("bid" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "b_type" varchar(20) NOT NULL, "b_price" real NOT NULL, "description" varchar(40) NOT NULL, "hotel_id" integer NOT NULL REFERENCES "hotel" ("hotel_id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__breakfast" ("bid", "b_type", "b_price", "description", "hotel_id") SELECT "bid", "b_type", "b_price", "description", NULL FROM "breakfast";
DROP TABLE "breakfast";
ALTER TABLE "new__breakfast" RENAME TO "breakfast";
CREATE INDEX "breakfast_hotel_id_410b714e" ON "breakfast" ("hotel_id");
--
-- Create constraint unique servicereview on model servicereview
--
CREATE TABLE "new__service_review" ("rid" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "review_date" date NOT NULL, "rating" integer unsigned NOT NULL CHECK ("rating" >= 0), "text" varchar(40) NOT NULL, "cid" integer NOT NULL REFERENCES "customer" ("cid") DEFERRABLE INITIALLY DEFERRED, "sid" integer NOT NULL REFERENCES "rresv_service" ("rs_id") DEFERRABLE INITIALLY DEFERRED, CONSTRAINT "unique servicereview" UNIQUE ("cid", "sid"));
INSERT INTO "new__service_review" ("rid", "review_date", "rating", "text", "cid", "sid") SELECT "rid", "review_date", "rating", "text", "cid", "sid" FROM "service_review";
DROP TABLE "service_review";
ALTER TABLE "new__service_review" RENAME TO "service_review";
CREATE INDEX "service_review_cid_12575593" ON "service_review" ("cid");
CREATE INDEX "service_review_sid_fe847c50" ON "service_review" ("sid");
--
-- Create constraint unique hotelservicetype on model service
--
CREATE TABLE "new__service" ("sid" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "s_type" varchar(20) NOT NULL, "s_price" real NOT NULL, "hotel_id" integer NOT NULL REFERENCES "hotel" ("hotel_id") DEFERRABLE INITIALLY DEFERRED, CONSTRAINT "unique hotelservicetype" UNIQUE ("hotel_id", "s_type"));
INSERT INTO "new__service" ("sid", "s_type", "s_price", "hotel_id") SELECT "sid", "s_type", "s_price", "hotel_id" FROM "service";
DROP TABLE "service";
ALTER TABLE "new__service" RENAME TO "service";
CREATE INDEX "service_hotel_id_5a184fee" ON "service" ("hotel_id");
--
-- Create constraint unique roomreview on model roomreview
--
CREATE TABLE "new__room_review" ("rid" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "review_date" date NULL, "rating" integer unsigned NOT NULL CHECK ("rating" >= 0), "text" varchar(40) NOT NULL, "cid" integer NOT NULL REFERENCES "customer" ("cid") DEFERRABLE INITIALLY DEFERRED, "room_id" integer NOT NULL REFERENCES "room" ("room_id") DEFERRABLE INITIALLY DEFERRED, CONSTRAINT "unique roomreview" UNIQUE ("cid", "room_id"));
INSERT INTO "new__room_review" ("rid", "review_date", "rating", "text", "cid", "room_id") SELECT "rid", "review_date", "rating", "text", "cid", "room_id" FROM "room_review";
DROP TABLE "room_review";
ALTER TABLE "new__room_review" RENAME TO "room_review";
CREATE INDEX "room_review_cid_657c5f74" ON "room_review" ("cid");
CREATE INDEX "room_review_room_id_aca2e2fc" ON "room_review" ("room_id");
--
-- Create constraint unique roomreservation on model roomreservation
--
CREATE TABLE "new__room_reservation" ("rr_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "check_in_date" date NOT NULL, "check_out_date" date NOT NULL, "hotel_id" integer NOT NULL REFERENCES "hotel" ("hotel_id") DEFERRABLE INITIALLY DEFERRED, "invoice_number" integer NOT NULL REFERENCES "reservation" ("invoice_number") DEFERRABLE INITIALLY DEFERRED, "room_no" integer NOT NULL REFERENCES "room" ("room_id") DEFERRABLE INITIALLY DEFERRED, CONSTRAINT "unique roomreservation" UNIQUE ("invoice_number", "hotel_id", "room_no", "check_in_date"));
INSERT INTO "new__room_reservation" ("rr_id", "check_in_date", "check_out_date", "hotel_id", "invoice_number", "room_no") SELECT "rr_id", "check_in_date", "check_out_date", "hotel_id", "invoice_number", "room_no" FROM "room_reservation";
DROP TABLE "room_reservation";
ALTER TABLE "new__room_reservation" RENAME TO "room_reservation";
CREATE INDEX "room_reservation_hotel_id_1e997af2" ON "room_reservation" ("hotel_id");
CREATE INDEX "room_reservation_invoice_number_9ed5b516" ON "room_reservation" ("invoice_number");
CREATE INDEX "room_reservation_room_no_c5f42443" ON "room_reservation" ("room_no");
--
-- Create constraint unique hotelroomid on model room
--
CREATE TABLE "new__room" ("room_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "room_no" varchar(10) NOT NULL, "room_type" varchar(20) NOT NULL, "price" real NOT NULL, "description" varchar(40) NOT NULL, "floor" integer unsigned NOT NULL CHECK ("floor" >= 0), "capacity" integer unsigned NOT NULL CHECK ("capacity" >= 0), "hotel_id" integer NOT NULL REFERENCES "hotel" ("hotel_id") DEFERRABLE INITIALLY DEFERRED, CONSTRAINT "unique hotelroomid" UNIQUE ("hotel_id", "room_no"));
INSERT INTO "new__room" ("room_id", "room_no", "room_type", "price", "description", "floor", "capacity", "hotel_id") SELECT "room_id", "room_no", "room_type", "price", "description", "floor", "capacity", "hotel_id" FROM "room";
DROP TABLE "room";
ALTER TABLE "new__room" RENAME TO "room";
CREATE INDEX "room_hotel_id_9bc4d861" ON "room" ("hotel_id");
--
-- Create constraint unique roomresservice on model reservationservice
--
CREATE TABLE "new__rresv_service" ("rs_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "sprice" real NOT NULL, "rr_id" integer NOT NULL REFERENCES "reservation" ("invoice_number") DEFERRABLE INITIALLY DEFERRED, "sid" integer NOT NULL REFERENCES "service" ("sid") DEFERRABLE INITIALLY DEFERRED, CONSTRAINT "unique roomresservice" UNIQUE ("sid", "rr_id"));
INSERT INTO "new__rresv_service" ("rs_id", "sprice", "rr_id", "sid") SELECT "rs_id", "sprice", "rr_id", "sid" FROM "rresv_service";
DROP TABLE "rresv_service";
ALTER TABLE "new__rresv_service" RENAME TO "rresv_service";
CREATE INDEX "rresv_service_rr_id_84b453f1" ON "rresv_service" ("rr_id");
CREATE INDEX "rresv_service_sid_6035fdd5" ON "rresv_service" ("sid");
--
-- Create constraint unique roomresbreakfast on model reservationbreakfast
--
CREATE TABLE "new__rresv_breakfast" ("rb_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nooforders" integer unsigned NOT NULL CHECK ("nooforders" >= 0), "bid" integer NOT NULL REFERENCES "breakfast" ("bid") DEFERRABLE INITIALLY DEFERRED, "rr_id" integer NOT NULL REFERENCES "reservation" ("invoice_number") DEFERRABLE INITIALLY DEFERRED, CONSTRAINT "unique roomresbreakfast" UNIQUE ("bid", "rr_id"));
INSERT INTO "new__rresv_breakfast" ("rb_id", "nooforders", "bid", "rr_id") SELECT "rb_id", "nooforders", "bid", "rr_id" FROM "rresv_breakfast";
DROP TABLE "rresv_breakfast";
ALTER TABLE "new__rresv_breakfast" RENAME TO "rresv_breakfast";
CREATE INDEX "rresv_breakfast_bid_c76a73f5" ON "rresv_breakfast" ("bid");
CREATE INDEX "rresv_breakfast_rr_id_471482c8" ON "rresv_breakfast" ("rr_id");
--
-- Create constraint unique reservation on model reservation
--
CREATE TABLE "new__reservation" ("invoice_number" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "r_date" date NOT NULL, "cc_number" integer NOT NULL REFERENCES "credit_card" ("ccid") DEFERRABLE INITIALLY DEFERRED, "cid" integer NOT NULL REFERENCES "customer" ("cid") DEFERRABLE INITIALLY DEFERRED, CONSTRAINT "unique reservation" UNIQUE ("cc_number", "r_date"));
INSERT INTO "new__reservation" ("invoice_number", "r_date", "cc_number", "cid") SELECT "invoice_number", "r_date", "cc_number", "cid" FROM "reservation";
DROP TABLE "reservation";
ALTER TABLE "new__reservation" RENAME TO "reservation";
CREATE INDEX "reservation_cc_number_d939d41c" ON "reservation" ("cc_number");
CREATE INDEX "reservation_cid_582e16c2" ON "reservation" ("cid");
--
-- Create constraint unique breakfastreview on model breakfastreview
--
CREATE TABLE "new__breakfast_review" ("rid" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "review_date" date NOT NULL, "rating" integer unsigned NOT NULL CHECK ("rating" >= 0), "text" varchar(40) NOT NULL, "bid" integer NOT NULL REFERENCES "rresv_breakfast" ("rb_id") DEFERRABLE INITIALLY DEFERRED, "cid" integer NOT NULL REFERENCES "customer" ("cid") DEFERRABLE INITIALLY DEFERRED, CONSTRAINT "unique breakfastreview" UNIQUE ("cid", "bid"));
INSERT INTO "new__breakfast_review" ("rid", "review_date", "rating", "text", "bid", "cid") SELECT "rid", "review_date", "rating", "text", "bid", "cid" FROM "breakfast_review";
DROP TABLE "breakfast_review";
ALTER TABLE "new__breakfast_review" RENAME TO "breakfast_review";
CREATE INDEX "breakfast_review_bid_85ce83af" ON "breakfast_review" ("bid");
CREATE INDEX "breakfast_review_cid_376cf138" ON "breakfast_review" ("cid");
--
-- Create constraint unique hotelbreakfasttype on model breakfast
--
CREATE TABLE "new__breakfast" ("bid" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "b_type" varchar(20) NOT NULL, "b_price" real NOT NULL, "description" varchar(40) NOT NULL, "hotel_id" integer NOT NULL REFERENCES "hotel" ("hotel_id") DEFERRABLE INITIALLY DEFERRED, CONSTRAINT "unique hotelbreakfasttype" UNIQUE ("hotel_id", "b_type"));
INSERT INTO "new__breakfast" ("bid", "b_type", "b_price", "description", "hotel_id") SELECT "bid", "b_type", "b_price", "description", "hotel_id" FROM "breakfast";
DROP TABLE "breakfast";
ALTER TABLE "new__breakfast" RENAME TO "breakfast";
CREATE INDEX "breakfast_hotel_id_410b714e" ON "breakfast" ("hotel_id");
COMMIT;
