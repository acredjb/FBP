create or replace procedure fbp_pre(ref_count in out number) is
       
  cans    number;
  y_count        number;
  n_count        number;
  res_count      number;
  r_li           number;
  r_ms           number;
  r_inte           number;
  r_w              number;
  r_game         varchar2(100);
  res            varchar2(100);
  res_y          varchar2(100);
  res_n          varchar2(100);
  group_by_count number;

  cursor fbp_cur is
    select * from fbp_predict;

  fbp_rec fbp_predict%rowtype;

begin
  cans:=3;
  group_by_count := 0;
  res_count      := 0;
  open fbp_cur;
  loop
    fetch fbp_cur
      into fbp_rec;
    exit when fbp_cur%notfound;
    r_li   := fbp_rec.li;
    r_ms   := fbp_rec.ms;
    r_inte   := fbp_rec.inte;
    r_w      :=fbp_rec.w;
    r_game := fbp_rec.game_cc;
  --li ms inte
    fbp_3board_li2ms2in(ref_count,
                     r_li,
                     r_ms,
                     r_inte,
                     res_count,
                     res,
                     group_by_count,
                     y_count,
                     res_y,
                     n_count,
                     res_n);
    if group_by_count = 1 then 
      if res_count > 2 then --y数量3及以上，n=0；或n数量3及以上，y=0
        res := res || to_char(res_count);
        update fbp_predict p set p.attr1 = res where p.game_cc = r_game;
        commit;
      end if;
    end if;
    if group_by_count = 2 then
      res_y := res_y || to_char(y_count);
      res_n := res_n || to_char(n_count);
      res   := res_y || '|' || res_n;
      if y_count>cans*n_count or n_count>cans*y_count then
      update fbp_predict p set p.attr1 = res where p.game_cc = r_game;
      commit;
      end if;
    end if;
    
    res:='';
    --li ms w
    fbp_3board_li2ms2w(ref_count,
                     r_li,
                     r_ms,
                     r_w,
                     res_count,
                     res,
                     group_by_count,
                     y_count,
                     res_y,
                     n_count,
                     res_n);
    if group_by_count = 1 then 
      if res_count > 2 then --y数量3及以上，n=0；或n数量3及以上，y=0
        res := res || to_char(res_count);
        update fbp_predict p set p.attr2 = res where p.game_cc = r_game;
        commit;
      end if;
    end if;
    if group_by_count = 2 then
      res_y := res_y || to_char(y_count);
      res_n := res_n || to_char(n_count);
      res   := res_y || '|' || res_n;
      if y_count>cans*n_count or n_count>cans*y_count then
      update fbp_predict p set p.attr2 = res where p.game_cc = r_game;
      commit;
      end if;
    end if;
    
    res:='';
    --li  inte w
    fbp_3board_li2in2w(ref_count,
                     r_li,
                     r_inte,
                     r_w,
                     res_count,
                     res,
                     group_by_count,
                     y_count,
                     res_y,
                     n_count,
                     res_n);
    if group_by_count = 1 then 
      if res_count > 2 then --y数量3及以上，n=0；或n数量3及以上，y=0
        res := res || to_char(res_count);
        update fbp_predict p set p.attr3 = res where p.game_cc = r_game;
        commit;
      end if;
    end if;
    if group_by_count = 2 then
      res_y := res_y || to_char(y_count);
      res_n := res_n || to_char(n_count);
      res   := res_y || '|' || res_n;
      if y_count>cans*n_count or n_count>cans*y_count then
      update fbp_predict p set p.attr3 = res where p.game_cc = r_game;
      commit;
      end if;
    end if;
    
    res:='';
    -- ms inte w
    fbp_3board_ms2in2w(ref_count,
                     r_ms,
                     r_inte,
                     r_w,
                     res_count,
                     res,
                     group_by_count,
                     y_count,
                     res_y,
                     n_count,
                     res_n);
    if group_by_count = 1 then 
      if res_count > 2 then --y数量3及以上，n=0；或n数量3及以上，y=0
        res := res || to_char(res_count);
        update fbp_predict p set p.attr4 = res where p.game_cc = r_game;
        commit;
      end if;
    end if;
    if group_by_count = 2 then
      res_y := res_y || to_char(y_count);
      res_n := res_n || to_char(n_count);
      res   := res_y || '|' || res_n;
      if y_count>cans*n_count or n_count>cans*y_count then
      update fbp_predict p set p.attr4 = res where p.game_cc = r_game;
      commit;
      end if;
    end if;
    
    
  end loop;

end fbp_pre;
