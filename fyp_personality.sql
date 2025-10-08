-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 08, 2025 at 11:45 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fyp_personality`
--

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`) VALUES
(2, 'jo', 'Jo@Gmail.com', 'b729dbb11c9006e73c2bfceb2225ea9c0e755296fd842a649ce0e9e8d84e6840'),
(3, 'nic', 'nic@gmail.com', '89ff1b070c2143a0438907b27dcb9646386797f6f0007e0fdc4b7d3d6d925e46'),
(4, 'chloe', 'c@gmail.com', '12b93e76280bc8ed3ef6179010a730b7ad98e809992c844e2e94f4fa765d8136'),
(7, 'test1', 'test@gmail.com', 'b729dbb11c9006e73c2bfceb2225ea9c0e755296fd842a649ce0e9e8d84e6840'),
(8, 'test', 'test2@gmail.com', '02d2411d92e6cd9d072af982ca3b7c22f7b1045e14da71176d5c81ae134a86f6'),
(9, 'Test3', 'test3@gmail.com', '983487d9c4b7451b0e7d282114470d3a0ad50dc5e554971a4d1cda04acde670b'),
(10, 'Test4', 'test4@gmail.com', 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'),
(11, 'test5', 'Test5', '88d4266fd4e6338d13b845fcf289579d209c897823b9217da3e161936f031589');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
