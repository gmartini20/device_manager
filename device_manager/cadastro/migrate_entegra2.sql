alter TABLE cadastro_room ADD column syndic_id int;
ALTER TABLE cadastro_room ADD CONSTRAINT cadastro_room_person_id_fkey FOREIGN KEY (syndic_id) REFERENCES cadastro_person(id);

insert into cadastro_feature (name, description, uri) VALUES ('syndic_room', 'Listar, criar e editar salas que é sindico', 'room');
insert into cadastro_feature (name, description, uri) VALUES ('edit_own_user', 'Editar o próprio usuário', 'user');
