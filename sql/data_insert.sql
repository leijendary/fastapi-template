do
$$
  begin
    for r in 1..10000000
      loop
        with row as (
          insert into sample (id, column_1, column_2, amount,
                              created_at,
                              modified_at, created_by,
                              modified_by)
            values (gen_random_uuid(), concat('Test sql loop insert ', r), r,
                    999999999.99, now(), now(), 'postgres',
                    'postgres') returning id
        )
        insert
        into sample_translation(language, ordinal, name, description,
                                reference_id)
        select 'en', 1, 'English', 'Test english translation', row.id
        from row
        UNION ALL
        select 'nl', 2, 'Dutch', 'Test dutch translation', row.id
        from row;
      end loop;
  end;
$$;