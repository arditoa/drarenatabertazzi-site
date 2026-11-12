-- Contatos / WhatsApp: telefone na agenda, recebimento direto das fontes e preferências por paciente
-- Aplicado no SQL Editor do Supabase em 10/11/2026.

alter table public.atendimentos add column if not exists telefone text;

-- Gravação da agenda (uso interno: chamada só pelas funções abaixo)
create or replace function public._gravar_atendimentos(de date, ate date, itens jsonb)
returns jsonb language plpgsql security definer set search_path to 'public' as $$
declare n int; js jsonb := _gravar_atendimentos.itens;
begin
  delete from atendimentos a where a.origem='eyecare' and a.data between _gravar_atendimentos.de and _gravar_atendimentos.ate
    and a.local in (select distinct x->>'local' from jsonb_array_elements(js) x);
  insert into atendimentos(id,data,inicio,unidade,local,paciente,paciente_id,nascimento,plano,itens,tipo,status,descricao,telefone)
  select x->>'id', (x->>'data')::date, nullif(x->>'inicio','')::timestamptz, x->>'unidade', x->>'local', x->>'paciente', x->>'paciente_id',
         nullif(x->>'nascimento','')::date, x->>'plano', x->>'itens', x->>'tipo', x->>'status', x->>'descricao', nullif(x->>'telefone','')
  from jsonb_array_elements(js) x
  on conflict (id) do update set data=excluded.data, inicio=excluded.inicio, unidade=excluded.unidade, local=excluded.local, paciente=excluded.paciente,
    plano=excluded.plano, itens=excluded.itens, tipo=excluded.tipo, status=excluded.status, descricao=excluded.descricao,
    telefone=coalesce(excluded.telefone, atendimentos.telefone), sincronizado_em=now();
  get diagnostics n = row_count;
  insert into sincronizacoes(de,ate,recebidos,inseridos) values (_gravar_atendimentos.de, _gravar_atendimentos.ate, jsonb_array_length(js), n);
  return jsonb_build_object('ok',true,'recebidos',jsonb_array_length(js),'gravados',n);
end $$;
revoke execute on function public._gravar_atendimentos(date,date,jsonb) from public, anon, authenticated;

-- Portal (usuário logado)
create or replace function public.sync_atendimentos(de date, ate date, itens jsonb)
returns jsonb language plpgsql security definer set search_path to 'public' as $$
begin
  if not public.autorizado() then raise exception 'sem permissão'; end if;
  return public._gravar_atendimentos(sync_atendimentos.de, sync_atendimentos.ate, sync_atendimentos.itens);
end $$;

-- Sincronização automática (direto da aba do EyecareBI/Amigo, com a mesma chave das planilhas)
create or replace function public.receber_agenda(chave text, de date, ate date, itens jsonb)
returns jsonb language plpgsql security definer set search_path to 'public' as $$
begin
  if not exists (select 1 from chave_planilhas c where c.chave = receber_agenda.chave) then raise exception 'chave inválida'; end if;
  if jsonb_array_length(receber_agenda.itens) > 5000 then raise exception 'pacote grande demais'; end if;
  return public._gravar_atendimentos(receber_agenda.de, receber_agenda.ate, receber_agenda.itens);
end $$;

-- Completa telefones de atendimentos antigos (só preenche vazios, nunca troca, nunca apaga)
create or replace function public.receber_telefones(chave text, itens jsonb)
returns jsonb language plpgsql security definer set search_path to 'public' as $$
declare n int;
begin
  if not exists (select 1 from chave_planilhas c where c.chave = receber_telefones.chave) then raise exception 'chave inválida'; end if;
  update atendimentos a set telefone = x.telefone
  from (select y->>'id' id, nullif(y->>'telefone','') telefone from jsonb_array_elements(receber_telefones.itens) y) x
  where a.id = x.id and x.telefone is not null and coalesce(a.telefone,'') = '';
  get diagnostics n = row_count;
  return jsonb_build_object('ok',true,'recebidos',jsonb_array_length(receber_telefones.itens),'atualizados',n);
end $$;

-- Preferências de contato por paciente (não enviar, consentimento, exportação, mensagens enviadas)
create table if not exists public.contatos_prefs (
  paciente_id   text primary key,
  nao_enviar    boolean not null default false,
  consentimento date,
  exportado_em  timestamptz,
  aniv_ano      int,      -- último ano em que foi enviado o "feliz aniversário"
  natal_ano     int,      -- último ano em que foi enviada a mensagem de Natal
  obs           text,
  atualizado_em timestamptz not null default now()
);
alter table public.contatos_prefs enable row level security;
drop policy if exists p_cprefs on public.contatos_prefs;
create policy p_cprefs on public.contatos_prefs for all to authenticated using (autorizado()) with check (autorizado());

-- Modelos de mensagem de aniversário e de Natal
alter table public.modelos drop constraint if exists modelos_tipo_check;
alter table public.modelos add constraint modelos_tipo_check check (tipo = any (array['mensagem','video','aniversario','natal']));
