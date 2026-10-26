-- public.excursion_plan_templates определение

-- Drop table

-- DROP TABLE public.excursion_plan_templates;

CREATE TABLE public.excursion_plan_templates (
	id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
	title varchar(200) NOT NULL,
	description text NULL,
	duration_minutes int4 NULL,
	CONSTRAINT excursion_plan_templates_duration_minutes_check CHECK ((duration_minutes > 0)),
	CONSTRAINT excursion_plan_templates_id_not_null NOT NULL id,
	CONSTRAINT excursion_plan_templates_pkey PRIMARY KEY (id),
	CONSTRAINT excursion_plan_templates_title_not_null NOT NULL title
);


-- public.organizations определение

-- Drop table

-- DROP TABLE public.organizations;

CREATE TABLE public.organizations (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	"name" varchar(200) NOT NULL,
	email varchar(254) NOT NULL,
	phone varchar(16) NOT NULL,
	password_hash varchar(100) NOT NULL,
	description text NULL,
	website varchar(255) NULL,
	CONSTRAINT organizations_email_format CHECK (((email)::text ~* '^[^@\s]+@[^@\s]+\.[^@\s]+$'::text)),
	CONSTRAINT organizations_email_not_null NOT NULL email,
	CONSTRAINT organizations_id_not_null NOT NULL id,
	CONSTRAINT organizations_name_not_null NOT NULL name,
	CONSTRAINT organizations_password_hash_not_null NOT NULL password_hash,
	CONSTRAINT organizations_phone_format CHECK (((phone)::text ~ '^\+[1-9][0-9]{9,14}$'::text)),
	CONSTRAINT organizations_phone_not_null NOT NULL phone,
	CONSTRAINT organizations_pkey PRIMARY KEY (id)
);


-- public.themes определение

-- Drop table

-- DROP TABLE public.themes;

CREATE TABLE public.themes (
	id int2 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 32767 START 1 CACHE 1 NO CYCLE) NOT NULL,
	"name" varchar(80) NOT NULL,
	CONSTRAINT themes_id_not_null NOT NULL id,
	CONSTRAINT themes_name_key UNIQUE (name),
	CONSTRAINT themes_name_not_null NOT NULL name,
	CONSTRAINT themes_pkey PRIMARY KEY (id)
);


-- public.users определение

-- Drop table

-- DROP TABLE public.users;

CREATE TABLE public.users (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	full_name varchar(120) NOT NULL,
	email varchar(254) NOT NULL,
	phone varchar(16) NOT NULL,
	password_hash varchar(100) NOT NULL,
	CONSTRAINT users_email_format CHECK (((email)::text ~* '^[^@\s]+@[^@\s]+\.[^@\s]+$'::text)),
	CONSTRAINT users_email_not_null NOT NULL email,
	CONSTRAINT users_full_name_not_null NOT NULL full_name,
	CONSTRAINT users_id_not_null NOT NULL id,
	CONSTRAINT users_password_hash_not_null NOT NULL password_hash,
	CONSTRAINT users_phone_format CHECK (((phone)::text ~ '^\+[1-9][0-9]{9,14}$'::text)),
	CONSTRAINT users_phone_not_null NOT NULL phone,
	CONSTRAINT users_pkey PRIMARY KEY (id)
);


-- public.guides определение

-- Drop table

-- DROP TABLE public.guides;

CREATE TABLE public.guides (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	organization_id int8 NOT NULL,
	full_name varchar(120) NOT NULL,
	bio text NULL,
	photo_url text NULL,
	languages _text DEFAULT '{rus}'::text[] NOT NULL,
	experience_years int2 NULL,
	rating_avg numeric(3, 2) DEFAULT 0 NOT NULL,
	reviews_count int4 DEFAULT 0 NOT NULL,
	CONSTRAINT guides_experience_years_check CHECK ((experience_years >= 0)),
	CONSTRAINT guides_full_name_not_null NOT NULL full_name,
	CONSTRAINT guides_id_not_null NOT NULL id,
	CONSTRAINT guides_id_organization_id_key UNIQUE (id, organization_id),
	CONSTRAINT guides_languages_not_null NOT NULL languages,
	CONSTRAINT guides_organization_id_not_null NOT NULL organization_id,
	CONSTRAINT guides_pkey PRIMARY KEY (id),
	CONSTRAINT guides_rating_avg_not_null NOT NULL rating_avg,
	CONSTRAINT guides_reviews_count_not_null NOT NULL reviews_count,
	CONSTRAINT guides_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id) ON DELETE CASCADE
);


-- public.sessions определение

-- Drop table

-- DROP TABLE public.sessions;

CREATE TABLE public.sessions (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	user_id int8 NULL,
	organization_id int8 NULL,
	refresh_token_hash bpchar(64) NOT NULL,
	user_agent text NULL,
	ip_address inet NULL,
	CONSTRAINT sessions_id_not_null NOT NULL id,
	CONSTRAINT sessions_one_owner CHECK ((num_nonnulls(user_id, organization_id) = 1)),
	CONSTRAINT sessions_pkey PRIMARY KEY (id),
	CONSTRAINT sessions_refresh_token_hash_key UNIQUE (refresh_token_hash),
	CONSTRAINT sessions_refresh_token_hash_not_null NOT NULL refresh_token_hash,
	CONSTRAINT sessions_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id) ON DELETE CASCADE,
	CONSTRAINT sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE
);


-- public.excursions определение

-- Drop table

-- DROP TABLE public.excursions;

CREATE TABLE public.excursions (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	organization_id int8 NOT NULL,
	guide_id int8 NOT NULL,
	plan_template_id int4 NULL,
	title varchar(200) NOT NULL,
	description text NULL,
	price numeric(10, 2) NOT NULL,
	duration_minutes int4 NOT NULL,
	max_participants int2 NOT NULL,
	meeting_point_address text NOT NULL,
	meeting_point_note text NULL,
	meeting_lat numeric(9, 6) NOT NULL,
	meeting_lng numeric(9, 6) NOT NULL,
	rating_avg numeric(3, 2) DEFAULT 0 NOT NULL,
	reviews_count int4 DEFAULT 0 NOT NULL,
	search_vector tsvector GENERATED ALWAYS AS (to_tsvector('russian'::regconfig, (COALESCE(title, ''::character varying)::text || ' '::text) || COALESCE(description, ''::text))) STORED NULL,
	CONSTRAINT excursions_duration_minutes_check CHECK ((duration_minutes > 0)),
	CONSTRAINT excursions_duration_minutes_not_null NOT NULL duration_minutes,
	CONSTRAINT excursions_guide_id_not_null NOT NULL guide_id,
	CONSTRAINT excursions_id_not_null NOT NULL id,
	CONSTRAINT excursions_max_participants_check CHECK ((max_participants > 0)),
	CONSTRAINT excursions_max_participants_not_null NOT NULL max_participants,
	CONSTRAINT excursions_meeting_lat_check CHECK (((meeting_lat >= ('-90'::integer)::numeric) AND (meeting_lat <= (90)::numeric))),
	CONSTRAINT excursions_meeting_lat_not_null NOT NULL meeting_lat,
	CONSTRAINT excursions_meeting_lng_check CHECK (((meeting_lng >= ('-180'::integer)::numeric) AND (meeting_lng <= (180)::numeric))),
	CONSTRAINT excursions_meeting_lng_not_null NOT NULL meeting_lng,
	CONSTRAINT excursions_meeting_point_address_not_null NOT NULL meeting_point_address,
	CONSTRAINT excursions_organization_id_not_null NOT NULL organization_id,
	CONSTRAINT excursions_pkey PRIMARY KEY (id),
	CONSTRAINT excursions_price_check CHECK ((price >= (0)::numeric)),
	CONSTRAINT excursions_price_not_null NOT NULL price,
	CONSTRAINT excursions_rating_avg_not_null NOT NULL rating_avg,
	CONSTRAINT excursions_reviews_count_not_null NOT NULL reviews_count,
	CONSTRAINT excursions_title_not_null NOT NULL title,
	CONSTRAINT excursions_guide_id_organization_id_fkey FOREIGN KEY (guide_id,organization_id) REFERENCES public.guides(id,organization_id),
	CONSTRAINT excursions_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id) ON DELETE CASCADE,
	CONSTRAINT excursions_plan_template_id_fkey FOREIGN KEY (plan_template_id) REFERENCES public.excursion_plan_templates(id) ON DELETE SET NULL
);


-- public.favorites определение

-- Drop table

-- DROP TABLE public.favorites;

CREATE TABLE public.favorites (
	user_id int8 NOT NULL,
	excursion_id int8 NOT NULL,
	CONSTRAINT favorites_excursion_id_not_null NOT NULL excursion_id,
	CONSTRAINT favorites_pkey PRIMARY KEY (user_id, excursion_id),
	CONSTRAINT favorites_user_id_not_null NOT NULL user_id,
	CONSTRAINT favorites_excursion_id_fkey FOREIGN KEY (excursion_id) REFERENCES public.excursions(id) ON DELETE CASCADE,
	CONSTRAINT favorites_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE
);


-- public.excursion_photos определение

-- Drop table

-- DROP TABLE public.excursion_photos;

CREATE TABLE public.excursion_photos (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	excursion_id int8 NOT NULL,
	url text NOT NULL,
	CONSTRAINT excursion_photos_excursion_id_not_null NOT NULL excursion_id,
	CONSTRAINT excursion_photos_id_not_null NOT NULL id,
	CONSTRAINT excursion_photos_pkey PRIMARY KEY (id),
	CONSTRAINT excursion_photos_url_not_null NOT NULL url,
	CONSTRAINT excursion_photos_excursion_id_fkey FOREIGN KEY (excursion_id) REFERENCES public.excursions(id) ON DELETE CASCADE
);


-- public.excursion_sessions определение

-- Drop table

-- DROP TABLE public.excursion_sessions;

CREATE TABLE public.excursion_sessions (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	excursion_id int8 NOT NULL,
	starts_at timestamptz NOT NULL,
	seats_total int2 NOT NULL,
	status varchar(10) DEFAULT 'open'::character varying NOT NULL,
	CONSTRAINT excursion_sessions_excursion_id_not_null NOT NULL excursion_id,
	CONSTRAINT excursion_sessions_excursion_id_starts_at_key UNIQUE (excursion_id, starts_at),
	CONSTRAINT excursion_sessions_id_not_null NOT NULL id,
	CONSTRAINT excursion_sessions_pkey PRIMARY KEY (id),
	CONSTRAINT excursion_sessions_seats_total_check CHECK ((seats_total > 0)),
	CONSTRAINT excursion_sessions_seats_total_not_null NOT NULL seats_total,
	CONSTRAINT excursion_sessions_starts_at_not_null NOT NULL starts_at,
	CONSTRAINT excursion_sessions_status_check CHECK (((status)::text = ANY ((ARRAY['open'::character varying, 'closed'::character varying, 'cancelled'::character varying])::text[]))),
	CONSTRAINT excursion_sessions_status_not_null NOT NULL status,
	CONSTRAINT excursion_sessions_excursion_id_fkey FOREIGN KEY (excursion_id) REFERENCES public.excursions(id) ON DELETE CASCADE
);


-- public.excursion_themes определение

-- Drop table

-- DROP TABLE public.excursion_themes;

CREATE TABLE public.excursion_themes (
	excursion_id int8 NOT NULL,
	theme_id int2 NOT NULL,
	CONSTRAINT excursion_themes_excursion_id_not_null NOT NULL excursion_id,
	CONSTRAINT excursion_themes_pkey PRIMARY KEY (excursion_id, theme_id),
	CONSTRAINT excursion_themes_theme_id_not_null NOT NULL theme_id,
	CONSTRAINT excursion_themes_excursion_id_fkey FOREIGN KEY (excursion_id) REFERENCES public.excursions(id) ON DELETE CASCADE,
	CONSTRAINT excursion_themes_theme_id_fkey FOREIGN KEY (theme_id) REFERENCES public.themes(id) ON DELETE CASCADE
);


-- public.bookings определение

-- Drop table

-- DROP TABLE public.bookings;

CREATE TABLE public.bookings (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	user_id int8 NOT NULL,
	session_id int8 NOT NULL,
	seats int2 NOT NULL,
	total_price numeric(10, 2) NOT NULL,
	status varchar(10) DEFAULT 'pending'::character varying NOT NULL,
	payment_status varchar(10) DEFAULT 'unpaid'::character varying NOT NULL,
	"comment" text NULL,
	CONSTRAINT bookings_id_not_null NOT NULL id,
	CONSTRAINT bookings_payment_status_check CHECK (((payment_status)::text = ANY ((ARRAY['unpaid'::character varying, 'paid'::character varying, 'refunded'::character varying])::text[]))),
	CONSTRAINT bookings_payment_status_not_null NOT NULL payment_status,
	CONSTRAINT bookings_pkey PRIMARY KEY (id),
	CONSTRAINT bookings_seats_check CHECK ((seats > 0)),
	CONSTRAINT bookings_seats_not_null NOT NULL seats,
	CONSTRAINT bookings_session_id_not_null NOT NULL session_id,
	CONSTRAINT bookings_status_check CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'confirmed'::character varying, 'cancelled'::character varying, 'completed'::character varying])::text[]))),
	CONSTRAINT bookings_status_not_null NOT NULL status,
	CONSTRAINT bookings_total_price_check CHECK ((total_price >= (0)::numeric)),
	CONSTRAINT bookings_total_price_not_null NOT NULL total_price,
	CONSTRAINT bookings_user_id_not_null NOT NULL user_id,
	CONSTRAINT bookings_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.excursion_sessions(id) ON DELETE RESTRICT,
	CONSTRAINT bookings_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE RESTRICT
);


-- public.reviews определение

-- Drop table

-- DROP TABLE public.reviews;

CREATE TABLE public.reviews (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	booking_id int8 NOT NULL,
	user_id int8 NOT NULL,
	excursion_id int8 NOT NULL,
	guide_id int8 NOT NULL,
	rating int2 NOT NULL,
	"comment" text NOT NULL,
	CONSTRAINT reviews_booking_id_key UNIQUE (booking_id),
	CONSTRAINT reviews_booking_id_not_null NOT NULL booking_id,
	CONSTRAINT reviews_comment_check CHECK (((char_length(comment) >= 1) AND (char_length(comment) <= 2000))),
	CONSTRAINT reviews_comment_not_null NOT NULL comment,
	CONSTRAINT reviews_excursion_id_not_null NOT NULL excursion_id,
	CONSTRAINT reviews_guide_id_not_null NOT NULL guide_id,
	CONSTRAINT reviews_id_not_null NOT NULL id,
	CONSTRAINT reviews_pkey PRIMARY KEY (id),
	CONSTRAINT reviews_rating_check CHECK (((rating >= 1) AND (rating <= 5))),
	CONSTRAINT reviews_rating_not_null NOT NULL rating,
	CONSTRAINT reviews_user_id_not_null NOT NULL user_id,
	CONSTRAINT reviews_booking_id_fkey FOREIGN KEY (booking_id) REFERENCES public.bookings(id) ON DELETE RESTRICT,
	CONSTRAINT reviews_excursion_id_fkey FOREIGN KEY (excursion_id) REFERENCES public.excursions(id) ON DELETE CASCADE,
	CONSTRAINT reviews_guide_id_fkey FOREIGN KEY (guide_id) REFERENCES public.guides(id) ON DELETE CASCADE,
	CONSTRAINT reviews_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE RESTRICT
);