CREATE TABLE `user_profile_history` (
  `user_id` int NOT NULL,
  `mode` int NOT NULL,
  `captured_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `rank` int NOT NULL,
  `pp` int NOT NULL,
  `country_rank` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

ALTER TABLE `user_profile_history`
  ADD PRIMARY KEY (`user_id`,`mode`,`captured_at`);
