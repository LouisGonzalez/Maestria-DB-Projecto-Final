DROP DATABASE tutorias;
CREATE DATABASE tutorias;
use tutorias;

CREATE TABLE `persona` (
  `dpi` BIGINT PRIMARY KEY,
  `primer_nombre` VARCHAR(50) NOT NULL,
  `segundo_nombre` VARCHAR(50),
  `primer_apellido` VARCHAR(50) NOT NULL,
  `segundo_apellido` VARCHAR(50),
  `fecha_de_nacimiento` DATE NOT NULL,
  `direccion` VARCHAR(500) NOT NULL
);

CREATE TABLE `telefono` (
  `id_telefono` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `dpi` BIGINT NOT NULL,
  `telefono` VARCHAR(20) NOT NULL,
  `tipo` BIGINT NOT NULL
);

CREATE TABLE `email` (
  `id_email` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `dpi` BIGINT NOT NULL,
  `email` VARCHAR(100) NOT NULL
);

CREATE TABLE `rol` (
  `id_rol` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `nombre` VARCHAR(50) NOT NULL
);

CREATE TABLE `rol_persona` (
  `dpi` BIGINT NOT NULL,
  `rol` BIGINT NOT NULL,
  PRIMARY KEY (`dpi`, `rol`)
);

CREATE TABLE `nivel` (
  `id_nivel` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `nivel` VARCHAR(50) NOT NULL
);

CREATE TABLE `materia` (
  `id_materia` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `materia` VARCHAR(150) NOT NULL
);

CREATE TABLE `materia_nivel` (
  `id_materia_nivel` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `materia` BIGINT NOT NULL,
  `nivel` BIGINT NOT NULL
);

CREATE TABLE `alumno_nivel` (
  `id_alumno_nivel` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `dpi_alumno` BIGINT NOT NULL,
  `nivel` BIGINT NOT NULL
);

CREATE TABLE `tutor_puede_impartir` (
  `id_tutor_impartir` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `dpi_tutor` BIGINT NOT NULL,
  `materia_nivel` BIGINT NOT NULL
);

CREATE TABLE `encargado_alumno` (
  `dpi_encargado` BIGINT NOT NULL,
  `dpi_alumno` BIGINT NOT NULL,
  PRIMARY KEY (`dpi_encargado`, `dpi_alumno`)
);

CREATE TABLE `estado_tutoria` (
  `estado` BIGINT NOT NULL,
  `descripcion` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`estado`)
);

CREATE TABLE `sucursal` (
  `id_sucursal` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `sucursal` VARCHAR(200) NOT NULL
);

CREATE TABLE `salon` (
  `id_salon` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `sucursal` BIGINT(200) NOT NULL,
  `salon` VARCHAR(200) NOT NULL
);

CREATE TABLE `tutoria` (
  `id_tutoria` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `tutor` BIGINT NOT NULL,
  `alumno` BIGINT NOT NULL,
  `id_materia_nivel` BIGINT NOT NULL,
  `fecha` DATE NOT NULL,
  `hora_inicio` TIME NOT NULL,
  `hora_fin` TIME NOT NULL,
  `estado` BIGINT NOT NULL,
  `salon` BIGINT NOT NULL,
  `calificacion` BIGINT
);

CREATE TABLE `horario_tutor` (
  `id_horario_tutor` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `tutor` BIGINT NOT NULL,
  `dia` VARCHAR(200) NOT NULL,
  `hora_inicio` VARCHAR(200) NOT NULL,
  `hora_fin` VARCHAR(200) NOT NULL
);

ALTER TABLE `telefono` ADD FOREIGN KEY (`dpi`) REFERENCES `persona` (`dpi`);

ALTER TABLE `email` ADD FOREIGN KEY (`dpi`) REFERENCES `persona` (`dpi`);

ALTER TABLE `rol_persona` ADD FOREIGN KEY (`dpi`) REFERENCES `persona` (`dpi`);

ALTER TABLE `rol_persona` ADD FOREIGN KEY (`rol`) REFERENCES `rol` (`id_rol`);

ALTER TABLE `materia_nivel` ADD FOREIGN KEY (`materia`) REFERENCES `materia` (`id_materia`);

ALTER TABLE `materia_nivel` ADD FOREIGN KEY (`nivel`) REFERENCES `nivel` (`id_nivel`);

ALTER TABLE `alumno_nivel` ADD FOREIGN KEY (`dpi_alumno`) REFERENCES `persona` (`dpi`);

ALTER TABLE `alumno_nivel` ADD FOREIGN KEY (`nivel`) REFERENCES `nivel` (`id_nivel`);

ALTER TABLE `tutor_puede_impartir` ADD FOREIGN KEY (`dpi_tutor`) REFERENCES `persona` (`dpi`);

ALTER TABLE `tutor_puede_impartir` ADD FOREIGN KEY (`materia_nivel`) REFERENCES `materia_nivel` (`id_materia_nivel`);

ALTER TABLE `encargado_alumno` ADD FOREIGN KEY (`dpi_encargado`) REFERENCES `persona` (`dpi`);

ALTER TABLE `encargado_alumno` ADD FOREIGN KEY (`dpi_alumno`) REFERENCES `persona` (`dpi`);

ALTER TABLE `salon` ADD FOREIGN KEY (`sucursal`) REFERENCES `sucursal` (`id_sucursal`);

ALTER TABLE `tutoria` ADD FOREIGN KEY (`tutor`) REFERENCES `persona` (`dpi`);

ALTER TABLE `tutoria` ADD FOREIGN KEY (`alumno`) REFERENCES `persona` (`dpi`);

ALTER TABLE `tutoria` ADD FOREIGN KEY (`id_materia_nivel`) REFERENCES `materia_nivel` (`id_materia_nivel`);

ALTER TABLE `tutoria` ADD FOREIGN KEY (`estado`) REFERENCES `estado_tutoria` (`estado`);

ALTER TABLE `tutoria` ADD FOREIGN KEY (`salon`) REFERENCES `salon` (`id_salon`);

ALTER TABLE `horario_tutor` ADD FOREIGN KEY (`tutor`) REFERENCES `persona` (`dpi`);
