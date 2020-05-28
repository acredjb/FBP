create or replace procedure fbp_3board(ref_count      in number,
                                             a              in number,
                                             b              in number,
                                             c              in number,
                                             res_count      out number,
                                             res            out varchar2,
                                             group_by_count out number,
                                             y_count        out number,
                                             res_y          out varchar2,
                                             n_count        out number,
                                             res_n          out varchar2) is

begin 

  --共有1行或2行
  select count(*)
    into group_by_count
    from (SELECT count(gameresult), gameresult
            FROM (select *
                    from fbp_pl
                   where rownum < ref_count
                   order by game_cc desc) p
           WHERE p.li = a
             and p.ms = b
             and p.inte = c
           group by gameresult);
  if group_by_count =1  then
    SELECT count(gameresult), gameresult
      into res_count, res
      FROM (select *
              from fbp_pl
             where rownum < ref_count
             order by game_cc desc) p
     WHERE p.li = a
       and p.ms = b
       and p.inte = c
     group by gameresult;
  end if;
  if group_by_count = 2 then
    --有两行时，y的数量          
    select q.c, q.r
      into y_count, res_y
      from (SELECT count(gameresult) c, gameresult r
              FROM (select *
                      from fbp_pl
                     where rownum < ref_count
                     order by game_cc desc) p
             WHERE p.li = a
               and p.ms = b
               and p.inte = c
             group by gameresult) q
     where q.r = 'y';
    --有两行时，n的数量
    select q.c, q.r
      into n_count, res_n
      from (SELECT count(gameresult) c, gameresult r
              FROM (select *
                      from fbp_pl
                     where rownum < ref_count
                     order by game_cc desc) p
             WHERE p.li = a
               and p.ms = b
               and p.inte = c
             group by gameresult) q
     where q.r = 'n';
  end if;
end fbp_3board;
