-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 30, 2025 at 08:42 PM
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
-- Table structure for table `jobs`
--

CREATE TABLE `jobs` (
  `id` int(11) NOT NULL,
  `cluster_id` int(11) DEFAULT NULL,
  `job_title` varchar(100) DEFAULT NULL,
  `company` varchar(100) DEFAULT NULL,
  `job_desc` text DEFAULT NULL,
  `requirements` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `jobs`
--

INSERT INTO `jobs` (`id`, `cluster_id`, `job_title`, `company`, `job_desc`, `requirements`) VALUES
(1, 0, 'Data Scientist', 'Insight Analytics', 'Apply statistical methods and machine learning algorithms to large datasets. Provide predictive insights and data-driven solutions.', 'Strong in Python/R, statistics, SQL, problem-solving, and analytical mindset.'),
(2, 0, 'Software Engineer', 'Tech Innovations Inc.', 'Design and maintain scalable applications. Collaborate with cross-functional teams to define and ship new features.', 'Knowledge of software development, teamwork, problem-solving, and critical thinking.'),
(3, 1, 'Marketing Specialist', 'Global Brands Co.', 'Plan and execute creative marketing campaigns. Analyze consumer behavior and manage digital platforms.', 'Excellent communication, creativity, social media skills, and adaptability.'),
(4, 1, 'Human Resources Officer', 'People First Sdn Bhd', 'Manage recruitment, onboarding, and employee engagement. Build strong workplace culture.', 'Empathy, people management, conflict resolution, and organizational skills.'),
(5, 2, 'Research Assistant', 'University Research Lab', 'Assist in academic and industrial research projects. Collect and analyze data to support studies.', 'Detail-oriented, statistical knowledge, academic writing, and patience.'),
(6, 2, 'Financial Analyst', 'Wealth Management Group', 'Prepare reports, analyze financial data, and forecast business trends for decision-making.', 'Strong in Excel, accounting principles, attention to detail, and critical thinking.'),
(7, 3, 'Nurse / Healthcare Assistant', 'CarePlus Clinic', 'Provide direct care to patients, assist doctors, and ensure patient comfort and safety.', 'Compassion, patience, teamwork, and basic medical knowledge.'),
(8, 3, 'Teacher / Lecturer', 'SmartEdu College', 'Teach and mentor students, develop lesson plans, and provide academic guidance.', 'Strong communication, empathy, subject expertise, and mentoring ability.');

-- --------------------------------------------------------

--
-- Table structure for table `personality_results`
--

CREATE TABLE `personality_results` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `taken_at` datetime DEFAULT current_timestamp(),
  `q1` tinyint(4) DEFAULT NULL,
  `q2` tinyint(4) DEFAULT NULL,
  `q3` tinyint(4) DEFAULT NULL,
  `q4` tinyint(4) DEFAULT NULL,
  `q5` tinyint(4) DEFAULT NULL,
  `q6` tinyint(4) DEFAULT NULL,
  `q7` tinyint(4) DEFAULT NULL,
  `q8` tinyint(4) DEFAULT NULL,
  `q9` tinyint(4) DEFAULT NULL,
  `q10` tinyint(4) DEFAULT NULL,
  `q11` tinyint(4) DEFAULT NULL,
  `q12` tinyint(4) DEFAULT NULL,
  `q13` tinyint(4) DEFAULT NULL,
  `q14` tinyint(4) DEFAULT NULL,
  `q15` tinyint(4) DEFAULT NULL,
  `q16` tinyint(4) DEFAULT NULL,
  `q17` tinyint(4) DEFAULT NULL,
  `q18` tinyint(4) DEFAULT NULL,
  `q19` tinyint(4) DEFAULT NULL,
  `q20` tinyint(4) DEFAULT NULL,
  `q21` tinyint(4) DEFAULT NULL,
  `q22` tinyint(4) DEFAULT NULL,
  `q23` tinyint(4) DEFAULT NULL,
  `q24` tinyint(4) DEFAULT NULL,
  `q25` tinyint(4) DEFAULT NULL,
  `q26` tinyint(4) DEFAULT NULL,
  `q27` tinyint(4) DEFAULT NULL,
  `q28` tinyint(4) DEFAULT NULL,
  `q29` tinyint(4) DEFAULT NULL,
  `q30` tinyint(4) DEFAULT NULL,
  `openness_raw` tinyint(4) DEFAULT NULL,
  `conscientiousness_raw` tinyint(4) DEFAULT NULL,
  `extraversion_raw` tinyint(4) DEFAULT NULL,
  `agreeableness_raw` tinyint(4) DEFAULT NULL,
  `neuroticism_raw` tinyint(4) DEFAULT NULL,
  `cluster_id` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `personality_results`
--

INSERT INTO `personality_results` (`id`, `user_id`, `taken_at`, `q1`, `q2`, `q3`, `q4`, `q5`, `q6`, `q7`, `q8`, `q9`, `q10`, `q11`, `q12`, `q13`, `q14`, `q15`, `q16`, `q17`, `q18`, `q19`, `q20`, `q21`, `q22`, `q23`, `q24`, `q25`, `q26`, `q27`, `q28`, `q29`, `q30`, `openness_raw`, `conscientiousness_raw`, `extraversion_raw`, `agreeableness_raw`, `neuroticism_raw`, `cluster_id`) VALUES
(1, 1, '2025-09-30 01:05:37', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10, 10, 10, 10, 14, 2),
(2, 1, '2025-10-01 00:18:20', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10, 10, 10, 10, 14, 2),
(3, 1, '2025-10-01 00:45:47', 4, 1, 4, 4, 5, 1, 4, 1, 4, 2, 5, 1, 4, 2, 5, 1, 5, 1, 3, 3, 2, 3, 1, 3, 3, 4, 3, 1, 5, 2, 15, 13, 14, 19, 24, 3),
(4, 1, '2025-10-01 01:42:39', 4, 5, 3, 2, 1, 4, 3, 4, 3, 5, 4, 1, 2, 1, 2, 1, 4, 2, 3, 5, 1, 2, 4, 2, 4, 2, 3, 1, 2, 3, 23, 18, 10, 15, 19, 3),
(5, 1, '2025-10-01 01:43:22', 2, 2, 4, 3, 3, 4, 4, 5, 2, 1, 4, 3, 2, 3, 1, 3, 2, 4, 5, 2, 5, 5, 1, 2, 5, 2, 5, 3, 2, 4, 18, 17, 17, 24, 19, 3),
(6, 1, '2025-10-01 01:46:38', 4, 2, 3, 3, 2, 2, 3, 2, 4, 5, 1, 3, 1, 3, 3, 4, 4, 1, 2, 3, 3, 5, 1, 3, 4, 3, 3, 4, 3, 2, 18, 22, 14, 21, 19, 3),
(7, 1, '2025-10-01 01:49:37', 2, 2, 2, 3, 3, 3, 5, 5, 3, 3, 5, 5, 1, 3, 2, 4, 5, 3, 4, 3, 2, 1, 3, 3, 1, 1, 2, 2, 4, 1, 15, 22, 14, 16, 17, 3),
(8, 1, '2025-10-01 02:07:35', 2, 4, 3, 4, 3, 5, 4, 4, 2, 3, 1, 2, 5, 5, 3, 1, 3, 2, 5, 2, 3, 2, 4, 2, 1, 2, 1, 5, 4, 3, 21, 20, 19, 16, 12, 3),
(9, 1, '2025-10-01 02:13:48', 3, 3, 4, 2, 3, 4, 1, 5, 4, 4, 2, 1, 4, 4, 2, 4, 4, 3, 3, 2, 3, 1, 4, 3, 5, 2, 3, 1, 3, 2, 19, 19, 19, 14, 22, 3);

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
(1, 'fitech', 'fitechcorporationif@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `jobs`
--
ALTER TABLE `jobs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `personality_results`
--
ALTER TABLE `personality_results`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

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
-- AUTO_INCREMENT for table `jobs`
--
ALTER TABLE `jobs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `personality_results`
--
ALTER TABLE `personality_results`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `personality_results`
--
ALTER TABLE `personality_results`
  ADD CONSTRAINT `personality_results_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
