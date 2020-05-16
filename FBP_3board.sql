SELECT count(gameresult), gameresult
  FROM (select *
          from (select * from fbp_pl p order by p.game_cc desc)
         where rownum < 9500) P
 WHERE 1 = 1
   and P.HG = 1.97
   and P.BET365 = 2
   and P.WILLIAM = 1.95
 group by gameresult;

     COUNT(GAMERESULT)    GAMERESULT
1	6	              y
2	1	              n
