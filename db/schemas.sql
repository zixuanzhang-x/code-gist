DROP TABLE IF EXISTS star;
DROP TABLE IF EXISTS fork;
DROP TABLE IF EXISTS gist_comment;
DROP TABLE IF EXISTS gist;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id SERIAL,
    username VARCHAR(30) NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    avatar BYTEA NOT NULL,
    signed_up TIMESTAMP NOT NULL,
    CONSTRAINT pk_user PRIMARY KEY(id)
);

CREATE TABLE gist (
    id SERIAL,
    user_id SERIAL NOT NULL,
    name VARCHAR NOT NULL,
    content TEXT NOT NULL,
    description TEXT NOT NULL,
    created TIMESTAMP NOT NULL,
    last_modified TIMESTAMP NOT NULL,
    stars INTEGER DEFAULT 0,
    forks INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    is_forked BOOLEAN DEFAULT false,
    forked_from SERIAL,
    CONSTRAINT pk_gist PRIMARY KEY(id),
    CONSTRAINT fk_user_id FOREIGN KEY(user_id) REFERENCES user(id),
    CONSTRAINT fk_forked_from FOREIGN KEY(forked_from) REFERENCES gist(id)
);

CREATE TABLE gist_comment (
    id SERIAL,
    content TEXT NOT NULL,
    created TIMESTAMP NOT NULL,
    user_id SERIAL NOT NULL,
    gist_id SERIAL NOT NULL,
    CONSTRAINT pk_gist_comment PRIMARY KEY(id),
    CONSTRAINT fk_user_id FOREIGN KEY(user_id) REFERENCES user(id),
    CONSTRAINT fk_gist_id FOREIGN KEY(gist_id) REFERENCES gist(id)
);

CREATE TABLE fork (
    user_id SERIAL,
    gist_id SERIAL,
    CONSTRAINT pk_fork PRIMARY KEY(user_id, gist_id),
    CONSTRAINT fk_user_id FOREIGN KEY(user_id) REFERENCES user(id),
    CONSTRAINT fk_gist_id FOREIGN KEY(gist_id) REFERENCES gist(id)
);

CREATE TABLE star (
    user_id SERIAL,
    gist_id SERIAL,
    CONSTRAINT pk_fork PRIMARY KEY(user_id, gist_id),
    CONSTRAINT fk_user_id FOREIGN KEY(user_id) REFERENCES user(id),
    CONSTRAINT fk_gist_id FOREIGN KEY(gist_id) REFERENCES gist(id)
);