-- Database Creation: Authored by Anusha
CREATE DATABASE GameStatsDB;

-- Players Table Creation Authored by Anusha
CREATE TABLE IF NOT EXISTS Players (
    player_id VARCHAR(32) NOT NULL,
    password VARCHAR(50) NOT NULL,
    PRIMARY KEY (player_id)
);

-- SoloStats Table Creation Authored by Anusha
CREATE TABLE IF NOT EXISTS SoloStats (
    stats_id INT NOT NULL,
    player_id VARCHAR(32) NOT NULL,
    score INT NOT NULL,
    top1 INT NOT NULL,
    kill_death_ratio INT NOT NULL,
    matches_count INT NOT NULL,
    kills INT NOT NULL,
    minutes_played INT NOT NULL,
    PRIMARY KEY (stats_id),
    FOREIGN KEY (player_id) REFERENCES Players(player_id) ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- DuosStats Table Creation Authored by Anusha
CREATE TABLE IF NOT EXISTS DuosStats (
    stats_id INT NOT NULL,
    player_id VARCHAR(32) NOT NULL,
    score INT NOT NULL,
    top1 INT NOT NULL,
    kill_death_ratio INT NOT NULL,
    matches_count INT NOT NULL,
    kills INT NOT NULL,
    minutes_played INT NOT NULL,
    PRIMARY KEY (stats_id),
    FOREIGN KEY (player_id) REFERENCES Players(player_id) ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- TriosStats Table Creation Authored by Anusha
CREATE TABLE IF NOT EXISTS TriosStats (
    stats_id INT NOT NULL,
    player_id VARCHAR(32) NOT NULL,
    score INT NOT NULL,
    top1 INT NOT NULL,
    kill_death_ratio INT NOT NULL,
    matches_count INT NOT NULL,
    kills INT NOT NULL,
    minutes_played INT NOT NULL,
    PRIMARY KEY (stats_id),
    FOREIGN KEY (player_id) REFERENCES Players(player_id) ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- SquadsStats Table Creation Authored by Anusha
CREATE TABLE IF NOT EXISTS SquadsStats (
    stats_id INT NOT NULL,
    player_id VARCHAR(32) NOT NULL,
    score INT NOT NULL,
    top1 INT NOT NULL,
    kill_death_ratio INT NOT NULL,
    matches_count INT NOT NULL,
    kills INT NOT NULL,
    minutes_played INT NOT NULL,
    PRIMARY KEY (stats_id),
    FOREIGN KEY (player_id) REFERENCES Players(player_id) ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- LTMStats Table Creation Authored by Anusha
CREATE TABLE IF NOT EXISTS LTMStats (
    stats_id INT NOT NULL,
    player_id VARCHAR(32) NOT NULL,
    score INT NOT NULL,
    top1 INT NOT NULL,
    kill_death_ratio INT NOT NULL,
    matches_count INT NOT NULL,
    kills INT NOT NULL,
    minutes_played INT NOT NULL,
    PRIMARY KEY (stats_id),
    FOREIGN KEY (player_id) REFERENCES Players(player_id) ON UPDATE NO ACTION ON DELETE NO ACTION
);