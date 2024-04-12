/* This script calculates the sum of the results of the 10 main queries */

/* 
Q_1: In the La Liga season of 2020/2021, sort the players from highest to lowest based on their average
xG scores. Output both the player names and their average xG scores. Consider only the players
who made at least one shot (the xG scores are greater than 0). 
*/
select 'Q_01' as query_number, sum(avg_xg) from (
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
order by avg_xg desc)

/* 
Q_2: In the La Liga season of 2020/2021, find the players with the most shots. Sort them from highest to
lowest. Output both the player names and the number of shots. Consider only the players who
made at least one shot (the lowest number of shots should be 1, not 0). 
*/
union select 'Q_02' as query_number, sum(shots) from (
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
order by count(s) desc)

/*
Q_3: In the La Liga seasons of 2020/2021, 2019/2020, and 2018/2019 combined, find the players with the
most first-time shots. Sort them from highest to lowest. Output the player names and the number
of first time shots. Consider only the players who made at least one shot (the lowest number of shots
should be 1, not 0).
*/
union select 'Q_03' as query_number, sum(shots) from (
	select player_name, count(s) shots from competitions c
inner join matches m
on c.competition_id = m.competition_id
and c.season_id = m.season_id
inner join events e
on m.match_id = e.match_id 
inner join players p
on e.player_id = p.player_id
inner join shot s
on e.id = s.event_id
where competition_name = 'La Liga'
and (
	season_name = '2020/2021'
	or season_name = '2019/2020'
	or season_name = '2018/2019'
	)
and first_time = true
group by player_name
order by count(s) desc)

/*
Q_4: In the La Liga season of 2020/2021, find the teams with the most passes made. Sort them from
highest to lowest. Output the team names and the number of passes. Consider the teams that
make at least one pass (the lowest number of passes is 1, not 0).
*/
union select 'Q_04' as query_number, sum(passes) from (
	select team_name, count(p) passes from competitions c
join matches m
on m.season_id = c.season_id
and m.competition_id = m.competition_id
join events e
on e.match_id = m.match_id
join pass p
on p.event_id = e.id
join teams t
on t.team_id = e.team_id
where season_name = '2020/2021'
and competition_name = 'La Liga'
group by team_name
order by count(p) desc)

/*
Q_5: In the Premier League season of 2003/2004, find the players who were the most intended recipients
of passes. Sort them from highest to lowest. Output the player names and the number of times
they were the intended recipients of passes. Consider the players who received at least one pass
(the lowest number of times they were the intended recipients is 1, not 0).
*/
union select 'Q_05' as query_number, sum(pass_recipient_count) from (
	select player_name, count(pass) pass_recipient_count from competitions c
join matches m
on m.season_id = c.season_id
and m.competition_id = m.competition_id
join events e
on e.match_id = m.match_id
join pass
on pass.event_id = e.id
join players
on players.player_id = pass.recipient
where season_name = '2003/2004'
and competition_name = 'Premier League'
group by player_name
order by count(pass) desc)

/*
Q_6: In the Premier League season of 2003/2004, find the teams with the most shots made. Sort them
from highest to lowest. Output the team names and the number of shots. Consider the teams that
made at least one shot (the lowest number of shots is 1, not 0).
*/
union select 'Q_06' as query_number, sum(shots) from (
	select team_name, count(s) shots from competitions c
join matches m
on m.season_id = c.season_id
and m.competition_id = m.competition_id
join events e
on e.match_id = m.match_id
join shot s
on s.event_id = e.id
join teams t
on t.team_id = e.team_id
where season_name = '2003/2004'
and competition_name = 'Premier League'
group by team_name
order by count(s) desc)

/*
Q_7: In the La Liga season of 2020/2021, find the players who made the most through balls. Sort them
from highest to lowest. Output the player names and the number of through balls. Consider the
players who made at least one through ball pass (the lowest number of through balls is 1, not 0).
*/
union select 'Q_07' as query_number, sum(through_balls) from (
	select player_name, count(pass) through_balls from competitions c
join matches m
on m.season_id = c.season_id
and m.competition_id = m.competition_id
join events e
on e.match_id = m.match_id
join pass
on pass.event_id = e.id
join players
on players.player_id = e.player_id
where season_name = '2020/2021'
and competition_name = 'La Liga'
and technique = 'Through Ball'
group by player_name
order by count(pass) desc)

/*
Q_8: In the La Liga season of 2020/2021, find the teams that made the most through balls. Sort them
from highest to lowest. Output the team names and the number of through balls. Consider the
teams with at least one through ball made in a match (the lowest total number of through balls is 1, not
0).
*/
union select 'Q_08' as query_number, sum(through_balls) from (
	select team_name, count(pass) through_balls from competitions c
join matches m
on m.season_id = c.season_id
and m.competition_id = m.competition_id
join events e
on e.match_id = m.match_id
join pass
on pass.event_id = e.id
join teams
on teams.team_id = e.team_id
where season_name = '2020/2021'
and competition_name = 'La Liga'
and technique = 'Through Ball'
group by team_name
order by count(pass) desc)

/*
Q_9: In the La Liga seasons of 2020/2021, 2019/2020, and 2018/2019 combined, find the players that
were the most successful in completed dribbles. Sort them from highest to lowest. Output the player
names and the number of successful completed dribbles. Consider the players that made at least
one successful dribble (the smallest number of successful dribbles is 1, not 0).
*/
union select 'Q_09' as query_number, sum(successful_dribbles) from (
	select player_name, count(d) successful_dribbles from competitions c
inner join matches m
on c.competition_id = m.competition_id
and c.season_id = m.season_id
inner join events e
on m.match_id = e.match_id 
inner join players p
on e.player_id = p.player_id
inner join dribble d
on e.id = d.event_id
where competition_name = 'La Liga'
and (
	season_name = '2020/2021'
	or season_name = '2019/2020'
	or season_name = '2018/2019'
	)
and d.outcome = 'Complete'
group by player_name
order by count(d) desc)

/*
Q_10: In the La Liga season of 2020/2021, find the players that were least dribbled past. Sort them from
lowest to highest. Output the player names and the number of dribbles. Consider the players
that were at least dribbled past once (the lowest number of occurrences of dribbling past the player is 1,
not 0).
*/
union select 'Q_10' as query_number, sum(dribbled_past_count) from (
	select player_name, count(e) dribbled_past_count from competitions c
inner join matches m
on c.competition_id = m.competition_id
and c.season_id = m.season_id
inner join events e
on m.match_id = e.match_id 
inner join event_types t
on t.event_type_id = e.event_type_id
inner join players p
on e.player_id = p.player_id
where competition_name = 'La Liga'
and season_name = '2020/2021'
and t.name = 'dribbled_past'
group by player_name
order by count(e) asc)
order by query_number

-- BONUS QUERIES
/*
1. Divide the goal into 6 equal-size areas (top-left, top-middle, top-right, bottom-left, bottom-middle, and
bottom-right). In the La Liga seasons of 2020/2021, 2019/2020, and 2018/2019 combined, find the players
who shot the most in either the top-left or top-right corners. Sort them from highest to lowest.
*/

/*
2. In the La Liga season of 2020/2021, find the teams with the most successful passes into the box. Sort
them from the highest to lowest.
*/