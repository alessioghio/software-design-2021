CREATE TABLE IF NOT EXISTS public.administrator
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    "lastName" character varying(100) COLLATE pg_catalog."default" NOT NULL,
    email character varying(100) COLLATE pg_catalog."default" NOT NULL,
    username character varying(100) COLLATE pg_catalog."default" NOT NULL,
    password character varying(100) COLLATE pg_catalog."default" NOT NULL,
    "userType" character varying(6) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT administrator_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.adminurl
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    name character varying(200) COLLATE pg_catalog."default",
    url character varying(200) COLLATE pg_catalog."default",
    admin_id bigint,
    CONSTRAINT "PK_adminurl" PRIMARY KEY (id),
    CONSTRAINT admin_id FOREIGN KEY (admin_id)
        REFERENCES public.administrator (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

CREATE TABLE IF NOT EXISTS public.supply
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    price numeric NOT NULL,
    quantity integer,
    category character varying(100) COLLATE pg_catalog."default" NOT NULL,
    visibility boolean NOT NULL,
    unit character varying(5) COLLATE pg_catalog."default" NOT NULL,
    description character varying(500) COLLATE pg_catalog."default",
    admin_id bigint,
    CONSTRAINT "PK_supply" PRIMARY KEY (id),
    CONSTRAINT admin_id FOREIGN KEY (admin_id)
        REFERENCES public.administrator (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS public."shoppingCart"
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    datetime date NOT NULL,
    client_id bigint,
    supply_id bigint,
    quantity integer,
    CONSTRAINT "PK_shoppingCart" PRIMARY KEY (id),
    CONSTRAINT supply_id FOREIGN KEY (supply_id)
        REFERENCES public.supply (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS public.client
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    "lastName" character varying(100) COLLATE pg_catalog."default" NOT NULL,
    email character varying(100) COLLATE pg_catalog."default" NOT NULL,
    username character varying(100) COLLATE pg_catalog."default" NOT NULL,
    password character varying(100) COLLATE pg_catalog."default" NOT NULL,
    "userType" character varying(6) COLLATE pg_catalog."default" NOT NULL,
    "shoppingCart_id" bigint,
    CONSTRAINT client_pkey PRIMARY KEY (id),
    CONSTRAINT "shoppingCart_id" FOREIGN KEY ("shoppingCart_id")
        REFERENCES public."shoppingCart" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

CREATE TABLE IF NOT EXISTS public.recipe
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    name character varying(100) COLLATE pg_catalog."default",
    quantity integer,
    supply_id bigint,
    admin_id bigint NOT NULL,
    price integer NOT NULL,
    description character varying(500) COLLATE pg_catalog."default",
    CONSTRAINT "PK_recipe" PRIMARY KEY (id),
    CONSTRAINT admin_id FOREIGN KEY (admin_id)
        REFERENCES public.administrator (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS public.transaction
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    datetime date NOT NULL,
    admin_id bigint,
    client_id bigint,
    price numeric,
    CONSTRAINT "PK_transactions" PRIMARY KEY (id),
    CONSTRAINT admin_id FOREIGN KEY (admin_id)
        REFERENCES public.administrator (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT client_id FOREIGN KEY (client_id)
        REFERENCES public.client (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);