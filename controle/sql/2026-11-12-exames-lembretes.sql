-- Aba "Exames": lembrete para pacientes de convênio voltarem após 3 meses do último atendimento com exames
-- Rode UMA vez no Supabase: SQL Editor > New query > cole tudo > Run.
create table if not exists public.exames_lembretes (
  id            uuid primary key default gen_random_uuid(),
  paciente      text not null,           -- nome normalizado (chave)
  nome          text,
  base_data     date not null,           -- data do último atendimento usado como base
  status        text not null default 'enviado' check (status in ('enviado','nao_enviar','adiado')),
  em            date not null default current_date,
  adiar_ate     date,
  por           text,
  criado_em     timestamptz not null default now()
);
create index if not exists exames_lembretes_pac on public.exames_lembretes (paciente);
alter table public.exames_lembretes enable row level security;
drop policy if exists p_ex_lemb on public.exames_lembretes;
create policy p_ex_lemb on public.exames_lembretes for all to authenticated using (autorizado()) with check (autorizado());

-- Condições conhecidas do paciente (diabetes, glaucoma, DMRI...) marcadas pela equipe
create table if not exists public.paciente_condicoes (
  paciente      text primary key,
  nome          text,
  condicoes     text[] not null default '{}',
  atualizado_em timestamptz not null default now(),
  por           text
);
alter table public.paciente_condicoes enable row level security;
drop policy if exists p_pac_cond on public.paciente_condicoes;
create policy p_pac_cond on public.paciente_condicoes for all to authenticated using (autorizado()) with check (autorizado());
