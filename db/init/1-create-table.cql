use formactions;

CREATE TABLE IF NOT EXISTS forms(
                            formID uuid,
                            clientID text,
                            questions list<text>,
                            responses list<text>,
                            actions list<text>,
                            created timestamp,
                            deadline timestamp,
                            PRIMARY KEY(formId));

CREATE TABLE IF NOT EXISTS questions(
                            questionID uuid,
                            formID text,
                            question text,
                            format text,
                            created timestamp,
                            PRIMARY KEY(questionId));

CREATE TABLE IF NOT EXISTS answers(
                                answerID uuid,
                                questionID uuid,
                                answer text,
                                PRIMARY KEY(answerId));

CREATE TABLE IF NOT EXISTS responses(
                            responseID uuid,
                            formID text,
                            userID text,
                            responses list<text>,
                            created timestamp,
                            PRIMARY KEY(responseId));

CREATE TYPE IF NOT EXISTS metadata(
                                meta_property text,
                                meta_value text
                            );

CREATE TABLE IF NOT EXISTS actions(
                            actionID uuid,
                            formID text,
                            action text,
                            trigger text,
                            meta   list<frozen<metadata>>,
                            PRIMARY KEY(actionId));
