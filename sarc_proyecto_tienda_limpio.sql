CREATE TABLE `app_eventos_cliente` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `fecha_registro` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_eventos_evento`
--

CREATE TABLE `app_eventos_evento` (
  `id` bigint(20) NOT NULL,
  `descripcion` longtext NOT NULL,
  `fecha_evento` datetime(6) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `cliente_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_finanzas_egreso`
--

CREATE TABLE `app_finanzas_egreso` (
  `id` bigint(20) NOT NULL,
  `tipo` varchar(15) NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `descripcion` longtext NOT NULL,
  `categoria` varchar(100) NOT NULL,
  `pedido_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Volcado de datos para la tabla `app_finanzas_egreso`
--

INSERT INTO `app_finanzas_egreso` (`id`, `tipo`, `fecha`, `monto`, `descripcion`, `categoria`, `pedido_id`) VALUES
(1, 'pedido', '2024-11-05 11:13:15.850606', 1836286.52, '', 'Pedido', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_finanzas_ingreso`
--

CREATE TABLE `app_finanzas_ingreso` (
  `id` bigint(20) NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `descripcion` longtext DEFAULT NULL,
  `venta_id` bigint(20) DEFAULT NULL,
  `tipo` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Volcado de datos para la tabla `app_finanzas_ingreso`
--

INSERT INTO `app_finanzas_ingreso` (`id`, `fecha`, `monto`, `descripcion`, `venta_id`, `tipo`) VALUES
(1, '2024-11-07 10:15:20.444214', 9000.00, 'Ingreso por Venta ID 1', 1, 'venta'),
(2, '2024-11-14 11:24:48.669737', 9000.00, 'Ingreso por Venta ID 2', 2, 'venta'),
(3, '2024-11-21 14:35:37.465000', 12000.00, 'Ingreso por Venta ID 3', 3, 'venta'),
(4, '2024-11-28 16:47:01.176030', 12000.00, 'Ingreso por Venta ID 4', 4, 'venta'),
(5, '2024-12-05 09:16:08.091558', 60000.00, 'Ingreso por Venta ID 5', 5, 'venta'),
(6, '2024-12-12 10:27:37.746320', 30000.00, 'Ingreso por Venta ID 6', 6, 'venta'),
(7, '2024-12-19 15:38:59.773049', 90000.00, 'Ingreso por Venta ID 7', 7, 'venta'),
(8, '2024-12-26 17:44:52.582925', 16000.00, 'Ingreso por Venta ID 8', 8, 'venta'),
(9, '2025-01-02 11:25:38.567368', 12000.00, 'Ingreso por Venta ID 9', 9, 'venta'),
(10, '2025-01-09 13:34:20.184036', 10000.00, 'Ingreso por Venta ID 10', 10, 'venta'),
(11, '2025-01-16 14:35:12.207012', 33000.00, 'Ingreso por Venta ID 11', 11, 'venta'),
(12, '2025-01-23 16:36:21.867403', 45000.00, 'Ingreso por Venta ID 12', 12, 'venta'),
(13, '2025-02-06 10:37:21.020570', 8000.00, 'Ingreso por Venta ID 13', 13, 'venta'),
(14, '2025-02-13 11:37:42.218151', 10000.00, 'Ingreso por Venta ID 14', 14, 'venta'),
(15, '2025-02-20 14:40:09.938573', 60000.00, 'Ingreso por Venta ID 15', 15, 'venta'),
(16, '2025-02-27 15:41:34.111486', 30000.00, 'Ingreso por Venta ID 16', 16, 'venta'),
(17, '2025-03-06 09:42:37.382716', 75000.00, 'Ingreso por Venta ID 17', 17, 'venta'),
(18, '2025-03-13 10:43:52.153947', 6000.00, 'Ingreso por Venta ID 18', 18, 'venta'),
(19, '2025-03-20 14:44:03.234011', 9000.00, 'Ingreso por Venta ID 19', 19, 'venta'),
(20, '2025-03-27 16:44:21.081482', 24000.00, 'Ingreso por Venta ID 20', 20, 'venta'),
(21, '2025-04-03 10:44:50.798263', 27000.00, 'Ingreso por Venta ID 21', 21, 'venta'),
(22, '2025-04-10 11:45:10.880687', 15000.00, 'Ingreso por Venta ID 22', 22, 'venta'),
(23, '2025-04-17 14:45:27.299545', 45000.00, 'Ingreso por Venta ID 23', 23, 'venta'),
(24, '2025-04-24 16:45:54.462231', 45000.00, 'Ingreso por Venta ID 24', 24, 'venta'),
(25, '2024-05-03 11:10:00.000000', 15000.00, 'Ingreso por Venta ID 25', 25, 'venta'),
(26, '2024-06-10 13:20:00.000000', 21000.00, 'Ingreso por Venta ID 26', 26, 'venta'),
(27, '2024-07-15 15:30:00.000000', 12000.00, 'Ingreso por Venta ID 27', 27, 'venta'),
(28, '2024-08-05 10:00:00.000000', 18000.00, 'Ingreso por Venta ID 28', 28, 'venta'),
(29, '2024-09-12 16:00:00.000000', 24000.00, 'Ingreso por Venta ID 29', 29, 'venta'),
(30, '2024-10-20 14:45:00.000000', 27000.00, 'Ingreso por Venta ID 30', 30, 'venta'),
(31, '2024-11-01 10:00:00.000000', 9000.00, 'Ingreso por Venta ID 31', 31, 'venta'),
(32, '2024-11-02 11:00:00.000000', 12000.00, 'Ingreso por Venta ID 32', 32, 'venta'),
(33, '2024-11-03 12:00:00.000000', 15000.00, 'Ingreso por Venta ID 33', 33, 'venta'),
(34, '2024-11-04 13:00:00.000000', 18000.00, 'Ingreso por Venta ID 34', 34, 'venta'),
(35, '2024-11-05 14:00:00.000000', 21000.00, 'Ingreso por Venta ID 35', 35, 'venta'),
(36, '2024-11-06 15:00:00.000000', 9000.00, 'Ingreso por Venta ID 36', 36, 'venta'),
(37, '2024-11-07 16:00:00.000000', 12000.00, 'Ingreso por Venta ID 37', 37, 'venta'),
(38, '2024-11-08 17:00:00.000000', 15000.00, 'Ingreso por Venta ID 38', 38, 'venta'),
(39, '2024-11-09 18:00:00.000000', 18000.00, 'Ingreso por Venta ID 39', 39, 'venta'),
(40, '2024-11-10 19:00:00.000000', 21000.00, 'Ingreso por Venta ID 40', 40, 'venta'),
(41, '2024-11-21 10:00:00.000000', 12000.00, 'Ingreso por Venta ID 41', 41, 'venta'),
(42, '2024-11-22 11:00:00.000000', 15000.00, 'Ingreso por Venta ID 42', 42, 'venta'),
(43, '2024-11-23 12:00:00.000000', 18000.00, 'Ingreso por Venta ID 43', 43, 'venta'),
(44, '2024-11-24 13:00:00.000000', 9000.00, 'Ingreso por Venta ID 44', 44, 'venta'),
(45, '2024-11-25 14:00:00.000000', 21000.00, 'Ingreso por Venta ID 45', 45, 'venta'),
(46, '2024-11-26 15:00:00.000000', 15000.00, 'Ingreso por Venta ID 46', 46, 'venta'),
(47, '2024-11-17 16:00:00.000000', 18000.00, 'Ingreso por Venta ID 47', 47, 'venta'),
(48, '2024-11-18 17:00:00.000000', 12000.00, 'Ingreso por Venta ID 48', 48, 'venta'),
(49, '2024-11-19 18:00:00.000000', 9000.00, 'Ingreso por Venta ID 49', 49, 'venta'),
(50, '2024-11-20 19:00:00.000000', 21000.00, 'Ingreso por Venta ID 50', 50, 'venta'),
(51, '2024-11-21 10:00:00.000000', 15000.00, 'Ingreso por Venta ID 51', 51, 'venta'),
(52, '2024-11-14 13:00:00.000000', 9000.00, 'Ingreso por Venta ID 52', 52, 'venta'),
(53, '2024-11-15 14:00:00.000000', 21000.00, 'Ingreso por Venta ID 53', 53, 'venta'),
(54, '2024-11-16 15:00:00.000000', 15000.00, 'Ingreso por Venta ID 54', 54, 'venta'),
(55, '2024-11-17 16:00:00.000000', 18000.00, 'Ingreso por Venta ID 55', 55, 'venta'),
(56, '2024-11-18 17:00:00.000000', 12000.00, 'Ingreso por Venta ID 56', 56, 'venta'),
(57, '2024-11-19 18:00:00.000000', 9000.00, 'Ingreso por Venta ID 57', 57, 'venta'),
(58, '2024-11-20 19:00:00.000000', 21000.00, 'Ingreso por Venta ID 58', 58, 'venta'),
(59, '2024-11-21 10:00:00.000000', 15000.00, 'Ingreso por Venta ID 59', 59, 'venta'),
(60, '2024-11-22 11:00:00.000000', 18000.00, 'Ingreso por Venta ID 60', 60, 'venta'),
(61, '2024-11-23 12:00:00.000000', 12000.00, 'Ingreso por Venta ID 61', 61, 'venta'),
(62, '2024-11-24 13:00:00.000000', 9000.00, 'Ingreso por Venta ID 62', 62, 'venta'),
(63, '2024-11-25 14:00:00.000000', 21000.00, 'Ingreso por Venta ID 63', 63, 'venta'),
(64, '2024-11-26 15:00:00.000000', 15000.00, 'Ingreso por Venta ID 64', 64, 'venta'),
(65, '2024-11-27 16:00:00.000000', 18000.00, 'Ingreso por Venta ID 65', 65, 'venta'),
(66, '2024-11-28 17:00:00.000000', 12000.00, 'Ingreso por Venta ID 66', 66, 'venta'),
(67, '2024-11-29 18:00:00.000000', 9000.00, 'Ingreso por Venta ID 67', 67, 'venta'),
(68, '2024-11-30 19:00:00.000000', 21000.00, 'Ingreso por Venta ID 68', 68, 'venta'),
(69, '2024-12-01 10:00:00.000000', 15000.00, 'Ingreso por Venta ID 69', 69, 'venta'),
(70, '2024-12-02 11:00:00.000000', 18000.00, 'Ingreso por Venta ID 70', 70, 'venta'),
(71, '2024-12-03 12:00:00.000000', 12000.00, 'Ingreso por Venta ID 71', 71, 'venta'),
(72, '2024-12-04 13:00:00.000000', 9000.00, 'Ingreso por Venta ID 72', 72, 'venta'),
(73, '2024-12-05 14:00:00.000000', 21000.00, 'Ingreso por Venta ID 73', 73, 'venta'),
(74, '2024-12-06 15:00:00.000000', 15000.00, 'Ingreso por Venta ID 74', 74, 'venta'),
(75, '2024-12-07 16:00:00.000000', 18000.00, 'Ingreso por Venta ID 75', 75, 'venta'),
(76, '2024-12-08 17:00:00.000000', 12000.00, 'Ingreso por Venta ID 76', 76, 'venta'),
(77, '2024-12-09 18:00:00.000000', 9000.00, 'Ingreso por Venta ID 77', 77, 'venta'),
(78, '2024-12-10 19:00:00.000000', 21000.00, 'Ingreso por Venta ID 78', 78, 'venta'),
(79, '2024-12-11 10:00:00.000000', 15000.00, 'Ingreso por Venta ID 79', 79, 'venta'),
(80, '2024-12-12 11:00:00.000000', 18000.00, 'Ingreso por Venta ID 80', 80, 'venta'),
(81, '2024-12-13 12:00:00.000000', 12000.00, 'Ingreso por Venta ID 81', 81, 'venta'),
(82, '2024-12-14 13:00:00.000000', 9000.00, 'Ingreso por Venta ID 82', 82, 'venta'),
(83, '2024-12-15 14:00:00.000000', 21000.00, 'Ingreso por Venta ID 83', 83, 'venta'),
(84, '2024-12-16 15:00:00.000000', 15000.00, 'Ingreso por Venta ID 84', 84, 'venta'),
(85, '2024-12-17 16:00:00.000000', 18000.00, 'Ingreso por Venta ID 85', 85, 'venta'),
(86, '2024-12-18 17:00:00.000000', 12000.00, 'Ingreso por Venta ID 86', 86, 'venta'),
(87, '2024-12-19 18:00:00.000000', 9000.00, 'Ingreso por Venta ID 87', 87, 'venta'),
(88, '2024-12-20 19:00:00.000000', 21000.00, 'Ingreso por Venta ID 88', 88, 'venta'),
(89, '2024-12-21 10:00:00.000000', 15000.00, 'Ingreso por Venta ID 89', 89, 'venta'),
(90, '2024-12-22 11:00:00.000000', 18000.00, 'Ingreso por Venta ID 90', 90, 'venta'),
(91, '2024-12-23 12:00:00.000000', 12000.00, 'Ingreso por Venta ID 91', 91, 'venta'),
(92, '2024-12-24 13:00:00.000000', 9000.00, 'Ingreso por Venta ID 92', 92, 'venta'),
(93, '2024-12-25 14:00:00.000000', 21000.00, 'Ingreso por Venta ID 93', 93, 'venta'),
(94, '2024-12-26 15:00:00.000000', 15000.00, 'Ingreso por Venta ID 94', 94, 'venta'),
(95, '2024-12-27 16:00:00.000000', 18000.00, 'Ingreso por Venta ID 95', 95, 'venta'),
(96, '2024-12-28 17:00:00.000000', 12000.00, 'Ingreso por Venta ID 96', 96, 'venta'),
(97, '2024-12-29 18:00:00.000000', 9000.00, 'Ingreso por Venta ID 97', 97, 'venta'),
(98, '2024-12-30 19:00:00.000000', 21000.00, 'Ingreso por Venta ID 98', 98, 'venta'),
(99, '2024-12-31 10:00:00.000000', 15000.00, 'Ingreso por Venta ID 99', 99, 'venta'),
(100, '2025-01-01 11:00:00.000000', 18000.00, 'Ingreso por Venta ID 100', 100, 'venta'),
(101, '2025-01-02 12:00:00.000000', 12000.00, 'Ingreso por Venta ID 101', 101, 'venta'),
(102, '2025-01-03 13:00:00.000000', 9000.00, 'Ingreso por Venta ID 102', 102, 'venta'),
(103, '2025-01-04 14:00:00.000000', 21000.00, 'Ingreso por Venta ID 103', 103, 'venta'),
(104, '2025-01-05 15:00:00.000000', 15000.00, 'Ingreso por Venta ID 104', 104, 'venta'),
(105, '2025-01-06 16:00:00.000000', 18000.00, 'Ingreso por Venta ID 105', 105, 'venta'),
(106, '2025-01-07 17:00:00.000000', 12000.00, 'Ingreso por Venta ID 106', 106, 'venta'),
(107, '2025-01-08 18:00:00.000000', 9000.00, 'Ingreso por Venta ID 107', 107, 'venta'),
(108, '2025-01-09 19:00:00.000000', 21000.00, 'Ingreso por Venta ID 108', 108, 'venta'),
(109, '2025-01-10 10:00:00.000000', 15000.00, 'Ingreso por Venta ID 109', 109, 'venta'),
(110, '2025-01-11 11:00:00.000000', 18000.00, 'Ingreso por Venta ID 110', 110, 'venta'),
(111, '2025-01-12 12:00:00.000000', 12000.00, 'Ingreso por Venta ID 111', 111, 'venta'),
(112, '2025-01-13 13:00:00.000000', 9000.00, 'Ingreso por Venta ID 112', 112, 'venta'),
(113, '2025-01-14 14:00:00.000000', 21000.00, 'Ingreso por Venta ID 113', 113, 'venta'),
(114, '2025-01-15 15:00:00.000000', 15000.00, 'Ingreso por Venta ID 114', 114, 'venta'),
(115, '2025-01-16 16:00:00.000000', 18000.00, 'Ingreso por Venta ID 115', 115, 'venta'),
(116, '2025-01-17 17:00:00.000000', 12000.00, 'Ingreso por Venta ID 116', 116, 'venta'),
(117, '2025-01-18 18:00:00.000000', 9000.00, 'Ingreso por Venta ID 117', 117, 'venta'),
(118, '2025-01-19 19:00:00.000000', 21000.00, 'Ingreso por Venta ID 118', 118, 'venta'),
(119, '2025-01-20 10:00:00.000000', 15000.00, 'Ingreso por Venta ID 119', 119, 'venta'),
(120, '2025-01-21 11:00:00.000000', 18000.00, 'Ingreso por Venta ID 120', 120, 'venta'),
(121, '2025-01-22 12:00:00.000000', 12000.00, 'Ingreso por Venta ID 121', 121, 'venta'),
(122, '2025-01-23 13:00:00.000000', 9000.00, 'Ingreso por Venta ID 122', 122, 'venta'),
(123, '2025-01-24 14:00:00.000000', 21000.00, 'Ingreso por Venta ID 123', 123, 'venta'),
(124, '2025-01-25 15:00:00.000000', 15000.00, 'Ingreso por Venta ID 124', 124, 'venta'),
(125, '2025-01-26 16:00:00.000000', 18000.00, 'Ingreso por Venta ID 125', 125, 'venta'),
(126, '2025-01-27 17:00:00.000000', 12000.00, 'Ingreso por Venta ID 126', 126, 'venta'),
(127, '2025-01-28 18:00:00.000000', 9000.00, 'Ingreso por Venta ID 127', 127, 'venta'),
(128, '2025-01-29 19:00:00.000000', 21000.00, 'Ingreso por Venta ID 128', 128, 'venta'),
(129, '2024-11-22 11:00:00.000000', 18000.00, 'Ingreso por Venta ID 129', 129, 'venta'),
(130, '2024-11-23 12:00:00.000000', 12000.00, 'Ingreso por Venta ID 130', 130, 'venta'),
(131, '2024-11-24 13:00:00.000000', 9000.00, 'Ingreso por Venta ID 131', 131, 'venta'),
(132, '2024-11-25 14:00:00.000000', 21000.00, 'Ingreso por Venta ID 132', 132, 'venta'),
(133, '2024-11-26 15:00:00.000000', 15000.00, 'Ingreso por Venta ID 133', 133, 'venta'),
(134, '2024-11-27 16:00:00.000000', 18000.00, 'Ingreso por Venta ID 134', 134, 'venta'),
(135, '2024-11-28 17:00:00.000000', 12000.00, 'Ingreso por Venta ID 135', 135, 'venta'),
(136, '2024-11-29 18:00:00.000000', 9000.00, 'Ingreso por Venta ID 136', 136, 'venta'),
(137, '2024-11-30 19:00:00.000000', 21000.00, 'Ingreso por Venta ID 137', 137, 'venta'),
(138, '2024-12-01 10:00:00.000000', 15000.00, 'Ingreso por Venta ID 138', 138, 'venta'),
(139, '2024-12-02 11:00:00.000000', 18000.00, 'Ingreso por Venta ID 139', 139, 'venta'),
(140, '2024-12-03 12:00:00.000000', 12000.00, 'Ingreso por Venta ID 140', 140, 'venta'),
(141, '2024-12-04 13:00:00.000000', 9000.00, 'Ingreso por Venta ID 141', 141, 'venta'),
(142, '2024-12-05 14:00:00.000000', 21000.00, 'Ingreso por Venta ID 142', 142, 'venta'),
(143, '2024-12-06 15:00:00.000000', 15000.00, 'Ingreso por Venta ID 143', 143, 'venta'),
(144, '2024-12-07 16:00:00.000000', 18000.00, 'Ingreso por Venta ID 144', 144, 'venta'),
(145, '2024-12-08 17:00:00.000000', 12000.00, 'Ingreso por Venta ID 145', 145, 'venta'),
(146, '2024-12-09 18:00:00.000000', 9000.00, 'Ingreso por Venta ID 146', 146, 'venta'),
(147, '2024-12-10 19:00:00.000000', 21000.00, 'Ingreso por Venta ID 147', 147, 'venta'),
(148, '2024-12-11 10:00:00.000000', 15000.00, 'Ingreso por Venta ID 148', 148, 'venta'),
(149, '2024-12-12 11:00:00.000000', 18000.00, 'Ingreso por Venta ID 149', 149, 'venta'),
(150, '2024-12-13 12:00:00.000000', 12000.00, 'Ingreso por Venta ID 150', 150, 'venta');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_inventario_producto`
--

CREATE TABLE `app_inventario_producto` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` longtext NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `cantidad_stock` int(11) NOT NULL,
  `stock_minimo` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Volcado de datos para la tabla `app_inventario_producto`
--

INSERT INTO `app_inventario_producto` (`id`, `nombre`, `descripcion`, `precio`, `cantidad_stock`, `stock_minimo`) VALUES
(1, 'Aguila Ligth Botella', 'Aguila Ligth  330ml', 3000.00, 552, 30),
(2, 'Aguila Original Botella', 'Aguila Original Botella 330 ml', 3000.00, 30, 30),
(3, 'Poker Botella', 'Poker botella  330 ml', 3000.00, 12, 30),
(4, 'budweiser botella', 'budweiser Botella', 3000.00, 0, 6),
(5, 'Costeña Bacana Botella', 'Costeña Bacana  Botella 330 ml', 3000.00, 89, 30),
(6, 'Coronita', 'Coronita botella 210 ml', 4000.00, 13, 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_pedidos_pedido`
--

CREATE TABLE `app_pedidos_pedido` (
  `id` bigint(20) NOT NULL,
  `fecha_pedido` date NOT NULL,
  `estado` varchar(20) NOT NULL,
  `proveedor_id` bigint(20) NOT NULL,
  `observaciones` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Volcado de datos para la tabla `app_pedidos_pedido`
--

INSERT INTO `app_pedidos_pedido` (`id`, `fecha_pedido`, `estado`, `proveedor_id`, `observaciones`) VALUES
(2, '2024-11-05', 'recibido', 1, 'Poker 2 canastas\r\nAguila Original 2 canastas \r\nAguila Ligth 22 canastas \r\nCoronita 4 six pack \r\nCosteña 4 canastas \r\nfecha 02-10-24');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_pedidos_pedidodetalle`
--

CREATE TABLE `app_pedidos_pedidodetalle` (
  `id` bigint(20) NOT NULL,
  `cantidad` int(10) UNSIGNED NOT NULL CHECK (`cantidad` >= 0),
  `costo_unitario` decimal(10,2) NOT NULL,
  `pedido_id` bigint(20) NOT NULL,
  `producto_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Volcado de datos para la tabla `app_pedidos_pedidodetalle`
--

INSERT INTO `app_pedidos_pedidodetalle` (`id`, `cantidad`, `costo_unitario`, `pedido_id`, `producto_id`) VALUES
(1, 60, 1946.00, 2, 3),
(2, 60, 2016.00, 2, 2),
(3, 659, 2029.00, 2, 1),
(4, 24, 2478.98, 2, 6),
(5, 120, 1683.00, 2, 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_pedidos_proveedor`
--

CREATE TABLE `app_pedidos_proveedor` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `direccion` longtext NOT NULL,
  `telefono` varchar(15) NOT NULL,
  `email` varchar(254) NOT NULL,
  `fecha_registro` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Volcado de datos para la tabla `app_pedidos_proveedor`
--

INSERT INTO `app_pedidos_proveedor` (`id`, `nombre`, `direccion`, `telefono`, `email`, `fecha_registro`) VALUES
(1, 'Bavaria', 'Carrera 53A # 127-35', '018000 526555', 'Protecciondedatos@co.ab-inbev.com', '2025-04-27 16:17:34.085363'),
(2, 'Distribuidora MR&T', 'N/A', '3218034028', 'distribuidoraMR&T@gmail.com', '2025-04-27 16:22:45.228737'),
(3, 'Gaseosas LUX S.A.S', 'CR 2 ESTE 1635', '018000515959', 'recepcionfe@gaslux.com.co', '2025-04-27 16:24:26.304170'),
(4, 'Distribuidora Distribuciones JYC Rico S.A.S', 'Cr 8601 Urb Bolonia MZ - El rosal', '3143598575', 'distribucionesJYCRico@gmail.com', '2025-04-27 16:27:48.910413'),
(5, 'Dulcería San Carlos', 'CR 8 No 11-04 Barrio San Carlos', '3217547484', 'alexrooos31@gmail.com', '2025-04-27 16:29:04.116705');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_predicciones_historialprediccion`
--

CREATE TABLE `app_predicciones_historialprediccion` (
  `id` bigint(20) NOT NULL,
  `fecha_evaluacion` datetime(6) NOT NULL,
  `precision` decimal(5,2) NOT NULL,
  `comentarios` longtext NOT NULL,
  `prediccion_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_predicciones_prediccionnegocio`
--

CREATE TABLE `app_predicciones_prediccionnegocio` (
  `id` bigint(20) NOT NULL,
  `fecha_generacion` datetime(6) NOT NULL,
  `tipo_prediccion` varchar(20) NOT NULL,
  `prioridad` varchar(10) NOT NULL,
  `ventas_ultimos_30_dias` int(10) UNSIGNED NOT NULL CHECK (`ventas_ultimos_30_dias` >= 0),
  `ventas_ultimos_90_dias` int(10) UNSIGNED NOT NULL CHECK (`ventas_ultimos_90_dias` >= 0),
  `rotacion_mensual` decimal(5,2) NOT NULL,
  `margen_actual` decimal(5,2) NOT NULL,
  `dias_stock_actual` int(10) UNSIGNED NOT NULL CHECK (`dias_stock_actual` >= 0),
  `cantidad_recomendada` int(10) UNSIGNED NOT NULL CHECK (`cantidad_recomendada` >= 0),
  `precio_recomendado` decimal(10,2) DEFAULT NULL,
  `fecha_accion_recomendada` date NOT NULL,
  `inversion_estimada` decimal(10,2) DEFAULT NULL,
  `ganancia_estimada` decimal(10,2) DEFAULT NULL,
  `roi_estimado` decimal(5,2) DEFAULT NULL,
  `analisis` longtext NOT NULL,
  `producto_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_reportes_estadisticaventa`
--

CREATE TABLE `app_reportes_estadisticaventa` (
  `id` bigint(20) NOT NULL,
  `fecha` date NOT NULL,
  `cantidad_vendida` int(10) UNSIGNED NOT NULL CHECK (`cantidad_vendida` >= 0),
  `ingreso_total` decimal(10,2) NOT NULL,
  `rotacion_inventario` decimal(5,2) NOT NULL,
  `dias_sin_venta` int(10) UNSIGNED NOT NULL CHECK (`dias_sin_venta` >= 0),
  `producto_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_reportes_venta`
--

CREATE TABLE `app_reportes_venta` (
  `id` bigint(20) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `fecha` date NOT NULL,
  `hora` time(6) NOT NULL,
  `observaciones` longtext DEFAULT NULL,
  `producto_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_usuarios_pin`
--

CREATE TABLE `app_usuarios_pin` (
  `id` bigint(20) NOT NULL,
  `pin` varchar(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_usuarios_profile`
--

CREATE TABLE `app_usuarios_profile` (
  `id` bigint(20) NOT NULL,
  `nombre_completo` varchar(100) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `fecha_contratacion` date DEFAULT NULL,
  `rol` varchar(20) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Volcado de datos para la tabla `app_usuarios_profile`
--

INSERT INTO `app_usuarios_profile` (`id`, `nombre_completo`, `telefono`, `direccion`, `fecha_contratacion`, `rol`, `user_id`) VALUES
(1, '', NULL, NULL, NULL, 'Administrador', 1),
(2, 'Juan Esteban Cortes Celis', '3002714478', 'El Rosal', '2024-10-01', 'Empleado', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_ventas_venta`
--

CREATE TABLE `app_ventas_venta` (
  `id` bigint(20) NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `fecha_modificacion` datetime(6) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `observaciones` longtext DEFAULT NULL,
  `creado_por_id` bigint(20) DEFAULT NULL,
  `empleado_id` bigint(20) NOT NULL,
  `modificado_por_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Volcado de datos para la tabla `app_ventas_venta`
--

INSERT INTO `app_ventas_venta` (`id`, `fecha_creacion`, `fecha_modificacion`, `estado`, `total`, `observaciones`, `creado_por_id`, `empleado_id`, `modificado_por_id`) VALUES
(1, '2024-11-07 10:15:20.444214', '2024-11-07 10:15:20.437606', 'completada', 9000.00, 'None', NULL, 1, 1),
(2, '2024-11-14 11:24:48.669737', '2024-11-14 11:24:48.692977', 'completada', 9000.00, NULL, NULL, 1, NULL),
(3, '2024-11-21 14:35:37.465000', '2024-11-21 14:35:37.492955', 'completada', 12000.00, NULL, NULL, 1, NULL),
(4, '2024-11-28 16:47:01.176030', '2024-11-28 16:47:01.206608', 'completada', 12000.00, NULL, NULL, 1, NULL),
(5, '2024-12-05 09:16:08.091558', '2024-12-05 09:16:08.119558', 'completada', 60000.00, NULL, NULL, 2, NULL),
(6, '2024-12-12 10:27:37.746320', '2024-12-12 10:27:37.783713', 'completada', 30000.00, NULL, NULL, 2, NULL),
(7, '2024-12-19 15:38:59.773049', '2024-12-19 15:38:59.820458', 'completada', 90000.00, NULL, NULL, 2, NULL),
(8, '2024-12-26 17:44:52.582925', '2024-12-26 17:44:52.640591', 'completada', 16000.00, NULL, NULL, 2, NULL),
(9, '2025-01-02 11:25:38.567368', '2025-01-02 11:25:38.585686', 'completada', 12000.00, NULL, NULL, 2, NULL),
(10, '2025-01-09 13:34:20.184036', '2025-01-09 13:34:20.217786', 'completada', 10000.00, NULL, NULL, 2, NULL),
(11, '2025-01-16 14:35:12.207012', '2025-01-16 14:35:12.221601', 'completada', 33000.00, NULL, NULL, 2, NULL),
(12, '2025-01-23 16:36:21.867403', '2025-01-23 16:36:21.897907', 'completada', 45000.00, NULL, NULL, 2, NULL),
(13, '2025-02-06 10:37:21.020570', '2025-02-06 10:37:21.035898', 'completada', 8000.00, NULL, NULL, 2, NULL),
(14, '2025-02-13 11:37:42.218151', '2025-02-13 11:37:42.234423', 'completada', 10000.00, NULL, NULL, 2, NULL),
(15, '2025-02-20 14:40:09.938573', '2025-02-20 14:40:09.960094', 'completada', 60000.00, NULL, NULL, 2, NULL),
(16, '2025-02-27 15:41:34.111486', '2025-02-27 15:41:34.146338', 'completada', 30000.00, NULL, NULL, 2, NULL),
(17, '2025-03-06 09:42:37.382716', '2025-03-06 09:42:37.407226', 'completada', 75000.00, NULL, NULL, 2, NULL),
(18, '2025-03-13 10:43:52.153947', '2025-03-13 10:43:52.166634', 'completada', 6000.00, NULL, NULL, 1, NULL),
(19, '2025-03-20 14:44:03.234011', '2025-03-20 14:44:03.249993', 'completada', 9000.00, NULL, NULL, 1, NULL),
(20, '2025-03-27 16:44:21.081482', '2025-03-27 16:44:21.093820', 'completada', 24000.00, NULL, NULL, 1, NULL),
(21, '2025-04-03 10:44:50.798263', '2025-04-03 10:44:50.823769', 'completada', 27000.00, NULL, NULL, 1, NULL),
(22, '2025-04-10 11:45:10.880687', '2025-04-10 11:45:10.903345', 'completada', 15000.00, NULL, NULL, 1, NULL),
(23, '2025-04-17 14:45:27.299545', '2025-04-17 14:45:27.313469', 'completada', 45000.00, NULL, NULL, 1, NULL),
(24, '2025-04-24 16:45:54.462231', '2025-04-24 16:45:54.481812', 'completada', 45000.00, NULL, NULL, 1, NULL),
(25, '2024-05-03 11:10:00.000000', '2024-05-03 11:10:00.000000', 'completada', 15000.00, NULL, 1, 1, 1),
(26, '2024-06-10 13:20:00.000000', '2024-06-10 13:20:00.000000', 'completada', 21000.00, NULL, 2, 2, 2),
(27, '2024-07-15 15:30:00.000000', '2024-07-15 15:30:00.000000', 'completada', 12000.00, NULL, 1, 1, 1),
(28, '2024-08-05 10:00:00.000000', '2024-08-05 10:00:00.000000', 'completada', 18000.00, NULL, 2, 2, 2),
(29, '2024-09-12 16:00:00.000000', '2024-09-12 16:00:00.000000', 'completada', 24000.00, NULL, 1, 1, 1),
(30, '2024-10-20 14:45:00.000000', '2024-10-20 14:45:00.000000', 'completada', 27000.00, NULL, 2, 2, 2),
(31, '2024-11-01 10:00:00.000000', '2024-11-01 10:00:00.000000', 'completada', 9000.00, NULL, 1, 1, 1),
(32, '2024-11-02 11:00:00.000000', '2024-11-02 11:00:00.000000', 'completada', 12000.00, NULL, 2, 2, 2),
(33, '2024-11-03 12:00:00.000000', '2024-11-03 12:00:00.000000', 'completada', 15000.00, NULL, 1, 1, 1),
(34, '2024-11-04 13:00:00.000000', '2024-11-04 13:00:00.000000', 'completada', 18000.00, NULL, 2, 2, 2),
(35, '2024-11-05 14:00:00.000000', '2024-11-05 14:00:00.000000', 'completada', 21000.00, NULL, 1, 1, 1),
(36, '2024-11-06 15:00:00.000000', '2024-11-06 15:00:00.000000', 'completada', 9000.00, NULL, 2, 2, 2),
(37, '2024-11-07 16:00:00.000000', '2024-11-07 16:00:00.000000', 'completada', 12000.00, NULL, 1, 1, 1),
(38, '2024-11-08 17:00:00.000000', '2024-11-08 17:00:00.000000', 'completada', 15000.00, NULL, 2, 2, 2),
(39, '2024-11-09 18:00:00.000000', '2024-11-09 18:00:00.000000', 'completada', 18000.00, NULL, 1, 1, 1),
(40, '2024-11-10 19:00:00.000000', '2024-11-10 19:00:00.000000', 'completada', 21000.00, NULL, 2, 2, 2),
(41, '2024-11-21 10:00:00.000000', '2024-11-21 10:00:00.000000', 'completada', 12000.00, NULL, 1, 1, 1),
(42, '2024-11-22 11:00:00.000000', '2024-11-22 11:00:00.000000', 'completada', 15000.00, NULL, 2, 2, 2),
(43, '2024-11-23 12:00:00.000000', '2024-11-23 12:00:00.000000', 'completada', 18000.00, NULL, 1, 1, 1),
(44, '2024-11-24 13:00:00.000000', '2024-11-24 13:00:00.000000', 'completada', 9000.00, NULL, 2, 2, 2),
(45, '2024-11-25 14:00:00.000000', '2024-11-25 14:00:00.000000', 'completada', 21000.00, NULL, 1, 1, 1),
(46, '2024-11-26 15:00:00.000000', '2024-11-26 15:00:00.000000', 'completada', 15000.00, NULL, 2, 2, 2),
(47, '2024-11-17 16:00:00.000000', '2024-11-17 16:00:00.000000', 'completada', 18000.00, NULL, 1, 1, 1),
(48, '2024-11-18 17:00:00.000000', '2024-11-18 17:00:00.000000', 'completada', 12000.00, NULL, 2, 2, 2),
(49, '2024-11-19 18:00:00.000000', '2024-11-19 18:00:00.000000', 'completada', 9000.00, NULL, 1, 1, 1),
(50, '2024-11-20 19:00:00.000000', '2024-11-20 19:00:00.000000', 'completada', 21000.00, NULL, 2, 2, 2),
(51, '2024-11-21 10:00:00.000000', '2024-11-21 10:00:00.000000', 'completada', 15000.00, NULL, 1, 1, 1),
(52, '2024-11-14 13:00:00.000000', '2024-11-14 13:00:00.000000', 'completada', 9000.00, NULL, 2, 2, 2),
(53, '2024-11-15 14:00:00.000000', '2024-11-15 14:00:00.000000', 'completada', 21000.00, NULL, 1, 1, 1),
(54, '2024-11-16 15:00:00.000000', '2024-11-16 15:00:00.000000', 'completada', 15000.00, NULL, 2, 2, 2),
(55, '2024-11-17 16:00:00.000000', '2024-11-17 16:00:00.000000', 'completada', 18000.00, NULL, 1, 1, 1),
(56, '2024-11-18 17:00:00.000000', '2024-11-18 17:00:00.000000', 'completada', 12000.00, NULL, 2, 2, 2),
(57, '2024-11-19 18:00:00.000000', '2024-11-19 18:00:00.000000', 'completada', 9000.00, NULL, 1, 1, 1),
(58, '2024-11-20 19:00:00.000000', '2024-11-20 19:00:00.000000', 'completada', 21000.00, NULL, 2, 2, 2),
(59, '2024-11-21 10:00:00.000000', '2024-11-21 10:00:00.000000', 'completada', 15000.00, NULL, 1, 1, 1),
(60, '2024-11-22 11:00:00.000000', '2024-11-22 11:00:00.000000', 'completada', 18000.00, NULL, 2, 2, 2),
(61, '2024-11-23 12:00:00.000000', '2024-11-23 12:00:00.000000', 'completada', 12000.00, NULL, 1, 1, 1),
(62, '2024-11-24 13:00:00.000000', '2024-11-24 13:00:00.000000', 'completada', 9000.00, NULL, 2, 2, 2),
(63, '2024-11-25 14:00:00.000000', '2024-11-25 14:00:00.000000', 'completada', 21000.00, NULL, 1, 1, 1),
(64, '2024-11-26 15:00:00.000000', '2024-11-26 15:00:00.000000', 'completada', 15000.00, NULL, 2, 2, 2),
(65, '2024-11-27 16:00:00.000000', '2024-11-27 16:00:00.000000', 'completada', 18000.00, NULL, 1, 1, 1),
(66, '2024-11-28 17:00:00.000000', '2024-11-28 17:00:00.000000', 'completada', 12000.00, NULL, 2, 2, 2),
(67, '2024-11-29 18:00:00.000000', '2024-11-29 18:00:00.000000', 'completada', 9000.00, NULL, 1, 1, 1),
(68, '2024-11-30 19:00:00.000000', '2024-11-30 19:00:00.000000', 'completada', 21000.00, NULL, 2, 2, 2),
(69, '2024-12-01 10:00:00.000000', '2024-12-01 10:00:00.000000', 'completada', 15000.00, NULL, 1, 1, 1),
(70, '2024-12-02 11:00:00.000000', '2024-12-02 11:00:00.000000', 'completada', 18000.00, NULL, 2, 2, 2),
(71, '2024-12-03 12:00:00.000000', '2024-12-03 12:00:00.000000', 'completada', 12000.00, NULL, 1, 1, 1),
(72, '2024-12-04 13:00:00.000000', '2024-12-04 13:00:00.000000', 'completada', 9000.00, NULL, 2, 2, 2),
(73, '2024-12-05 14:00:00.000000', '2024-12-05 14:00:00.000000', 'completada', 21000.00, NULL, 1, 1, 1),
(74, '2024-12-06 15:00:00.000000', '2024-12-06 15:00:00.000000', 'completada', 15000.00, NULL, 2, 2, 2),
(75, '2024-12-07 16:00:00.000000', '2024-12-07 16:00:00.000000', 'completada', 18000.00, NULL, 1, 1, 1),
(76, '2024-12-08 17:00:00.000000', '2024-12-08 17:00:00.000000', 'completada', 12000.00, NULL, 2, 2, 2),
(77, '2024-12-09 18:00:00.000000', '2024-12-09 18:00:00.000000', 'completada', 9000.00, NULL, 1, 1, 1),
(78, '2024-12-10 19:00:00.000000', '2024-12-10 19:00:00.000000', 'completada', 21000.00, NULL, 2, 2, 2),
(79, '2024-12-11 10:00:00.000000', '2024-12-11 10:00:00.000000', 'completada', 15000.00, NULL, 1, 1, 1),
(80, '2024-12-12 11:00:00.000000', '2024-12-12 11:00:00.000000', 'completada', 18000.00, NULL, 2, 2, 2),
(81, '2024-12-13 12:00:00.000000', '2024-12-13 12:00:00.000000', 'completada', 12000.00, NULL, 1, 1, 1),
(82, '2024-12-14 13:00:00.000000', '2024-12-14 13:00:00.000000', 'completada', 9000.00, NULL, 2, 2, 2),
(83, '2024-12-15 14:00:00.000000', '2024-12-15 14:00:00.000000', 'completada', 21000.00, NULL, 1, 1, 1),
(84, '2024-12-16 15:00:00.000000', '2024-12-16 15:00:00.000000', 'completada', 15000.00, NULL, 2, 2, 2),
(85, '2024-12-17 16:00:00.000000', '2024-12-17 16:00:00.000000', 'completada', 18000.00, NULL, 1, 1, 1),
(86, '2024-12-18 17:00:00.000000', '2024-12-18 17:00:00.000000', 'completada', 12000.00, NULL, 2, 2, 2),
(87, '2024-12-19 18:00:00.000000', '2024-12-19 18:00:00.000000', 'completada', 9000.00, NULL, 1, 1, 1),
(88, '2024-12-20 19:00:00.000000', '2024-12-20 19:00:00.000000', 'completada', 21000.00, NULL, 2, 2, 2),
(89, '2024-12-21 10:00:00.000000', '2024-12-21 10:00:00.000000', 'completada', 15000.00, NULL, 1, 1, 1),
(90, '2024-12-22 11:00:00.000000', '2024-12-22 11:00:00.000000', 'completada', 18000.00, NULL, 2, 2, 2),
(91, '2024-12-23 12:00:00.000000', '2024-12-23 12:00:00.000000', 'completada', 12000.00, NULL, 1, 1, 1),
(92, '2024-12-24 13:00:00.000000', '2024-12-24 13:00:00.000000', 'completada', 9000.00, NULL, 2, 2, 2),
(93, '2024-12-25 14:00:00.000000', '2024-12-25 14:00:00.000000', 'completada', 21000.00, NULL, 1, 1, 1),
(94, '2024-12-26 15:00:00.000000', '2024-12-26 15:00:00.000000', 'completada', 15000.00, NULL, 2, 2, 2),
(95, '2024-12-27 16:00:00.000000', '2024-12-27 16:00:00.000000', 'completada', 18000.00, NULL, 1, 1, 1),
(96, '2024-12-28 17:00:00.000000', '2024-12-28 17:00:00.000000', 'completada', 12000.00, NULL, 2, 2, 2),
(97, '2024-12-29 18:00:00.000000', '2024-12-29 18:00:00.000000', 'completada', 9000.00, NULL, 1, 1, 1),
(98, '2024-12-30 19:00:00.000000', '2024-12-30 19:00:00.000000', 'completada', 21000.00, NULL, 2, 2, 2),
(99, '2024-12-31 10:00:00.000000', '2024-12-31 10:00:00.000000', 'completada', 15000.00, NULL, 1, 1, 1),
(100, '2025-01-01 11:00:00.000000', '2025-01-01 11:00:00.000000', 'completada', 18000.00, NULL, 2, 2, 2),
(101, '2025-01-02 12:00:00.000000', '2025-01-02 12:00:00.000000', 'completada', 12000.00, NULL, 1, 1, 1),
(102, '2025-01-03 13:00:00.000000', '2025-01-03 13:00:00.000000', 'completada', 9000.00, NULL, 2, 2, 2),
(103, '2025-01-04 14:00:00.000000', '2025-01-04 14:00:00.000000', 'completada', 21000.00, NULL, 1, 1, 1),
(104, '2025-01-05 15:00:00.000000', '2025-01-05 15:00:00.000000', 'completada', 15000.00, NULL, 2, 2, 2),
(105, '2025-01-06 16:00:00.000000', '2025-01-06 16:00:00.000000', 'completada', 18000.00, NULL, 1, 1, 1),
(106, '2025-01-07 17:00:00.000000', '2025-01-07 17:00:00.000000', 'completada', 12000.00, NULL, 2, 2, 2),
(107, '2025-01-08 18:00:00.000000', '2025-01-08 18:00:00.000000', 'completada', 9000.00, NULL, 1, 1, 1),
(108, '2025-01-09 19:00:00.000000', '2025-01-09 19:00:00.000000', 'completada', 21000.00, NULL, 2, 2, 2),
(109, '2025-01-10 10:00:00.000000', '2025-01-10 10:00:00.000000', 'completada', 15000.00, NULL, 1, 1, 1),
(110, '2025-01-11 11:00:00.000000', '2025-01-11 11:00:00.000000', 'completada', 18000.00, NULL, 2, 2, 2),
(111, '2025-01-12 12:00:00.000000', '2025-01-12 12:00:00.000000', 'completada', 12000.00, NULL, 1, 1, 1),
(112, '2025-01-13 13:00:00.000000', '2025-01-13 13:00:00.000000', 'completada', 9000.00, NULL, 2, 2, 2),
(113, '2025-01-14 14:00:00.000000', '2025-01-14 14:00:00.000000', 'completada', 21000.00, NULL, 1, 1, 1),
(114, '2025-01-15 15:00:00.000000', '2025-01-15 15:00:00.000000', 'completada', 15000.00, NULL, 2, 2, 2),
(115, '2025-01-16 16:00:00.000000', '2025-01-16 16:00:00.000000', 'completada', 18000.00, NULL, 1, 1, 1),
(116, '2025-01-17 17:00:00.000000', '2025-01-17 17:00:00.000000', 'completada', 12000.00, NULL, 2, 2, 2),
(117, '2025-01-18 18:00:00.000000', '2025-01-18 18:00:00.000000', 'completada', 9000.00, NULL, 1, 1, 1),
(118, '2025-01-19 19:00:00.000000', '2025-01-19 19:00:00.000000', 'completada', 21000.00, NULL, 2, 2, 2),
(119, '2025-01-20 10:00:00.000000', '2025-01-20 10:00:00.000000', 'completada', 15000.00, NULL, 1, 1, 1),
(120, '2025-01-21 11:00:00.000000', '2025-01-21 11:00:00.000000', 'completada', 18000.00, NULL, 2, 2, 2),
(121, '2025-01-22 12:00:00.000000', '2025-01-22 12:00:00.000000', 'completada', 12000.00, NULL, 1, 1, 1),
(122, '2025-01-23 13:00:00.000000', '2025-01-23 13:00:00.000000', 'completada', 9000.00, NULL, 2, 2, 2),
(123, '2025-01-24 14:00:00.000000', '2025-01-24 14:00:00.000000', 'completada', 21000.00, NULL, 1, 1, 1),
(124, '2025-01-25 15:00:00.000000', '2025-01-25 15:00:00.000000', 'completada', 15000.00, NULL, 2, 2, 2),
(125, '2025-01-26 16:00:00.000000', '2025-01-26 16:00:00.000000', 'completada', 18000.00, NULL, 1, 1, 1),
(126, '2025-01-27 17:00:00.000000', '2025-01-27 17:00:00.000000', 'completada', 12000.00, NULL, 2, 2, 2),
(127, '2025-01-28 18:00:00.000000', '2025-01-28 18:00:00.000000', 'completada', 9000.00, NULL, 1, 1, 1),
(128, '2025-01-29 19:00:00.000000', '2025-01-29 19:00:00.000000', 'completada', 21000.00, NULL, 2, 2, 2),
(129, '2024-11-22 11:00:00.000000', '2024-11-22 11:00:00.000000', 'completada', 18000.00, NULL, 2, 2, 2),
(130, '2024-11-23 12:00:00.000000', '2024-11-23 12:00:00.000000', 'completada', 12000.00, NULL, 1, 1, 1),
(131, '2024-11-24 13:00:00.000000', '2024-11-24 13:00:00.000000', 'completada', 9000.00, NULL, 2, 2, 2),
(132, '2024-11-25 14:00:00.000000', '2024-11-25 14:00:00.000000', 'completada', 21000.00, NULL, 1, 1, 1),
(133, '2024-11-26 15:00:00.000000', '2024-11-26 15:00:00.000000', 'completada', 15000.00, NULL, 2, 2, 2),
(134, '2024-11-27 16:00:00.000000', '2024-11-27 16:00:00.000000', 'completada', 18000.00, NULL, 1, 1, 1),
(135, '2024-11-28 17:00:00.000000', '2024-11-28 17:00:00.000000', 'completada', 12000.00, NULL, 2, 2, 2),
(136, '2024-11-29 18:00:00.000000', '2024-11-29 18:00:00.000000', 'completada', 9000.00, NULL, 1, 1, 1),
(137, '2024-11-30 19:00:00.000000', '2024-11-30 19:00:00.000000', 'completada', 21000.00, NULL, 2, 2, 2),
(138, '2024-12-01 10:00:00.000000', '2024-12-01 10:00:00.000000', 'completada', 15000.00, NULL, 1, 1, 1),
(139, '2024-12-02 11:00:00.000000', '2024-12-02 11:00:00.000000', 'completada', 18000.00, NULL, 2, 2, 2),
(140, '2024-12-03 12:00:00.000000', '2024-12-03 12:00:00.000000', 'completada', 12000.00, NULL, 1, 1, 1),
(141, '2024-12-04 13:00:00.000000', '2024-12-04 13:00:00.000000', 'completada', 9000.00, NULL, 2, 2, 2),
(142, '2024-12-05 14:00:00.000000', '2024-12-05 14:00:00.000000', 'completada', 21000.00, NULL, 1, 1, 1),
(143, '2024-12-06 15:00:00.000000', '2024-12-06 15:00:00.000000', 'completada', 15000.00, NULL, 2, 2, 2),
(144, '2024-12-07 16:00:00.000000', '2024-12-07 16:00:00.000000', 'completada', 18000.00, NULL, 1, 1, 1),
(145, '2024-12-08 17:00:00.000000', '2024-12-08 17:00:00.000000', 'completada', 12000.00, NULL, 2, 2, 2),
(146, '2024-12-09 18:00:00.000000', '2024-12-09 18:00:00.000000', 'completada', 9000.00, NULL, 1, 1, 1),
(147, '2024-12-10 19:00:00.000000', '2024-12-10 19:00:00.000000', 'completada', 21000.00, NULL, 2, 2, 2),
(148, '2024-12-11 10:00:00.000000', '2024-12-11 10:00:00.000000', 'completada', 15000.00, NULL, 1, 1, 1),
(149, '2024-12-12 11:00:00.000000', '2024-12-12 11:00:00.000000', 'completada', 18000.00, NULL, 2, 2, 2),
(150, '2024-12-13 12:00:00.000000', '2024-12-13 12:00:00.000000', 'completada', 12000.00, NULL, 1, 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_ventas_ventadetalle`
--

CREATE TABLE `app_ventas_ventadetalle` (
  `id` bigint(20) NOT NULL,
  `cantidad` int(10) UNSIGNED NOT NULL CHECK (`cantidad` >= 0),
  `precio_unitario` decimal(10,2) NOT NULL,
  `precio_total` decimal(10,2) NOT NULL,
  `producto_id` bigint(20) NOT NULL,
  `venta_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Volcado de datos para la tabla `app_ventas_ventadetalle`
--

INSERT INTO `app_ventas_ventadetalle` (`id`, `cantidad`, `precio_unitario`, `precio_total`, `producto_id`, `venta_id`) VALUES
(1, 2, 3000.00, 6000.00, 1, 1),
(2, 1, 3000.00, 3000.00, 3, 1),
(3, 1, 3000.00, 3000.00, 1, 2),
(4, 1, 3000.00, 3000.00, 3, 2),
(5, 1, 3000.00, 3000.00, 1, 2),
(6, 2, 3000.00, 6000.00, 1, 3),
(7, 2, 3000.00, 6000.00, 2, 3),
(8, 2, 3000.00, 6000.00, 1, 4),
(9, 2, 3000.00, 6000.00, 3, 4),
(10, 15, 3000.00, 45000.00, 1, 5),
(11, 5, 3000.00, 15000.00, 3, 5),
(12, 6, 3000.00, 18000.00, 5, 6),
(13, 4, 3000.00, 12000.00, 3, 6),
(14, 10, 3000.00, 30000.00, 1, 7),
(15, 10, 3000.00, 30000.00, 5, 7),
(16, 5, 3000.00, 15000.00, 3, 7),
(17, 5, 3000.00, 15000.00, 2, 7),
(18, 1, 3000.00, 3000.00, 1, 8),
(19, 1, 3000.00, 3000.00, 2, 8),
(20, 1, 3000.00, 3000.00, 3, 8),
(21, 1, 3000.00, 3000.00, 5, 8),
(22, 1, 4000.00, 4000.00, 6, 8),
(23, 4, 3000.00, 12000.00, 3, 9),
(24, 2, 3000.00, 6000.00, 1, 10),
(25, 1, 4000.00, 4000.00, 6, 10),
(26, 4, 3000.00, 12000.00, 1, 11),
(27, 7, 3000.00, 21000.00, 2, 11),
(28, 4, 3000.00, 12000.00, 1, 12),
(29, 4, 3000.00, 12000.00, 1, 12),
(30, 3, 3000.00, 9000.00, 3, 12),
(31, 4, 3000.00, 12000.00, 5, 12),
(32, 1, 4000.00, 4000.00, 6, 13),
(33, 1, 4000.00, 4000.00, 6, 13),
(34, 1, 4000.00, 4000.00, 6, 14),
(35, 2, 3000.00, 6000.00, 1, 14),
(36, 14, 3000.00, 42000.00, 1, 15),
(37, 2, 3000.00, 6000.00, 1, 15),
(38, 4, 3000.00, 12000.00, 3, 15),
(39, 2, 3000.00, 6000.00, 1, 16),
(40, 2, 3000.00, 6000.00, 2, 16),
(41, 5, 3000.00, 15000.00, 3, 16),
(42, 1, 3000.00, 3000.00, 5, 16),
(43, 10, 3000.00, 30000.00, 1, 17),
(44, 5, 3000.00, 15000.00, 5, 17),
(45, 10, 3000.00, 30000.00, 3, 17),
(46, 2, 3000.00, 6000.00, 1, 18),
(47, 3, 3000.00, 9000.00, 3, 19),
(48, 6, 4000.00, 24000.00, 6, 20),
(49, 4, 3000.00, 12000.00, 1, 21),
(50, 5, 3000.00, 15000.00, 2, 21),
(51, 4, 3000.00, 12000.00, 5, 22),
(52, 1, 3000.00, 3000.00, 2, 22),
(53, 15, 3000.00, 45000.00, 1, 23),
(54, 7, 3000.00, 21000.00, 2, 24),
(55, 8, 3000.00, 24000.00, 1, 24),
(56, 3, 3000.00, 9000.00, 1, 25),
(57, 2, 3000.00, 6000.00, 3, 25),
(58, 7, 3000.00, 21000.00, 2, 26),
(59, 2, 3000.00, 6000.00, 5, 26),
(60, 4, 3000.00, 12000.00, 1, 27),
(61, 2, 3000.00, 6000.00, 3, 27),
(62, 4, 3000.00, 12000.00, 5, 28),
(63, 2, 3000.00, 6000.00, 6, 28),
(64, 5, 3000.00, 15000.00, 1, 29),
(65, 3, 3000.00, 9000.00, 2, 29),
(66, 6, 3000.00, 18000.00, 5, 30),
(67, 3, 3000.00, 9000.00, 6, 30),
(68, 3, 4000.00, 12000.00, 1, 52),
(69, 2, 3000.00, 6000.00, 2, 52),
(70, 5, 3000.00, 15000.00, 3, 53),
(71, 1, 3000.00, 3000.00, 4, 53),
(72, 6, 3000.00, 18000.00, 5, 54),
(73, 2, 3000.00, 6000.00, 6, 54),
(74, 4, 3000.00, 12000.00, 1, 55),
(75, 2, 3000.00, 6000.00, 2, 55),
(76, 7, 3000.00, 21000.00, 3, 56),
(77, 1, 3000.00, 3000.00, 4, 56),
(78, 5, 3000.00, 15000.00, 5, 57),
(79, 2, 3000.00, 6000.00, 6, 57),
(80, 4, 3000.00, 12000.00, 1, 58),
(81, 2, 3000.00, 6000.00, 2, 58),
(82, 6, 3000.00, 18000.00, 3, 59),
(83, 1, 3000.00, 3000.00, 4, 59),
(84, 5, 3000.00, 15000.00, 5, 60),
(85, 2, 3000.00, 6000.00, 6, 60),
(86, 4, 3000.00, 12000.00, 1, 61),
(87, 2, 3000.00, 6000.00, 2, 61),
(88, 7, 3000.00, 21000.00, 3, 62),
(89, 1, 3000.00, 3000.00, 4, 62),
(90, 5, 3000.00, 15000.00, 5, 63),
(91, 2, 3000.00, 6000.00, 6, 63),
(92, 4, 3000.00, 12000.00, 1, 64),
(93, 2, 3000.00, 6000.00, 2, 64),
(94, 6, 3000.00, 18000.00, 3, 65),
(95, 1, 3000.00, 3000.00, 4, 65),
(96, 5, 3000.00, 15000.00, 5, 66),
(97, 2, 3000.00, 6000.00, 6, 66),
(98, 4, 3000.00, 12000.00, 1, 67),
(99, 2, 3000.00, 6000.00, 2, 67),
(100, 6, 3000.00, 18000.00, 3, 68),
(101, 1, 3000.00, 3000.00, 4, 68),
(102, 5, 3000.00, 15000.00, 5, 69),
(103, 2, 3000.00, 6000.00, 6, 69),
(104, 4, 3000.00, 12000.00, 1, 70),
(105, 2, 3000.00, 6000.00, 2, 70),
(106, 7, 3000.00, 21000.00, 3, 71),
(107, 1, 3000.00, 3000.00, 4, 71),
(108, 5, 3000.00, 15000.00, 5, 72),
(109, 2, 3000.00, 6000.00, 6, 72),
(110, 4, 3000.00, 12000.00, 1, 73),
(111, 2, 3000.00, 6000.00, 2, 73),
(112, 6, 3000.00, 18000.00, 3, 74),
(113, 1, 3000.00, 3000.00, 4, 74),
(114, 5, 3000.00, 15000.00, 5, 75),
(115, 2, 3000.00, 6000.00, 6, 75),
(116, 4, 3000.00, 12000.00, 1, 76),
(117, 2, 3000.00, 6000.00, 2, 76),
(118, 7, 3000.00, 21000.00, 3, 77),
(119, 1, 3000.00, 3000.00, 4, 77),
(120, 5, 3000.00, 15000.00, 5, 78),
(121, 2, 3000.00, 6000.00, 6, 78),
(122, 4, 3000.00, 12000.00, 1, 79),
(123, 2, 3000.00, 6000.00, 2, 79),
(124, 6, 3000.00, 18000.00, 3, 80),
(125, 1, 3000.00, 3000.00, 4, 80),
(126, 5, 3000.00, 15000.00, 5, 81),
(127, 2, 3000.00, 6000.00, 6, 81),
(128, 4, 3000.00, 12000.00, 1, 82),
(129, 2, 3000.00, 6000.00, 2, 82),
(130, 7, 3000.00, 21000.00, 3, 83),
(131, 1, 3000.00, 3000.00, 4, 83),
(132, 5, 3000.00, 15000.00, 5, 84),
(133, 2, 3000.00, 6000.00, 6, 84),
(134, 4, 3000.00, 12000.00, 1, 85),
(135, 2, 3000.00, 6000.00, 2, 85),
(136, 6, 3000.00, 18000.00, 3, 86),
(137, 1, 3000.00, 3000.00, 4, 86),
(138, 5, 3000.00, 15000.00, 5, 87),
(139, 2, 3000.00, 6000.00, 6, 87),
(140, 4, 3000.00, 12000.00, 1, 88),
(141, 2, 3000.00, 6000.00, 2, 88),
(142, 7, 3000.00, 21000.00, 3, 89),
(143, 1, 3000.00, 3000.00, 4, 89),
(144, 5, 3000.00, 15000.00, 5, 90),
(145, 2, 3000.00, 6000.00, 6, 90),
(146, 4, 3000.00, 12000.00, 1, 91),
(147, 2, 3000.00, 6000.00, 2, 91),
(148, 6, 3000.00, 18000.00, 3, 92),
(149, 1, 3000.00, 3000.00, 4, 92),
(150, 5, 3000.00, 15000.00, 5, 93),
(151, 2, 3000.00, 6000.00, 6, 93),
(152, 4, 3000.00, 12000.00, 1, 94),
(153, 2, 3000.00, 6000.00, 2, 94),
(154, 6, 3000.00, 18000.00, 3, 95),
(155, 1, 3000.00, 3000.00, 4, 95),
(156, 5, 3000.00, 15000.00, 5, 96),
(157, 2, 3000.00, 6000.00, 6, 96),
(158, 4, 3000.00, 12000.00, 1, 97),
(159, 2, 3000.00, 6000.00, 2, 97),
(160, 7, 3000.00, 21000.00, 3, 98),
(161, 1, 3000.00, 3000.00, 4, 98),
(162, 5, 3000.00, 15000.00, 5, 99),
(163, 2, 3000.00, 6000.00, 6, 99),
(164, 4, 3000.00, 12000.00, 1, 100),
(165, 2, 3000.00, 6000.00, 2, 100),
(166, 6, 3000.00, 18000.00, 3, 101),
(167, 1, 3000.00, 3000.00, 4, 101),
(168, 5, 3000.00, 15000.00, 5, 102),
(169, 2, 3000.00, 6000.00, 6, 102),
(170, 4, 3000.00, 12000.00, 1, 103),
(171, 2, 3000.00, 6000.00, 2, 103),
(172, 7, 3000.00, 21000.00, 3, 104),
(173, 1, 3000.00, 3000.00, 4, 104),
(174, 5, 3000.00, 15000.00, 5, 105),
(175, 2, 3000.00, 6000.00, 6, 105),
(176, 4, 3000.00, 12000.00, 1, 106),
(177, 2, 3000.00, 6000.00, 2, 106),
(178, 6, 3000.00, 18000.00, 3, 107),
(179, 1, 3000.00, 3000.00, 4, 107),
(180, 5, 3000.00, 15000.00, 5, 108),
(181, 2, 3000.00, 6000.00, 6, 108),
(182, 4, 3000.00, 12000.00, 1, 109),
(183, 2, 3000.00, 6000.00, 2, 109),
(184, 7, 3000.00, 21000.00, 3, 110),
(185, 1, 3000.00, 3000.00, 4, 110),
(186, 5, 3000.00, 15000.00, 5, 111),
(187, 2, 3000.00, 6000.00, 6, 111),
(188, 4, 3000.00, 12000.00, 1, 112),
(189, 2, 3000.00, 6000.00, 2, 112),
(190, 6, 3000.00, 18000.00, 3, 113),
(191, 1, 3000.00, 3000.00, 4, 113),
(192, 5, 3000.00, 15000.00, 5, 114),
(193, 2, 3000.00, 6000.00, 6, 114),
(194, 4, 3000.00, 12000.00, 1, 115),
(195, 2, 3000.00, 6000.00, 2, 115),
(196, 7, 3000.00, 21000.00, 3, 116),
(197, 1, 3000.00, 3000.00, 4, 116),
(198, 5, 3000.00, 15000.00, 5, 117),
(199, 2, 3000.00, 6000.00, 6, 117),
(200, 4, 3000.00, 12000.00, 1, 118),
(201, 2, 3000.00, 6000.00, 2, 118),
(202, 6, 3000.00, 18000.00, 3, 119),
(203, 1, 3000.00, 3000.00, 4, 119),
(204, 5, 3000.00, 15000.00, 5, 120),
(205, 2, 3000.00, 6000.00, 6, 120),
(206, 4, 3000.00, 12000.00, 1, 121),
(207, 2, 3000.00, 6000.00, 2, 121),
(208, 7, 3000.00, 21000.00, 3, 122),
(209, 1, 3000.00, 3000.00, 4, 122),
(210, 5, 3000.00, 15000.00, 5, 123),
(211, 2, 3000.00, 6000.00, 6, 123),
(212, 4, 3000.00, 12000.00, 1, 124),
(213, 2, 3000.00, 6000.00, 2, 124),
(214, 6, 3000.00, 18000.00, 3, 125),
(215, 1, 3000.00, 3000.00, 4, 125),
(216, 5, 3000.00, 15000.00, 5, 126),
(217, 2, 3000.00, 6000.00, 6, 126),
(218, 4, 3000.00, 12000.00, 1, 127),
(219, 2, 3000.00, 6000.00, 2, 127),
(220, 7, 3000.00, 21000.00, 3, 128),
(221, 1, 3000.00, 3000.00, 4, 128),
(222, 5, 3000.00, 15000.00, 5, 129),
(223, 2, 3000.00, 6000.00, 6, 129),
(224, 4, 3000.00, 12000.00, 1, 130),
(225, 2, 3000.00, 6000.00, 2, 130),
(226, 6, 3000.00, 18000.00, 3, 131),
(227, 1, 3000.00, 3000.00, 4, 131),
(228, 5, 3000.00, 15000.00, 5, 132),
(229, 2, 3000.00, 6000.00, 6, 132),
(230, 4, 3000.00, 12000.00, 1, 133),
(231, 2, 3000.00, 6000.00, 2, 133),
(232, 7, 3000.00, 21000.00, 3, 134),
(233, 1, 3000.00, 3000.00, 4, 134),
(234, 5, 3000.00, 15000.00, 5, 135),
(235, 2, 3000.00, 6000.00, 6, 135),
(236, 4, 3000.00, 12000.00, 1, 136),
(237, 2, 3000.00, 6000.00, 2, 136),
(238, 6, 3000.00, 18000.00, 3, 137),
(239, 1, 3000.00, 3000.00, 4, 137),
(240, 5, 3000.00, 15000.00, 5, 138),
(241, 2, 3000.00, 6000.00, 6, 138),
(242, 4, 3000.00, 12000.00, 1, 139),
(243, 2, 3000.00, 6000.00, 2, 139),
(244, 7, 3000.00, 21000.00, 3, 140),
(245, 1, 3000.00, 3000.00, 4, 140),
(246, 5, 3000.00, 15000.00, 5, 141),
(247, 2, 3000.00, 6000.00, 6, 141),
(248, 4, 3000.00, 12000.00, 1, 142),
(249, 2, 3000.00, 6000.00, 2, 142),
(250, 6, 3000.00, 18000.00, 3, 143),
(251, 1, 3000.00, 3000.00, 4, 143),
(252, 5, 3000.00, 15000.00, 5, 144),
(253, 2, 3000.00, 6000.00, 6, 144),
(254, 4, 3000.00, 12000.00, 1, 145),
(255, 2, 3000.00, 6000.00, 2, 145),
(256, 7, 3000.00, 21000.00, 3, 146),
(257, 1, 3000.00, 3000.00, 4, 146),
(258, 5, 3000.00, 15000.00, 5, 147),
(259, 2, 3000.00, 6000.00, 6, 147),
(260, 4, 3000.00, 12000.00, 1, 148),
(261, 2, 3000.00, 6000.00, 2, 148),
(262, 6, 3000.00, 18000.00, 3, 149),
(263, 1, 3000.00, 3000.00, 4, 149),
(264, 5, 3000.00, 15000.00, 5, 150),
(265, 2, 3000.00, 6000.00, 6, 150),
(266, 4, 3000.00, 12000.00, 1, 151),
(267, 2, 3000.00, 6000.00, 2, 151),
(268, 7, 3000.00, 21000.00, 3, 152),
(269, 1, 3000.00, 3000.00, 4, 152),
(270, 5, 3000.00, 15000.00, 5, 153),
(271, 2, 3000.00, 6000.00, 6, 153),
(272, 4, 3000.00, 12000.00, 1, 154),
(273, 2, 3000.00, 6000.00, 2, 154),
(274, 6, 3000.00, 18000.00, 3, 155),
(275, 1, 3000.00, 3000.00, 4, 155),
(276, 5, 3000.00, 15000.00, 5, 156),
(277, 2, 3000.00, 6000.00, 6, 156),
(278, 4, 3000.00, 12000.00, 1, 157),
(279, 2, 3000.00, 6000.00, 2, 157),
(280, 7, 3000.00, 21000.00, 3, 158),
(281, 1, 3000.00, 3000.00, 4, 158),
(282, 5, 3000.00, 15000.00, 5, 159),
(283, 2, 3000.00, 6000.00, 6, 159),
(284, 4, 3000.00, 12000.00, 1, 160),
(285, 2, 3000.00, 6000.00, 2, 160),
(286, 6, 3000.00, 18000.00, 3, 161),
(287, 1, 3000.00, 3000.00, 4, 161);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add pin', 7, 'add_pin'),
(26, 'Can change pin', 7, 'change_pin'),
(27, 'Can delete pin', 7, 'delete_pin'),
(28, 'Can view pin', 7, 'view_pin'),
(29, 'Can add profile', 8, 'add_profile'),
(30, 'Can change profile', 8, 'change_profile'),
(31, 'Can delete profile', 8, 'delete_profile'),
(32, 'Can view profile', 8, 'view_profile'),
(33, 'Can add pedido', 9, 'add_pedido'),
(34, 'Can change pedido', 9, 'change_pedido'),
(35, 'Can delete pedido', 9, 'delete_pedido'),
(36, 'Can view pedido', 9, 'view_pedido'),
(37, 'Can add Proveedor', 10, 'add_proveedor'),
(38, 'Can change Proveedor', 10, 'change_proveedor'),
(39, 'Can delete Proveedor', 10, 'delete_proveedor'),
(40, 'Can view Proveedor', 10, 'view_proveedor'),
(41, 'Can add pedido detalle', 11, 'add_pedidodetalle'),
(42, 'Can change pedido detalle', 11, 'change_pedidodetalle'),
(43, 'Can delete pedido detalle', 11, 'delete_pedidodetalle'),
(44, 'Can view pedido detalle', 11, 'view_pedidodetalle'),
(45, 'Can add venta', 12, 'add_venta'),
(46, 'Can change venta', 12, 'change_venta'),
(47, 'Can delete venta', 12, 'delete_venta'),
(48, 'Can view venta', 12, 'view_venta'),
(49, 'Can add Estadística de Venta', 13, 'add_estadisticaventa'),
(50, 'Can change Estadística de Venta', 13, 'change_estadisticaventa'),
(51, 'Can delete Estadística de Venta', 13, 'delete_estadisticaventa'),
(52, 'Can view Estadística de Venta', 13, 'view_estadisticaventa'),
(53, 'Can add producto', 14, 'add_producto'),
(54, 'Can change producto', 14, 'change_producto'),
(55, 'Can delete producto', 14, 'delete_producto'),
(56, 'Can view producto', 14, 'view_producto'),
(57, 'Can add egreso', 15, 'add_egreso'),
(58, 'Can change egreso', 15, 'change_egreso'),
(59, 'Can delete egreso', 15, 'delete_egreso'),
(60, 'Can view egreso', 15, 'view_egreso'),
(61, 'Can add ingreso', 16, 'add_ingreso'),
(62, 'Can change ingreso', 16, 'change_ingreso'),
(63, 'Can delete ingreso', 16, 'delete_ingreso'),
(64, 'Can view ingreso', 16, 'view_ingreso'),
(65, 'Can add venta', 17, 'add_venta'),
(66, 'Can change venta', 17, 'change_venta'),
(67, 'Can delete venta', 17, 'delete_venta'),
(68, 'Can view venta', 17, 'view_venta'),
(69, 'Can add venta detalle', 18, 'add_ventadetalle'),
(70, 'Can change venta detalle', 18, 'change_ventadetalle'),
(71, 'Can delete venta detalle', 18, 'delete_ventadetalle'),
(72, 'Can view venta detalle', 18, 'view_ventadetalle'),
(73, 'Can add cliente', 19, 'add_cliente'),
(74, 'Can change cliente', 19, 'change_cliente'),
(75, 'Can delete cliente', 19, 'delete_cliente'),
(76, 'Can view cliente', 19, 'view_cliente'),
(77, 'Can add evento', 20, 'add_evento'),
(78, 'Can change evento', 20, 'change_evento'),
(79, 'Can delete evento', 20, 'delete_evento'),
(80, 'Can view evento', 20, 'view_evento'),
(81, 'Can add Predicción de Negocio', 21, 'add_prediccionnegocio'),
(82, 'Can change Predicción de Negocio', 21, 'change_prediccionnegocio'),
(83, 'Can delete Predicción de Negocio', 21, 'delete_prediccionnegocio'),
(84, 'Can view Predicción de Negocio', 21, 'view_prediccionnegocio'),
(85, 'Can add historial prediccion', 22, 'add_historialprediccion'),
(86, 'Can change historial prediccion', 22, 'change_historialprediccion'),
(87, 'Can delete historial prediccion', 22, 'delete_historialprediccion'),
(88, 'Can view historial prediccion', 22, 'view_historialprediccion'),
(89, 'Can add SES Stat', 23, 'add_sesstat'),
(90, 'Can change SES Stat', 23, 'change_sesstat'),
(91, 'Can delete SES Stat', 23, 'delete_sesstat'),
(92, 'Can view SES Stat', 23, 'view_sesstat'),
(93, 'Can add blacklisted email', 24, 'add_blacklistedemail'),
(94, 'Can change blacklisted email', 24, 'change_blacklistedemail'),
(95, 'Can delete blacklisted email', 24, 'delete_blacklistedemail'),
(96, 'Can view blacklisted email', 24, 'view_blacklistedemail');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Volcado de datos para la tabla `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$870000$gYxTfwDY341mrTetw6wEwI$idNNWYwbsNKuF2Sfr1YKVyz2FwcgouQGD3eqVcCTsXs=', '2025-04-27 18:43:03.211260', 1, 'Admin', '', '', 'santiagoproyectosuser5@gmail.com', 1, 1, '2025-04-22 13:02:36.071461'),
(2, 'pbkdf2_sha256$870000$cRtodWLCKjZrCIQfBjGUof$Xw5T1x/Cb3NjZqmfFLEed72tT+/4uV6QWrZwy5ubTh8=', '2025-04-27 18:39:19.279319', 0, 'Juan', '', '', 'esteban202@gmail.com', 0, 1, '2025-04-27 18:12:31.908183');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(19, 'app_eventos', 'cliente'),
(20, 'app_eventos', 'evento'),
(15, 'app_finanzas', 'egreso'),
(16, 'app_finanzas', 'ingreso'),
(14, 'app_inventario', 'producto'),
(9, 'app_pedidos', 'pedido'),
(11, 'app_pedidos', 'pedidodetalle'),
(10, 'app_pedidos', 'proveedor'),
(22, 'app_predicciones', 'historialprediccion'),
(21, 'app_predicciones', 'prediccionnegocio'),
(13, 'app_reportes', 'estadisticaventa'),
(12, 'app_reportes', 'venta'),
(7, 'app_usuarios', 'pin'),
(8, 'app_usuarios', 'profile'),
(17, 'app_ventas', 'venta'),
(18, 'app_ventas', 'ventadetalle'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(24, 'django_ses', 'blacklistedemail'),
(23, 'django_ses', 'sesstat'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-04-29 18:40:38.250742'),
(2, 'auth', '0001_initial', '2025-04-29 18:40:38.511795'),
(3, 'admin', '0001_initial', '2025-04-29 18:40:38.566719'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-04-29 18:40:38.576024'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-04-29 18:40:38.582697'),
(6, 'app_eventos', '0001_initial', '2025-04-29 18:40:38.627106'),
(7, 'app_usuarios', '0001_initial', '2025-04-29 18:40:38.709971'),
(8, 'app_inventario', '0001_initial', '2025-04-29 18:40:38.717048'),
(9, 'app_ventas', '0001_initial', '2025-04-29 18:40:38.882932'),
(10, 'app_pedidos', '0001_initial', '2025-04-29 18:40:38.994227'),
(11, 'app_finanzas', '0001_initial', '2025-04-29 18:40:39.096286'),
(12, 'app_finanzas', '0002_alter_ingreso_unique_together_ingreso_tipo_and_more', '2025-04-29 18:40:39.349089'),
(13, 'app_finanzas', '0003_alter_ingreso_options_ingreso_subtotal', '2025-04-29 18:40:39.381641'),
(14, 'app_finanzas', '0004_remove_ingreso_subtotal', '2025-04-29 18:40:39.403690'),
(15, 'app_finanzas', '0005_auto_20250331_2038', '2025-04-29 18:40:39.405856'),
(16, 'app_pedidos', '0002_alter_proveedor_options_proveedor_fecha_registro_and_more', '2025-04-29 18:40:39.492609'),
(17, 'app_pedidos', '0003_alter_pedidodetalle_costo_unitario_and_more', '2025-04-29 18:40:39.514992'),
(18, 'app_pedidos', '0004_pedido_observaciones', '2025-04-29 18:40:39.533749'),
(19, 'app_predicciones', '0001_initial', '2025-04-29 18:40:39.716855'),
(20, 'app_predicciones', '0002_alter_prediccionnegocio_fecha_accion_recomendada', '2025-04-29 18:40:39.727145'),
(21, 'app_predicciones', '0003_prediccionestacional', '2025-04-29 18:40:39.780699'),
(22, 'app_predicciones', '0004_alter_prediccionestacional_unique_together_and_more', '2025-04-29 18:40:40.127300'),
(23, 'app_reportes', '0001_initial', '2025-04-29 18:40:40.184443'),
(24, 'app_reportes', '0002_estadisticaventa', '2025-04-29 18:40:40.244933'),
(25, 'app_usuarios', '0002_profile_unique_user_profile', '2025-04-29 18:40:40.270061'),
(26, 'app_usuarios', '0003_delete_usuario_alter_profile_user', '2025-04-29 18:40:40.294432'),
(27, 'app_ventas', '0002_alter_venta_creado_por', '2025-04-29 18:40:40.444377'),
(28, 'contenttypes', '0002_remove_content_type_name', '2025-04-29 18:40:40.506685'),
(29, 'auth', '0002_alter_permission_name_max_length', '2025-04-29 18:40:40.544393'),
(30, 'auth', '0003_alter_user_email_max_length', '2025-04-29 18:40:40.564922'),
(31, 'auth', '0004_alter_user_username_opts', '2025-04-29 18:40:40.568601'),
(32, 'auth', '0005_alter_user_last_login_null', '2025-04-29 18:40:40.603751'),
(33, 'auth', '0006_require_contenttypes_0002', '2025-04-29 18:40:40.603751'),
(34, 'auth', '0007_alter_validators_add_error_messages', '2025-04-29 18:40:40.616666'),
(35, 'auth', '0008_alter_user_username_max_length', '2025-04-29 18:40:40.634690'),
(36, 'auth', '0009_alter_user_last_name_max_length', '2025-04-29 18:40:40.659920'),
(37, 'auth', '0010_alter_group_name_max_length', '2025-04-29 18:40:40.688007'),
(38, 'auth', '0011_update_proxy_permissions', '2025-04-29 18:40:40.710028'),
(39, 'auth', '0012_alter_user_first_name_max_length', '2025-04-29 18:40:40.735971'),
(40, 'django_ses', '0001_initial', '2025-04-29 18:40:40.747404'),
(41, 'django_ses', '0002_blacklistedemail', '2025-04-29 18:40:40.753842'),
(42, 'sessions', '0001_initial', '2025-04-29 18:40:40.781560');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('h0qss7uurdplhsyw1psqsp8i9r6qwgws', '.eJxVTUsOwiAQvQvrhgz9kNKle09gDBmGwVZNMYW6Md5darrQ3fu_l7C45tGuiRc7eTEIJapfzSHdeN4Mf8X5EiXFOS-Tk1tE7m6Sx-j5ftizfwMjprG0UfXoWtIGdaObUAdgE8C4vlfQaqrbwB015BwAKAZPvjBmMEAKa-zK6GOJfqUck33ynFEMp3MlvtDmmPFeXkC8P5zZRew:1u970k:18r3t_Ko_WGdd9qj_NIc6Nle-SsxJfe-Qvm-u1t3MoQ', '2025-05-11 18:45:54.550400');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_ses_blacklistedemail`
--

CREATE TABLE `django_ses_blacklistedemail` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_ses_sesstat`
--

CREATE TABLE `django_ses_sesstat` (
  `id` int(11) NOT NULL,
  `date` date NOT NULL,
  `delivery_attempts` int(10) UNSIGNED NOT NULL CHECK (`delivery_attempts` >= 0),
  `bounces` int(10) UNSIGNED NOT NULL CHECK (`bounces` >= 0),
  `complaints` int(10) UNSIGNED NOT NULL CHECK (`complaints` >= 0),
  `rejects` int(10) UNSIGNED NOT NULL CHECK (`rejects` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `app_eventos_cliente`
--
ALTER TABLE `app_eventos_cliente`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indices de la tabla `app_eventos_evento`
--
ALTER TABLE `app_eventos_evento`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_eventos_evento_cliente_id_a40b78f5_fk_app_eventos_cliente_id` (`cliente_id`);

--
-- Indices de la tabla `app_finanzas_egreso`
--
ALTER TABLE `app_finanzas_egreso`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `pedido_id` (`pedido_id`);

--
-- Indices de la tabla `app_finanzas_ingreso`
--
ALTER TABLE `app_finanzas_ingreso`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `venta_id` (`venta_id`);

--
-- Indices de la tabla `app_inventario_producto`
--
ALTER TABLE `app_inventario_producto`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `app_pedidos_pedido`
--
ALTER TABLE `app_pedidos_pedido`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_pedidos_pedido_proveedor_id_45ff1350_fk_app_pedid` (`proveedor_id`);

--
-- Indices de la tabla `app_pedidos_pedidodetalle`
--
ALTER TABLE `app_pedidos_pedidodetalle`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_pedidos_pedidode_pedido_id_c14d4dfe_fk_app_pedid` (`pedido_id`),
  ADD KEY `app_pedidos_pedidode_producto_id_9f9c0532_fk_app_inven` (`producto_id`);

--
-- Indices de la tabla `app_pedidos_proveedor`
--
ALTER TABLE `app_pedidos_proveedor`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `app_pedidos_proveedor_email_cdd89d45_uniq` (`email`);

--
-- Indices de la tabla `app_predicciones_historialprediccion`
--
ALTER TABLE `app_predicciones_historialprediccion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_predicciones_his_prediccion_id_8aa57468_fk_app_predi` (`prediccion_id`);

--
-- Indices de la tabla `app_predicciones_prediccionnegocio`
--
ALTER TABLE `app_predicciones_prediccionnegocio`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_predicciones_pre_producto_id_aaf071de_fk_app_inven` (`producto_id`);

--
-- Indices de la tabla `app_reportes_estadisticaventa`
--
ALTER TABLE `app_reportes_estadisticaventa`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `app_reportes_estadisticaventa_producto_id_fecha_bba311ac_uniq` (`producto_id`,`fecha`);

--
-- Indices de la tabla `app_reportes_venta`
--
ALTER TABLE `app_reportes_venta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_reportes_venta_producto_id_1914e625_fk_app_inven` (`producto_id`);

--
-- Indices de la tabla `app_usuarios_pin`
--
ALTER TABLE `app_usuarios_pin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indices de la tabla `app_usuarios_profile`
--
ALTER TABLE `app_usuarios_profile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD UNIQUE KEY `unique_user_profile` (`user_id`);

--
-- Indices de la tabla `app_ventas_venta`
--
ALTER TABLE `app_ventas_venta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_ventas_venta_empleado_id_49a5787d_fk_app_usuarios_profile_id` (`empleado_id`),
  ADD KEY `app_ventas_venta_modificado_por_id_56782b65_fk_app_usuar` (`modificado_por_id`),
  ADD KEY `app_ventas_venta_creado_por_id_28285417_fk_app_usuar` (`creado_por_id`);

--
-- Indices de la tabla `app_ventas_ventadetalle`
--
ALTER TABLE `app_ventas_ventadetalle`
  ADD PRIMARY KEY (`id`),
  ADD KEY `app_ventas_ventadeta_producto_id_672e663c_fk_app_inven` (`producto_id`),
  ADD KEY `app_ventas_ventadetalle_venta_id_5ec1d1f6_fk_app_ventas_venta_id` (`venta_id`);

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `django_ses_blacklistedemail`
--
ALTER TABLE `django_ses_blacklistedemail`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indices de la tabla `django_ses_sesstat`
--
ALTER TABLE `django_ses_sesstat`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `date` (`date`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `app_eventos_cliente`
--
ALTER TABLE `app_eventos_cliente`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `app_eventos_evento`
--
ALTER TABLE `app_eventos_evento`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `app_finanzas_egreso`
--
ALTER TABLE `app_finanzas_egreso`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `app_finanzas_ingreso`
--
ALTER TABLE `app_finanzas_ingreso`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=151;

--
-- AUTO_INCREMENT de la tabla `app_inventario_producto`
--
ALTER TABLE `app_inventario_producto`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `app_pedidos_pedido`
--
ALTER TABLE `app_pedidos_pedido`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `app_pedidos_pedidodetalle`
--
ALTER TABLE `app_pedidos_pedidodetalle`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `app_pedidos_proveedor`
--
ALTER TABLE `app_pedidos_proveedor`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `app_predicciones_historialprediccion`
--
ALTER TABLE `app_predicciones_historialprediccion`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `app_predicciones_prediccionnegocio`
--
ALTER TABLE `app_predicciones_prediccionnegocio`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `app_reportes_estadisticaventa`
--
ALTER TABLE `app_reportes_estadisticaventa`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `app_reportes_venta`
--
ALTER TABLE `app_reportes_venta`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `app_usuarios_pin`
--
ALTER TABLE `app_usuarios_pin`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `app_usuarios_profile`
--
ALTER TABLE `app_usuarios_profile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `app_ventas_venta`
--
ALTER TABLE `app_ventas_venta`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=151;

--
-- AUTO_INCREMENT de la tabla `app_ventas_ventadetalle`
--
ALTER TABLE `app_ventas_ventadetalle`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=288;

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=97;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT de la tabla `django_ses_blacklistedemail`
--
ALTER TABLE `django_ses_blacklistedemail`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_ses_sesstat`
--
ALTER TABLE `django_ses_sesstat`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `app_eventos_evento`
--
ALTER TABLE `app_eventos_evento`
  ADD CONSTRAINT `app_eventos_evento_cliente_id_a40b78f5_fk_app_eventos_cliente_id` FOREIGN KEY (`cliente_id`) REFERENCES `app_eventos_cliente` (`id`);

--
-- Filtros para la tabla `app_finanzas_egreso`
--
ALTER TABLE `app_finanzas_egreso`
  ADD CONSTRAINT `app_finanzas_egreso_pedido_id_1c723a5e_fk_app_pedidos_pedido_id` FOREIGN KEY (`pedido_id`) REFERENCES `app_pedidos_pedido` (`id`);

--
-- Filtros para la tabla `app_finanzas_ingreso`
--
ALTER TABLE `app_finanzas_ingreso`
  ADD CONSTRAINT `app_finanzas_ingreso_venta_id_25dbd1fe_fk_app_ventas_venta_id` FOREIGN KEY (`venta_id`) REFERENCES `app_ventas_venta` (`id`);

--
-- Filtros para la tabla `app_pedidos_pedido`
--
ALTER TABLE `app_pedidos_pedido`
  ADD CONSTRAINT `app_pedidos_pedido_proveedor_id_45ff1350_fk_app_pedid` FOREIGN KEY (`proveedor_id`) REFERENCES `app_pedidos_proveedor` (`id`);

--
-- Filtros para la tabla `app_pedidos_pedidodetalle`
--
ALTER TABLE `app_pedidos_pedidodetalle`
  ADD CONSTRAINT `app_pedidos_pedidode_pedido_id_c14d4dfe_fk_app_pedid` FOREIGN KEY (`pedido_id`) REFERENCES `app_pedidos_pedido` (`id`),
  ADD CONSTRAINT `app_pedidos_pedidode_producto_id_9f9c0532_fk_app_inven` FOREIGN KEY (`producto_id`) REFERENCES `app_inventario_producto` (`id`);

--
-- Filtros para la tabla `app_predicciones_historialprediccion`
--
ALTER TABLE `app_predicciones_historialprediccion`
  ADD CONSTRAINT `app_predicciones_his_prediccion_id_8aa57468_fk_app_predi` FOREIGN KEY (`prediccion_id`) REFERENCES `app_predicciones_prediccionnegocio` (`id`);

--
-- Filtros para la tabla `app_predicciones_prediccionnegocio`
--
ALTER TABLE `app_predicciones_prediccionnegocio`
  ADD CONSTRAINT `app_predicciones_pre_producto_id_aaf071de_fk_app_inven` FOREIGN KEY (`producto_id`) REFERENCES `app_inventario_producto` (`id`);

--
-- Filtros para la tabla `app_reportes_estadisticaventa`
--
ALTER TABLE `app_reportes_estadisticaventa`
  ADD CONSTRAINT `app_reportes_estadis_producto_id_c60fbd28_fk_app_inven` FOREIGN KEY (`producto_id`) REFERENCES `app_inventario_producto` (`id`);

--
-- Filtros para la tabla `app_reportes_venta`
--
ALTER TABLE `app_reportes_venta`
  ADD CONSTRAINT `app_reportes_venta_producto_id_1914e625_fk_app_inven` FOREIGN KEY (`producto_id`) REFERENCES `app_inventario_producto` (`id`);

--
-- Filtros para la tabla `app_usuarios_pin`
--
ALTER TABLE `app_usuarios_pin`
  ADD CONSTRAINT `app_usuarios_pin_user_id_8d2a2275_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `app_usuarios_profile`
--
ALTER TABLE `app_usuarios_profile`
  ADD CONSTRAINT `app_usuarios_profile_user_id_65bf9a9a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `app_ventas_venta`
--
ALTER TABLE `app_ventas_venta`
  ADD CONSTRAINT `app_ventas_venta_creado_por_id_28285417_fk_app_usuar` FOREIGN KEY (`creado_por_id`) REFERENCES `app_usuarios_profile` (`id`),
  ADD CONSTRAINT `app_ventas_venta_empleado_id_49a5787d_fk_app_usuarios_profile_id` FOREIGN KEY (`empleado_id`) REFERENCES `app_usuarios_profile` (`id`),
  ADD CONSTRAINT `app_ventas_venta_modificado_por_id_56782b65_fk_app_usuar` FOREIGN KEY (`modificado_por_id`) REFERENCES `app_usuarios_profile` (`id`);

--
-- Filtros para la tabla `app_ventas_ventadetalle`
--
ALTER TABLE `app_ventas_ventadetalle`
  ADD CONSTRAINT `app_ventas_ventadeta_producto_id_672e663c_fk_app_inven` FOREIGN KEY (`producto_id`) REFERENCES `app_inventario_producto` (`id`),
  ADD CONSTRAINT `app_ventas_ventadetalle_venta_id_5ec1d1f6_fk_app_ventas_venta_id` FOREIGN KEY (`venta_id`) REFERENCES `app_ventas_venta` (`id`);

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

