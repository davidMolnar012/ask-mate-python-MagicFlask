--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS pk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS pk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS pk_comment_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS pk_question_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.tag DROP CONSTRAINT IF EXISTS pk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_id CASCADE;

DROP TABLE IF EXISTS public.question;
DROP SEQUENCE IF EXISTS public.question_id_seq;
CREATE TABLE question (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text,
    users_id integer NOT NULL
);

DROP TABLE IF EXISTS public.answer;
DROP SEQUENCE IF EXISTS public.answer_id_seq;
CREATE TABLE answer (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text,
    users_id integer NOT NULL
);

DROP TABLE IF EXISTS public.comment;
DROP SEQUENCE IF EXISTS public.comment_id_seq;
CREATE TABLE comment (
    id serial NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer,
    users_id integer NOT NULL
);


DROP TABLE IF EXISTS public.question_tag;
CREATE TABLE question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);

DROP TABLE IF EXISTS public.tag;
DROP SEQUENCE IF EXISTS public.tag_id_seq;
CREATE TABLE tag (
    id serial NOT NULL,
    name text,
    users_id integer NOT NULL
);

DROP TABLE IF EXISTS public.users;
DROP SEQUENCE IF EXISTS public.users_seq;
CREATE TABLE users (
    id serial NOT NULL,
    user_name text,
    password text,
    submission_time timestamp without time zone
);

ALTER TABLE ONLY answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);

ALTER TABLE ONLY question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);

ALTER TABLE ONLY tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);

ALTER TABLE ONLY users
    ADD CONSTRAINT pk_user_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id);

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id);

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_user_id FOREIGN KEY (users_id) REFERENCES users(id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_user_id FOREIGN KEY (users_id) REFERENCES users(id);

ALTER TABLE ONLY question
    ADD CONSTRAINT fk_user_id FOREIGN KEY (users_id) REFERENCES users(id);

ALTER TABLE ONLY tag
    ADD CONSTRAINT fk_user_id FOREIGN KEY (users_id) REFERENCES users(id);

INSERT INTO users VALUES (1,'admin','$2b$12$qQmXvohdve3MDXsqdpKPE.UkXrYeuT/ac1bEDtbNP46vdKTDxUTYu', '2017-04-28 08:29:00');
SELECT pg_catalog.setval('users_id_seq', 1, true);

INSERT INTO question VALUES (0, '2017-04-28 08:29:00', 29, 7, 'How to make lists in Python?', 'I am totally new to this, any hints?', 'None',1);
INSERT INTO question VALUES (1, '2017-04-29 09:19:00', 15, 9, 'Wordpress loading multiple jQuery Versions', 'I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(".myBook").booklet();

I could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.

BUT in my theme i also using jquery via webpack so the loading order is now following:

jquery
booklet
app.js (bundled file with webpack, including jquery)', 'https://i.kym-cdn.com/photos/images/original/000/482/170/a44.jpg', 1);
INSERT INTO question VALUES (2, '2017-05-01 10:41:00', 1364, 57, 'Drawing canvas with an image picked with Cordova Camera Plugin', 'I''m getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I''m on IOS, it throws errors such as cross origin issue, or that I''m trying to use an unknown format.
', 'None' ,1);
INSERT INTO question VALUES (3, '2019-10-02 13:29:52.000000', 158, 32, 'Rubber Duck inventor', 'Who invented the Yellow Rubber Duck?', 'https://images-na.ssl-images-amazon.com/images/I/51-JQx6aE6L._SX425_.jpg', 1);
INSERT INTO question VALUES (4, '2019-10-02 13:59:18.000000' ,95 ,67 ,'NASA honesty' , 'Why won’t NASA be honest with us and admit that the Earth is flat and the Moon landing was faked?' ,'https://www.moonmontchronicle.com/uploads/3/1/1/0/31106889/9265848.jpg?602', 1);
INSERT INTO question VALUES (5, '2019-10-02 14:06:58.000000', 113, 90 , 'Biggest Ass', 'How big is the biggest ass on the world, and where can I find it?' , 'https://www.madmagazine.com/sites/default/files/MAD-Magazine-Alfred-E-Neuman-Norman-Mingo.jpg', 1);
SELECT pg_catalog.setval('question_id_seq', 5, true);

INSERT INTO answer VALUES (1, '2017-04-28 16:49:00', 4, 1, 'You need to use brackets: my_list = []', 'None', 1);
INSERT INTO answer VALUES (2, '2017-04-25 14:42:00', 35, 1, 'Look it up in the Python docs', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQY4RusHBTJdCfK3nGlAaEG-Fl16hX4U-05iZDghzQ7YTkn3fWI4w', 1);
INSERT INTO answer VALUES (3, '2019-10-02 13:38:05.000000', 18, 3, 'Sculptor Peter Ganine created a sculpture of a duck in the 1940s. He then patented it and reproduced it as a floating toy, of which over 50 million were sold.', 'https://c.stocksy.com/a/c7X200/z9/603980.jpg?1564682295', 1);
INSERT INTO answer VALUES (4, '2019-10-02 14:08:28.000000', 1, 2, 'aerzeqz', 'None', 1);
INSERT INTO answer VALUES (5, '2019-10-03 16:41:53.000000', -5, 0, 'first', 'https://i.pinimg.com/originals/a5/df/c2/a5dfc21fc9ad530068537135aef51ba5.png' , 1);
INSERT INTO answer VALUES (6, '2019-10-03 16:43:21.000000', -8, 0, 'fake!', 'http://www.dariushghatan.com/wp-content/uploads/depositphotos_57228163-stock-illustration-fake-red-stamp-text-886x590.jpg', 1);
INSERT INTO answer VALUES (7, '2019-10-03 17:06:44.000000', 25, 4, 'Because nobody can call their bluff, because they are on the other side of Flat Earth.', 'https://i.imgur.com/t5jbb21.jpg', 1);
INSERT INTO answer VALUES (8, '2019-10-03 17:07:56.000000', 12, 4, 'No. We are on the other side.', 'https://i.pinimg.com/originals/f8/b2/c7/f8b2c72e42a698a61ebf4337fbdee85a.jpg', 1);
INSERT INTO answer VALUES (9, '2019-10-03 17:11:32.000000', -69, 5, 'Romulus is the worlds tallest living donkey, as certified by the Guinness World Records. 12 years old and has been measured at 17 hands 68 inches, 173 cm from hooves to withers, two inches taller than the former tallest donkey, Oklahoma Sam. Romulus weighs about,1 1,300 pounds 590 kg. He is owned by Phil and Cara Barker Yellott of Adrian, Michigan. ', 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Romulus_Nov6_2013_01.jpg/800px-Romulus_Nov6_2013_01.jpg', 1);
SELECT pg_catalog.setval('answer_id_seq', 9, true);

INSERT INTO comment VALUES (1, 0, NULL, 'Please clarify the question as it is too vague!', '2017-05-01 05:49:00', 0, 1);
INSERT INTO comment VALUES (2, NULL, 1, 'I think you could use my_list = list() as well.', '2017-05-02 16:55:00', 0, 1);
INSERT INTO comment VALUES (4, 0, 9, 'That is not helpful.', '2019-10-03 19:56:39.000000', 0, 1);
INSERT INTO comment VALUES (5, 0, 9, 'Such a beautiful ass.', '2019-10-03 19:57:20.000000', 0, 1);
INSERT INTO comment VALUES (6, 0, 8, 'No. Australia is on the other side.', '2019-10-03 19:58:38.000000', 0, 1);
INSERT INTO comment VALUES (7, 0, 7, 'Chuck Norris can punch through the crust of Earth.', '2019-10-03 20:00:08.000000', 0, 1);
INSERT INTO comment VALUES (8, 4, NULL, 'first', '2019-10-03 20:00:49.000000', 0, 1);
INSERT INTO comment VALUES (9, 3, NULL, 'I want to know that too.', '2019-10-03 20:01:29.000000', 0, 1);
INSERT INTO comment VALUES (10, 0, 3, 'Thanks.', '2019-10-03 20:01:45.000000', 0, 1);
INSERT INTO comment VALUES (11, 3, NULL, 'This duck is cute enough.', '2019-10-03 21:01:57.000000', 0, 1);
SELECT pg_catalog.setval('comment_id_seq', 11, true);

INSERT INTO tag VALUES (1, 'python',1);
INSERT INTO tag VALUES (2, 'sql',1);
INSERT INTO tag VALUES (3, 'css',1);
SELECT pg_catalog.setval('tag_id_seq', 3, true);

INSERT INTO question_tag VALUES (0, 1);
INSERT INTO question_tag VALUES (1, 3);
INSERT INTO question_tag VALUES (2, 3);
