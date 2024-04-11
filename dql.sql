/* 
Q_1: In the La Liga season of 2020/2021, sort the players from highest to lowest based on their average
xG scores. Output both the player names and their average xG scores. Consider only the players
who made at least one shot (the xG scores are greater than 0). 
*/
select player_name, avg(statsbomb_xg) as avg_xg from competitions c
inner join matches m
on c.competition_id = m.competition_id
and c.season_id = m.season_id
inner join events e
on m.match_id = e.match_id 
inner join players p
on e.player_id = p.player_id
inner join shot s
on e.id = s.event_id
where season_name = '2020/2021'
and competition_name = 'La Liga'
group by player_name
order by avg_xg desc;

/* 
Q_2: In the La Liga season of 2020/2021, find the players with the most shots. Sort them from highest to
lowest. Output both the player names and the number of shots. Consider only the players who
made at least one shot (the lowest number of shots should be 1, not 0). 
*/
select player_name, count(s) as shots from competitions c
inner join matches m
on c.competition_id = m.competition_id
and c.season_id = m.season_id
inner join events e
on m.match_id = e.match_id 
inner join players p
on e.player_id = p.player_id
inner join shot s
on e.id = s.event_id
where season_name = '2020/2021'
and competition_name = 'La Liga'
group by player_name
order by count(s) desc;

/*
Q_3: In the La Liga seasons of 2020/2021, 2019/2020, and 2018/2019 combined, find the players with the
most first-time shots. Sort them from highest to lowest. Output the player names and the number
of first time shots. Consider only the players who made at least one shot (the lowest number of shots
should be 1, not 0).
*/
-- select player_name, count(s) shots from competitions c
-- inner join matches m
-- on c.competition_id = m.competition_id
-- and c.season_id = m.season_id
-- inner join events e
-- on m.match_id = e.match_id 
-- inner join players p
-- on e.player_id = p.player_id
-- inner join shot s
-- on e.id = s.event_id
-- where competition_name = 'La Liga'
-- and (
-- 	season_name = '2020/2021'
-- 	or season_name = '2019/2020'
-- 	or season_name = '2018/2019'
-- 	)
-- and first_time = true
-- group by player_name
-- order by count(s) desc;