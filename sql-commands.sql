CREATE TABLE IF NOT EXISTS public."user"
(
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    "lastName" character varying(100) COLLATE pg_catalog."default" NOT NULL,
    email character varying(100) COLLATE pg_catalog."default" NOT NULL,
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    password character varying(30) COLLATE pg_catalog."default" NOT NULL,
    id bigint NOT NULL DEFAULT nextval('user_id_seq'::regclass),
    CONSTRAINT user_pkey PRIMARY KEY (id)
)

CREATE TABLE IF NOT EXISTS public.transaction
(
    id bigint NOT NULL DEFAULT nextval('transactions_id_seq'::regclass),
    datetime date NOT NULL,
    unit character varying(5) COLLATE pg_catalog."default" NOT NULL,
    quantity integer NOT NULL,
    supply_id bigint,
    recipe_id bigint,
    admin_id bigint,
    "shoppingCart_id" bigint,
    CONSTRAINT "PK_transactions" PRIMARY KEY (id)
)

CREATE TABLE IF NOT EXISTS public.supply
(
    id bigint NOT NULL DEFAULT nextval('supply_id_seq'::regclass),
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    price numeric NOT NULL,
    quantity integer NOT NULL,
    category character varying(100) COLLATE pg_catalog."default" NOT NULL,
    visibility boolean NOT NULL,
    CONSTRAINT "PK_supply" PRIMARY KEY (id)
)

CREATE TABLE IF NOT EXISTS public."shoppingCart"
(
    id bigint NOT NULL DEFAULT nextval('"shoppingCart_id_seq"'::regclass),
    datetime date NOT NULL,
    client_id bigint,
    supply_id bigint,
    CONSTRAINT "PK_shoppingCart" PRIMARY KEY (id),
    CONSTRAINT "unique_shoppingCart" UNIQUE (client_id),
    CONSTRAINT client_id FOREIGN KEY (client_id)
        REFERENCES public.client (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT supply_id FOREIGN KEY (supply_id)
        REFERENCES public.supply (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

CREATE TABLE IF NOT EXISTS public.recipe
(
    id bigint NOT NULL DEFAULT nextval('recipe_id_seq'::regclass),
    name character varying(100) COLLATE pg_catalog."default",
    quantity integer,
    supply_id bigint,
    CONSTRAINT "PK_recipe" PRIMARY KEY (id)
)

CREATE TABLE IF NOT EXISTS public.client
(
    -- Inherited from table public."user": id bigint NOT NULL DEFAULT nextval('client_id_seq'::regclass),
    "shoppingCart_id" bigint,
    -- Inherited from table public."user": name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    -- Inherited from table public."user": "lastName" character varying(100) COLLATE pg_catalog."default" NOT NULL,
    -- Inherited from table public."user": email character varying(100) COLLATE pg_catalog."default" NOT NULL,
    -- Inherited from table public."user": username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    -- Inherited from table public."user": password character varying(30) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "PK_client" PRIMARY KEY (id),
    CONSTRAINT "shoppingCart_id" FOREIGN KEY ("shoppingCart_id")
        REFERENCES public."shoppingCart" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)
    INHERITS (public."user")

CREATE TABLE IF NOT EXISTS public.administrator
(
    -- Inherited from table public."user": id bigint NOT NULL DEFAULT nextval('administrator_id_seq'::regclass),
    -- Inherited from table public."user": name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    -- Inherited from table public."user": "lastName" character varying(100) COLLATE pg_catalog."default" NOT NULL,
    -- Inherited from table public."user": email character varying(100) COLLATE pg_catalog."default" NOT NULL,
    -- Inherited from table public."user": username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    -- Inherited from table public."user": password character varying(30) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT administrator_pkey PRIMARY KEY (id),
    CONSTRAINT unique_administrator UNIQUE (username)
)
    INHERITS (public."user")

CREATE TABLE IF NOT EXISTS public."adminURL"
(
    id bigint NOT NULL DEFAULT nextval('"adminURL_id_seq"'::regclass),
    name character varying(200) COLLATE pg_catalog."default",
    url character varying(200) COLLATE pg_catalog."default",
    CONSTRAINT "PK_adminURL" PRIMARY KEY (id),
    CONSTRAINT admin_id FOREIGN KEY (id)
        REFERENCES public.administrator (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)