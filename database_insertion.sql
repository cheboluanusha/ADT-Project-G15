-- Inserting Data into Players Table : Authored by Naman

INSERT INTO Players (player_id, password) 
VALUES 
('player1', 'password123'),
('player2', 'password456'),
('player3', 'password789'),
('player4', 'passwordabc'),
('player5', 'passworddef'),
('player6', 'passwordghi'),
('player7', 'passwordjkl'),
('player8', 'passwordmno'),
('player9', 'passwordpqr'),
('player10', 'passwordstu');

-- Inserting Data into SoloStats Table : Authored by Naman

INSERT INTO SoloStats (stats_id, player_id, score, top1, kill_death_ratio, matches_count, kills, minutes_played) 
VALUES 
(1, 'player1', 1500, 12, 1.5, 20, 15, 60),
(2, 'player2', 2000, 11, 2.0, 25, 20, 70),
(3, 'player3', 1700, 12, 2.5, 30, 25, 80),
(4, 'player4', 1900, 15, 3.0, 35, 30, 90),
(5, 'player5', 900, 5, 3.5, 40, 35, 100),
(6, 'player6', 1000, 20, 4.0, 45, 40, 110),
(7, 'player7', 1200, 40, 4.5, 50, 45, 120),
(8, 'player8', 1400, 50, 5.0, 55, 50, 130),
(9, 'player9', 1600, 43, 5.5, 60, 55, 140),
(10, 'player10', 2100, 21, 6.0, 65, 60, 150);

-- Inserting Data into DuosStats Table : Authored by Naman
INSERT INTO DuosStats (stats_id, player_id, score, top1, kill_death_ratio, matches_count, kills, minutes_played) 
VALUES 
(1, 'player1', 500, 14, 1.5, 20, 15, 60),
(2, 'player2', 300, 12, 1.7, 22, 18, 65),
(3, 'player3', 400, 21, 2.0, 24, 21, 70),
(4, 'player4', 800, 11, 2.3, 26, 24, 75),
(5, 'player5', 900, 8, 2.6, 28, 27, 80),
(6, 'player6', 200, 2, 2.9, 30, 30, 85),
(7, 'player7', 1100, 26, 3.2, 32, 33, 90),
(8, 'player8', 700, 21, 3.5, 34, 36, 95),
(9, 'player9', 1300, 27, 3.8, 36, 39, 100),
(10, 'player10', 100, 24, 4.1, 38, 42, 105);

-- Inserting Data into TriosStats Table : Authored by Naman
INSERT INTO TriosStats (stats_id, player_id, score, top1, kill_death_ratio, matches_count, kills, minutes_played) 
VALUES 
(1, 'player1', 550, 10, 1.6, 21, 16, 62),
(2, 'player2', 750, 18, 1.9, 23, 19, 67),
(3, 'player3', 250, 19, 2.2, 25, 22, 72),
(4, 'player4', 1250, 11, 2.5, 27, 25, 77),
(5, 'player5', 1650, 9, 2.8, 29, 28, 82),
(6, 'player6', 1150, 2, 3.1, 31, 31, 87),
(7, 'player7', 1050, 23, 3.4, 33, 34, 92),
(8, 'player8', 1350, 29, 3.7, 35, 37, 97),
(9, 'player9', 550, 22, 4.0, 37, 40, 102),
(10, 'player10', 1450, 31, 4.3, 39, 43, 107);

-- Inserting Data into SquadsStats Table : Authored by Naman
INSERT INTO SquadsStats (stats_id, player_id, score, top1, kill_death_ratio, matches_count, kills, minutes_played) 
VALUES 
(1, 'player1', 500, 16, 1.7, 22, 17, 64),
(2, 'player2', 800, 11, 2.0, 24, 20, 69),
(3, 'player3', 200, 19, 2.3, 26, 23, 74),
(4, 'player4', 1200, 20, 2.6, 28, 26, 79),
(5, 'player5', 1000, 10, 2.9, 30, 29, 84),
(6, 'player6', 100, 23, 3.2, 32, 32, 89),
(7, 'player7', 300, 29, 3.5, 34, 35, 94),
(8, 'player8', 700, 33, 3.8, 36, 38, 99),
(9, 'player9', 900, 32, 4.1, 38, 41, 104),
(10, 'player10', 1200, 21, 4.4, 40, 44, 109);

-- Inserting Data into LTMStats Table : Authored by Naman
INSERT INTO LTMStats (stats_id, player_id, score, top1, kill_death_ratio, matches_count, kills, minutes_played) 
VALUES 
(1, 'player1', 150, 3, 1.8, 23, 18, 66),
(2, 'player2', 450, 21, 2.1, 25, 21, 71),
(3, 'player3', 950, 19, 2.4, 27, 24, 76),
(4, 'player4', 350, 11, 2.7, 29, 27, 81),
(5, 'player5', 1050, 25, 3.0, 31, 30, 86),
(6, 'player6', 1150, 30, 3.3, 33, 33, 91),
(7, 'player7', 850, 2, 3.6, 35, 36, 96),
(8, 'player8', 1350, 21, 3.9, 37, 39, 101),
(9, 'player9', 650, 9, 4.2, 39, 42, 106),
(10, 'player10', 1250, 35, 4.5, 41, 45, 111);


select * from Players;
select * from SoloStats;
select * from DuosStats;
select * from TriosStats;
select * from SquadsStats;
select * from LTMStats;

