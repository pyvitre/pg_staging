select 'delete from '
  ||(select n1.nspname||'.'||c1.relname from pg_class c1 join pg_namespace n1 on c1.relnamespace=n1.oid
			where c1.oid=con.confrelid)
  ||' where row( '
  || array_to_string(array( select a1.attname::text from pg_attribute a1, generate_series( 1, array_upper(con.conkey, 1) ) as s(i)
			where  a1.attnum=con.confkey[s.i] and a1.attrelid=con.confrelid ) ,', ')
  || ' ) not in ( select '
  || array_to_string(array( select a1.attname::text from pg_attribute a1, generate_series( 1, array_upper(con.conkey, 1) ) as s(i)
			where  a1.attnum=con.conkey[s.i] and a1.attrelid=c.oid ) ,', ')
  || ' from '||n.nspname||'.'||c.relname || ' group by '
  || array_to_string(array( select a1.attname::text from pg_attribute a1, generate_series( 1, array_upper(con.conkey, 1) ) as s(i)
				where  a1.attnum=con.conkey[s.i] and a1.attrelid=c.oid ) ,', ')
  || ' ) '
from pg_class c join pg_namespace n
  on c.relnamespace=n.oid
  join pg_constraint con on c.oid = con.conrelid
  where n.nspname||'.'||c.relname in
  ( 'public.comptes','public.affiliations_prc','public.affiliations_revmap','public.affiliations_sites',
    'public.comptes_parametres','public.documents','public.documents_details','public.documents_paliers',
    'public.i18n_charset','public.i18n_mail','public.indicatifs_pays','public.ip_country','public.ip_country_exception',
    'public.l10n_locale','public.l10n_project','public.paliers','public.paliers_description','public.paliers_details_audiotel',
    'public.paliers_details_cb','public.paliers_details_neosurf','public.paliers_details_sms','public.paliers_details_wha',
    'public.paliers_droits','public.paliers_langue','public.paliers_ordre','public.paliers_pays','public.paliers_revers',
    'public.paliers_type','public.parametres','public.pasr_alias','public.pasr_palier','public.pasr_stype','public.sites',
    'public.tarifs_speciaux','public.paliers_details_dineromail','public.paliers_details_sms_extension',
    'public.paliers_details_hipay' )
   and con.contype='f' 