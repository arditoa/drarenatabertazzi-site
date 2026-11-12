-- Aba "Procedimentos": agenda de procedimentos, "não realizado" com motivo e ordem por última modificação
-- Rode UMA vez no Supabase: painel do projeto > SQL Editor > New query > cole tudo > Run.

-- 1) Procedimentos agendados que NÃO foram realizados (pressão alta, glicemia, faltou...)
create table if not exists public.proc_nao_realizados (
  id             uuid primary key default gen_random_uuid(),
  caso_id        uuid not null references public.casos(id) on delete cascade,
  sessao_id      uuid references public.sessoes(id) on delete set null,
  data_prevista  date not null,
  motivo         text not null,
  obs            text,
  remarcado_para date,
  criado_em      timestamptz not null default now(),
  criado_por     text
);
create index if not exists proc_nao_realizados_caso on public.proc_nao_realizados (caso_id);
alter table public.proc_nao_realizados enable row level security;
drop policy if exists p_proc_nr on public.proc_nao_realizados;
create policy p_proc_nr on public.proc_nao_realizados for all to authenticated using (autorizado()) with check (autorizado());

-- 2) Carimbo "atualizado_em" (para mostrar sempre primeiro o que foi mexido por último)
create or replace function public._carimba_atualizado() returns trigger language plpgsql as $$
begin new.atualizado_em := now(); return new; end $$;

alter table public.casos        add column if not exists atualizado_em timestamptz not null default now();
alter table public.sessoes      add column if not exists atualizado_em timestamptz not null default now();
alter table public.pos_contatos add column if not exists atualizado_em timestamptz not null default now();

drop trigger if exists t_atualizado on public.casos;
create trigger t_atualizado before update on public.casos for each row execute function public._carimba_atualizado();
drop trigger if exists t_atualizado on public.sessoes;
create trigger t_atualizado before update on public.sessoes for each row execute function public._carimba_atualizado();
drop trigger if exists t_atualizado on public.pos_contatos;
create trigger t_atualizado before update on public.pos_contatos for each row execute function public._carimba_atualizado();

-- 3) Confirmação manual de que o procedimento foi realizado (quando o prontuário ainda não tem a evolução)
alter table public.pos_contatos add column if not exists confirmado_em date;
