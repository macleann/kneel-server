CREATE TABLE `Metals`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `metal` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE `Styles`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `style_type` NVARCHAR(30) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE `Sizes`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `carets` NUMERIC(5,2) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

DROP TABLE `Sizes`;

CREATE TABLE `Orders`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `timestamp` TIME NOT NULL,
    `metal_id` INTEGER NOT NULL,
    `style_id` INTEGER NOT NULL,
    `size_id` INTEGER NOT NULL,
    FOREIGN KEY (`metal_id`) REFERENCES `Metals`(`id`),
    FOREIGN KEY (`style_id`) REFERENCES `Styles`(`id`),
    FOREIGN KEY (`size_id`) REFERENCES `Sizes`(`id`)
);

INSERT INTO `Metals` (`metal`, `price`) VALUES ('Sterling Silver', 12.42);
INSERT INTO `Metals` (`metal`, `price`) VALUES ('14K Gold', 736.4);
INSERT INTO `Metals` (`metal`, `price`) VALUES ('24K Gold', 1258.9);
INSERT INTO `Metals` (`metal`, `price`) VALUES ('Platinum', 795.45);
INSERT INTO `Metals` (`metal`, `price`) VALUES ('Palladium', 1241.0);

INSERT INTO `Styles` (`style_type`, `price`) VALUES ('Classic', 500);
INSERT INTO `Styles` (`style_type`, `price`) VALUES ('Modern', 710);
INSERT INTO `Styles` (`style_type`, `price`) VALUES ('Vintage', 965);

INSERT INTO `Sizes` (`carets`, `price`) VALUES (0.5, 405);
INSERT INTO `Sizes` (`carets`, `price`) VALUES (0.75, 782);
INSERT INTO `Sizes` (`carets`, `price`) VALUES (1, 1470);
INSERT INTO `Sizes` (`carets`, `price`) VALUES (1.5, 1997);
INSERT INTO `Sizes` (`carets`, `price`) VALUES (2, 3638);

INSERT INTO `Orders` (`timestamp`, `metal_id`, `style_id`, `size_id`) VALUES (1614659931693, 1, 2, 3);
INSERT INTO `Orders` (`timestamp`, `metal_id`, `style_id`, `size_id`) VALUES (1616333988188, 2, 3, 1);
INSERT INTO `Orders` (`timestamp`, `metal_id`, `style_id`, `size_id`) VALUES (1616334884289, 3, 1, 2);
INSERT INTO `Orders` (`timestamp`, `metal_id`, `style_id`, `size_id`) VALUES (1616334980694, 4, 3, 2);

SELECT
    o.timestamp,
    o.size_id,
    o.style_id,
    o.metal_id,
    m.metal,
    m.price
FROM `Orders` o
JOIN Metals m ON m.id = o.metal_id