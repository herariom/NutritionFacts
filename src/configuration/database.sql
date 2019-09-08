USE `pymysql`;

CREATE TABLE `product_data` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `file_name` varchar(300) NOT NULL,
  `product_name` varchar(300) NOT NULL,
  `calories` smallint(5) unsigned NOT NULL,
  `fat` smallint(5) unsigned NOT NULL,
  `carbohydrates` smallint(5) unsigned NOT NULL,
  `protein` smallint(5) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;