/*
Navicat MySQL Data Transfer

Source Server         : LOCAL
Source Server Version : 80017
Source Host           : localhost:3306
Source Database       : capacity

Target Server Type    : MYSQL
Target Server Version : 80017
File Encoding         : 65001

Date: 2019-11-27 10:02:47
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for camerainfo
-- ----------------------------
DROP TABLE IF EXISTS `camerainfo`;
CREATE TABLE `camerainfo` (
  `cameraId` int(11) NOT NULL,
  `sciencId` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `adminId` int(11) DEFAULT NULL,
  `adminName` varchar(255) DEFAULT NULL,
  `deviceType` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`cameraId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of camerainfo
-- ----------------------------
INSERT INTO `camerainfo` VALUES ('2', '1', 'CA00HS151116043', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('3', '1', 'CA00HS151116043', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('4', '1', 'CA00HS151116043', '1', '10000', '张森', '摄像头');
INSERT INTO `camerainfo` VALUES ('5', '1', 'CA00HS151116043', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('6', '1', 'CA00HS151116043', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('7', '1', 'CA00HS151116043', '1', '10000', '张森', '摄像头');
INSERT INTO `camerainfo` VALUES ('8', '1', 'CA00HS151116043', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('9', '1', 'CA00HS151116043', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('10', '1', 'CA00HS151116043', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('11', '2', 'CA20HS140718064', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('12', '2', 'CA20HS140718064', '1', '10000', '张森', '摄像头');
INSERT INTO `camerainfo` VALUES ('13', '2', 'CA20HS140718064', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('14', '2', 'CA20HS140718064', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('15', '2', 'CA20HS140718064', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('16', '2', 'CA20HS140718064', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('17', '2', 'CA20HS140718064', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('18', '2', 'CA20HS140718064', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('19', '2', 'CA20HS140718064', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('20', '2', 'CA20HS140718064', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('21', '3', 'CA20HS150826001', '1', '10000', '张森', '摄像头');
INSERT INTO `camerainfo` VALUES ('22', '3', 'CA20HS150826001', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('23', '3', 'CA20HS150826001', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('24', '3', 'CA20HS150826001', '1', '10000', '张森', '摄像头');
INSERT INTO `camerainfo` VALUES ('25', '3', 'CA20HS150826001', '1', '10000', '张森', '摄像头');
INSERT INTO `camerainfo` VALUES ('26', '3', 'CA20HS150826001', '1', '10000', '张森', '摄像头');
INSERT INTO `camerainfo` VALUES ('27', '3', 'CA20HS150826001', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('28', '3', 'CA20HS150826001', '1', '10000', '张森', '摄像头');
INSERT INTO `camerainfo` VALUES ('29', '3', 'CA20HS150826001', '1', '10000', '张森', '摄像头');
INSERT INTO `camerainfo` VALUES ('30', '3', 'CA20HS150826001', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('31', '4', 'CA10HS140718003', '1', '10000', '张森', '摄像头');
INSERT INTO `camerainfo` VALUES ('32', '4', 'CA10HS140718003', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('33', '4', 'CA10HS140718003', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('34', '4', 'CA10HS140718003', '1', '10000', '张森', '摄像头');
INSERT INTO `camerainfo` VALUES ('35', '4', 'CA10HS140718003', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('36', '4', 'CA10HS140718003', '1', '10000', '张森', '摄像头');
INSERT INTO `camerainfo` VALUES ('37', '4', 'CA10HS140718003', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('38', '4', 'CA10HS140718003', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('39', '4', 'CA10HS140718003', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('40', '4', 'CA10HS140718003', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('41', '5', 'CA10HS140718005', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('42', '5', 'CA10HS140718005', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('43', '5', 'CA10HS140718005', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('44', '5', 'CA10HS140718005', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('45', '5', 'CA10HS140718005', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('46', '5', 'CA10HS140718005', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('47', '5', 'CA10HS140718005', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('48', '5', 'CA10HS140718005', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('49', '5', 'CA10HS140718005', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('50', '5', 'CA10HS140718005', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('51', '6', 'CA10HS140718006', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('52', '6', 'CA10HS140718006', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('53', '6', 'CA10HS140718006', '1', '10000', '张森', '摄像头');
INSERT INTO `camerainfo` VALUES ('54', '6', 'CA10HS140718006', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('55', '6', 'CA10HS140718006', '1', '10000', '张森', '摄像头');
INSERT INTO `camerainfo` VALUES ('56', '6', 'CA10HS140718006', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('57', '6', 'CA10HS140718006', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('58', '6', 'CA10HS140718006', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('59', '6', 'CA10HS140718006', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('60', '6', 'CA10HS140718006', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('61', '7', 'CA10HS150104026', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('62', '7', 'CA10HS150104026', '1', '10000', '张森', '摄像头');
INSERT INTO `camerainfo` VALUES ('63', '7', 'CA10HS150104026', '1', '10000', '张森', '摄像头');
INSERT INTO `camerainfo` VALUES ('64', '7', 'CA10HS150104026', '1', '10000', '张森', '摄像头');
INSERT INTO `camerainfo` VALUES ('65', '7', 'CA10HS150104026', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('66', '7', 'CA10HS150104026', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('67', '7', 'CA10HS150104026', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('68', '7', 'CA10HS150104026', '1', '10000', '张森', '摄像头');
INSERT INTO `camerainfo` VALUES ('69', '7', 'CA10HS150104026', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('70', '7', 'CA10HS150104026', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('71', '8', 'CA10HS150104021', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('72', '8', 'CA10HS150104021', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('73', '8', 'CA10HS150104021', '1', '10000', '张森', '摄像头');
INSERT INTO `camerainfo` VALUES ('74', '8', 'CA10HS150104021', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('75', '8', 'CA10HS150104021', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('76', '8', 'CA10HS150104021', '1', '10002', '李四', '摄像头');
INSERT INTO `camerainfo` VALUES ('77', '8', 'CA10HS150104021', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('78', '8', 'CA10HS150104021', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('79', '8', 'CA10HS150104021', '1', '10001', '王五', '摄像头');
INSERT INTO `camerainfo` VALUES ('80', '8', 'CA10HS150104021', '1', '10000', '张森', '摄像头');
INSERT INTO `camerainfo` VALUES ('99', '1', '摄像头99', '1', '10099', '陆继鹏', '摄像头');
