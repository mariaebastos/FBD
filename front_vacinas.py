#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import date
import panel as pn

pn.extension()


engine = create_engine("postgresql://postgres:FBD2025@localhost:5432/vacinas_db")
Session = sessionmaker(bind=engine)
session = Session()


Base = declarative_base()





# In[2]:


class Fabricante(Base):
    __tablename__ = 'fabricante'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)

class Vacina(Base):
    __tablename__ = 'vacina'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    fabricante_id = Column(Integer, ForeignKey('fabricante.id'))
    fabricante = relationship("Fabricante")

class UnidadeSaude(Base):
    __tablename__ = 'unidade_saude'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    endereco = Column(String)

class Paciente(Base):
    __tablename__ = 'paciente'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    data_nascimento = Column(Date)
    cpf = Column(String, unique=True)

class Aplicacao(Base):
    __tablename__ = 'aplicacao'
    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey('paciente.id'))
    vacina_id = Column(Integer, ForeignKey('vacina.id'))
    unidade_id = Column(Integer, ForeignKey('unidade_saude.id'))
    data_aplicacao = Column(Date)

    paciente = relationship("Paciente")
    vacina = relationship("Vacina")
    unidade = relationship("UnidadeSaude")





# In[3]:


input_nome = pn.widgets.TextInput(name="Nome do Fabricante")
input_id = pn.widgets.IntInput(name="ID do Fabricante")
output = pn.pane.Markdown("")

def criar_fabricante(event=None):
    nome = input_nome.value.strip()
    if nome:
        novo = Fabricante(nome=nome)
        session.add(novo)
        session.commit()
        output.object = f"✅ Fabricante '{nome}' adicionado."
    else:
        output.object = "⚠️ Nome inválido."

def listar_fabricantes(event=None):
    fabricantes = session.query(Fabricante).all()
    texto = "\n".join([f"{f.id} - {f.nome}" for f in fabricantes]) or "Nenhum fabricante encontrado."
    output.object = f"### Fabricantes:\n{texto}"

def atualizar_fabricante(event=None):
    fab = session.get(Fabricante, input_id.value)
    if fab:
        fab.nome = input_nome.value
        session.commit()
        output.object = f"✏️ Fabricante ID {fab.id} atualizado."
    else:
        output.object = "❌ Fabricante não encontrado."

def remover_fabricante(event=None):
    fab = session.get(Fabricante, input_id.value)
    if fab:
        session.delete(fab)
        session.commit()
        output.object = f"🗑️ Fabricante ID {fab.id} removido."
    else:
        output.object = "❌ Fabricante não encontrado."

painel_fabricante = pn.Column(
    "## Fabricantes",
    input_id, input_nome,
    pn.Row(
        pn.widgets.Button(name="Criar", button_type="primary", on_click=criar_fabricante),
        pn.widgets.Button(name="Listar", button_type="success", on_click=listar_fabricantes),
        pn.widgets.Button(name="Atualizar", button_type="warning", on_click=atualizar_fabricante),
        pn.widgets.Button(name="Remover", button_type="danger", on_click=remover_fabricante),
    ),
    output
)




# In[4]:


vacina_id = pn.widgets.IntInput(name="ID da Vacina")
vacina_nome = pn.widgets.TextInput(name="Nome")
vacina_tipo = pn.widgets.TextInput(name="Tipo")
vacina_fab = pn.widgets.IntInput(name="ID do Fabricante")
vac_out = pn.pane.Markdown("")

def criar_vacina(event=None):
    if vacina_nome.value and vacina_tipo.value:
        session.add(Vacina(nome=vacina_nome.value, tipo=vacina_tipo.value, fabricante_id=vacina_fab.value))
        session.commit()
        vac_out.object = "✅ Vacina adicionada."
    else:
        vac_out.object = "⚠️ Dados inválidos."

def listar_vacinas(event=None):
    vacs = session.query(Vacina).all()
    texto = "\n".join([f"{v.id} - {v.nome} ({v.tipo}) - Fab: {v.fabricante_id}" for v in vacs]) or "Nenhuma vacina encontrada."
    vac_out.object = f"### Vacinas:\n{texto}"

def atualizar_vacina(event=None):
    v = session.get(Vacina, vacina_id.value)
    if v:
        v.nome = vacina_nome.value
        v.tipo = vacina_tipo.value
        v.fabricante_id = vacina_fab.value
        session.commit()
        vac_out.object = "✏️ Atualizado."
    else:
        vac_out.object = "❌ Não encontrada."

def remover_vacina(event=None):
    v = session.get(Vacina, vacina_id.value)
    if v:
        session.delete(v)
        session.commit()
        vac_out.object = "🗑️ Removida."
    else:
        vac_out.object = "❌ Não encontrada."

painel_vacina = pn.Column(
    "## Vacinas",
    vacina_id, vacina_nome, vacina_tipo, vacina_fab,
    pn.Row(
        pn.widgets.Button(name="Criar", button_type="primary", on_click=criar_vacina),
        pn.widgets.Button(name="Listar", button_type="success", on_click=listar_vacinas),
        pn.widgets.Button(name="Atualizar", button_type="warning", on_click=atualizar_vacina),
        pn.widgets.Button(name="Remover", button_type="danger", on_click=remover_vacina)
    ),
    vac_out
)



# In[5]:


unid_id = pn.widgets.IntInput(name="ID")
unid_nome = pn.widgets.TextInput(name="Nome")
unid_endereco = pn.widgets.TextInput(name="Endereço")
unid_out = pn.pane.Markdown("")

def criar_unidade(event=None):
    if unid_nome.value:
        session.add(UnidadeSaude(nome=unid_nome.value, endereco=unid_endereco.value))
        session.commit()
        unid_out.object = "✅ Unidade criada."
    else:
        unid_out.object = "⚠️ Nome inválido."

def listar_unidades(event=None):
    unids = session.query(UnidadeSaude).all()
    texto = "\n".join([f"{u.id} - {u.nome}, {u.endereco}" for u in unids]) or "Nenhuma encontrada."
    unid_out.object = f"### Unidades:\n{texto}"

def atualizar_unidade(event=None):
    u = session.get(UnidadeSaude, unid_id.value)
    if u:
        u.nome = unid_nome.value
        u.endereco = unid_endereco.value
        session.commit()
        unid_out.object = "✏️ Atualizado."
    else:
        unid_out.object = "❌ Não encontrada."

def remover_unidade(event=None):
    u = session.get(UnidadeSaude, unid_id.value)
    if u:
        session.delete(u)
        session.commit()
        unid_out.object = "🗑️ Removida."
    else:
        unid_out.object = "❌ Não encontrada."

painel_unidade = pn.Column(
    "## Unidades de Saúde",
    unid_id, unid_nome, unid_endereco,
    pn.Row(
        pn.widgets.Button(name="Criar", button_type="primary", on_click=criar_unidade),
        pn.widgets.Button(name="Listar", button_type="success", on_click=listar_unidades),
        pn.widgets.Button(name="Atualizar", button_type="warning", on_click=atualizar_unidade),
        pn.widgets.Button(name="Remover", button_type="danger", on_click=remover_unidade)
    ),
    unid_out
)



# In[6]:


pac_id = pn.widgets.IntInput(name="ID")
pac_nome = pn.widgets.TextInput(name="Nome")
pac_data = pn.widgets.DatePicker(name="Nascimento")
pac_cpf = pn.widgets.TextInput(name="CPF")
pac_out = pn.pane.Markdown("")

def criar_paciente(event=None):
    if pac_nome.value and pac_cpf.value:
        session.add(Paciente(nome=pac_nome.value, data_nascimento=pac_data.value, cpf=pac_cpf.value))
        session.commit()
        pac_out.object = "✅ Paciente criado."
    else:
        pac_out.object = "⚠️ Dados inválidos."

def listar_pacientes(event=None):
    pacs = session.query(Paciente).all()
    texto = "\n".join([f"{p.id} - {p.nome}, {p.cpf}, {p.data_nascimento}" for p in pacs]) or "Nenhum paciente encontrado."
    pac_out.object = f"### Pacientes\n{texto}"

def atualizar_paciente(event=None):
    p = session.get(Paciente, pac_id.value)
    if p:
        p.nome = pac_nome.value
        p.data_nascimento = pac_data.value
        p.cpf = pac_cpf.value
        session.commit()
        pac_out.object = "✏️ Atualizado."
    else:
        pac_out.object = "❌ Não encontrado."

def remover_paciente(event=None):
    p = session.get(Paciente, pac_id.value)
    if p:
        session.delete(p)
        session.commit()
        pac_out.object = "🗑️ Removido."
    else:
        pac_out.object = "❌ Não encontrado."

painel_paciente = pn.Column(
    "## Pacientes",
    pac_id, pac_nome, pac_data, pac_cpf,
    pn.Row(
        pn.widgets.Button(name="Criar", button_type="primary", on_click=criar_paciente),
        pn.widgets.Button(name="Listar", button_type="success", on_click=listar_pacientes),
        pn.widgets.Button(name="Atualizar", button_type="warning", on_click=atualizar_paciente),
        pn.widgets.Button(name="Remover", button_type="danger", on_click=remover_paciente)
    ),
    pac_out
)



# In[7]:


apl_id = pn.widgets.IntInput(name="ID Aplicação")
apl_paciente = pn.widgets.IntInput(name="Paciente ID")
apl_vacina = pn.widgets.IntInput(name="Vacina ID")
apl_unidade = pn.widgets.IntInput(name="Unidade ID")
apl_data = pn.widgets.DatePicker(name="Data")
apl_out = pn.pane.Markdown("")

def criar_aplicacao(event=None):
    session.add(Aplicacao(
        paciente_id=apl_paciente.value,
        vacina_id=apl_vacina.value,
        unidade_id=apl_unidade.value,
        data_aplicacao=apl_data.value
    ))
    session.commit()
    apl_out.object = "✅ Aplicação registrada."

def listar_aplicacoes(event=None):
    apli = session.query(Aplicacao).all()
    texto = "\n".join([
        f"{a.id} - Paciente {a.paciente_id}, Vacina {a.vacina_id}, Unidade {a.unidade_id} ({a.data_aplicacao})"
        for a in apli
    ]) or "Nenhuma aplicação registrada."
    apl_out.object = f"### Aplicações\n{texto}"

def remover_aplicacao(event=None):
    a = session.get(Aplicacao, apl_id.value)
    if a:
        session.delete(a)
        session.commit()
        apl_out.object = "🗑️ Removida."
    else:
        apl_out.object = "❌ Não encontrada."

painel_aplicacao = pn.Column(
    "## Aplicações",
    apl_id, apl_paciente, apl_vacina, apl_unidade, apl_data,
    pn.Row(
        pn.widgets.Button(name="Registrar", button_type="primary", on_click=criar_aplicacao),
        pn.widgets.Button(name="Listar", button_type="success", on_click=listar_aplicacoes),
        pn.widgets.Button(name="Remover", button_type="danger", on_click=remover_aplicacao)
    ),
    apl_out
)



# In[8]:


pn.serve({
    "Fabricantes": painel_fabricante,
    "Vacinas": painel_vacina,
    "Unidades de Saúde": painel_unidade,
    "Pacientes": painel_paciente,
    "Aplicações": painel_aplicacao
}, port=5006, show=True)


# In[ ]:




