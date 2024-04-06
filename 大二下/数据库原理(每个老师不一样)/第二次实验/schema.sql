CREATE TABLE `供应商` (
  `供应商名` varchar(64) NOT NULL,
  PRIMARY KEY (`供应商名`));
CREATE TABLE `经销商` (
  `经销商名` varchar(64) NOT NULL,
  PRIMARY KEY (`经销商名`));
CREATE TABLE `客户` (
  `姓名` varchar(32) NOT NULL,
  `电话` varchar(16) DEFAULT NULL,
  `性别` varchar(1) DEFAULT NULL,
  `收入` int DEFAULT NULL,
  `地址` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`姓名`));
CREATE TABLE `车辆` (
  `VIN` int NOT NULL,
  `颜色` varchar(8) DEFAULT NULL,
  `排量` varchar(8) DEFAULT NULL,
  `变速器` varchar(16) DEFAULT NULL,
  `型号名` varchar(16) DEFAULT NULL,
  `金额` int DEFAULT NULL,
  `经销商名` varchar(64) DEFAULT NULL,
  `购买日期` date DEFAULT NULL,
  PRIMARY KEY (`VIN`),
  KEY `经销商_idx` (`经销商名`),
  CONSTRAINT `经销商` FOREIGN KEY (`经销商名`) REFERENCES `经销商` (`经销商名`));
  CREATE TABLE `销售` (
  `经销商名` varchar(64) NOT NULL,
  `VIN` int NOT NULL,
  `姓名` varchar(32) NOT NULL,
  `日期` date NOT NULL,
  PRIMARY KEY (`经销商名`,`VIN`,`姓名`),
  KEY `车辆_idx` (`VIN`),
  KEY `客户_idx` (`姓名`),
  CONSTRAINT `客户` FOREIGN KEY (`姓名`) REFERENCES `客户` (`姓名`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `经销商名` FOREIGN KEY (`经销商名`) REFERENCES `经销商` (`经销商名`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `车辆` FOREIGN KEY (`VIN`) REFERENCES `车辆` (`VIN`) ON DELETE CASCADE ON UPDATE CASCADE);
    CREATE TABLE `品牌` (
  `品牌名` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`品牌名`));
CREATE TABLE `型号` (
  `型号名` VARCHAR(32) NOT NULL,
  `品牌名` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`型号名`),
  INDEX `品牌_idx` (`品牌名` ASC) VISIBLE,
  CONSTRAINT `品牌`
    FOREIGN KEY (`品牌名`)
    REFERENCES `品牌` (`品牌名`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);
CREATE TABLE `零件` (
  `零件名` VARCHAR(32) NOT NULL,
  `供应商名` VARCHAR(64) NULL,
  PRIMARY KEY (`零件名`),
  INDEX `供应商_idx` (`供应商名` ASC) VISIBLE,
  CONSTRAINT `供应商`
    FOREIGN KEY (`供应商名`)
    REFERENCES `供应商` (`供应商名`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);
CREATE TABLE `零件属于` (
  `零件名` VARCHAR(32) NOT NULL,
  `型号名` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`零件名`, `型号名`),
  INDEX `型号_idx` (`型号名` ASC) VISIBLE,
  CONSTRAINT `零件`
    FOREIGN KEY (`零件名`)
    REFERENCES `零件` (`零件名`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `型号`
    FOREIGN KEY (`型号名`)
    REFERENCES `型号` (`型号名`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

