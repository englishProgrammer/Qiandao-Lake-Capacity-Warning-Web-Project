/*
Navicat MySQL Data Transfer

Source Server         : LOCAL
Source Server Version : 80017
Source Host           : localhost:3306
Source Database       : capacity

Target Server Type    : MYSQL
Target Server Version : 80017
File Encoding         : 65001

Date: 2019-11-27 10:03:21
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for wifiinfo
-- ----------------------------
DROP TABLE IF EXISTS `wifiinfo`;
CREATE TABLE `wifiinfo` (
  `deviceType` varchar(255) DEFAULT NULL,
  `tvId` int(11) NOT NULL,
  `sciencId` int(11) DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `state` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `adminId` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `adminName` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`tvId`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of wifiinfo
-- ----------------------------
INSERT INTO `wifiinfo` VALUES ('WIFI', '2', '1', 'CA00HS151116043', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '3', '1', 'CA00HS151116043', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '4', '1', 'CA00HS151116043', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '5', '1', 'CA00HS151116043', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '6', '1', 'CA00HS151116043', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '7', '1', 'CA00HS151116043', '1', '10000', '张森');
INSERT INTO `wifiinfo` VALUES ('WIFI', '8', '1', 'CA00HS151116043', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '9', '1', 'CA00HS151116043', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '10', '1', 'CA00HS151116043', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '11', '2', 'CA20HS140718064', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '12', '2', 'CA20HS140718064', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '13', '2', 'CA20HS140718064', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '14', '2', 'CA20HS140718064', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '15', '2', 'CA20HS140718064', '1', '10000', '张森');
INSERT INTO `wifiinfo` VALUES ('WIFI', '16', '2', 'CA20HS140718064', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '17', '2', 'CA20HS140718064', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '18', '2', 'CA20HS140718064', '1', '10000', '张森');
INSERT INTO `wifiinfo` VALUES ('WIFI', '19', '2', 'CA20HS140718064', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '20', '2', 'CA20HS140718064', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '21', '3', 'CA20HS150826001', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '22', '3', 'CA20HS150826001', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '23', '3', 'CA20HS150826001', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '24', '3', 'CA20HS150826001', '1', '10000', '张森');
INSERT INTO `wifiinfo` VALUES ('WIFI', '25', '3', 'CA20HS150826001', '1', '10000', '张森');
INSERT INTO `wifiinfo` VALUES ('WIFI', '26', '3', 'CA20HS150826001', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '27', '3', 'CA20HS150826001', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '28', '3', 'CA20HS150826001', '1', '10000', '张森');
INSERT INTO `wifiinfo` VALUES ('WIFI', '29', '3', 'CA20HS150826001', '1', '10000', '张森');
INSERT INTO `wifiinfo` VALUES ('WIFI', '30', '3', 'CA20HS150826001', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '31', '4', 'CA10HS140718003', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '32', '4', 'CA10HS140718003', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '33', '4', 'CA10HS140718003', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '34', '4', 'CA10HS140718003', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '35', '4', 'CA10HS140718003', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '36', '4', 'CA10HS140718003', '1', '10000', '张森');
INSERT INTO `wifiinfo` VALUES ('WIFI', '37', '4', 'CA10HS140718003', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '38', '4', 'CA10HS140718003', '1', '10000', '张森');
INSERT INTO `wifiinfo` VALUES ('WIFI', '39', '4', 'CA10HS140718003', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '40', '4', 'CA10HS140718003', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '41', '5', 'CA10HS140718005', '1', '10000', '张森');
INSERT INTO `wifiinfo` VALUES ('WIFI', '42', '5', 'CA10HS140718005', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '43', '5', 'CA10HS140718005', '1', '10000', '张森');
INSERT INTO `wifiinfo` VALUES ('WIFI', '44', '5', 'CA10HS140718005', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '45', '5', 'CA10HS140718005', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '46', '5', 'CA10HS140718005', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '47', '5', 'CA10HS140718005', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '48', '5', 'CA10HS140718005', '1', '10000', '张森');
INSERT INTO `wifiinfo` VALUES ('WIFI', '49', '5', 'CA10HS140718005', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '50', '5', 'CA10HS140718005', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '51', '6', 'CA10HS140718006', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '52', '6', 'CA10HS140718006', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '53', '6', 'CA10HS140718006', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '54', '6', 'CA10HS140718006', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '55', '6', 'CA10HS140718006', '1', '10000', '张森');
INSERT INTO `wifiinfo` VALUES ('WIFI', '56', '6', 'CA10HS140718006', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '57', '6', 'CA10HS140718006', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '58', '6', 'CA10HS140718006', '1', '10000', '张森');
INSERT INTO `wifiinfo` VALUES ('WIFI', '59', '6', 'CA10HS140718006', '1', '10000', '张森');
INSERT INTO `wifiinfo` VALUES ('WIFI', '60', '6', 'CA10HS140718006', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '61', '7', 'CA10HS150104026', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '62', '7', 'CA10HS150104026', '1', '10000', '张森');
INSERT INTO `wifiinfo` VALUES ('WIFI', '63', '7', 'CA10HS150104026', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '64', '7', 'CA10HS150104026', '1', '10000', '张森');
INSERT INTO `wifiinfo` VALUES ('WIFI', '65', '7', 'CA10HS150104026', '1', '10000', '张森');
INSERT INTO `wifiinfo` VALUES ('WIFI', '66', '7', 'CA10HS150104026', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '67', '7', 'CA10HS150104026', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '68', '7', 'CA10HS150104026', '1', '10000', '张森');
INSERT INTO `wifiinfo` VALUES ('WIFI', '69', '7', 'CA10HS150104026', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '70', '7', 'CA10HS150104026', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '71', '8', 'CA10HS150104021', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '72', '8', 'CA10HS150104021', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '73', '8', 'CA10HS150104021', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '74', '8', 'CA10HS150104021', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '75', '8', 'CA10HS150104021', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '76', '8', 'CA10HS150104021', '1', '10001', '王五');
INSERT INTO `wifiinfo` VALUES ('WIFI', '77', '8', 'CA10HS150104021', '1', '10000', '张森');
INSERT INTO `wifiinfo` VALUES ('WIFI', '78', '8', 'CA10HS150104021', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '79', '8', 'CA10HS150104021', '1', '10002', '李四');
INSERT INTO `wifiinfo` VALUES ('WIFI', '80', '8', 'CA10HS150104021', '1', '10000', '张森');
INSERT INTO `wifiinfo` VALUES ('WIFI', '98', '1', 'WIFI98', '1', '10099', '陆级鹏');
