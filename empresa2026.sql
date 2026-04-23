-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 13-04-2026 a las 20:37:25
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `empresa2026`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `departamentos`
--

CREATE TABLE `departamentos` (
  `id_area` int(11) NOT NULL,
  `Nombrearea` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `departamentos`
--

INSERT INTO `departamentos` (`id_area`, `Nombrearea`) VALUES
(1, 'Recursos Humanos'),
(2, 'Sistemas'),
(3, 'Administracion'),
(4, 'Contabilidad'),
(5, 'Cafeteria');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleados`
--

CREATE TABLE `empleados` (
  `id_empleado` int(11) NOT NULL,
  `docuempleado` varchar(50) NOT NULL,
  `nombreemple` varchar(50) NOT NULL,
  `apellidoemple` varchar(50) NOT NULL,
  `cargoemple` varchar(50) NOT NULL,
  `salarioB` decimal(10,2) DEFAULT NULL,
  `Horasextras` int(11) DEFAULT NULL,
  `bonificacion` decimal(10,2) DEFAULT NULL,
  `salud` decimal(10,2) DEFAULT NULL,
  `pension` decimal(10,2) DEFAULT NULL,
  `salarioneto` decimal(10,2) DEFAULT NULL,
  `id_area` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `empleados`
--

INSERT INTO `empleados` (`id_empleado`, `docuempleado`, `nombreemple`, `apellidoemple`, `cargoemple`, `salarioB`, `Horasextras`, `bonificacion`, `salud`, `pension`, `salarioneto`, `id_area`) VALUES
(2, '1234567', 'Leidy ', 'Diaz Borda', 'Administrativo', 2198800.00, 30, 500000.00, 95600.00, 95600.00, 2390000.00, 1),
(3, '987654321', 'Aleskha', 'Torres Perez', 'Administrativo', 1800000.00, 30, 350000.00, 89600.00, 89600.00, 2060800.00, 2),
(4, '1654577898', 'Ailyn', 'Betancour Mendez', 'Administrativo', 1800000.00, 20, 220000.00, 83200.00, 83200.00, 1913600.00, 5),
(5, '1006544343', 'Ana', 'Muñoz García', 'Contador', 2800000.00, 12, 300000.00, 125440.00, 125440.00, 2885120.00, 2),
(6, '109498383', 'Sara ', 'Culma ', 'Gerente', 5000000.00, 25, 500000.00, 223000.00, 223000.00, 5129000.00, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `usuario` varchar(50) NOT NULL,
  `PASSWORD` varchar(255) NOT NULL,
  `rol` varchar(20) NOT NULL,
  `docuempleado` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `usuario`, `PASSWORD`, `rol`, `docuempleado`) VALUES
(1, 'Felipe4567', '123456', 'administrador', NULL),
(2, 'Leidy ', '87654321', 'Empleado', '1234567'),
(3, 'Aleska', '34455', 'Empleado', '987654321'),
(4, 'Ailyn2026', '34567ujhg', 'Empleado', '1654577898'),
(5, 'Ana4556', '344567', 'Empleado', '1006544343'),
(6, 'Saracul34', 'g5g54r4d4d', 'Empleado', '109498383');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `departamentos`
--
ALTER TABLE `departamentos`
  ADD PRIMARY KEY (`id_area`);

--
-- Indices de la tabla `empleados`
--
ALTER TABLE `empleados`
  ADD PRIMARY KEY (`id_empleado`),
  ADD UNIQUE KEY `docuempleado` (`docuempleado`),
  ADD KEY `id_area` (`id_area`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD KEY `docuempleado` (`docuempleado`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `departamentos`
--
ALTER TABLE `departamentos`
  MODIFY `id_area` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `empleados`
--
ALTER TABLE `empleados`
  MODIFY `id_empleado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `empleados`
--
ALTER TABLE `empleados`
  ADD CONSTRAINT `empleados_ibfk_1` FOREIGN KEY (`id_area`) REFERENCES `departamentos` (`id_area`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
