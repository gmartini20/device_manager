alter TABLE cadastro_room ADD column syndic_id int;
ALTER TABLE cadastro_room ADD CONSTRAINT cadastro_room_person_id_fkey FOREIGN KEY (syndic_id) REFERENCES cadastro_person(id);

insert into cadastro_feature (name, description, uri) VALUES ('syndic_room', 'Listar, criar e editar salas que é sindico', 'room');
insert into cadastro_feature (name, description, uri) VALUES ('edit_own_user', 'Editar o próprio usuário', 'user');

CREATE TABLE cadastro_role (id bigserial PRIMARY KEY, name VARCHAR(255));
insert into cadastro_role (name) VALUES ('Bolsista');
insert into cadastro_role (name) VALUES ('Orientador');
insert into cadastro_role (name) VALUES ('Visitante');
insert into cadastro_role (name) VALUES ('Temporário');

ALTER TABLE cadastro_person ADD COLUMN role_id INT;
ALTER TABLE cadastro_person ADD FOREIGN KEY (role_id) REFERENCES cadastro_role(id);
Alter table cadastro_role ADD column is_removed BOOLEAN Default false;

update cadastro_person set role_id = (select id from cadastro_role where name = 'Bolsista') where role = 'Bolsista';
update cadastro_person set role_id = (select id from cadastro_role where name = 'Orientador') where role = 'Orientador';
update cadastro_person set role_id = (select id from cadastro_role where name = 'Visitante') where role = 'Visitante';
update cadastro_person set role_id = (select id from cadastro_role where name = 'Temporário') where role = 'Temporário';

ALTER TABLE cadastro_person drop COLUMN role;

insert into cadastro_feature (name, description, uri) VALUES ('role', 'Listar, criar e editar papéis', 'role');
