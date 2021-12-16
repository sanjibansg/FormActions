use formactions;

CREATE TABLE IF NOT EXISTS forms(
                            form_id uuid,
                            client_id text,
                            questions list<text>,
                            responses list<text>,
                            actions list<text>,
                            created timestamp,
                            deadline timestamp,
                            PRIMARY KEY(form_id));

CREATE TABLE IF NOT EXISTS questions(
                            question_id uuid,
                            form_id text,
                            question text,
                            format text,
                            created timestamp,
                            PRIMARY KEY(question_id));

CREATE TABLE IF NOT EXISTS answers(
                                answer_id uuid,
                                question_id uuid,
                                answer text,
                                PRIMARY KEY(answer_id));

CREATE TABLE IF NOT EXISTS responses(
                            response_id uuid,
                            form_id text,
                            user_id text,
                            responses list<text>,
                            created timestamp,
                            PRIMARY KEY(response_id));

CREATE TYPE IF NOT EXISTS action_meta_data(
                                meta_property text,
                                meta_value text
                            );

CREATE TABLE IF NOT EXISTS actions(
                            action_id uuid,
                            form_id text,
                            action text,
                            trigger text,
                            meta   list<frozen<action_meta_data>>,
                            PRIMARY KEY(action_id));
