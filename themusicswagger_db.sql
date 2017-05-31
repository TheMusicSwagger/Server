-- phpMyAdmin SQL Dump
-- version 4.6.6deb4
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: May 31, 2017 at 09:15 PM
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
(14, 2, 0, 'DIST', 'Distortion');

-- --------------------------------------------------------

--
-- Table structure for table `boxes`
--

CREATE TABLE `boxes` (
  `ID` int(11) NOT NULL,
  `TYPE` varchar(10) NOT NULL,
  `BOX_ID` int(11) NOT NULL,
  `SPEC_PARAM` varchar(512) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `connections`
--

CREATE TABLE `connections` (
  `ID` int(11) NOT NULL,
  `GUID` varchar(32) NOT NULL,
  `CUID` int(11) NOT NULL,
  `inited` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `links`
--

CREATE TABLE `links` (
  `ID` int(11) NOT NULL,
  `FROM_B` int(11) NOT NULL,
  `TO_B` int(11) NOT NULL,
  `WHERE_L` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `specifications`
--

CREATE TABLE `specifications` (
  `ID` int(11) NOT NULL,
  `numchan` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `CUID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `update_number`
--

CREATE TABLE `update_number` (
  `ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `available_tools`
--
ALTER TABLE `available_tools`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `boxes`
--
ALTER TABLE `boxes`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `connections`
--
ALTER TABLE `connections`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `links`
--
ALTER TABLE `links`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `specifications`
--
ALTER TABLE `specifications`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `update_number`
--
ALTER TABLE `update_number`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `available_tools`
--
ALTER TABLE `available_tools`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
--
-- AUTO_INCREMENT for table `boxes`
--
ALTER TABLE `boxes`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=428;
--
-- AUTO_INCREMENT for table `connections`
--
ALTER TABLE `connections`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=589;
--
-- AUTO_INCREMENT for table `links`
--
ALTER TABLE `links`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=356;
--
-- AUTO_INCREMENT for table `specifications`
--
ALTER TABLE `specifications`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;
--
-- AUTO_INCREMENT for table `update_number`
--
ALTER TABLE `update_number`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
