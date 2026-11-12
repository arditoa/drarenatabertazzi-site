-- Etapa "Em dúvida · aquecendo" + registro dos conteúdos enviados
alter table public.casos drop constraint if exists casos_etapa_check;
alter table public.casos add constraint casos_etapa_check check (etapa = any (array['indicado','orcamento','aguardando','duvida','fechado','agendado','realizado','pos_op','finalizado','em_tratamento','desistiu']));
alter table public.modelos drop constraint if exists modelos_tipo_check;
alter table public.modelos add constraint modelos_tipo_check check (tipo = any (array['mensagem','video','aniversario','natal','aquecimento']));
create table if not exists public.aquecimentos (
  id uuid primary key default gen_random_uuid(),
  caso_id uuid not null references public.casos(id) on delete cascade,
  em date not null default current_date,
  conteudo text not null,
  criado_em timestamptz not null default now()
);
alter table public.aquecimentos enable row level security;
drop policy if exists p_aquec on public.aquecimentos;
create policy p_aquec on public.aquecimentos for all to authenticated using (autorizado()) with check (autorizado());
