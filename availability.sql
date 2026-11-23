-- READ-ONLY. Returns only property id, planned/active state and the end of the stay/block covering today.
-- No guest names, phones, emails or prices are selected.
with today as (select (now() at time zone 'Asia/Dubai')::date::text d)
select coalesce(json_agg(row_to_json(x) order by x.id), '[]') from (
  select p.id, p.status as pms_status,
    (select max(r.check_out) from reservations r, today
      where r.property_id = p.id and r.status in ('confirmed','checked_in','blocked')
        and r.check_in <= today.d and r.check_out > today.d) as busy_until,
    (select bool_or(r.status <> 'blocked') from reservations r, today
      where r.property_id = p.id and r.status in ('confirmed','checked_in','blocked')
        and r.check_in <= today.d and r.check_out > today.d) as is_booking
  from properties p where p.status <> 'archived'
) x;
