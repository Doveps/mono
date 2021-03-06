PGDMP     !                
    t            doveps    9.4.9    9.5.1     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                       false            �           1262    33195    doveps    DATABASE     x   CREATE DATABASE doveps WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';
    DROP DATABASE doveps;
             postgres    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
             roselle    false            �           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                  roselle    false    6            �           0    0    public    ACL     �   REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM roselle;
GRANT ALL ON SCHEMA public TO roselle;
GRANT ALL ON SCHEMA public TO PUBLIC;
                  roselle    false    6                        3079    12123    plpgsql 	   EXTENSION     ?   CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
    DROP EXTENSION plpgsql;
                  false            �           0    0    EXTENSION plpgsql    COMMENT     @   COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';
                       false    1            �            1259    33223    Flavor    TABLE     T   CREATE TABLE "Flavor" (
    id integer NOT NULL,
    name character varying(255)
);
    DROP TABLE public."Flavor";
       public         postgres    false    6            �            1259    33221    Flavor_id_seq    SEQUENCE     q   CREATE SEQUENCE "Flavor_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public."Flavor_id_seq";
       public       postgres    false    6    174            �           0    0    Flavor_id_seq    SEQUENCE OWNED BY     5   ALTER SEQUENCE "Flavor_id_seq" OWNED BY "Flavor".id;
            public       postgres    false    173            �            1259    33231    Metadata    TABLE     v   CREATE TABLE "Metadata" (
    id integer NOT NULL,
    name character varying(255),
    flavor_id integer NOT NULL
);
    DROP TABLE public."Metadata";
       public         postgres    false    6            �            1259    33229    Metadata_id_seq    SEQUENCE     s   CREATE SEQUENCE "Metadata_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public."Metadata_id_seq";
       public       postgres    false    6    176            �           0    0    Metadata_id_seq    SEQUENCE OWNED BY     9   ALTER SEQUENCE "Metadata_id_seq" OWNED BY "Metadata".id;
            public       postgres    false    175            i           2604    33226    id    DEFAULT     \   ALTER TABLE ONLY "Flavor" ALTER COLUMN id SET DEFAULT nextval('"Flavor_id_seq"'::regclass);
 :   ALTER TABLE public."Flavor" ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    174    173    174            j           2604    33234    id    DEFAULT     `   ALTER TABLE ONLY "Metadata" ALTER COLUMN id SET DEFAULT nextval('"Metadata_id_seq"'::regclass);
 <   ALTER TABLE public."Metadata" ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    176    175    176            �          0    33223    Flavor 
   TABLE DATA               %   COPY "Flavor" (id, name) FROM stdin;
    public       postgres    false    174   P       �           0    0    Flavor_id_seq    SEQUENCE SET     7   SELECT pg_catalog.setval('"Flavor_id_seq"', 1, false);
            public       postgres    false    173            �          0    33231    Metadata 
   TABLE DATA               2   COPY "Metadata" (id, name, flavor_id) FROM stdin;
    public       postgres    false    176   m       �           0    0    Metadata_id_seq    SEQUENCE SET     9   SELECT pg_catalog.setval('"Metadata_id_seq"', 1, false);
            public       postgres    false    175            l           2606    33228    Flavor_pkey 
   CONSTRAINT     M   ALTER TABLE ONLY "Flavor"
    ADD CONSTRAINT "Flavor_pkey" PRIMARY KEY (id);
 @   ALTER TABLE ONLY public."Flavor" DROP CONSTRAINT "Flavor_pkey";
       public         postgres    false    174    174            n           2606    33236    Metadata_pkey 
   CONSTRAINT     Q   ALTER TABLE ONLY "Metadata"
    ADD CONSTRAINT "Metadata_pkey" PRIMARY KEY (id);
 D   ALTER TABLE ONLY public."Metadata" DROP CONSTRAINT "Metadata_pkey";
       public         postgres    false    176    176            o           2606    33237    Metadata_flavor_id_fkey    FK CONSTRAINT     z   ALTER TABLE ONLY "Metadata"
    ADD CONSTRAINT "Metadata_flavor_id_fkey" FOREIGN KEY (flavor_id) REFERENCES "Flavor"(id);
 N   ALTER TABLE ONLY public."Metadata" DROP CONSTRAINT "Metadata_flavor_id_fkey";
       public       postgres    false    176    2156    174            �      x������ � �      �      x������ � �     