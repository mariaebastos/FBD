#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import date

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


Base.metadata.create_all(engine)
print("Tabelas criadas com sucesso.")


# In[4]:


def criar_fabricante(nome):
    novo = Fabricante(nome=nome)
    session.add(novo)
    session.commit()
    print("Fabricante adicionado.")

def listar_fabricantes():
    fabricantes = session.query(Fabricante).all()
    if not fabricantes:
        print("Nenhum fabricante cadastrado.")
    for f in fabricantes:
        print(f"{f.id} - {f.nome}")

def atualizar_fabricante(id_fab, novo_nome):
    fab = session.get(Fabricante, id_fab)
    if fab:
        fab.nome = novo_nome
        session.commit()
        print("Fabricante atualizado.")
    else:
        print("Fabricante não encontrado.")

def remover_fabricante(id_fab):
    fab = session.get(Fabricante, id_fab)
    if not fab:
        print("Fabricante não encontrado.")
        return

    vacinas_relacionadas = session.query(Vacina).filter_by(fabricante_id=id_fab).all()
    if vacinas_relacionadas:
        print(f"Não é possível remover o fabricante com ID {id_fab}. Existem vacinas associadas a ele.")
        return

    session.delete(fab)
    session.commit()
    print("Fabricante removido com sucesso.")




# In[5]:


def criar_vacina(nome, tipo, fabricante_id):
    nova = Vacina(nome=nome, tipo=tipo, fabricante_id=fabricante_id)
    session.add(nova)
    session.commit()
    print("Vacina adicionada.")

def listar_vacinas():
    vacinas = session.query(Vacina).all()
    for v in vacinas:
        print(f"{v.id} - {v.nome} ({v.tipo}) - Fabricante ID: {v.fabricante_id}")

def atualizar_vacina(id_vac, nome, tipo, fabricante_id):
    v = session.get(Vacina, id_vac)
    if v:
        v.nome = nome
        v.tipo = tipo
        v.fabricante_id = fabricante_id
        session.commit()
        print("Vacina atualizada.")
    else:
        print("Vacina não encontrada.")

def remover_vacina(id_vac):
    v = session.get(Vacina, id_vac)
    if v:
        session.delete(v)
        session.commit()
        print("Vacina removida.")
    else:
        print("Vacina não encontrada.")




# In[6]:


def criar_unidade(nome, endereco):
    nova = UnidadeSaude(nome=nome, endereco=endereco)
    session.add(nova)
    session.commit()
    print("Unidade de saúde adicionada.")

def listar_unidades():
    unidades = session.query(UnidadeSaude).all()
    for u in unidades:
        print(f"{u.id} - {u.nome} ({u.endereco})")

def atualizar_unidade(id_unid, nome, endereco):
    u = session.get(UnidadeSaude, id_unid)
    if u:
        u.nome = nome
        u.endereco = endereco
        session.commit()
        print("Unidade atualizada.")
    else:
        print("Unidade não encontrada.")

def remover_unidade(id_unid):
    u = session.get(UnidadeSaude, id_unid)
    if u:
        session.delete(u)
        session.commit()
        print("Unidade removida.")
    else:
        print("Unidade não encontrada.")


# In[7]:


def criar_paciente(nome, data_nascimento, cpf):
    novo = Paciente(nome=nome, data_nascimento=data_nascimento, cpf=cpf)
    session.add(novo)
    session.commit()
    print("Paciente adicionado.")

def listar_pacientes():
    pacientes = session.query(Paciente).all()
    for p in pacientes:
        print(f"{p.id} - {p.nome} ({p.cpf})")

def atualizar_paciente(id_pac, nome, data_nascimento, cpf):
    p = session.get(Paciente, id_pac)
    if p:
        p.nome = nome
        p.data_nascimento = data_nascimento
        p.cpf = cpf
        session.commit()
        print("Paciente atualizado.")
    else:
        print("Paciente não encontrado.")

def remover_paciente(id_pac):
    p = session.get(Paciente, id_pac)
    if p:
        session.delete(p)
        session.commit()
        print("Paciente removido.")
    else:
        print("Paciente não encontrado.")


# In[8]:


def criar_aplicacao(paciente_id, vacina_id, unidade_id, data_aplicacao):
    nova = Aplicacao(
        paciente_id=paciente_id,
        vacina_id=vacina_id,
        unidade_id=unidade_id,
        data_aplicacao=data_aplicacao
    )
    session.add(nova)
    session.commit()
    print("Aplicação registrada.")

def listar_aplicacoes():
    aplicacoes = session.query(Aplicacao).all()
    for a in aplicacoes:
        print(f"{a.id} - Paciente {a.paciente_id}, Vacina {a.vacina_id}, Unidade {a.unidade_id} - {a.data_aplicacao}")

def remover_aplicacao(id_apl):
    a = session.get(Aplicacao, id_apl)
    if a:
        session.delete(a)
        session.commit()
        print("Aplicação removida.")
    else:
        print("Aplicação não encontrada.")


# In[9]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




