-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : mar. 24 juin 2025 à 05:48
-- Version du serveur : 8.3.0
-- Version de PHP : 8.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `jfn_consultations`
--

-- --------------------------------------------------------

--
-- Structure de la table `consultations`
--

DROP TABLE IF EXISTS `consultations`;
CREATE TABLE IF NOT EXISTS `consultations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `patient` varchar(255) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `symptomes` text,
  `traitement` text,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `consultations`
--

INSERT INTO `consultations` (`id`, `patient`, `date`, `symptomes`, `traitement`) VALUES
(1, 'dc', '0000-00-00', 'sdf', 'sdfsd'),
(2, 'ssdf', '0000-00-00', 'sdf', 'sdfsd'),
(3, 'sdfsd', '0000-00-00', 'sdfsdf	sdf', 'sdfsd'),
(4, 'qsdqsd', '0000-00-00', 'qsdqsd', 'qssdd qsdqs qsdqsd qsdqsd qsdqsd qsdqsd qsdq dqdqsdqsd'),
(5, 'dfsd', '0000-00-00', 'sdfs', 'sdsdf');

-- --------------------------------------------------------

--
-- Structure de la table `password_resets`
--

DROP TABLE IF EXISTS `password_resets`;
CREATE TABLE IF NOT EXISTS `password_resets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `code` varchar(6) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `used` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `password_resets`
--

INSERT INTO `password_resets` (`id`, `email`, `code`, `created_at`, `used`) VALUES
(1, 'fresnelktf@gmail.com', '271564', '2025-06-16 15:25:29', 0),
(2, 'fresnelktf@gmail.com', '469031', '2025-06-16 15:30:33', 1),
(3, 'fresnelktf@gmail.com', '638911', '2025-06-20 15:12:44', 1);

-- --------------------------------------------------------

--
-- Structure de la table `pending_requests`
--

DROP TABLE IF EXISTS `pending_requests`;
CREATE TABLE IF NOT EXISTS `pending_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(50) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `pending_users`
--

DROP TABLE IF EXISTS `pending_users`;
CREATE TABLE IF NOT EXISTS `pending_users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` text,
  `role` varchar(50) DEFAULT NULL,
  `validated` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `pending_users`
--

INSERT INTO `pending_users` (`id`, `full_name`, `email`, `password`, `role`, `validated`) VALUES
(1, 'blabla', 'balbal@gmail.com', 'fe6b57e537d2ff888ead8bc8484965b34838088143d9d7f12c82c964104be641', 'chef_infirmier', 0),
(2, 'sdfsdf', 'sdfsdfsd', 'd7ef0a04f3c8055644677299a9414a75adcb15916eb48417416c9317ace2ff4f', 'chef_infirmier', 0),
(3, 'qsqsd', 'sdsdfsdf@gmail.com', '05dd08f781a5dd535ff404b732cd3ff992ef57aee6669d8ea52ffaed49ddb571', 'chef_infirmier', 0),
(4, 'sdfsdf', 'ssdsdfsd', '18ee24150dcb1d96752a4d6dd0f20dfd8ba8c38527e40aa8509b7adecf78f9c6', 'admin', 0),
(5, 'truc', 'fresnelktf1@gmail.com', '51095e40cdabd090efa12ce9707c515a504f3a5a81f64e72be866cc1ca5810fa', 'chef_infirmier', 0),
(6, 'chose', 'chose@gmail.com', '1c512eec1641b3f7a988fd9ed7e12899ed0321bc7195d27012f80b454368b331', 'chef_infirmier', 0),
(7, 'sdfsf', 'sdsf', '7d4f6e945f3e0b48cba456ee0734cce9ab520405211bc9c4a903203b77ba7eb8', 'chef_infirmier', 0),
(8, 'sdf', 'sdfzf', '4bac27393bdd9777ce02453256c5577cd02275510b2227f473d03f533924f877', 'chef_infirmier', 0);

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` text NOT NULL,
  `role` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `users`
--

INSERT INTO `users` (`id`, `full_name`, `email`, `password`, `role`) VALUES
(10, 'kenne1 fresnel1', 'fresnelktf1@gmail.com', 'd330115ef34d11698d2732720db8b9913d3c73653a318fc5dc73ad2a8de1f4d3', 'chef_infirmier'),
(3, 'kenne fresnel', 'fresnelktf@gmail.com', '1c512eec1641b3f7a988fd9ed7e12899ed0321bc7195d27012f80b454368b331', 'admin'),
(8, 'fresnel_truc1', 'jeuxvideofresnel@gmail.com', '1c512eec1641b3f7a988fd9ed7e12899ed0321bc7195d27012f80b454368b331', 'chef_infirmier');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
