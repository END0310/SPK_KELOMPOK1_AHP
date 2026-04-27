-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 27, 2026 at 10:05 AM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `spk_ahp`
--

-- --------------------------------------------------------

--
-- Table structure for table `analysis_history`
--

CREATE TABLE `analysis_history` (
  `id` int NOT NULL,
  `created_at` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `k` int NOT NULL,
  `a` int NOT NULL,
  `nama_kriteria` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `weights` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `ranking` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `CR` double NOT NULL,
  `total_score` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `analysis_history`
--

INSERT INTO `analysis_history` (`id`, `created_at`, `k`, `a`, `nama_kriteria`, `weights`, `ranking`, `CR`, `total_score`) VALUES
(5, '2026-04-27 16:22:24', 4, 3, '[\"Tingkat Kerusakan\", \"Dampak terhadap Akademik\", \"Frekuensi Penggunaan\", \"Biaya Perbaikan\"]', '[0.32064156773459096, 0.4253740445600911, 0.16399007968775411, 0.08999430801756383]', '[[\"Gedung Belajar Bersama H\", 0.533992], [\"Gedung Auditorium\", 0.260739], [\"Gedung Convention Hall\", 0.20527]]', 0.07921954431985512, 1);

-- --------------------------------------------------------

--
-- Table structure for table `prediksi`
--

CREATE TABLE `prediksi` (
  `id` int NOT NULL,
  `banyak_alternatif` int NOT NULL,
  `nama_alternatif` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `bobot_alternatif` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `hasil_keputusan` text COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `prediksi`
--

INSERT INTO `prediksi` (`id`, `banyak_alternatif`, `nama_alternatif`, `bobot_alternatif`, `hasil_keputusan`) VALUES
(1, 3, '[\"Gedung Belajar Bersama H\", \"Gedung Convention Hall\", \"Gedung Auditorium\"]', '[0.5339917266982452, 0.2052696522029844, 0.26073862109877033]', '[[\"Gedung Belajar Bersama H\", 0.533992], [\"Gedung Auditorium\", 0.260739], [\"Gedung Convention Hall\", 0.20527]]');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `analysis_history`
--
ALTER TABLE `analysis_history`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `prediksi`
--
ALTER TABLE `prediksi`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `analysis_history`
--
ALTER TABLE `analysis_history`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `prediksi`
--
ALTER TABLE `prediksi`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
