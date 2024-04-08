/* Q 1: In the La Liga season of 2020/2021, sort the players from highest to lowest based on their average
xG scores. Output both the player names and their average xG scores. Consider only the players
who made at least one shot (the xG scores are greater than 0). 
HERE ITS FOR 2018/2019

*/

select player_name, avg(statsbomb_xg)::decimal(8, 8) as avg_xg from matches
natural join competitions
natural join events
natural join players
join shots
on events.id = event_id
where season_name = '2018/2019'
and competition_name = 'La Liga'
group by player_name, player_id
order by avg_xg desc;
-- select * from competitions
-- select match_id, season_name, player_name, statsbomb_xg from lineups
-- select * from lineups
-- natural join matches
-- natural join players
-- natural join competitions
-- natural join events
-- join shots on events.id = event_id
-- where player_name like 'Aoife%'