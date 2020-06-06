create or replace procedure fbp_3board(ref_count      in number,
                                       a              in number,
                                       b              in number,
                                       c              in number,
                                       p1             in varchar2,
                                       p2             in varchar2,
                                       p3             in varchar2,
                                       res_count      out number,
                                       res            out varchar2,
                                       group_by_count out number,
                                       y_count        out number,
                                       res_y          out varchar2,
                                       n_count        out number,
                                       res_n          out varchar2) is
  y varchar2(10);
  n varchar2(10);
begin
  y := 'y';
  n := 'n';
  --共有1行或2行

  execute immediate 'select count(*)    
  from (SELECT count(gameresult), gameresult
          FROM (select *
                  from fbp_pl
                 where rownum < ' || ref_count ||
                    ' order by game_cc desc) p
         WHERE    p.' || p1 || '=' || a || ' and p.' || p2 || '=' || b ||
                    ' and p.' || p3 || '=' || c || ' group by gameresult)'
    into group_by_count;
  if group_by_count = 1 then
    execute immediate 'SELECT count(gameresult), gameresult        
      FROM (select *
              from fbp_pl
             where rownum < ' || ref_count ||
                      ' order by game_cc desc) p
           WHERE    p.' || p1 || '=' || a || ' and p.' || p2 || '=' || b ||
                      ' and p.' || p3 || '=' || c || ' group by gameresult'
      into res_count, res;
  end if;
  if group_by_count = 2 then
    --有两行时，y的数量          
    execute immediate 'select q.c, q.r      
      from (SELECT count(gameresult) c, gameresult r
              FROM (select *
                      from fbp_pl
                     where rownum < ' || ref_count ||
                      ' order by game_cc desc) p
           WHERE    p.' || p1 || '=' || a || ' and p.' || p2 || '=' || b ||
                      ' and p.' || p3 || '=' || c || ' group by gameresult) q
     where q.r = ' || '''' || y || ''''
      into y_count, res_y;
    --有两行时，n的数量
    execute immediate 'select q.c, q.r      
      from (SELECT count(gameresult) c, gameresult r
              FROM (select *
                      from fbp_pl
                     where rownum < ' || ref_count ||
                      ' order by game_cc desc) p
           WHERE    p.' || p1 || '=' || a || ' and p.' || p2 || '=' || b ||
                      ' and p.' || p3 || '=' || c || ' group by gameresult) q
     where q.r = ' || '''' || n || ''''
      into n_count, res_n;
  end if;
end fbp_3board;

示例：
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
