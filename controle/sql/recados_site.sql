-- Recados e dúvidas enviados pelo formulário do site (drarenatabertazzi.com.br/#fale-com-a-dra)
-- Rode UMA vez no Supabase: painel do projeto > SQL Editor > New query > cole tudo > Run.
--
-- Quem pode o quê:
--   visitante do site (anon)      -> só ENVIAR (não consegue ler nada)
--   equipe logada no /controle     -> ler, mudar status e apagar

create table if not exists public.recados_site (
  id                uuid primary key default gen_random_uuid(),
  criado_em         timestamptz not null default now(),
  tipo              text not null default 'recado' check (tipo in ('recado', 'duvida')),
  nome              text not null check (char_length(nome) between 2 and 80),
  cidade            text check (char_length(cidade) <= 60),
  contato           text check (char_length(contato) <= 30),
  mensagem          text not null check (char_length(mensagem) between 5 and 1500),
  autoriza_publicar boolean not null default false,
  consentimento     boolean not null check (consentimento),
  status            text not null default 'novo' check (status in ('novo', 'respondido', 'virou_conteudo', 'arquivado')),
  obs               text
);

create index if not exists recados_site_criado_em on public.recados_site (criado_em desc);

alter table public.recados_site enable row level security;

drop policy if exists "site envia recado" on public.recados_site;
create policy "site envia recado" on public.recados_site
  for insert to anon, authenticated
  with check (status = 'novo' and consentimento and obs is null);

drop policy if exists "equipe le recados" on public.recados_site;
create policy "equipe le recados" on public.recados_site
  for select to authenticated using (public.autorizado());

drop policy if exists "equipe atualiza recados" on public.recados_site;
create policy "equipe atualiza recados" on public.recados_site
  for update to authenticated using (public.autorizado()) with check (public.autorizado());

drop policy if exists "equipe apaga recados" on public.recados_site;
create policy "equipe apaga recados" on public.recados_site
  for delete to authenticated using (public.autorizado());

grant insert on public.recados_site to anon;
grant select, insert, update, delete on public.recados_site to authenticated;
