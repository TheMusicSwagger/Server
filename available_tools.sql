-- phpMyAdmin SQL Dump
-- version 4.6.6deb4
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 01, 2017 at 10:42 AM
-- Server version: 5.6.30-1
-- PHP Version: 7.0.19-1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `themusicswagger_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `available_tools`
--

CREATE TABLE `available_tools` (
  `ID` int(11) NOT NULL,
  `inputs` int(11) NOT NULL,
  `need_input` int(11) NOT NULL DEFAULT '0',
  `name` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `available_tools`
--

INSERT INTO `available_tools` (`ID`, `inputs`, `need_input`, `name`, `type`) VALUES
(1, 2, 0, 'Pitch', 'PITCH'),
(2, 3, 0, 'Add', 'ADD'),
(3, 0, 1, 'Value', 'VALUE'),
(4, 1, 0, 'Device', 'DEVICE'),
(5, 1, 0, 'Sine', 'SINE'),
(6, 4, 0, 'More', 'MORE'),
(7, 4, 0, 'Less', 'LESS'),
(9, 0, 0, 'Random', 'RAND'),
(10, 2, 0, 'Multiply', 'MULTI'),
(11, 2, 0, 'Sum', 'SUM'),
(12, 2, 0, 'Doppler', 'DOP'),
(13, 2, 0, 'Ampli', 'AMP'),
(14, 2, 0, 'DIST', 'Distortion'),
(15, 3, 0, 'Crop', 'CROP'),
(16, 5, 0, 'Resize', 'RESI'),
(17, 1, 0, 'Abs', 'ABS');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `available_tools`
--
ALTER TABLE `available_tools`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `available_tools`
--
ALTER TABLE `available_tools`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
